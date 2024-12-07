import geopandas as gpd
import folium
from branca.colormap import linear

def create_map(data, world_shapefile="image/world.shp"):
    world = gpd.read_file(world_shapefile)
    if world.crs is None:
        world.set_crs("EPSG:4326", allow_override=True, inplace=True)

    m = folium.Map(location=[1.3521, 103.8198], zoom_start=2, tiles="CartoDB positron")
    folium.GeoJson(world, style_function=lambda x: {
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0
    }).add_to(m)

    max_visits = data['Visits'].max()
    color_scale = linear.YlOrRd_09.scale(0, max_visits)

    for _, row in data.iterrows():
        country_code = row['Country Code']
        country_name = row['Country']
        visits = row['Visits']
        places = row['Places']
        days = row['Total Number of Days']
        color = color_scale(visits)

        popup = folium.Popup(f"<b>{country_name}</b><br><br>Visits: {visits}<br>Cities: {places}<br>Total Days: {days}", max_width=300)
        folium.GeoJson(
            world[world['SOV_A3'] == country_code].geometry,
            style_function=lambda x, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            popup=popup
        ).add_to(m)
    return m
