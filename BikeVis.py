import pandas as pd
import datetime as dt
import geopandas as gpd
import folium
import branca.colormap as cm
from folium.plugins import TimestampedGeoJson
#from folium.features import GeoJsonPopup, GeoJsonTooltip
#Reading json file
bikedata=pd.read_json('/Users/alexanderlindell/Documents/Programmering /Python/Sthlm-EbikeVis-/stations2-copy.json')
#Dict with column names 
df={'date':[],'station':[],'occupancy':[],'capacity':[],'long':[],'lat':[]}
df
for _,row in bikedata.iterrows():
    for item in row:
        for cell in item['data']: 
            #print(cell['date'])
            df['occupancy'].append(cell['occupancy'])
            df['capacity'].append(cell['capacity'])
            df['date'].append(cell['date'])
            df['station'].append(item['id'])
            #print(cell['date'],item['coord']['lon'],item['coord']['lat'])
            df['long'].append(item['coord']['lon'])
            df['lat'].append(item['coord']['lat'])

#Setting up dataframe from dict and fix formatting on timestamp. 
data=pd.DataFrame.from_dict(df)
data['date']= pd.to_datetime(df['date'],unit='s')
data['date']=data['date'].dt.strftime('%Y-%m-%dT%H:%M:%S')
data=data.sort_values(by='date')
data
#Setting the status colors for occupancy dependent on capacity.
colorbar = cm.StepColormap(colors=['#15B01A','#FFA500','#FF7F00','#FF4500','#8B0000'], vmin=0,vmax=1)
data['color']=list(colorbar(x/y) for x,y in zip(data['occupancy'],data['capacity']))
#Adjusting size of markers. 
def setradius(size):
    radius=4 if (size*0.2) < 4 else (size*0.2)
    return(radius)

features = [{'type': 'Feature',
            'geometry': {'type':'Point', 'coordinates':[row['long'],row['lat']]},
            'properties': {'time': row['date'],
                           'popup':('Occupancy: '+str(row['occupancy'])+'/'+str(row['capacity'])),
                           'style': {'color' : ''},
                           'icon': 'circle',
                           'iconstyle':{'fillColor': row['color'],
                                        'fillOpacity': 1,
                                        'stroke': 'true',
                                        'radius': setradius(row['capacity'])}}
            } for _,row in data.iterrows()]
map = folium.Map(location = [59.32760990395156, 18.06760960579676], tiles='Stamen Toner' , zoom_start = 12)
TimestampedGeoJson( features,
                            add_last_point = True,
                           period='PT10M',
                           loop_button=True,
                           time_slider_drag_update=True,
                           transition_time = 100,
                           
                            ).add_to(map)
map.add_child(colorbar)
map

map.save('SthlmEBikeVis.html')
