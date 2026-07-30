import streamlit as st

from data_service import DataService
from charts import create_iv_chart, create_iiv_chart


# ==========================================================
# PAGE
# ==========================================================

st.set_page_config(
    page_title="VolatilityForge",
    page_icon="📈",
    layout="wide",
)

service = DataService()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Controls")

symbol = st.sidebar.selectbox(
    "Symbol",
    ["NIFTY"],
)

lookback = st.sidebar.selectbox(
    "Lookback",
    [30, 60, 90, 126, 252, 504, "All"],
    index=4,
)

# Load data
df = service.load_symbol(symbol)
df = service.prepare(df)
df = service.apply_lookback(df, lookback)

latest = service.latest(df)

# ==========================================================
# HEADER
# ==========================================================

st.title("📈 VolatilityForge")
st.caption("Institutional Volatility Analytics Platform")

# ==========================================================
# METRICS
# ==========================================================

r1 = st.columns(4)

r1[0].metric(
    "Current IV",
    f"{latest['ATM_IV']:.2%}"
)

r1[1].metric(
    "IV Rank",
    f"{latest['IV_RANK']:.2f}"
)

r1[2].metric(
    "IV Percentile",
    f"{latest['IV_PERCENTILE']:.2f}"
)

r1[3].metric(
    "Historical Vol",
    f"{latest['HV']:.2%}"
)

r2 = st.columns(4)

r2[0].metric(
    "IV / HV",
    f"{latest['IV_HV_RATIO']:.2f}"
)

r2[1].metric(
    "IV Premium",
    f"{latest['IV_PREMIUM_PCT']:.2f}%"
)

r2[2].metric(
    "Regime",
    latest["VOL_REGIME"]
)

r2[3].metric(
    "Future",
    f"{latest['FUTURE_CLOSE']:,.2f}"
)

st.divider()

st.subheader("IV / HV / Futures")

fig = create_iv_chart(df)

st.plotly_chart(
    fig,
    width="stretch",
)

# ==========================================================
# INTRADAY IV CHART
# ==========================================================

if {"IIV", "FUTURE_CLOSE"}.issubset(df.columns):

    st.subheader("Intraday IV Change")

    fig = create_iiv_chart(df)

    st.plotly_chart(
        fig,
        width="stretch",
    )
else:
    st.info(
        "Intraday IV chart is not available yet. "
        "The dataset does not contain the required 'IIV' column."
    )
# ==========================================================
# TABLE
# ==========================================================

st.divider()

st.subheader("Historical Data")

display_columns = [
    "TRADE_DATE",
    "FUTURE_CLOSE",
    "SPOT_CLOSE",
    "ATM_IV",
    "HV",
    "IV_RANK",
    "IV_PERCENTILE",
    "IV_HV_RATIO",
    "IV_PREMIUM_PCT",
    "VOL_REGIME",
]

st.dataframe(
    df[display_columns],
    width="stretch",
)