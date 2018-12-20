###############################################################################
#                     LIVE GRAPH FOR TEMPERATURE SENSOR                       #
#                                                                             #
###############################################################################
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
#import random
import plotly.graph_objs as go
from collections import deque  
import socket

class values(object):
    result =  ''
    result_int = 0
    temp = 0
    fsr = 0

#Connect to server
s = socket.socket()        
host = '192.168.4.1' 
port = 80               

s.connect((host, port))

#Initiate parameters for graph1
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

#Initiate parameters for graph2
X1 = deque(maxlen=20)
X1.append(1)
Y1 = deque(maxlen=20)
Y1.append(1)

class mat_arr(object):
    result = 0

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        #Design of graph1
        dcc.Graph(id='live-graph',animate=True),
        dcc.Interval(
            id='graph-update',
            interval=500
        ),
        #Design of graph2
        dcc.Graph(id='live-graph1',animate=True),
        dcc.Interval(
            id='graph-update1',
            interval= 500
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    values.result = s.recv(10).decode('utf-8')
    values.result_int = int(values.result)
    values.fsr = values.result_int % 100
    values.temp = int(values.result_int / 100)
    print(values.fsr)
    X.append(X[-1]+1)
    Y.append(values.fsr)
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )
    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}
@app.callback(Output('live-graph1', 'figure'),
              events=[Event('graph-update1', 'interval')])
def update_graph_scatter1():
    #values.result = s.recv(1024).decode('utf-8')
    X1.append(X1[-1]+1)
    Y1.append(float(values.temp))
    
    data = plotly.graph_objs.Scatter(
            x=list(X1),
            y=list(Y1),
            name='Scatter',
            mode= 'lines+markers'
            )
    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X1),max(X1)]),
                                                yaxis=dict(range=[min(Y1),max(Y1)]),)}


if __name__ == '__main__':
    app.run_server()