"""
VolatilityForge Dashboard Launcher
----------------------------------

Launches the Streamlit dashboard.

Run:
    python run_dashboard.py
"""

import sys
import streamlit.web.cli as stcli


def main():
    sys.argv = [
        "streamlit",
        "run",
        "dashboard/app.py",
        "--server.headless=false",
        "--browser.gatherUsageStats=false",
    ]

    sys.exit(stcli.main())


if __name__ == "__main__":
    main()