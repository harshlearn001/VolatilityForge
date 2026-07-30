import plotly.graph_objects as go


def create_iiv_chart(df):

    colors = [
        "limegreen" if x >= 0 else "red"
        for x in df["IIV"]
    ]

    fig = go.Figure()

    # --------------------------
    # IIV Bars
    # --------------------------

    fig.add_trace(
        go.Bar(
            x=df["TRADE_DATE"],
            y=df["IIV"],
            name="IIV",
            marker_color=colors,
            yaxis="y1",
        )
    )

    # --------------------------
    # Futures Price
    # --------------------------

    fig.add_trace(
        go.Scatter(
            x=df["TRADE_DATE"],
            y=df["FUTURE_CLOSE"],
            mode="lines",
            name="Future",
            yaxis="y2",
        )
    )

    # --------------------------
    # Layout
    # --------------------------

    fig.update_layout(

        template="plotly_dark",

        height=700,

        hovermode="x unified",

        title="Intraday IV Change",

        yaxis=dict(
            title="IIV",
            zeroline=True,
        ),

        yaxis2=dict(
            title="Future",
            overlaying="y",
            side="right",
        ),

        xaxis=dict(
            rangeslider_visible=False,
        ),
    )

    return fig