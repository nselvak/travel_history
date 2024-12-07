import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import streamlit as st

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
    result = grouped_data.merge(data[["Country", "Country Code"]].drop_duplicates(), on="Country", how="left")

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
    
    # Generate Plotly map
    fig = px.choropleth(
        data,
        locations="Country",
        locationmode="country names",
        color="Visits",  # Color intensity based on the number of visits
        hover_name="Country",  # Hover over country name
        hover_data={"Visits": True, "Places": True, "Country Code": False},  # Show visits and cities on hover
        color_continuous_scale='YlOrRd',  # Warm color scale (yellow to red)
        title="My Travel Map",
        projection="natural earth",  # More natural-looking map projection
        template="plotly_dark"  # Choose a darker, modern template for aesthetics
    )
    
    # Set the color of the water bodies and land
    fig.update_geos(
        landcolor="lightgray",  # Color of the land (countries that are not visited will be light gray)
        showlakes=True,  # Show lakes (ocean-like features)
        lakecolor="lightblue",  # Color of lakes (should be similar to water bodies)
        showland=True,  # Show land
        showcoastlines=True,  # Show coastlines
        coastlinecolor="white",  # Coastline color
        showcountries=True,  # Show countries borders
        countrycolor="white",  # Borders of countries in white
        projection_scale=4,  # Adjust zoom level for the center (Singapore)
        center={"lat": 1.3521, "lon": 103.8198}  # Center on Singapore
    )

    # Display the map in Streamlit
    st.plotly_chart(fig)
    
    # Display flags of countries visited below the map
    st.markdown("### Flags of Countries Visited")

    # Create a container for flags
    cols = st.columns(5)  # Split into 5 columns to limit the number of flags per row
    col_idx = 0  # Start with the first column

    # Display flags by looping through the unique countries
    for _, row in data.iterrows():
        country_code = row['Country Code']
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
            if col_idx >= 5:  # Once 5 flags are displayed, move to the next row
                col_idx = 0

if __name__ == "__main__":
    main()
