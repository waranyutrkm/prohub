# ProHub — Global Market Intelligence

Independent MACD breadth research dashboard, inspired by [Global Flow Lab](https://github.com/waranyutrkm/global-capital-flow-lab). Python + yfinance, static HTML/JS and Plotly, GitHub Actions and Pages.

[Planned dashboard](https://waranyutrkm.github.io/prohub/) | [Workflow](https://github.com/waranyutrkm/prohub/actions/workflows/publish.yml)

## ภาพรวม

Historical Heatmap, Breadth Rotation with historical trails, market ranking and CSV export across eight market groups. The 169-symbol universe is configurable in universe.json. Computation runs outside TradingView.

## Run locally

Install with `pip install -r requirements.txt`, run `python -m unittest -v`, then `python refresh.py` and `python -m http.server 8000 --directory site`. Open localhost:8000.

## Deploy

Enable Settings > Pages > Source: GitHub Actions, then run ProHub daily refresh and Pages. Scheduled daily at 06:30 UTC (13:30 ICT), including weekends for crypto. The site artifact contains only the frontend and computed aggregate data. No raw prices or secrets are published. Verify data redistribution rights before making the site public.

## Method

Compute MACD 12/26/9 on each symbol's observed closes before alignment. UF: MACD>0 and >signal; UP: >0 and <signal; DP: <0 and >signal; DF: <0 and <signal. Equality is neutral. Trend = (UF+UP-DF-DP)/valid*100; Momentum = (UF+DP-DF-UP)/valid*100; Composite = (UF+w*UP-DF-w*DP)/valid*100. Full and Pausing retain original logic. UI can adjust w from 0 to 1; MACD periods require engine configuration changes. Calendar dates align markets with at most four days of forward-filled state; exclude current UTC date. Coverage below 60% suppresses scores. No synchronized close timestamps, point-in-time universe, or investment backtest. US yield curve and Thai stock proxies are not equivalent to original global yields and sector indices. Yahoo symbols may fail; data availability is reported. No claim of money flow or predictive performance.

## Design

Obsidian-inspired dark surface, cyan emphasis, directional emerald/rose, compact tabular numbers, no decorative emoji. Responsive charts and keyboard controls; accessibility conformance not independently audited. See DESIGN.md and AGENTS.md.

Research only. Yahoo Finance data is subject to provider terms. Code license does not grant data rights.
