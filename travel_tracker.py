import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import streamlit as st

# === Google Sheets API Setup ===
def setup_google_sheets():
    """
    Set up and authorize access to Google Sheets.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials_file = "credentials.json"  # Path to credentials.json
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(credentials)
    return client

# === Fetch and Clean Data ===
@st.cache(ttl=600, suppress_st_warning=True)  # Cache data for 10 minutes
def fetch_and_clean_data(_sheet):
    """
    Fetch data from Google Sheets and clean it for visualization.
    """
    # Load data into a DataFrame
    data = pd.DataFrame(_sheet.get_all_records())

    # Clean data: Group by country and aggregate visit counts and unique places
    data = data.groupby("Country", as_index=False).agg({
        "Visits": "sum",  # Sum visits for each country
        "Places": lambda x: ", ".join(sorted(set(", ".join(x).split(", "))))  # Unique and sorted city names
    })
    return data

# === Streamlit UI ===
def main():
    st.title("Travel Tracker Map 🌍")

    st.markdown("""
    This interactive map highlights the countries you've visited. Hover over each country for details like:
    - **Number of visits**
    - **Cities visited**
    """)

    # Set up Google Sheets API and fetch data
    client = setup_google_sheets()
    sheet = client.open("TravelData").worksheet("Travel")  # Explicitly access the "Travel" worksheet
    
    # Fetch and clean data
    data = fetch_and_clean_data(sheet)

    # Plotly Choropleth Map
    fig = px.choropleth(
        data,
        locations="Country",
        locationmode="country names",
        color="Visits",
        hover_name="Country",
        hover_data={"Visits": True, "Places": True},
        color_continuous_scale="Viridis",
        title="My Travel Map"
    )

    # Display the map
    st.plotly_chart(fig, use_container_width=True)

# === Main Entry Point ===
if __name__ == "__main__":
    main()
