import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import polars as pl
import subprocess
import json

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

#Loading the dataset with polars. 
DATA_FILE = 'worldcities.csv'
df = pl.read_csv(DATA_FILE)

# Since the dataset is way too large and has some errors (missing capitals), load another manual dataset of US states and capitals.  
US_df = pl.read_csv('state_capitals.csv')



#Merge both datasets with a join operation to filter the data for US states and capitals. 
df_filtered = df.join(
    US_df,
    left_on=['admin_name', 'city'],  # Use admin_name for state in worldcities
    right_on=['state', 'capital'],   #l Use state and capital in known_capitals
    how='inner'
)


#print(f"Number of rows: {df_filtered.height}") 


def get_temp(lat, lon, api_key):
    """Get temperature from OpenWeatherMap API with curl and subproccesses"""
    url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
        data = json.loads(result.stdout)

        if data.get('cod') == 200:
            return data['main']['temp']
        else:
            return None
    except subprocess.CalledProcessError:
        return None

def get_state_capitals(letter):
    """Get capitals of US states starting with a specific letter from the filtered/cleaned dataset."""
    capitals = df_filtered.filter(
        pl.col('admin_name').str.starts_with(letter.upper())
    )
    return capitals

def analyze_capitals(letter,api_key):
    """Find the temperatures of capitals of US states starting with the given letter."""
    capitals_df = get_state_capitals(letter)

    temps = []
    city_state = []

    for row in capitals_df.iter_rows(named=True):
        city = row['city']
        state = row ['admin_name']
        lat = row['lat']
        lon = row['lng']

        
        temp = get_temp(lat, lon, api_key)
        if temp is not None:
                temps.append(temp)
                city_state.append(f"{city}, {state}")
            

    avg_temp = sum(temps) / len(temps) if temps else None
    return city_state, temps, avg_temp

# Create dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("U.S Capitals Weather App"),
    html.Label("Enter your OpenWeather API key: "),
    dcc.Input(id='api-key-input', type='text', value=''),
    html.Br(),
    html.Label("Enter the starting letter of the states you want to analyze: "),
    dcc.Input(id='letter-input', type='text', value='M'),
    dcc.Graph(id='temp-graph'),
    html.Div(id='avg-temp')
])

# Define callback to update the graph based on the letter input
@app.callback(
    [Output('temp-graph', 'figure'),
     Output('avg-temp', 'children')],
    [Input('letter-input', 'value'),
     Input('api-key-input', 'value')]
)
def update_graph(letter, api_key):

    if not api_key:
        return go.Figure(), "Please enter your API key."
    
    city_state, temps, avg_temp = analyze_capitals(letter,api_key)


    if temps:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=city_state,
            y=temps,
            marker_color='green',
            name='Temperatures'
        ))
        fig.add_trace(go.Scatter(
            x= city_state,
            y=[avg_temp] * len(city_state),
            mode='lines',
            name='Average Temperature',
            line=dict(color='red', dash='dash')
        ))


        fig.update_layout(
            title=f' Current Temperatures of Capitals in States Starting with "{letter}"',
            xaxis_title='City, State',
            yaxis_title='Temperature (°C)',
            xaxis_tickangle= 45 
        )
        avg_temp_output = f'Average Temperature: {avg_temp:.2f}°C'
    else:
        fig = go.Figure()
        avg_temp_output = 'No data available.'

    return fig, avg_temp_output

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
