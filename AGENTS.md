# Project guidelines

Maintain the independent Python computation and static Pages frontend. Keep the existing LICENSE. Follow DESIGN.md, preserve semantic text/color, keyboard access, responsive layout and explicit missing-data states. No fabricated market data or predictive claims. Do not publish raw prices or secrets. Preserve per-symbol observed-session MACD before alignment. Add tests for calculation changes, disclose stale-data and fixed-universe limitations, and avoid future information in historical calculations. Run python -m unittest -v and node --check site/app.js before release.
