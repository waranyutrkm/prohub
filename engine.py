import numpy as np
import pandas as pd


def states(close, fast=12, slow=26, signal=9):
    p = close.dropna()
    m = p.ewm(span=fast, adjust=False, min_periods=fast).mean() - p.ewm(span=slow, adjust=False, min_periods=slow).mean()
    s = m.ewm(span=signal, adjust=False, min_periods=signal).mean()
    out = pd.Series(np.select([(m>0)&(m>s),(m>0)&(m<s),(m<0)&(m>s),(m<0)&(m<s)], [2,1,-1,-2], default=0), index=p.index, dtype=float)
    return out.where(m.notna() & s.notna()).reindex(close.index)


def breadth(frame, symbols, fast=12, slow=26, signal=9, weight=.5, coverage=.6, stale=4):
    cols = frame.reindex(columns=symbols)
    st = pd.DataFrame({c:states(cols[c],fast,slow,signal) for c in cols})
    if stale:
        st = st.ffill(limit=stale)
    n = st.count(axis=1)
    uf,up,dp,df = [(st==k).sum(axis=1) for k in [2,1,-1,-2]]
    den = n.replace(0,np.nan)
    out = pd.DataFrame({'UF':100*uf/den,'UP':100*up/den,'DP':100*dp/den,'DF':100*df/den,'Neutral':100*(st==0).sum(axis=1)/den,'Trend':100*(uf+up-dp-df)/den,'Momentum':100*(uf+dp-up-df)/den,'Composite':100*(uf+weight*up-weight*dp-df)/den,'Full':100*(uf-df)/den,'Pausing':100*(up-dp)/den,'Valid':n,'Requested':len(symbols),'Coverage':n/len(symbols)*100})
    out.loc[out.Coverage<coverage*100,['Trend','Momentum','Composite','Full','Pausing']] = np.nan
    return out
