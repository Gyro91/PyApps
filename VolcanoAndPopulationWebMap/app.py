import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation< 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
            return 'red'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38.58,-99.09], zoom_start=6, tiles="Stamen Terrain")

fgVolcanoes = folium.FeatureGroup(name="Volcanoes")

for lt, lg, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgVolcanoes.add_child(folium.Marker(location=[lt, lg], popup=folium.Popup(iframe), icon=folium.Icon(color=color_producer(el))))

fgPopulation = folium.FeatureGroup(name="Population")

fgPopulation.add_child(folium.GeoJson(data=(open("world.json", "r", encoding="utf-8-sig").read()),
style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgPopulation)
map.add_child(fgVolcanoes)
map.add_child(folium.LayerControl())

map.save("Map1.html")