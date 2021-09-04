import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

spacex_df = pd.read_csv('dataset/spacex_launch_dash.csv')
launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites.insert(0, 'All Sites')

payload_min , payload_max = spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()
app.layout = html.Div(
    children=[html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36',
                                                                'font-size': 40}),
              dcc.Dropdown(id='site-dropdown',
                           options=[{'label': i, 'value': i} for i in launch_sites],
                           value='All Sites',
                           placeholder="Select a Launch Site here",
                           searchable=True),
              html.Br(),

              html.Div(dcc.Graph(id='success-pie-chart')),
              html.Br(),

              html.P("Payload range (Kg):"),
              dcc.RangeSlider(id='payload-slider', min=payload_min, max=10000, step=1000, value=[payload_min,
                                                                                                    payload_max]),
              html.Br(),
              html.Div(dcc.Graph(id='success-payload-scatter-chart')),
              ])


@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'All Sites':
        fig = px.pie(spacex_df, names="Launch Site", values='class')
    else:
        pie_filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(pie_filtered_df, names="class")
    return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value'), ]
)
def get_slider_chart(entered_site, payload_value):
    if entered_site == 'All Sites':
        scatter_plot = px.scatter(spacex_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",)
    else:
        slide_df = spacex_df[(spacex_df['Payload Mass (kg)'].between(left=payload_value[0], right=payload_value[1])) & (spacex_df['Launch Site'] == entered_site)]
        scatter_plot = px.scatter(slide_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",)
    return scatter_plot


if __name__ == '__main__':
    app.run_server(debug=True)
