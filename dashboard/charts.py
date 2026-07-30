from __future__ import annotations

import plotly.graph_objects as go


# ==========================================================
# IV / HV / FUTURES CHART
# ==========================================================

def create_iv_chart(df):

    fig = go.Figure()

    # ATM IV
    fig.add_trace(
        go.Scatter(
            x=df["TRADE_DATE"],
            y=df["ATM_IV"],
            mode="lines",
            name="ATM IV",
            yaxis="y1",
        )
    )

    # Historical Volatility
    fig.add_trace(
        go.Scatter(
            x=df["TRADE_DATE"],
            y=df["HV"],
            mode="lines",
            name="Historical Vol",
            yaxis="y1",
        )
    )

    # Futures Price
    fig.add_trace(
        go.Scatter(
            x=df["TRADE_DATE"],
            y=df["FUTURE_CLOSE"],
            mode="lines",
            name="Future",
            yaxis="y2",
        )
    )

    fig.update_layout(

        template="plotly_dark",

        height=650,

        hovermode="x unified",

        title="IV / HV / Futures",

        legend=dict(
            orientation="h"
        ),

        yaxis=dict(
            title="Volatility"
        ),

        yaxis2=dict(
            title="Future Price",
            overlaying="y",
            side="right",
        ),

        xaxis=dict(
            title="Date",
            rangeslider_visible=False,
        ),
    )

    return fig


# ==========================================================
# IIV CHART
# ==========================================================

def create_iiv_chart(df):

    colors = [
        "limegreen" if x >= 0 else "red"
        for x in df["IIV"]
    ]

    fig = go.Figure()

    # IIV Bars
    fig.add_trace(
        go.Bar(
            x=df["TRADE_DATE"],
            y=df["IIV"],
            marker_color=colors,
            name="IV Change",
            yaxis="y1",
        )
    )

    # Futures Price
    fig.add_trace(
        go.Scatter(
            x=df["TRADE_DATE"],
            y=df["FUTURE_CLOSE"],
            mode="lines",
            name="Future",
            yaxis="y2",
        )
    )

    fig.update_layout(

        template="plotly_dark",

        height=650,

        hovermode="x unified",

        title="IV Change vs Futures",

        legend=dict(
            orientation="h"
        ),

        yaxis=dict(
            title="IV Change",
            zeroline=True,
            zerolinewidth=2,
        ),

        yaxis2=dict(
            title="Future Price",
            overlaying="y",
            side="right",
        ),

        xaxis=dict(
            title="Date",
            rangeslider_visible=False,
        ),
    )

    return fig