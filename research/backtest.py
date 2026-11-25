"""Fixed-universe exploratory rotation; no orders at signal-day prices."""
import json
import os
from pathlib import Path
import numpy as np
import pandas as pd
import vectorbt as vbt
import yfinance as yf
from engine import breadth
from refresh import download

ROOT=Path(__file__).resolve().parents[1]
PROXIES=[os.environ.get('US_PROXY','SPY'),'ACWI','THD','BTC-USD','IEF','UUP','DBA','GLD']
CASH='BIL'
BENCH=['SPY','QQQ','ACWI']
STRATEGIES=['rank','top1','top3','top50','trend','momentum','leading','recovering','positive_momentum','acceleration','dual','inverse_vol','price','hybrid']
def metrics(v):
    r=v.pct_change().dropna()
    years=(v.index[-1]-v.index[0]).days/365.25
    return {'CAGR':round((v.iloc[-1]/v.iloc[0])**(1/years)-1,6),'Sharpe':round(float(r.mean()/r.std()*np.sqrt(252)),4) if r.std()>0 else None,'MaxDD':round(float((v/v.cummax()-1).min()),6),'Total':round(float(v.iloc[-1]/v.iloc[0]-1),6)}
def targets(strategy,t,m,c,p,vol,rb,top=3):
    score=c.copy()
    if strategy=='trend':score=t
    if strategy=='momentum':score=m
    if strategy=='acceleration':score=c.diff(20)
    if strategy=='price':score=p
    if strategy=='hybrid':score=c.rank(axis=1,pct=True)+p.rank(axis=1,pct=True)
    if strategy=='leading':score=score.where((t>10)&(m>10))
    if strategy=='recovering':score=m.where((t< -10)&(m>10))
    if strategy=='positive_momentum':score=m.where(m>10)
    if strategy=='dual':score=score.where(score>0)
    n={'top1':1,'top50':4,'rank':8}.get(strategy,top)
    weights=pd.DataFrame(np.nan,index=score.index,columns=PROXIES+[CASH])
    for i in range(0,len(score),rb):
        s=score.iloc[i].dropna().sort_values(ascending=False,kind='stable').head(n)
        w=pd.Series(0.,index=weights.columns)
        if len(s):
            if strategy=='rank':a=pd.Series(np.arange(len(s),0,-1),index=s.index,dtype=float)
            elif strategy=='inverse_vol':a=1/vol.iloc[i].reindex(s.index).replace(0,np.nan)
            else:a=pd.Series(1.,index=s.index)
            a=a.replace([np.inf,-np.inf],np.nan).dropna()
            if a.sum()>0:w.loc[a.index]=a/a.sum()*min(1,len(a)/n)*.995
        w[CASH]=.995-w.sum()
        weights.iloc[i]=w
    return weights
def portfolio(prices,weights,cost,details=False):
    pf=vbt.Portfolio.from_orders(prices,size=weights,size_type='targetpercent',cash_sharing=True,group_by=True,call_seq='auto',init_cash=100000,fees=cost,slippage=0.,freq='1D')
    return pf if details else pf.value()
def rotation_details(pf,px,w,m,bench):
    import datetime
    dates=px.index.strftime('%Y-%m-%d').tolist()
    equity=pf.value()
    # Reconstruct individual holdings from actual executed order records, independent of grouping labels.
    records=pf.orders.records
    changes=np.zeros(px.shape,dtype=float)
    cash_changes=np.zeros(len(px),dtype=float)
    for o in records.itertuples(index=False):
        sign=1 if int(o.side)==0 else -1
        changes[int(o.idx),int(o.col)]+=sign*float(o.size)
        cash_changes[int(o.idx)]-=sign*float(o.size)*float(o.price)+float(o.fees)
    shares=pd.DataFrame(changes.cumsum(axis=0),index=px.index,columns=px.columns)
    cash=pd.Series(100000+cash_changes.cumsum(),index=px.index)
    if not np.allclose(shares.mul(px).sum(axis=1)+cash,equity,rtol=1e-8,atol=1e-5):raise RuntimeError('Order ledger does not reconcile to VectorBT equity')
    actual=shares.mul(px).div(equity,axis=0)
    actual['Cash']=cash/equity
    if not np.allclose(actual.sum(axis=1),1,atol=1e-6):raise RuntimeError('Portfolio weights fail reconciliation')
    orders=[]
    for o in pf.orders.records.itertuples(index=False):
        orders.append(dict(date=dates[int(o.idx)],ticker=px.columns[int(o.col)],side='BUY' if int(o.side)==0 else 'SELL',quantity=float(o.size),price=float(o.price),fees=float(o.fees),notional=float(o.size*o.price)))
    reb=[]
    for i in range(len(w)):
        if w.iloc[i].notna().any():
            reb.append(dict(date=dates[i],signal_date=str((px.index[i]-pd.Timedelta(days=1)).date()),target={k:round(float(v),8) for k,v in w.iloc[i].items() if v>1e-10},scores={k:(round(float(v),4) if pd.notna(v) else None) for k,v in m.iloc[i].items()},actual={k:round(float(v),8) for k,v in actual.iloc[i].items() if v>1e-10}))
    pos=[dict(ticker=k,quantity=float(shares[k].iloc[-1]),price=float(px[k].iloc[-1]),value=float(shares[k].iloc[-1]*px[k].iloc[-1]),weight=float(actual[k].iloc[-1]),target=float(reb[-1]['target'].get(k,0))) for k in px.columns if shares[k].iloc[-1]>1e-10]
    pos.append(dict(ticker='Cash',quantity=None,price=None,value=float(cash.iloc[-1]),weight=float(actual['Cash'].iloc[-1]),target=.005))
    return dict(generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),dates=dates,tickers=list(actual.columns),weights=actual.round(7).values.tolist(),equity=equity.round(2).tolist(),benchmarks={k:(bench[k]/bench[k].iloc[0]*100000).round(2).tolist() for k in BENCH},positions=pos,orders=orders,rebalances=reb,last_rebalance=reb[-1]['date'],sessions_to_next=20-((len(px)-1)%20),as_of=dates[-1],equity_latest=float(equity.iloc[-1]),latest_scores={k:(round(float(v),4) if pd.notna(v) else None) for k,v in m.iloc[-1].items()},latest_signal_date=str((px.index[-1]-pd.Timedelta(days=1)).date()))

def main():
    universe=json.loads((ROOT/'universe.json').read_text())
    cache=ROOT/'signal_prices.pkl'
    raw=pd.read_pickle(cache) if cache.exists() else download(list(dict.fromkeys(' '.join(universe.values()).split())))
    raw=raw.reindex(pd.date_range(raw.index.min(),raw.index.max(),freq='D'))
    groups=[breadth(raw,s.split()) for s in universe.values()]
    def signal(k):
        x=pd.concat([g[k] for g in groups],axis=1);x.columns=PROXIES
        x[['IEF','UUP']]*=-1
        return x
    tickers=list(dict.fromkeys(PROXIES+[CASH]+BENCH))
    prices=yf.download(tickers,start='2010-01-01',auto_adjust=True,progress=False,threads=False)['Close']
    prices.index=pd.to_datetime(prices.index).tz_localize(None).normalize()
    prices=prices.loc[prices.index<pd.Timestamp.now(tz='UTC').tz_localize(None).normalize()]
    # Use common US trading sessions; BTC weekend performance included in next session return.
    prices=prices.loc[prices.SPY.notna(),tickers].dropna()
    # Signals from preceding calendar date, never execution close; additional session lag for price signals.
    def align(x):return x.reindex(prices.index-pd.Timedelta(days=1)).set_axis(prices.index)
    t,m,c=map(lambda k:align(signal(k)),['Trend','Momentum','Composite'])
    p=prices[PROXIES].pct_change(120).shift(1)
    vol=prices[PROXIES].pct_change().rolling(20).std().shift(1)
    valid=t.notna().all(axis=1)&m.notna().all(axis=1)&p.notna().all(axis=1)
    if not valid.any():raise RuntimeError('No complete signal history')
    start=valid[valid].index[0]
    prices=prices.loc[start:];t,m,c,p,vol=[x.loc[start:] for x in [t,m,c,p,vol]]
    # Fixed chronological split, exploratory only (no claim of true independent OOS).
    split=prices.index[int(len(prices)*.7)]
    rows=[]
    rotation=None
    for strategy in STRATEGIES:
        for rb in [5,20,60]:
            w=targets(strategy,t,m,c,p,vol,rb)
            for cost in [.0005,.001,.002]:
                if strategy=='momentum' and rb==20 and cost==.001:
                    pf=portfolio(prices[PROXIES+[CASH]],w,cost,details=True)
                    v=pf.value()
                    rotation=rotation_details(pf,prices[PROXIES+[CASH]],w,m,prices)
                else:
                    v=portfolio(prices[PROXIES+[CASH]],w,cost)
                rows.append(dict(strategy=strategy,rebalance=rb,cost=cost,full=metrics(v),train=metrics(v.loc[v.index<split]),test=metrics(v.loc[split:])))
    for b in BENCH:
        v=prices[b]/prices[b].iloc[0]*100000
        rows.append(dict(strategy=b,rebalance=None,cost=0,full=metrics(v),train=metrics(v.loc[v.index<split]),test=metrics(v.loc[split:])))
    # Equal weight and 60/40 use same execution simulator.
    for label,alloc in [('equal',{k:.995/8 for k in PROXIES}),('60/40',{'SPY':.597,'IEF':.398})]:
        bench_cols=list(dict.fromkeys(PROXIES+[CASH]+list(alloc)))
        w=pd.DataFrame(np.nan,index=prices.index,columns=bench_cols)
        w.iloc[::20]=0.
        for k,a in alloc.items():w.loc[w.index[::20],k]=a
        v=portfolio(prices[bench_cols],w,.001)
        rows.append(dict(strategy=label,rebalance=20,cost=.001,full=metrics(v),train=metrics(v.loc[v.index<split]),test=metrics(v.loc[split:])))
    result=dict(us_proxy=PROXIES[0],start=str(prices.index[0].date()),end=str(prices.index[-1].date()),split=str(split.date()),sessions=len(prices),rows=rows,limitations='Fixed universe; exploratory split; adjusted close execution; prior calendar day breadth; US sessions; equal member breadth; inverse yield/FX heuristic; no tax or extra slippage.')
    if rotation is None:raise RuntimeError('Missing reference portfolio')
    rotation.update(us_proxy=PROXIES[0],start=result['start'],end=result['end'],split=result['split'],metrics=next(x for x in rows if x['strategy']=='momentum' and x['rebalance']==20 and x['cost']==.001),results=rows)
    (ROOT/'site'/('rotation_'+PROXIES[0]+'.json')).write_text(json.dumps(rotation,separators=(',',':'),allow_nan=False))
    out=ROOT/('research_results_'+PROXIES[0]+'.json');out.write_text(json.dumps(result,indent=2,allow_nan=False))
    print('RESEARCH_RESULT_'+PROXIES[0],json.dumps(result,separators=(',',':'),allow_nan=False))
if __name__=='__main__':main()
