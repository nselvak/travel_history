import geopandas as gpd
import folium
from branca.colormap import linear

def get_color(visits, max_visits, color_scale):
    """Return the color based on the number of visits."""
    return color_scale(visits) if max_visits > 0 else "gray"

def create_popup(country_name, visits, places, days):
    """Create a popup with country details."""
    return folium.Popup(f"<b>{country_name}</b><br><br>Visits: {visits}<br>Cities: {places}<br>Total Days: {days}", max_width=300)

def get_style_function(color):
    """Return style function for GeoJson feature."""
    return lambda x: {
        'fillColor': color,
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    }

def create_map(data, world_shapefile="image/world.shp"):
    # Load world shapefile and set CRS if necessary
    world = gpd.read_file(world_shapefile)
    if world.crs is None:
        world.set_crs("EPSG:4326", allow_override=True, inplace=True)

    # Initialize folium map
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=3, tiles="CartoDB positron")
    folium.GeoJson(world, style_function=lambda x: {
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0
    }).add_to(m)

    # Calculate color scale based on visits
    max_visits = data['Visits'].max()
    color_scale = linear.viridis.scale(0, max_visits).to_step(n=5)

    # Loop through each row in data and plot on map
    for _, row in data.iterrows():
        country_code = row['Country Code']
        country_name = row['Country']
        visits = row['Visits']
        places = row['Places']
        days = row['Total Number of Days']

        # Get color and popup
        color = get_color(visits, max_visits, color_scale)
        popup = create_popup(country_name, visits, places, days)

        # Add country to the map with popup and style
        folium.GeoJson(
            world[world['SOV_A3'] == country_code].geometry,
            style_function=get_style_function(color),
            popup=popup
        ).add_to(m)

    # Add the color scale legend to the map
    color_scale.caption = 'Number of Visits'
    color_scale.add_to(m)

    return m
