# U.S Capital Weather App

This is a web application that uses Dash to visualize the average temperature and current temperatures of a set of capitals for states starting with a given letter. The temperatures are soured from 
OpenWeather API using longitute and latitude coordinates. Users enter the first letter of the states that they want to filter and their API key to visualize the data.

## Getting Started


### Requirements
  - Python 3.7 or higher
  - Plotly
  - Dash
  - Polars
  - curl

### Datasets

- `worldcities.csv`: This main dataset contains various information such as longititude and latitute about cities around the world .
- `state_capitals.csv`: This dataset contains U.S state capitals and their corresponding states and used to clean/filter the main dataset for U.S capitals and states.
  
### Installation & Execution

1. Install necessary Python libraries using the following command:
   
  ```sh
  pip install dash plotly polars 
  ```
2. Get an API key at [https://api.openweathermap.org/data/2.5/weather](https://api.openweathermap.org/data/2.5/weather) and insert in Dash app when prompted. 
3. Clone the repository:
   
     ```sh
   git clone https://github.com/karenjohn35/us_weather_app.git
    ```
5. Ensure `worldcities.csv` and `state_capitals.csv` are in the project directory.
6. Run the python script to start the Dash server :
   
   ```sh
   python analyze_capitals.py
    ```
7. Access [http://127.0.0.1:8050](http://127.0.0.1:8050) to interact with Dash app.

## Usage
1. Enter your API key in the input field.
2. Enter the starting letter to filter capitals from states that start with that letter.
3. View the current temperatures of the capitals in addition to the average temperature of the set in a figure.

## Short Description of Tools/Libraries Used

* [Dash](https://dash.plotly.com/) for web application
* [Plotly](https://plotly.com/python/) for visualization and graphing
* [Polars](https://docs.pola.rs/) for data processing
* [curl](https://curl.se/) for command-line data transfer
* [subprocess](https://docs.python.org/3/library/subprocess.html) for running command-line in python program
   
   
