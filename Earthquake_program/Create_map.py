import folium 
import folium.map
import pandas
import numpy
import Gui
import __Api

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
    def zoomMap(value,location,marker_locations,popups):
        __location = location
        Zoom_level = value

        NewMap = folium.Map(
            location = __location,
            zoom_start = Zoom_level,
            tiles='Cartodb dark_matter'
        )

        for fdata__,popup in marker_locations,popups:
            folium.Marker(location=fdata__,
                          popup=popup).add_to(NewMap)

        return NewMap.get_root().render()

class DrawEarthquakeZones():
    def __init__(self,Map,latitude,Longtidue,Magnitude,Country,City):
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

        

        



    
    




