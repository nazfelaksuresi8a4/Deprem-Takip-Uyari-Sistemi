from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import Create_map
from __Api import CustomData
from Create_map import DrawEarthquakeZones
import file_actions
import json
import sys
import folium as fl

class LoadGui(QMainWindow):
    def __init__(self):
        super().__init__()

        #datas#
        citys = file_actions.CityList().List()
        citys = json.loads(citys)
        token = 'Tüm iller'

        self.Map = None
        self.strings = []
        self.coordinates = []

        #map-datas#
        self.location = None

        css_file = r'program_css.qss'

        #main#
        self.tabbar = QTabWidget(self)

        #layouts#
        self.main_layout = QHBoxLayout()
        self.scroll_area_layout = QVBoxLayout()

        #widgets-main#
        self.main_widget = QWidget()
        self.second_widget = QWidget()

        #widgets-widget#
        container = [QLabel(text=''),
                     QLabel(text=''),
                     QLabel(text=''),
                     QLabel(text='')]

        self.scroll_area_widget = QWidget()

        #tab-bar-actions#
        self.tabbar.addTab(self.main_widget, 'Deprem Haritası')
        self.tabbar.addTab(self.second_widget, 'Yangın Haritası')

        #tool-widgets#
        self.webwidget = QWebEngineView()

        self.city_label = QLabel(text='-*Deprem Sorgula*-')
        self.select_proveince_label = QLabel(text='--İl seçin--')

        self.map_label = QLabel(text='--Deprem Haritası--')
        self.go_back_map = QPushButton('Eski noktaya geri dön')

        self.map_zoom_label = QLabel(text='Zoom oranı: 6')
        self.map_zoom_label.setAlignment(Qt.AlignCenter)

        self.map_zoom_slider = QSlider(Qt.Horizontal)
        self.map_zoom_slider.setValue(6)
        self.map_zoom_slider.setRange(0, 19)

        self.start_time_splitter = QSplitter(Qt.Horizontal)
        self.end_time_splitter = QSplitter(Qt.Horizontal)

        self.start_date_splitter = QSplitter(Qt.Horizontal)
        self.end_date_splitter = QSplitter(Qt.Horizontal)

        #time-side#
        #start-side#
        self.start_time_setting = QTimeEdit()

        #end-side#
        #hour#
        self.end_time_setting = QTimeEdit()

        #date-side#
        #start-side#
        self.start_date_setting = QDateEdit()

        #end-side#
        self.end_date_setting = QDateEdit()

        #limit-input#

        self.limit_input = QSpinBox()
        self.limit_input.setValue(81)
        self.limit_input.setRange(0,2000)

        #time-date-settings#
        self.start_time_setting.setDisplayFormat('HH:mm:ss')
        self.end_time_setting.setDisplayFormat('HH:mm:ss')

        self.start_date_setting.setAlignment(Qt.AlignCenter)
        self.end_date_setting.setAlignment(Qt.AlignCenter)
        self.start_time_setting.setAlignment(Qt.AlignCenter)
        self.end_time_setting.setAlignment(Qt.AlignCenter)

        self.limit_input.setAlignment(Qt.AlignCenter)

        self.start_time_label = QLabel(text='Başlangıç yılı')
        self.end_time_label = QLabel(text='Bitiş yılı')
        self.start_hms_label = QLabel(text='Başlangıç Saat/Dakika/Saniye')
        self.end_hms_label = QLabel(text='Bitiş Saat/Dakika/Saniye')
        self.limit_label = QLabel(text='Kaç veri çekilsin')

        #self.start_time.setPlaceholderText('Başlangıç yılını girin...')
        #self.end_time.setPlaceholderText('Bitiş yılını girin...')
        #self.start_hms.setPlaceholderText('Başlangıç Saat/Dakika/Saniyesini girin...')
        #self.end_hms.setPlaceholderText('Bitiş Başlangıç Saat/Dakika/Saniyesini girin...')
        #self.limit_input.setPlaceholderText('Kaç tane konum bilgisi istersin...')

        self.start_time_label.setAlignment(Qt.AlignCenter)
        self.end_time_label.setAlignment(Qt.AlignCenter)
        self.start_hms_label.setAlignment(Qt.AlignCenter)
        self.end_hms_label.setAlignment(Qt.AlignCenter)

        self.apply_earthquake_datas = QPushButton(text='Sorgula')

        #splitters#
        self.splitters_side = QSplitter(Qt.Horizontal)
        
        self.city_splitter = QSplitter(Qt.Vertical)
        self.map_side = QSplitter(Qt.Vertical)

        self.map_actions_splitter = QSplitter(Qt.Horizontal)
        self.zoom_splitter = QSplitter(Qt.Vertical)
        self.earthquake_data_splitter = QSplitter(Qt.Vertical)

        #list-areas#
        self.citys_list = QComboBox()

        #layout-actions#
        self.main_widget.setLayout(self.main_layout)
        self.scroll_area_widget.setLayout(self.scroll_area_layout)

        self.setCentralWidget(self.tabbar)
        
        #adding-widgets-1#
        self.main_layout.addWidget(self.splitters_side)
        
        #adding-widgets-2#
        self.splitters_side.addWidget(self.city_splitter)
        self.splitters_side.addWidget(self.map_side)
        self.splitters_side.addWidget(self.map_actions_splitter)

        #self.earthquake_data_splitter.addWidget(self.select_proveince_label)
        self.earthquake_data_splitter.addWidget(self.city_label)
        self.earthquake_data_splitter.addWidget(self.citys_list)

        self.map_side.addWidget(self.map_label)
        self.map_side.addWidget(self.webwidget)
        self.map_side.addWidget(self.go_back_map)

        self.map_side.addWidget(self.map_zoom_label)
        self.map_side.addWidget(self.map_zoom_slider)

        self.map_actions_splitter.addWidget(self.earthquake_data_splitter)

        self.earthquake_data_splitter.addWidget(self.start_hms_label)
        self.earthquake_data_splitter.addWidget(self.start_time_setting)
        self.earthquake_data_splitter.addWidget(self.end_hms_label)
        self.earthquake_data_splitter.addWidget(self.end_time_setting)
        self.earthquake_data_splitter.addWidget(self.start_time_label)
        self.earthquake_data_splitter.addWidget(self.start_date_setting)
        self.earthquake_data_splitter.addWidget(self.end_time_label)
        self.earthquake_data_splitter.addWidget(self.end_date_setting)
        self.earthquake_data_splitter.addWidget(self.limit_label)
        self.earthquake_data_splitter.addWidget(self.limit_input)
        self.earthquake_data_splitter.addWidget(self.apply_earthquake_datas)


        #setting-widget-2#
        self.city_label.setAlignment(Qt.AlignCenter)
        self.map_label.setAlignment(Qt.AlignCenter)
        self.select_proveince_label.setAlignment(Qt.AlignCenter)

        #adding-widgets-3#
        self.citys_list.addItem(token)

        #map actions#
        self.Turkiye_map = Create_map.ExampleMap().CreateExampleMap()
        self.webwidget.setHtml(self.Turkiye_map.get_root().render())

        for city in range(1, len(citys)):
            self.citys_list.addItem(citys[f'{city}'])  

        #css side#    
        css_data = open(css_file,'r').read()
        self.setStyleSheet(str(css_data))

        #signal-slots#
        self.map_zoom_slider.valueChanged.connect(self.StartZoom)
        self.apply_earthquake_datas.clicked.connect(self.connect_api)

        self.location_timer = QTimer(self)
        self.location_timer.timeout.connect(self.update_map_location)
        self.location_timer.start(1) 
    
    def StartZoom(self):
        self.zoom_level = self.map_zoom_slider.value()
        
        __Function = Create_map.ZoomMap.zoomMap(value=self.zoom_level,location=self.location,marker_locations=self.coordinates,popups=self.strings)

        self.webwidget.setHtml(__Function)
    
    def update_map_location(self):
        static_location = self.Turkiye_map.location

        self.location = static_location
    
    def MapReset(self):
        old_map = Create_map.ExampleMap().CreateExampleMap()
        self.webwidget.setHtml(old_map.get_root().render())
    
    def RefreshMap(self):
        self.webwidget.reload()
    
    def connect_api(self):
        self.new_map = fl.Map(location=[39,35],
                              zoom_start=6,
                              tiles='Cartodb dark_matter')
        
        self.start_date = self.start_date_setting.date().toPyDate()
        self.end_date = self.end_date_setting.date().toPyDate()

        self.start_time = self.start_time_setting.time().toPyTime()
        self.end_time = self.end_time_setting.time().toPyTime()

        self.start_date_tokenized = f'{self.start_date}T{self.start_time}'
        self.end_date_tokenized = f'{self.end_date}T{self.end_time}'

        lim_data = self.limit_input.value()

        host = CustomData(start=self.start_date_tokenized, end=self.end_date_tokenized, lim=lim_data)

        host_data = host.Parse()

        for coordinate_data,string_data in host_data[0],host_data[1]:
            self.coordinates.append(coordinate_data)
            self.strings.append(string_data)
            

        for data in host_data:
            MarkerFunction = Create_map.DrawEarthquakeZones(Map=self.new_map,
                                           latitude=data[0],
                                           Longtidue=data[1],
                                           Magnitude=data[2],
                                           Country=data[3],
                                           City=data[4])

            MarkedMap = MarkerFunction.Draw()

            self.webwidget.setHtml(MarkedMap.get_root().render())  
        

sp = QApplication(sys.argv) 
sw = LoadGui()

def ShowWindow():
    sw.show()

    
