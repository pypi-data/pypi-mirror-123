#We use just-in-time importing here to improve load times
#Here are the imports:
#import plotly.express as px
#import matplotlib.pyplot as plt

def plotlyGrid(data, x, y, output="Output", title=""):
    try:
        import plotly.express as px
    except:
        raise Exception("Plotly is required to use this graph. Install with `pip install plotly`")
    fig = px.scatter_3d(data, x, y, output, title=title)
    return fig

def plotlyAnimation(data, x, y, anim, output="Output", title=""):
    try:
        import plotly.express as px
    except:
        raise Exception("Plotly is required to use this graph. Install with `pip install plotly`")
    fig = px.scatter_3d(data, x, y, output, animation_frame=anim, title=title)
    return fig

def matplotlibGrid(data, x, y, output="Output", title=""):
    """Returns a plt instance, a fig, and the ax"""
    try:
        import matplotlib.pyplot as plt
    except:
        raise Exception("Matplotlib is required to use this graph. Install with `pip install matplotlib`")
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(data[x], data[y], data[output])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_zlabel(output)
    ax.set_title(title)

    return plt, fig, ax