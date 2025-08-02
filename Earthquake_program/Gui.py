from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import Create_map
from __Api import CustomData
from Create_map import DrawEarthquakeZones
import timezone
import file_actions
import json
import sys
import folium as fl

class LoadGui(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName('main_window')

        #datas#
        citys = file_actions.CityList().List()
        citys = json.loads(citys)
        token = 'Tüm iller'

        self.Map = None
        self.strings = []
        self.coordinates = []

        self.coordinates_recent = []
        self.strings_recent = []

        #map-datas#
        self.location = None

        css_file = r'program_css.qss'

        #main#

        #layouts#
        self.main_layout = QHBoxLayout()
        self.scroll_area_layout = QVBoxLayout()

        #widgets-main#
        self.main_widget = QWidget()
        self.second_widget = QWidget()

        #widgets-widget#
        container = [QLabel(text=''),
                     QLabel(text=''),
                     QLabel(text='V-1.0')]
        
        containerf = [QLabel(text=''),
                     QLabel(text=''),
                     QLabel(text='Deprem Takip sistemi')]

        self.scroll_area_widget = QWidget()

        #tab-bar-actions#

        #tool-widgets#
        self.webwidget = QWebEngineView()

        self.city_label = QLabel(text='Deprem Sorgula')
        self.city_label.setObjectName('sort_label')

        self.select_proveince_label = QLabel(text='--İl seçin--')

        reset_settings = QPushButton('Ayarları sıfırla')

        self.map_label = QLabel(text='--Deprem Haritası--')
        self.go_back_map = QPushButton('Eski noktaya geri dön')

        self.map_zoom_label = QLabel(text='Zoom oranı: 6')
        self.map_zoom_label.setAlignment(Qt.AlignCenter)

        self.map_zoom_slider = QSlider(Qt.Horizontal)
        self.map_zoom_slider.setValue(6)
        self.map_zoom_slider.setRange(0, 19)

        recent_earthquakes_label = QLabel(text='Son depremler')

        earthquake_date_label = QLabel(text='Başlangıç tarihi(Eski)')
        self.earthquake_date = QDateEdit()
        earthquake_time_label = QLabel(text='Başlangıç saati(Eski)')
        self.earthquake_time = QTimeEdit()

        recent_earthquake_date_label = QLabel(text='Bitiş tarihi(Güncel)')
        self.recent_date = QDateEdit()
        recent_earthquake_time_label = QLabel(text='Bitiş saati(Güncel)')
        self.recent_time = QTimeEdit()

        self.recent_date.setDisplayFormat('yyyy-MM-dd')
        self.recent_time.setDisplayFormat('HH:mm:ss')

        self.earthquake_date.setDisplayFormat('yyyy-MM-dd')
        self.earthquake_time.setDisplayFormat('HH:mm:ss')

        self.recent_earthquakes_list = QListWidget()
        self.sort_earthquakes = QPushButton(text='Son depremleri çek')
        self.show_recent_earthquakes_with_map = QPushButton('Son depremleri haritada göster')
        

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

        self.start_date_setting.setDisplayFormat('yyyy-MM-dd')
        self.end_date_setting.setDisplayFormat('yyyy-MM-dd')

        #limit-input#

        self.limit_input = QSpinBox()
        self.limit_input.setValue(81)
        self.limit_input.setRange(0,2000)

        self.limit_input_2 = QSpinBox()
        self.limit_input_2.setValue(81)
        self.limit_input_2.setRange(0,2000)

        #time-date-settings#
        self.start_time_setting.setDisplayFormat('HH:mm:ss')
        self.end_time_setting.setDisplayFormat('HH:mm:ss')

        self.start_date_setting.setAlignment(Qt.AlignCenter)
        self.end_date_setting.setAlignment(Qt.AlignCenter)
        self.start_time_setting.setAlignment(Qt.AlignCenter)
        self.end_time_setting.setAlignment(Qt.AlignCenter)
        earthquake_date_label.setAlignment(Qt.AlignCenter)
        earthquake_time_label.setAlignment(Qt.AlignCenter)
        recent_earthquakes_label.setAlignment(Qt.AlignCenter)
        recent_earthquake_date_label.setAlignment(Qt.AlignCenter)
        recent_earthquake_time_label.setAlignment(Qt.AlignCenter)

        recent_earthquakes_label.setObjectName('recent_earthquakes')

        self.limit_input.setAlignment(Qt.AlignCenter)
        self.limit_input_2.setAlignment(Qt.AlignCenter)

        self.start_time_label = QLabel(text='Başlangıç yılı')
        self.end_time_label = QLabel(text='Bitiş yılı')
        self.start_hms_label = QLabel(text='Başlangıç Saati')
        self.end_hms_label = QLabel(text='Bitiş Saati')
        self.limit_label = QLabel(text='Kaç veri çekilsin')
        self.limit_label_2 = QLabel(text='Kaç veri çekilsin')

        self.limit_label_2.setAlignment(Qt.AlignCenter)

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
        
        self.recent_earthquakes_splitter = QSplitter(Qt.Vertical)
        self.map_side = QSplitter(Qt.Vertical)
        self.city_splitter = QSplitter(Qt.Vertical)

        self.map_actions_splitter = QSplitter(Qt.Horizontal)
        self.zoom_splitter = QSplitter(Qt.Vertical)
        self.earthquake_data_splitter = QSplitter(Qt.Vertical)

        #list-areas#
        self.citys_list = QComboBox()

        #layout-actions#
        self.main_widget.setLayout(self.main_layout)
        self.scroll_area_widget.setLayout(self.scroll_area_layout)

        self.setCentralWidget(self.main_widget)
        
        #adding-widgets-1#
        self.main_layout.addWidget(self.splitters_side)
        
        #adding-widgets-2#
        self.splitters_side.addWidget(self.recent_earthquakes_splitter)
        self.splitters_side.addWidget(self.map_side)
        self.splitters_side.addWidget(self.earthquake_data_splitter)

        self.recent_earthquakes_splitter.addWidget(recent_earthquakes_label)
        self.recent_earthquakes_splitter.addWidget(earthquake_date_label)
        self.recent_earthquakes_splitter.addWidget(self.earthquake_date)
        self.recent_earthquakes_splitter.addWidget(earthquake_time_label)
        self.recent_earthquakes_splitter.addWidget(self.earthquake_time)
        self.recent_earthquakes_splitter.addWidget(recent_earthquake_date_label)
        self.recent_earthquakes_splitter.addWidget(self.recent_date)
        self.recent_earthquakes_splitter.addWidget(recent_earthquake_time_label)
        self.recent_earthquakes_splitter.addWidget(self.recent_time)
        self.recent_earthquakes_splitter.addWidget(self.limit_label_2)
        self.recent_earthquakes_splitter.addWidget(self.limit_input_2)
        self.recent_earthquakes_splitter.addWidget(self.recent_earthquakes_list)
        self.recent_earthquakes_splitter.addWidget(self.sort_earthquakes)
        self.recent_earthquakes_splitter.addWidget(self.show_recent_earthquakes_with_map)
        for _container in containerf:
            _container.setStyleSheet('background-color:rgb(25, 19, 19);border:none')
            _container.setAlignment(Qt.AlignCenter)
            self.recent_earthquakes_splitter.addWidget(_container)

        self.map_side.addWidget(self.map_label)
        self.map_side.addWidget(self.webwidget)
        self.map_side.addWidget(self.go_back_map)
        self.map_side.addWidget(self.map_zoom_label)
        self.map_side.addWidget(self.map_zoom_slider)

        #self.earthquake_data_splitter.addWidget(self.select_proveince_label)
        self.earthquake_data_splitter.addWidget(self.city_label)
        #self.earthquake_data_splitter.addWidget(self.citys_list)
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
        self.earthquake_data_splitter.addWidget(reset_settings)
        for _container in container:
            _container.setStyleSheet('background-color:rgb(25, 19, 19);border:none')
            _container.setAlignment(Qt.AlignCenter)
            self.earthquake_data_splitter.addWidget(_container)


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
        self.optimize_dates()

        self.map_zoom_slider.valueChanged.connect(self.StartZoom)
        self.apply_earthquake_datas.clicked.connect(self.connect_api)
        self.sort_earthquakes.clicked.connect(self.sort_recent_earthquakes_function)
        self.show_recent_earthquakes_with_map.clicked.connect(self.draw_earthquakes_function)


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
        try:
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

            for data in host_data:
                MarkerFunction = Create_map.DrawEarthquakeZones(Map=self.new_map,
                                            latitude=data[0],
                                            Longtidue=data[1],
                                            Magnitude=data[2],
                                            Country=data[3],
                                            City=data[4])
                
                self.coordinate_matris = [data[0],data[1]]
                self.string_matris = [data[2],data[3],data[4]]

                self.coordinates.append(self.coordinate_matris)
                self.strings.append(self.string_matris)

                MarkedMap = MarkerFunction.Draw()

                self.webwidget.setHtml(MarkedMap.get_root().render())  
        except Exception as exception_1:
            QMessageBox.critical(self,'Uyarı',f'{self.start_date} // {self.end_date} tarihleri arasında Deprem görülmemektedir!')

    def optimize_dates(self):
        self.recent_date.setDate(QDate().currentDate())
        self.recent_time.setTime(QTime().currentTime())

        self.earthquake_date.setDate(QDate.currentDate())

    def draw_earthquakes_function(self):
        try:
            self.recent_earthquakes_list.clear()
            
            self.new_map_recent = fl.Map(location=[39,35],
                                zoom_start=6,
                                tiles='Cartodb dark_matter')
            
            self.start_date_recent = self.recent_date.date().toPyDate()
            self.end_date_recent = self.earthquake_date.date().toPyDate()

            self.start_time_recent = self.start_time_setting.time().toPyTime()
            self.end_time_recent = self.end_time_setting.time().toPyTime()

            print(self.start_date_recent)

            self.start_date_tokenized_recent = f'{self.end_date_recent}T{self.end_time_recent}'
            self.end_date_tokenized_recent = f'{self.start_date_recent}T{self.end_time_recent}'

            #lim_data = self.limit_input.value()
            print(self.start_date_tokenized_recent)
            print(self.end_date_tokenized_recent)

            host_recent = CustomData(start=self.start_date_tokenized_recent, end=self.end_date_tokenized_recent, lim=self.limit_input_2.value())

            host_data_recent = host_recent.Parse()

            for data in host_data_recent:
                MarkerFunction_recent = Create_map.DrawEarthquakeZones(Map=self.new_map_recent,
                                            latitude=data[0],
                                            Longtidue=data[1],
                                            Magnitude=data[2],
                                            Country=data[3],
                                            City=data[4])
                
                self.coordinate_matris_recent = [data[0],data[1]]
                self.string_matris_recent = [data[2],data[3],data[4]]

                self.coordinates_recent.append(self.coordinate_matris_recent)
                self.strings_recent.append(self.string_matris_recent)

                MarkedMap_recent = MarkerFunction_recent.Draw()

                self.webwidget.setHtml(MarkedMap_recent.get_root().render())          
        except Exception as exception_2:
            QMessageBox.critical(self,'Uyarı',f'{self.start_date_recent} // {self.end_date_recent} tarihleri arasında Deprem görülmemektedir!')

    def sort_recent_earthquakes_function(self):
        try:
            self.recent_earthquakes_list.clear()

            self.start_date_recent = self.recent_date.date().toPyDate()
            self.end_date_recent = self.earthquake_date.date().toPyDate()

            self.start_time_recent = self.start_time_setting.time().toPyTime()
            self.end_time_recent = self.end_time_setting.time().toPyTime()

            self.start_date_tokenized_f = f'{self.end_date_recent}T{self.end_time_recent}'
            self.end_date_tokenized_f = f'{self.start_date_recent}T{self.start_time_recent}'

            #lim_data = self.limit_input.value()
            print(self.start_date_tokenized_f)
            print(self.end_date_tokenized_f)

            host_recent = CustomData(start=self.start_date_tokenized_f, end=self.end_date_tokenized_f, lim=self.limit_input_2.value())

            host_data_recent_f = host_recent.Parse()

            for data in host_data_recent_f:
                datas = data[2:5]

                formatted_string = QListWidgetItem(f'|| Ülke: {datas[1]} || Şehir: {datas[2]} || Büyüklük: {datas[0]} ||')
                formatted_string.setTextAlignment(Qt.AlignCenter)
                
                self.recent_earthquakes_list.addItem(formatted_string)
                self.recent_earthquakes_list.setItemAlignment(Qt.AlignCenter)

        except Exception as exception_2:
            QMessageBox.critical(self,'Uyarı',f'{self.start_date_recent} // {self.end_date_recent} tarihleri arasında Deprem görülmemektedir! {exception_2}')

sp = QApplication(sys.argv) 

sw = LoadGui()

def ShowWindow():
    sw.show()

    
