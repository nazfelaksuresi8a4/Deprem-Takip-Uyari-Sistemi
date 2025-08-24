import folium 
import folium.map
import pandas
import numpy
import Gui
import __Api
from folium.plugins import HeatMap

class ExampleMap():
    def __init__(self):
        super().__init__()
        self.location = [39,35]
        self.zoom_level = 6

    def CreateExampleMap(self):

        ExampleTurkiyeMap = folium.Map(
            location = self.location,
            zoom_start = self.zoom_level,
            tiles='Cartodb dark_matter'
        )

        return ExampleTurkiyeMap

class ZoomMap():
    def __init__(self,value,location,marker_locations,heatmap_locations,popups,map_type):
        super().__init__()
        self.zoom_level = value
        self.location = location
        self.marker_locations = marker_locations
        self.heatmap_locations = heatmap_locations
        self.popups = popups
        self.map_type = map_type

    def zoomMap(self):
        NewMap = folium.Map(
                    location = self.location,
                    zoom_start = self.zoom_level,
                    tiles='Cartodb dark_matter'
            )

        for fdata__f,popupf in zip(self.marker_locations,self.popups):
            popupf = f'Ülke:{popupf[1]}\nŞehir:{popupf[2]}\nBüyüklük:{popupf[0]}'

            folium.Marker(location=fdata__f,
                                popup=popupf).add_to(NewMap)

        return NewMap.get_root().render()

    def zoomHeatmap(self):
        trash = []
        __location = self.location
        Zoom_level = self.zoom_level

        NewMapf = folium.Map(
                location = __location,
                zoom_start = Zoom_level,
                tiles='Cartodb dark_matter'
        )

        for fdata__ in self.heatmap_locations:
                HeatMap([fdata__]).add_to(NewMapf)

        return NewMapf.get_root().render()


class DrawEarthquakeZones():
    def __init__(self,Map,latitude,Longtidue,Magnitude,Country,City,map_type):
        super().__init__()
        self.map = Map
                                
        self.latidude = latitude
        self.longtidude = Longtidue
        self.magnitude = Magnitude
        self.country = Country
        self.city = City


    def Draw(self):
        popup = f'Ülke:{self.country}\nŞehir:{self.city}\nBüyüklük:{str(self.magnitude)}'

        self.marker = folium.Marker(location=[self.latidude,self.longtidude],
                                        popup=popup,
                                        ).add_to(self.map)
            
        return self.marker

    def Draw_heatmap(self):
        try:
            print(self.latidude,self.longtidude)
            data = [[self.latidude,self.longtidude,float(self.magnitude)]]

            self.heatmap = HeatMap(data).add_to(self.map)
                
            return self.heatmap
        except Exception as  heatmap_exception:
            print(heatmap_exception)
            
        
    

        



    
    
