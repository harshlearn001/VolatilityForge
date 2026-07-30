import plotly.graph_objects as go


def create_iv_chart(df):

    fig = go.Figure()

    # --------------------------------------------------
    # ATM IV
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=df["TRADE_DATE"],
            y=df["ATM_IV"],
            name="ATM IV",
            mode="lines",
            line=dict(width=2),
            yaxis="y1",
        )
    )

    # --------------------------------------------------
    # Historical Volatility
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=df["TRADE_DATE"],
            y=df["HV"],
            name="Historical Vol",
            mode="lines",
            line=dict(width=2),
            yaxis="y1",
        )
    )

    # --------------------------------------------------
    # Futures Price
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=df["TRADE_DATE"],
            y=df["FUTURE_CLOSE"],
            name="Future",
            mode="lines",
            line=dict(width=2),
            yaxis="y2",
        )
    )

    fig.update_layout(

        height=550,

        hovermode="x unified",

        legend=dict(
            orientation="h",
            y=1.05,
            x=0,
        ),

        xaxis=dict(
            title="Trade Date"
        ),

        yaxis=dict(
            title="Volatility",
            side="left",
        ),

        yaxis2=dict(
            title="Future Price",
            overlaying="y",
            side="right",
            showgrid=False,
        ),

        margin=dict(
            l=50,
            r=50,
            t=40,
            b=40,
        ),
    )

    return fig