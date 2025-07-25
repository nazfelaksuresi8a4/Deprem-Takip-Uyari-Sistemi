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

class LoadGui(QMainWindow):
    def __init__(self):
        super().__init__()

        #datas#
        citys = file_actions.CityList().List()
        citys = json.loads(citys)
        token = 'Tüm iller'

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
        self.reload_map = QPushButton('Haritayı yenile')
        self.reset_map = QPushButton('Haritayı sıfırla')
        self.go_back_map = QPushButton('Eski noktaya geri dön')

        self.map_zoom_label = QLabel(text='Zoom oranı: 6')
        self.map_zoom_label.setAlignment(Qt.AlignCenter)

        self.map_zoom_slider = QSlider(Qt.Horizontal)
        self.map_zoom_slider.setValue(6)
        self.map_zoom_slider.setRange(0, 19)

        self.start_time = QLineEdit()
        self.end_time = QLineEdit()
        self.start_hms = QLineEdit()
        self.end_hms = QLineEdit()
        self.limit_input = QLineEdit()

        self.start_time_label = QLabel(text='Başlangıç yılı')
        self.end_time_label = QLabel(text='Bitiş yılı')
        self.start_hms_label = QLabel(text='Başlangıç Saat/Dakika/Saniye')
        self.end_hms_label = QLabel(text='Bitiş Saat/Dakika/Saniye')
        self.limit_label = QLabel(text='Kaç veri çekilsin')

        self.start_time.setPlaceholderText('Başlangıç yılını girin...')
        self.end_time.setPlaceholderText('Bitiş yılını girin...')
        self.start_hms.setPlaceholderText('Başlangıç Saat/Dakika/Saniyesini girin...')
        self.end_hms.setPlaceholderText('Bitiş Başlangıç Saat/Dakika/Saniyesini girin...')
        self.limit_input.setPlaceholderText('Kaç tane konum bilgisi istersin...')

        self.start_time_label.setAlignment(Qt.AlignCenter)
        self.end_time_label.setAlignment(Qt.AlignCenter)
        self.start_hms_label.setAlignment(Qt.AlignCenter)
        self.end_hms_label.setAlignment(Qt.AlignCenter)

        self.start_time.setAlignment(Qt.AlignCenter)
        self.end_time.setAlignment(Qt.AlignCenter)
        self.start_hms.setAlignment(Qt.AlignCenter)
        self.end_hms.setAlignment(Qt.AlignCenter)

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

        self.earthquake_data_splitter.addWidget(self.select_proveince_label)
        self.earthquake_data_splitter.addWidget(self.city_label)
        self.earthquake_data_splitter.addWidget(self.citys_list)

        self.map_side.addWidget(self.map_label)
        self.map_side.addWidget(self.webwidget)
        self.map_side.addWidget(self.reload_map)
        self.map_side.addWidget(self.reset_map)
        self.map_side.addWidget(self.go_back_map)

        self.map_side.addWidget(self.map_zoom_label)
        self.map_side.addWidget(self.map_zoom_slider)

        self.map_actions_splitter.addWidget(self.earthquake_data_splitter)

        self.earthquake_data_splitter.addWidget(self.start_hms_label)
        self.earthquake_data_splitter.addWidget(self.start_hms)
        self.earthquake_data_splitter.addWidget(self.end_hms_label)
        self.earthquake_data_splitter.addWidget(self.end_hms)
        self.earthquake_data_splitter.addWidget(self.start_time_label)
        self.earthquake_data_splitter.addWidget(self.start_time)
        self.earthquake_data_splitter.addWidget(self.end_time_label)
        self.earthquake_data_splitter.addWidget(self.end_time)
        self.earthquake_data_splitter.addWidget(self.limit_label)
        self.earthquake_data_splitter.addWidget(self.limit_input)
        self.earthquake_data_splitter.addWidget(self.apply_earthquake_datas)
        for __widget in container:
            __widget.setStyleSheet('background-color:white')
            self.earthquake_data_splitter.addWidget(__widget)

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
        self.reset_map.clicked.connect(self.MapReset)
        self.reload_map.clicked.connect(self.RefreshMap)
        self.apply_earthquake_datas.clicked.connect(self.connect_api)

        self.location_timer = QTimer(self)
        self.location_timer.timeout.connect(self.update_map_location)
        self.location_timer.start(1) 
    
    def StartZoom(self):
        self.zoom_level = self.map_zoom_slider.value()
        
        __Function = Create_map.ZoomMap.zoomMap(value=self.zoom_level,location=self.location)

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
        start_time = self.start_time.text()
        end_time = self.end_time.text()
        start_hms = self.start_hms.text()
        end_hms = self.end_hms.text()
        lim_data = self.limit_input.text()

        start_date = f'{start_time}T{start_hms}'
        end_date = f'{end_time}T{end_hms}'

        host = CustomData(start=start_date,end=end_date,lim=lim_data)

        host_data = host.Parse()

        for data in host_data:
            MarkerFunction = Create_map.DrawEarthquakeZones(Map=self.Turkiye_map,
                                           latitude=data[0],
                                           Longtidue=data[1],
                                           Magnitude=data[2])

            MarkedMap = MarkerFunction.Draw()

            self.webwidget.setHtml(MarkedMap.get_root().render())  

sp = QApplication(sys.argv) 
sw = LoadGui()

def ShowWindow():
    sw.show()

    
