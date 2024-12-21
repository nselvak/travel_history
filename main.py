"""
Main script for the Travel Tracker Map Streamlit app.
This script loads custom CSS, fetches travel data from Google Sheets,
generates a map, and displays the map and flags of visited countries.
"""

import streamlit as st
from google_sheets import setup_google_sheets, fetch_and_clean_data
from map_visualization import create_map
from ui_components import display_map, display_flags, load_css

def main():
    # Load custom CSS
    load_css()

    st.title("Travel Tracker Map")
    st.markdown("""
    Map shows the countries visited, the number of times you've been there. Hover over the countries to see details such as:
    - The number of visits
    - The cities you have visited in each country
    - Total number of days spent in the country
    """)

    # Set up Google Sheets client and fetch data
    client = setup_google_sheets()
    sheet = client.open("TravelData").worksheet("Travel")
    data = fetch_and_clean_data(sheet)

    # Generate the map based on the fetched data
    m = create_map(data)

    # Display map and flags using UI components
    display_map(m)
    display_flags(data)

if __name__ == "__main__":
    main()