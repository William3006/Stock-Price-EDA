## Project Structure
SPEDA/
├── main.py                  # Entry point, pipeline orchestration
├── app.py                   # Streamlit dashboard (Phase 2)
├── data/
│   └── loader.py            # Data loading and saving
├── features/
│   └── features.py          # Feature engineering
├── analysis/
│   ├── anomaly.py           # Anomaly detection (IQR, Z-score, Isolation Forest)
│   ├── fattails.py          # Fat tails, kurtosis, skewness, correlation
│   ├── drawdown.py          # Drawdown analysis
│   └── report.py            # Automated EDA report (Phase 2)
└── plots/
└── plots.py             # All plotting functions

---

## Features

### Phase 1 — Backend EDA Pipeline 
- **Data loading** — yfinance integration with local CSV caching
- **Feature engineering** — daily returns, rolling mean, volatility, net profit
- **Fat tails analysis** — return histogram with normal curve overlay, kurtosis and skewness annotations
- **Correlation matrix** — seaborn heatmap of user-specified columns
- **Candlestick charts** — OHLC visualisation
- **Drawdown analysis** — cumulative max drawdown over time
- **Three-layer anomaly detection**:
  - Rolling IQR (point outliers in returns)
  - Rolling Z-score (local spikes relative to recent window)
  - Isolation Forest (multivariate — days that are globally unusual)
  - Consensus `Flagged` column — days flagged by 2+ methods
- **Modular structure** — all functions importable, works across any ticker

### Phase 2 — Streamlit Dashboard 
- Interactive Plotly charts with zoom, pan, hover
- Ticker input and date range selection
- Full pipeline triggered from UI
- Automated EDA report with interpreted results

---

## Usage

Explained in function_guide.txt

---

## Dependencies
pandas
numpy
matplotlib
seaborn
scipy
yfinance
scikit-learn
streamlit        # Phase 2
plotly           # Phase 2

Install with:
```bash
pip install -r requirements.txt
```

---

## Key Findings (META 10y)

- Kurtosis ~19 — extreme fat tails, returns are far from normally distributed
- Max drawdown ~75% (2021–2022 rate hike period)
- Anomaly detection flags ~5% of trading days as high-confidence outliers
- Profitable days ~53% of trading days

---

## Roadmap

- [ ] Phase 2: Streamlit dashboard with Plotly
- [ ] Automated interpreted EDA report
- [ ] Multi-ticker comparison
- [ ] Rolling correlation matrix
- [ ] Sharpe ratio and risk-adjusted return metrics
- [ ] Statistical significance testing on anomalies