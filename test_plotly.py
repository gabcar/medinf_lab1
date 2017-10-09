import plotly as py
from plotly.graph_objs import *

py.tools.set_credentials_file(username='gabcar', api_key='a1M0F3ZTssR0IXIZyH7H')

data = Data([
    Scatter(
        x=[1, 2],
        y=[3, 4]
    )
])

plot_url = py.plotly.plot(data, filename='my plot')
