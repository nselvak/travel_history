# Travel Tracker Map

## Overview
The Travel Tracker Map is a Streamlit application that visualizes your travel history on an interactive map. It fetches travel data from a Google Sheets document, displays the countries you have visited, the number of times you've been there, and other details such as cities visited and total days spent in each country.

## Features
- Interactive map showing countries visited
- Hover over countries to see details like number of visits, cities visited, and total days spent
- Display flags of visited countries
- Customizable UI with external CSS

## Project Structure

```plaintext
travel_history/
├── main.py
├── ui_components.py
├── google_sheets.py
├── map_visualization.py
├── styles.css
├── requirements.txt
└── README.md
```


### `main.py`
Main script for the Travel Tracker Map Streamlit app. It loads custom CSS, fetches travel data from Google Sheets, generates a map, and displays the map and flags of visited countries.

### `ui_components.py`
Contains UI components for the Streamlit app, including functions to load custom CSS, display an interactive map, and display flags of visited countries.

### `google_sheets.py`
Sets up the Google Sheets client and fetches and cleans travel data from a Google Sheets document.

### `map_visualization.py`
Creates a map visualization using Folium and GeoPandas. It loads a world shapefile, colors countries based on the number of visits, and adds popups with travel details.

### `styles.css`
Contains styles for the Streamlit app, including global styles, map container styles, and flag container styles.

### `requirements.txt`
Lists all the dependencies required for the project.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/travel_history.git
   cd travel_history
2. Create a virtual environment and activate it:
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux

3. Install the required dependencies:
pip install -r requirements.txt

4. Set up your Google Sheets API credentials:
Follow instructions to setup credentials.json [HERE](https://docs.gspread.org/en/latest/oauth2.html)
Place the credentials.json file in the root directory of the project.

## Usage
1. Run the Streamlit app using the following command:
streamlit run main.py

2. Open your web browser and go to http://localhost:8501 to view the app.

## License
This project is licensed under the MIT License. See the LICENSE file for details.