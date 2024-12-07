import streamlit as st
from streamlit_folium import st_folium

# Function to load external CSS from the styles.css file
def load_css():
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to display the interactive map
def display_map(m):
    st.markdown("### Interactive Travel Map")
    st_folium(m)

# Function to display flags of countries visited
def display_flags(data):
    st.markdown("### Flags of Countries Visited")
    cols = st.columns(5)
    col_idx = 0
    for _, row in data.iterrows():
        country_code = row['Country Code 2']
        country_name = row['Country']
        if country_code:
            flag_url = f"https://flagcdn.com/64x48/{country_code.lower()}.png"
            cols[col_idx].markdown(f"""
            <div class="flag-container">
                <img src="{flag_url}" width="40px" height="30px">
                <br>{country_name}
            </div>
            """, unsafe_allow_html=True)
            col_idx += 1
            if col_idx >= 5:
                col_idx = 0
