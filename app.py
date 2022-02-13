import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
import pandas as pd


########### Define a few variables ######

tabtitle = 'DC Properties'
sourceurl = 'https://plot.ly/python/scattermapbox/'
githublink = 'https://github.com/austinlasseter/dc-properties-map'
mapbox_access_token = open("assets/mytoken.mapbox_token").read()
df = pd.read_csv('resources/DC_Properties.csv', index_col='Unnamed: 0')
df = df.sample(500)
varlist=['BATHRM', 'HF_BATHRM', 'ROOMS', 'BEDRM', 'STORIES',  'PRICE']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########## Figure
def getFig(value):
    fig = go.Figure(go.Scattermapbox(
        lat=df['LATITUDE'],
        lon=df['LONGITUDE'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            colorscale='Purples',
            color=df[value]
        ),
        text=df['ASSESSMENT_SUBNBHD']

    ))
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=38.92,
                lon=-77.07
            ),
            pitch=0,
            zoom=10
        ),
    )
    return fig



########### Layout

app.layout = html.Div(children=[
    html.H1('DC Properties'),
    # Dropdowns
    html.Div(children=[
        # left side
        html.Div([
                html.H6('Select a variable for colorscale:'),
                dcc.Dropdown(
                    id='stats-drop',
                    options=[{'label': i, 'value': i} for i in varlist],
                    value='PRICE'
                ),
        ], className='three columns'),
        # right side
        html.Div([
            dcc.Graph(id='dc-map')
        ], className='nine columns'),
    ], className='twelve columns'),

    # Footer
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Callbacks
@app.callback(Output('dc-map', 'figure'),
             [Input('stats-drop', 'value')])
def updateFigWith(value):
    return getFig(value)

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
