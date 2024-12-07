import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import geopandas as gpd
import folium
import streamlit as st
from streamlit_folium import st_folium  # Import st_folium instead of folium_static
from folium import plugins
from folium.plugins import HeatMap
from branca.colormap import linear

# Google Sheets API setup
def setup_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials_file = "credentials.json"  # Make sure to replace with the path to your credentials file
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(credentials)
    return client

# Fetch and clean data
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def fetch_and_clean_data(_sheet):
    # Load data from Google Sheets into a Pandas DataFrame
    data = pd.DataFrame(_sheet.get_all_records())

    # Group by 'Country' and aggregate
    grouped_data = data.groupby("Country", as_index=False).agg({
        "Visits": "sum",  # Sum of visits for each country
        "Places": lambda x: ", ".join(sorted(set(", ".join(x).split(", "))))  # Unique cities
    })

    # Retain 'Country Code' by merging it back from the original DataFrame
    result = grouped_data.merge(data[["Country", "Country Code", "Country Code 2"]].drop_duplicates(), on="Country", how="left")

    return result

# Streamlit UI
def main():
    st.title("Travel Tracker Map")
    
    # Display instructions
    st.markdown("""
    This interactive map shows the countries you have visited and the number of times you've been there. Hover over the countries to see details such as:
    - The number of visits
    - The cities you have visited in each country
    """)
    
    # Set up Google Sheets API and fetch data
    client = setup_google_sheets()
    sheet = client.open("TravelData").worksheet("Travel")  # Replace with your actual Google Sheet name
    
    # Fetch and clean data
    data = fetch_and_clean_data(sheet)
    
    # Initialize Folium Map
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=2, tiles="CartoDB positron")
    
    # Load GeoPandas world shapefile for country boundaries
    world = gpd.read_file("image/world.shp")

    # Check if the CRS is set
    if world.crs is None:
        # Assign the EPSG:4326 CRS (WGS 84)
        world.set_crs("EPSG:4326", allow_override=True, inplace=True)

    # Add countries boundaries to the map
    folium.GeoJson(world, style_function=lambda x: {
        'color': 'black',  # Set country border color
        'weight': 1,  # Border thickness
        'fillOpacity': 0  # No fill color for borders
    }).add_to(m)

    # Get the maximum number of visits
    max_visits = data['Visits'].max()

    # Define a dynamic color scale using linear colormap (warm color range)
    color_scale = linear.YlOrRd_09.scale(0, max_visits)  # Yellow to Red color scale

    # Add country-specific markers or choropleth colors
    for _, row in data.iterrows():
        country_code = row['Country Code']
        country_name = row['Country']
        visits = row['Visits']
        
        # Set the color based on the dynamic scale
        color = color_scale(visits)
        
        # Create a GeoJson popup with visit details
        popup = folium.Popup(f"<b>{country_name}</b><br>Visits: {visits}<br>Cities: {row['Places']}", max_width=300)
        
        # Add country-specific GeoJSON to map
        folium.GeoJson(
            world[world['SOV_A3'] == country_code].geometry,
            style_function=lambda x, color=color: {
                'fillColor': color, 
                'color': 'black',  # Add border color
                'weight': 1,  # Border thickness
                'fillOpacity': 0.7  # Set fill opacity
            },
            popup=popup  # Show popup with country details
        ).add_to(m)

    # Add ocean color (background color for the map)
    m.get_root().html.add_child(folium.Element("""
    <style>
        .leaflet-container { background-color: #FFFFFF !important; }
    </style>
    """))

    # Display the map in Streamlit (ensure it's only called once)
    st.markdown("### Interactive Travel Map")
    st_folium(m)  # Use st_folium instead of folium_static
    
    # Display flags of countries visited below the map
    st.markdown("### Flags of Countries Visited")

    # Create a container for flags
    cols = st.columns(5)  # Split into 5 columns
    col_idx = 0  # Start with the first column

    # Display flags by looping through unique countries
    for _, row in data.iterrows():
        country_code = row['Country Code 2']  # Using 2-letter country code
        country_name = row['Country']
        if country_code:
            flag_url = f"https://flagcdn.com/64x48/{country_code.lower()}.png"  # Correct flag URL
            cols[col_idx].markdown(f"""
            <div style="text-align:center;">
                <img src="{flag_url}" width="40px" height="30px" style="margin-bottom:5px;"><br>
                {country_name}
            </div>
            """, unsafe_allow_html=True)
            col_idx += 1
            if col_idx >= 5:  # Move to the next row after 5 flags
                col_idx = 0

if __name__ == "__main__":
    main()
