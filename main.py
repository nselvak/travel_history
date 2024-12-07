import streamlit as st
from google_sheets import setup_google_sheets, fetch_and_clean_data
from map_visualization import create_map
from ui_components import display_map, display_flags

def main():
    st.title("Travel Tracker Map")
    st.markdown("""
    Map shows the countries visited, the number of times you've been there. Hover over the countries to see details such as:
    - The number of visits
    - The cities you have visited in each country
    - Total number of days spent in the country
    """)

    client = setup_google_sheets()
    sheet = client.open("TravelData").worksheet("Travel")
    data = fetch_and_clean_data(sheet)

    m = create_map(data)
    display_map(m)
    display_flags(data)

if __name__ == "__main__":
    main()
