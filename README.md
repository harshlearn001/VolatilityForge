# VolatilityForge

Institutional-grade implied volatility analytics platform.

## Features

- IV analytics
- IV change analysis
- Dashboard
- Data services
- Extensible analytics engine

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   - pip install -r requirements.txt
3. Run the analytics pipeline:
   - python run.py
4. Run the dashboard:
   - python run_dashboard.py

## Notes

- The application reads input data from the local data directory under the repository.
- The CLI now raises clear file-not-found errors when required data files are missing.
- The dashboard launcher reports a clear message if Streamlit is not installed.
