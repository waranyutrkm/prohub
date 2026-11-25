import json, time
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from engine import breadth

ROOT = Path(__file__).resolve().parent

def download(tickers):
    import yfinance as yf
    series = {}
    for start in range(0, len(tickers), 15):
        batch = tickers[start:start+15]
        for attempt in range(3):
            missing = [s for s in batch if s not in series]
            if not missing: break
            try:
                raw = yf.download(missing, period='max', interval='1d', auto_adjust=False, progress=False, threads=False, timeout=25)
                close = raw['Close']
                if isinstance(close, pd.Series): close = close.to_frame(missing[0])
                for s in missing:
                    if s in close and close[s].notna().any():
                        p = close[s].dropna(); p.index = pd.to_datetime(p.index).tz_localize(None).normalize()
                        series[s] = p[~p.index.duplicated(keep='last')]
            except Exception as exc: print(type(exc).__name__, str(exc)[:200])
            if attempt < 2: time.sleep(2**attempt)
        time.sleep(1)
    if not series: raise RuntimeError('No data downloaded; refusing to publish empty results')
    return pd.DataFrame(series).sort_index()

def build(frame, universe):
    today = pd.Timestamp(datetime.now(timezone.utc).date())
    frame = frame.loc[frame.index < today].reindex(pd.date_range(frame.index.min(), min(frame.index.max(),today-pd.Timedelta(days=1)),freq='D'))
    if frame.empty: raise RuntimeError('No completed daily observations')
    groups = {}
    for name, symbols in universe.items():
        syms = symbols.split()
        r = breadth(frame, syms, stale=4)
        groups[name] = {'symbols':syms,'available':[s for s in syms if s in frame and frame[s].notna().any()], 'rows': json.loads(r.round(4).to_json(orient='values'))}
    return {'generated_at':datetime.now(timezone.utc).isoformat(),'dates':frame.index.strftime('%Y-%m-%d').tolist(),'columns':list(r.columns),'groups':groups,'parameters':{'fast':12,'slow':26,'signal':9,'minimum_coverage':60,'max_stale_calendar_days':4}}

if __name__ == '__main__':
    universe = json.loads((ROOT/'universe.json').read_text())
    tickers = list(dict.fromkeys(' '.join(universe.values()).split()))
    frame=download(tickers)
    frame.to_pickle(ROOT/'signal_prices.pkl')
    data = build(frame,universe)
    path=ROOT/'site'/'breadth.json'; tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,separators=(',',':'),allow_nan=False)); tmp.replace(path)
