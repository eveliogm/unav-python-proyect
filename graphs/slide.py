import plotly.express as px


def slide_plot(data,currency):
    """
    Create a currency plot with slider
    Arguments:

    """
    fig = px.line(data, x='time', y='close', title=f"{currency} plot")
    fig.update_xaxes(rangeslider_visible=True)
    return fig