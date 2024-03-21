
import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import plotly.express as px


import pandas as pd
data = pd.read_csv(r'C:\Users\USER\Downloads\dash\2023_data.csv')

G=['Incomer G3','Incomer G4','Incomer 1 G2','Incomer 5 G1','Incomer 2 G5']
PV=['PV Gen','PV EDL']
EDL=['EDLTF-1','EDLTF-2','EDLTF-3']
generator_names = G + PV + EDL
all_column_names = data.columns
receiver_options=[name for name in all_column_names if name not in generator_names and name !='Date/time' ]
data['Date/time'] = pd.to_datetime(data['Date/time'])
month_numeric = data['Date/time'].dt.month
month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
               7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
categories = [G ,PV, EDL]
app =dash.Dash(__name__)

def filter_data(data, selected_category, min_date, max_date):
    filtered_data = data[data['Category'] == selected_category]
    filtered_data = filtered_data[(filtered_data['Date'] >= min_date) & (filtered_data['Date'] <= max_date)]
    return filtered_data

min_date_as_num = data['Date/time'].min().fromtimestamp  # Convert to Unix timestamp
max_date_as_num = data['Date/time'].max().fromtimestamp

category_options = [name for name in all_column_names if name  in generator_names and name !='Date/time' ]



app.layout = html.Div([
    html.Div([
        html.Div([
            html.Span("Receivers",style={'font-weight': 'bold', 'font-size': '2rem', 'text-align':'center','margin-left': '10%'})
        ]),
        html.Div([
            html.Span("Select receiver: ", style={'font-weight': 'bold', 'color': '#333', 'margin-bottom': '40px'}),
            dcc.Dropdown(
                id='y_axis_dropdown',
                options=[{'label': option, 'value': option} for option in receiver_options],
                value=receiver_options[0],
                multi=False
            ),
        ],
            style={'margin-bottom': 20, 'width': '50%', 'margin-left': '10%'}
        ),
        html.Div(
            dcc.Graph(id='the_graph'),
            style={'width': '80%', 'margin': 'auto', 'margin-top': 20}
        ),
        html.Div(
            [
                html.Span("Select Month: ", style={'font-weight': 'bold', 'color': '#333', 'margin-bottom': 40}),
                dcc.Slider(
                    id='crossfilter_month_slider',
                    min=month_numeric.min(),
                    max=month_numeric.max(),
                    step=None,
                    value=data['Date/time'].dt.month.max(),
                    marks={str(month): str(month) for month in month_names}
                )
            ],
            style={'margin-top': 20, 'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}
        )
    ], style={'flex': 1}), 

    
    html.Div([
        html.Div([
            html.Span("Generators",style={'font-weight': 'bold', 'font-size': '2rem', 'text-align':'center','margin-left': '10%'})
        ]),
        html.Div([
            html.Span("Select generator: ", style={'font-weight': 'bold', 'color': '#333', 'margin-bottom': '40px'}),
            dcc.Dropdown(
            id='y_axis_dropdown2',
            options=[{'label': option, 'value': option} for option in generator_names],
            value=generator_names[0],
            multi=False
        )
        ], style={'margin-bottom': 20, 'width': '50%', 'margin-left': '10%'}),
        html.Div(
            dcc.Graph(id='the_graph2'),
            style={'width': '80%', 'margin': 'auto', 'margin-top': 20}
        ),
        html.Div(
            [
                html.Span("Select Month: ", style={'font-weight': 'bold', 'color': '#333', 'margin-bottom': 40}),
                dcc.Slider(
                    id='crossfilter_month_slider2',
                    min=month_numeric.min(),
                    max=month_numeric.max(),
                    step=None,
                    value=data['Date/time'].dt.month.max(),
                    marks={str(month): str(month) for month in month_names}
                )
            ],
            style={'margin-top': 20, 'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}
        )
    ], style={'flex': 1}),  # Set flex to make it fill space proportionally
], style={'background-color': '#f5f5f5', 'font-family': 'sans-serif', 'display': 'flex'})



@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='y_axis_dropdown', component_property='value'),
     Input('crossfilter_month_slider', 'value')]
)
def update_graph(y_axis_dropdown, crossfilter_month_slider):
    #filtered_month_range = (month_numeric.min(), crossfilter_month_slider)
    filtered_data = data[data['Date/time'].dt.month == crossfilter_month_slider]
    figure = px.line(
        filtered_data,
        x='Date/time',
        y=y_axis_dropdown  
    )
    return figure

@app.callback(
    Output(component_id='the_graph2', component_property='figure'),
    [Input(component_id='y_axis_dropdown2', component_property='value'),
     Input('crossfilter_month_slider2', 'value')]
)
def update_graph(y_axis_dropdown2, crossfilter_month_slider2):
    filtered_data = data[data['Date/time'].dt.month == crossfilter_month_slider2]
    figure = px.line(
        filtered_data,
        x='Date/time',
        y=y_axis_dropdown2  
    )
    return figure




if __name__ == '__main__':
    app.run(debug=True)

