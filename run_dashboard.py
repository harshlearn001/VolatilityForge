"""
VolatilityForge Dashboard Launcher
----------------------------------

Launches the Streamlit dashboard.

Run:
    python run_dashboard.py
"""

import sys


def main() -> None:
    try:
        import streamlit.web.cli as stcli
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Streamlit is required to run the dashboard. Install it with 'pip install streamlit plotly'."
        ) from exc

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