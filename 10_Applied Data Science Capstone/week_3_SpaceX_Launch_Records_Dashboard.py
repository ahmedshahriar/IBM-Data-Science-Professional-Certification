import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# create a dash application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# read the dataset
spacex_df = pd.read_csv('dataset/spacex_launch_dash.csv')

# create a list of all launch sites
launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites.insert(0, 'All Sites')

<<<<<<< HEAD
# payload min , max range
=======
>>>>>>> f2003e1aacf7e92dec35c3a501767e794326403c
payload_min, payload_max = spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()
app.layout = html.Div(
    children=[html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36',
                                                                'font-size': 40}),

              # https://dash.plotly.com/dash-core-components/dropdown
              dcc.Dropdown(id='site-dropdown',
                           options=[{'label': i, 'value': i} for i in launch_sites],
                           value='All Sites',
                           placeholder="Select a Launch Site here",
                           searchable=True),
              html.Br(),

              html.Div(dcc.Graph(id='success-pie-chart')),
              html.Br(),

              html.P("Payload range (Kg):"),
<<<<<<< HEAD

              # https://dash.plotly.com/dash-core-components/rangeslider
=======
>>>>>>> f2003e1aacf7e92dec35c3a501767e794326403c
              dcc.RangeSlider(id='payload-slider', min=payload_min, max=10000,
                              marks={
                                  0: '0',
                                  2500: '2500',
                                  5000: '5000',
                                  7500: '7500',
                                  10000: '10000'
                              },
                              step=1000, value=[payload_min, payload_max]),
              html.Br(),
              html.Div(dcc.Graph(id='success-payload-scatter-chart')),
              ])


@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # https://community.plotly.com/t/graph-if-empty-dropdown/7483/2
    # leave callback Output unchanged
    if entered_site is None:
        raise Exception()
<<<<<<< HEAD

    # to clear the graph
    # if entered_site is None:
    #     return {'data': []}

    # https://plotly.com/python/pie-charts/
=======
    # to clear the graph
    # if entered_site is None:
    #     return {'data': []}
>>>>>>> f2003e1aacf7e92dec35c3a501767e794326403c
    if entered_site == 'All Sites':
        fig = px.pie(spacex_df, names="Launch Site", values='class', title='Total Success Launches By Site')
    else:
        pie_filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(pie_filtered_df, names="class", title='Total Success Launches By Site')
    return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value'), ]
)
def get_slider_chart(entered_site, payload_value):
    # https://plotly.com/python/line-and-scatter/
    if entered_site == 'All Sites':
        slide_df = spacex_df[(spacex_df['Payload Mass (kg)'].between(left=payload_value[0], right=payload_value[1]))]
        scatter_plot = px.scatter(slide_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                                  labels={
                                      "class": "Launch Outcome",
                                  },
                                  title="Correlation between Payload and Success for all sites")
    else:
        slide_df = spacex_df[(spacex_df['Payload Mass (kg)'].between(left=payload_value[0], right=payload_value[1])) & (
                spacex_df['Launch Site'] == entered_site)]
        scatter_plot = px.scatter(slide_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                                  labels={
                                      "class": "Launch Outcome",
                                  },
                                  title="Correlation between Payload and Success for all sites")
    return scatter_plot

if __name__ == '__main__':
    app.run_server(debug=True)
