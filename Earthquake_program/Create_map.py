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
            zoom_start = self.zoom_level
        )

        return ExampleTurkiyeMap

class ZoomMap():
    def zoomMap(value,location):
        __location = location
        Zoom_level = value

        NewMap = folium.Map(
            location = __location,
            zoom_start = Zoom_level
        )

        return NewMap.get_root().render()

class DrawEarthquakeZones():
    def __init__(self,Map,latitude,Longtidue,Magnitude):
        super().__init__()
        self.map = Map
                              
        self.latidude = latitude
        self.longtidude = Longtidue
        self.magnitude = Magnitude


    def Draw(self):
        popup = f'Büyüklük:{self.magnitude}'

        self.marker = folium.Marker(location=[self.latidude,self.longtidude],
                                    popup=popup,
                                    ).add_to(self.map)
        
        return self.marker

        

        



    
    




