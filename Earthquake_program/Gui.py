from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import scrapping
import Create_map
from __Api import CustomData
from Create_map import DrawEarthquakeZones
import timezone
import file_actions
import json
import sys
import folium as fl
from folium.plugins import HeatMap
import threading

html_array = []

class Signal(QObject):
    signal = pyqtSignal(str)

    def __init__(self,start_hmsmmy,end_hmsmmy,lim,coordinates,coordinates_heatmap,strings,webwidget,new_map,map_type):
        super().__init__()
        self.start_hmsmmy = start_hmsmmy
        self.end_hmsmmy = end_hmsmmy
        self.lim_data = lim
        self.coordinates_heatmap = coordinates_heatmap
        self.coordinates = coordinates
        self.strings = strings
        self.webwidget = webwidget
        self.new_map = new_map
        self.map_type = map_type

    def run(self):
        host_data = CustomData(start=self.start_hmsmmy, end=self.end_hmsmmy, lim=str(self.lim_data)).Parse()

        for data in host_data:

            MarkerFunction = Create_map.DrawEarthquakeZones(
                                            Map=self.new_map,
                                            latitude=data[0],
                                            Longtidue=data[1],
                                            Magnitude=data[2],
                                            Country=data[3],
                                            City=data[4],
                                            map_type=self.map_type)
            print(data)
                
            self.heatmap_latlonmag = [float(data[0]),float(data[1]),float(data[2])]

            self.coordinate_matris = [data[0],data[1]]
            self.string_matris = [data[2],data[3],data[4]]
            
            self.coordinates_heatmap.append(self.heatmap_latlonmag)
            self.coordinates.append(self.coordinate_matris)
            self.strings.append(self.string_matris)

            if self.map_type == 'Harita gösterimi türü: Klasik harita':
                MarkedMap = MarkerFunction.Draw()

                self.signal.emit(MarkedMap.get_root().render())
            
            elif self.map_type == 'Harita gösterimi türü: Isı haritası':
                MarkedMap = MarkerFunction.Draw_heatmap()

                self.signal.emit(MarkedMap.get_root().render())
    
    def custom_earthquake(self,lat_lon_array,map,Magnitude,Country,City,Map_type):
        host_data =  [lat_lon_array]
        Map = None
        magnitude = None
        country = None
        city = None
        map_type = None

        for data in host_data:
            MarkerFunction = Create_map.DrawEarthquakeZones(
                                Map=self.new_map,
                                latitude=data[0],
                                Longtidue=data[1],
                                Magnitude=data[2],
                                Country=data[3],
                                City=data[4],
                                map_type=self.map_type)
            print(data)
                
            self.heatmap_latlonmag = [float(data[0]),float(data[1]),float(data[2])]

            self.coordinate_matris = [data[0],data[1]]
            self.string_matris = [data[2],data[3],data[4]]
            
            self.coordinates_heatmap.append(self.heatmap_latlonmag)
            self.coordinates.append(self.coordinate_matris)
            self.strings.append(self.string_matris)

            marked_map = MarkerFunction.Draw()
            
            return marked_map.get_root().render()



class LoadGui(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName('main_window')

        self.toolbar_button_heatmap = QPushButton(text='Isı haritası')
        self.toolbar_button_marker = QPushButton(text='Klasik harita')
        self.toolbar_map_type_label = QLabel(text='Harita gösterimi türü: ')

        self.main_toolbar = QToolBar()
        self.main_toolbar.addWidget(self.toolbar_button_heatmap)
        self.main_toolbar.addWidget(self.toolbar_button_marker)
        self.main_toolbar.addWidget(self.toolbar_map_type_label)

        #datas#
        citys = file_actions.CityList().List()
        citys = json.loads(citys)
        token = 'Tüm iller'

        self.Map = None
        self.strings = []
        self.coordinates = []
        self.heatmap_coordinates = []

        self.coordinates_recent = []
        self.strings_recent = []

        #map-datas#
        self.location = None

        self.latidude = []
        self.longitude = []
        self.magnitude = []
        self.country = []
        self.city = []

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

        day_selector_label = QLabel(text='Kaç gün öncenin verilerini istersiniz')
        self.day_selector = QSpinBox()

        self.day_selector.setRange(0,30)
        self.day_selector.setValue(2)

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

        earthquake_date_label = QLabel(text='Başlangıç tarihi')
        self.earthquake_date = QDateEdit()
        earthquake_time_label = QLabel(text='Başlangıç saati')
        self.earthquake_time = QTimeEdit()

        recent_earthquake_date_label = QLabel(text='Bitiş tarihi(Güncel)')
        self.recent_date = QDateEdit()
        recent_earthquake_time_label = QLabel(text='Bitiş saati(Güncel)')
        self.recent_time = QTimeEdit()

        self.recent_date.setDisplayFormat('yyyy-MM-dd')
        self.recent_time.setDisplayFormat('HH:mm:ss')

        self.earthquake_date.setDisplayFormat('yyyy-MM-dd')
        self.earthquake_time.setDisplayFormat('HH:mm:ss')

        self.recent_earthquakes_list = QTableWidget()
        self.sort_earthquakes = QPushButton(text='Son depremleri çek')
        self.show_recent_earthquake_with_map = QPushButton(text='Secili depremin detaylarını haritada göster')
        self.show_recent_earthquakes_with_map = QPushButton(text='Secili depremlerin detaylarını haritada göster')
        

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
        self.limit_input.setRange(0,90000)

        self.limit_input_2 = QSpinBox()
        self.limit_input_2.setValue(81)
        self.limit_input_2.setRange(0,90000)

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
        
        day_selector_label.setAlignment(Qt.AlignCenter)
        self.day_selector.setAlignment(Qt.AlignCenter)


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

        self.recent_earthquakes_list.setColumnCount(7)
        self.recent_earthquakes_list.setRowCount(100)
        self.recent_earthquakes_list.resizeRowsToContents()

        self.recent_earthquakes_list.setHorizontalHeaderItem(0,QTableWidgetItem('Tarih(TS)'))
        self.recent_earthquakes_list.setHorizontalHeaderItem(1,QTableWidgetItem('Enlem'))
        self.recent_earthquakes_list.setHorizontalHeaderItem(2,QTableWidgetItem('Boylam'))
        self.recent_earthquakes_list.setHorizontalHeaderItem(3,QTableWidgetItem('Derinlik(Km)'))
        self.recent_earthquakes_list.setHorizontalHeaderItem(4,QTableWidgetItem('Tip'))
        self.recent_earthquakes_list.setHorizontalHeaderItem(5,QTableWidgetItem('Büyüklük	'))
        self.recent_earthquakes_list.setHorizontalHeaderItem(6,QTableWidgetItem('Yer'))

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

        self.main_toolbar.setParent(self.map_side)

        self.setCentralWidget(self.main_widget)
        
        #adding-widgets-1#
        self.main_layout.addWidget(self.splitters_side)
        
        #adding-widgets-2#
        self.splitters_side.addWidget(self.recent_earthquakes_splitter)
        self.splitters_side.addWidget(self.map_side)
        self.splitters_side.addWidget(self.earthquake_data_splitter)

        #self.recent_earthquakes_splitter.addWidget(recent_earthquakes_label)
        #self.recent_earthquakes_splitter.addWidget(earthquake_date_label)
        #self.recent_earthquakes_splitter.addWidget(self.earthquake_date)
        #self.recent_earthquakes_splitter.addWidget(earthquake_time_label)
        #self.recent_earthquakes_splitter.addWidget(self.earthquake_time)
        #self.recent_earthquakes_splitter.addWidget(self.limit_label_2)
        #self.recent_earthquakes_splitter.addWidget(self.limit_input_2)
        #self.recent_earthquakes_splitter.addWidget(day_selector_label)
        #self.recent_earthquakes_splitter.addWidget(self.day_selector)
        self.recent_earthquakes_splitter.addWidget(self.recent_earthquakes_list)
        self.recent_earthquakes_splitter.addWidget(self.sort_earthquakes)
        self.recent_earthquakes_splitter.addWidget(self.show_recent_earthquake_with_map)
        self.recent_earthquakes_splitter.addWidget(self.show_recent_earthquakes_with_map)

        for _container in containerf:
            _container.setStyleSheet('background-color:rgb(25, 19, 19);border:none')
            _container.setAlignment(Qt.AlignCenter)
            #self.recent_earthquakes_splitter.addWidget(_container)

        self.map_side.addWidget(self.map_label)
        self.map_side.addWidget(self.webwidget)
        self.map_side.addWidget(self.go_back_map)
        self.map_side.addWidget(self.map_zoom_label)
        self.map_side.addWidget(self.map_zoom_slider)

        self.thread_is_running = False

        self.earthquake_data_splitter.addWidget(self.city_label)
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
        self.change_default_map_option()

        self.map_zoom_slider.valueChanged.connect(self.StartZoom)
        self.apply_earthquake_datas.clicked.connect(self.connect_api)
        self.sort_earthquakes.clicked.connect(self.worker_function_sorting_recent_earthquakes)
        self.show_recent_earthquake_with_map.clicked.connect(self.worker_show_recent_earthquakes_with_map)
        self.show_recent_earthquakes_with_map.clicked.connect(self.worker_show_recent_earthquake_with_map)
        self.toolbar_button_heatmap.clicked.connect(self.change_heatmap)
        self.toolbar_button_marker.clicked.connect(self.change_classic_map)


        self.location_timer = QTimer(self)
        self.location_timer.timeout.connect(self.update_map_location)
        self.location_timer.start(1) 
    
    def worker_function_sorting_recent_earthquakes(self):
        thread = threading.Thread(target=self.sort_recent_earthquakes_function,daemon=True)
        thread.start()
    
    def worker_show_recent_earthquakes_with_map(self):
        try:
            self.draw_earthquakes_function()
        except Exception as exception:
            print(f'hata: {exception}')

    def worker_show_recent_earthquake_with_map(self):
        try:
            self.draw_earthquake_function()
        except Exception as exception:
            print(f'hata: {exception}')
        
    def StartZoom(self):    
        self.zoom_level = self.map_zoom_slider.value()
        _Function = Create_map.ZoomMap(value=self.zoom_level,location=self.location,marker_locations=self.coordinates,heatmap_locations=self.heatmap_coordinates,popups=self.strings,map_type=str(self.toolbar_map_type_label.text()))
        
        if self.toolbar_map_type_label.text() == 'Harita gösterimi türü: Klasik harita':
            fFunction = _Function.zoomMap()
            print(fFunction)
        
        elif self.toolbar_map_type_label.text() == 'Harita gösterimi türü: Isı haritası':
            fFunction = _Function.zoomHeatmap()
            print(fFunction)

        self.webwidget.setHtml(fFunction)
    
    def update_map_location(self):
        static_location = self.Turkiye_map.location

        self.location = static_location
    
    def MapReset(self):
        old_map = Create_map.ExampleMap().CreateExampleMap()
        self.webwidget.setHtml(old_map.get_root().render())
    
    def RefreshMap(self):
        self.webwidget.reload()
    
    def connect_api(self, data):
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

            self.lim_data = self.limit_input.value()

            self.thread_ = QThread()
            self.signal = Signal(start_hmsmmy=self.start_date_tokenized,end_hmsmmy=self.end_date_tokenized,lim=self.lim_data,coordinates=self.coordinates,coordinates_heatmap=self.heatmap_coordinates,strings=self.strings,webwidget=self.webwidget,new_map=self.new_map,map_type=str(self.toolbar_map_type_label.text()))

            if self.thread_is_running == True:
                self.thread_.quit()
                self.thread_.wait()
                self.thread_is_running = False
            
            self.signal = Signal(start_hmsmmy=self.start_date_tokenized,end_hmsmmy=self.end_date_tokenized,lim=self.lim_data,coordinates=self.coordinates,coordinates_heatmap=self.heatmap_coordinates,strings=self.strings,webwidget=self.webwidget,new_map=self.new_map,map_type=str(self.toolbar_map_type_label.text()))
            self.signal.moveToThread(self.thread_)

            self.signal.signal.connect(self.update_html)
            self.thread_.started.connect(self.signal.run)

            self.thread_.start()

            self.thread_.quit()
            self.thread_is_running = True


        except Exception as exception_1:
            print(f'exception: {exception_1}')
            QMessageBox.critical(self,'Uyarı',f'{self.start_date} // {self.end_date} tarihleri arasında Deprem görülmemektedir!')
    
    def falser(self):
        self.thread_is_running = False

    def update_html(self,html):
        self.webwidget.setHtml(html)

    def worker_api(self):
        signal = Signal(start_hmsmmy=self.start_date_tokenized,end_hmsmmy=self.end_date_tokenized,lim=self.lim_data,coordinates=self.coordinates,coordinates_heatmap=self.heatmap_coordinates,strings=self.strings,webwidget=self.webwidget,new_map=self.new_map,map_type=str(self.toolbar_map_type_label.text()))
        signal.signal.emit('test')

    def optimize_dates(self):
        value = self.day_selector.value()
        current_date = timezone.current_date(value).returner()

        self.recent_date.setDate(QDate().currentDate())


    def draw_earthquakes_function(self):
        try:
            lat_lon_array = []

            value = self.day_selector.value()
            current_date = timezone.current_date(value).returner()
            
            self.earthquake_date.setDate(current_date)

            #self.recent_earthquakes_list.clear()
            
            self.new_map_recent = fl.Map(location=[39,35],
                                zoom_start=6,
                                tiles='Cartodb dark_matter')
            
            self.start_date_recent = self.recent_date.date().toPyDate()
            self.end_date_recent = self.earthquake_date.date().toPyDate()

            self.start_time_recent = self.start_time_setting.time().toPyTime()
            self.end_time_recent = self.end_time_setting.time().toPyTime()

            self.start_date_tokenized_recent = f'{self.end_date_recent}T{self.end_time_recent}'
            self.end_date_tokenized_recent = f'{self.start_date_recent}T{self.end_time_recent}'

            #lim_data = self.limit_input.value()

            self.nonetypearray = []
            self.all_datas = []

            self.index = 0
            self.user_index = self.recent_earthquakes_list.currentRow() #example column number


            for row in range(self.recent_earthquakes_list.rowCount()):
                self.index += 1

                for column in range(self.recent_earthquakes_list.columnCount()):
                    if row == self.user_index:
                        if self.recent_earthquakes_list.item(row,column) == None or self.recent_earthquakes_list.item(row,column) == '':
                            self.nonetypearray.append(self.recent_earthquakes_list.item(row,column))
                            print('none     ',self.all_datas)

                        else:
                            self.all_datas.append(self.recent_earthquakes_list.item(row,column).text())
                            print(self.all_datas)

            lat_lon = [float(self.all_datas[1]),float(self.all_datas[2])]
            popup_vars = f'''Tarih: {self.all_datas[0]}\n'
Enlem: {self.all_datas[1]}\n
Boylam: {self.all_datas[2]}\n
Derinlik: {self.all_datas[3]}\n
Tip: {self.all_datas[4]}\n
Büyüklük: {self.all_datas[5]}\n
Yer: {self.all_datas[6]}\n
'''
            popup = fl.Popup(popup_vars,max_width=600,sticky=True,lazy=True)

            if self.toolbar_map_type_label.text() == 'Harita gösterimi türü: Klasik harita':
                fl.Marker(location=lat_lon,
                        popup=popup,
                        draggable=True,
                        ).add_to(self.new_map_recent)
                    
                

            elif self.toolbar_map_type_label.text() == 'Harita gösterimi türü: Isı haritası':
                HeatMap(data=[lat_lon],
                        min_opacity=float(self.all_datas[5]),
                        ).add_to(self.new_map_recent)

            self.webwidget.setHtml(self.new_map_recent.get_root().render())

        except Exception as exception_2:
            QMessageBox.critical(self,'Uyarı',f'{self.start_date_recent} // {self.end_date_recent} tarihleri arasında Deprem görülmemektedir! {exception_2}')

    def draw_earthquake_function(self):
        try:
            lat_lon_array = []
            array_like = []
            string_matris = []

            value = self.day_selector.value()
            current_date = timezone.current_date(value).returner()
            
            self.earthquake_date.setDate(current_date)

            #self.recent_earthquakes_list.clear()
            
            self.new_map_recent = fl.Map(location=[39,35],
                                zoom_start=6,
                                tiles='Cartodb dark_matter')
            
            self.start_date_recent = self.recent_date.date().toPyDate()
            self.end_date_recent = self.earthquake_date.date().toPyDate()

            self.start_time_recent = self.start_time_setting.time().toPyTime()
            self.end_time_recent = self.end_time_setting.time().toPyTime()

            self.start_date_tokenized_recent = f'{self.end_date_recent}T{self.end_time_recent}'
            self.end_date_tokenized_recent = f'{self.start_date_recent}T{self.end_time_recent}'

            #lim_data = self.limit_input.value()

            self.nonetypearray = []
            self.all_datas = []

            #self.index = 0
            #self.user_index = self.recent_earthquakes_list.currentRow() #example column number

            for row in range(self.recent_earthquakes_list.rowCount()):
                #self.index += 1
                for column in range(self.recent_earthquakes_list.columnCount()):   
                    if self.recent_earthquakes_list.item(row,column) == None or self.recent_earthquakes_list.item(row,column) == '':
                        self.nonetypearray.append(self.recent_earthquakes_list.item(row,column))
                        print('none     ',self.all_datas)

                    else:
                            self.all_datas.append(self.recent_earthquakes_list.item(row,column).text())
                            print(self.all_datas)

            changed_items = self.recent_earthquakes_list.selectedItems()

            for item in changed_items:
                lat_lon_array.append([float(self.recent_earthquakes_list.item(self.recent_earthquakes_list.row(item),1).text()),
                                      float(self.recent_earthquakes_list.item(self.recent_earthquakes_list.row(item),2).text()),
                                    ])
                string_matris.append(f'''
                                      Tarih(TS): {self.recent_earthquakes_list.item(self.recent_earthquakes_list.row(item),0).text()}\n
                                      Enlem: {self.recent_earthquakes_list.item(self.recent_earthquakes_list.row(item),1).text()}\n
                                      Boylam: {self.recent_earthquakes_list.item(self.recent_earthquakes_list.row(item),2).text()}\n
                                      Derinlik: {self.recent_earthquakes_list.item(self.recent_earthquakes_list.row(item),3).text()}\n
                                      Tip: {self.recent_earthquakes_list.item(self.recent_earthquakes_list.row(item),4).text()}\n
                                      Büyüklük: {self.recent_earthquakes_list.item(self.recent_earthquakes_list.row(item),5).text()}\n
                                      Yer: {self.recent_earthquakes_list.item(self.recent_earthquakes_list.row(item),6).text()}\n
                                    ''')


            if self.toolbar_map_type_label.text() == 'Harita gösterimi türü: Klasik harita':
                for latitude_longitude,strings in zip(lat_lon_array,string_matris): 
                        fl.Marker(location=latitude_longitude,
                                popup=fl.Popup(strings,max_width=600,sticky=True,lazy=True),
                                draggable=True,
                                ).add_to(self.new_map_recent)
                self.webwidget.setHtml(self.new_map_recent.get_root().render())    
                

            elif self.toolbar_map_type_label.text() == 'Harita gösterimi türü: Isı haritası':
                HeatMap(data=lat_lon_array,
                        min_opacity=float(self.all_datas[5]),
                        ).add_to(self.new_map_recent)

                self.webwidget.setHtml(self.new_map_recent.get_root().render())

        except Exception as exception_2:
            QMessageBox.critical(self,'Uyarı',f'{self.start_date_recent} // {self.end_date_recent} tarihleri arasında Deprem görülmemektedir! {exception_2}')
    def sort_recent_earthquakes_function(self):
        try:
            #https://deprem.afad.gov.tr/last-earthquakes.html
            value = self.day_selector.value()
            current_date = timezone.current_date(value).returner()
            
            self.earthquake_date.setDate(current_date)

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

            host_recentf = scrapping.ScrappingClass().returnerf()

            index = 0
            for dataf in host_recentf:
                
                timecode_item = QTableWidgetItem(str(dataf[0]))
                latidude_item = QTableWidgetItem(str(dataf[1]))
                longitude_item = QTableWidgetItem(str(dataf[2]))
                depth_item = QTableWidgetItem(str(dataf[3]))
                type_item = QTableWidgetItem(str(dataf[4]))
                magnitude_item = QTableWidgetItem(str(dataf[5]))
                location_item = QTableWidgetItem(str(dataf[6]))
                
                self.recent_earthquakes_list.setItem(index,0,timecode_item)
                self.recent_earthquakes_list.setItem(index,1,latidude_item)
                self.recent_earthquakes_list.setItem(index,2,longitude_item)
                self.recent_earthquakes_list.setItem(index,3,depth_item)
                self.recent_earthquakes_list.setItem(index,4,type_item)
                self.recent_earthquakes_list.setItem(index,5,magnitude_item)
                self.recent_earthquakes_list.setItem(index,6,location_item)

                index += 1

        except Exception as exception_2:
            QMessageBox.critical(self,'Uyarı',f'{self.start_date_recent} // {self.end_date_recent} tarihleri arasında Deprem görülmemektedir! {exception_2}')

    def change_heatmap(self):
        self.toolbar_map_type_label.setText(f'Harita gösterimi türü: {str(self.toolbar_button_heatmap.text())}') 
        self.toolbar_button_heatmap.setStyleSheet('''background-color: orange;
    color: black;
    border: 0.7px solid rgb(177, 21, 21);
    border-radius: 4px;
    font-weight: bolder;
    font-size: 24px;
}
QPushButton:hover{
    background-color: rgb(92, 16, 16);
    color: rgb(108, 93, 7);
    font-size: 25;
}
QPushButton:pressed{
    background-color: red;
    color: gold;
    font-size: 30px;
}''')
        
        self.toolbar_button_marker.setStyleSheet('''background-color: white;
    color: black;
    border: 0.7px solid rgb(177, 21, 21);
    border-radius: 4px;
    font-weight: bolder;
    font-size: 24px;
}
QPushButton:hover{
    background-color: rgb(92, 16, 16);
    color: rgb(108, 93, 7);
    font-size: 25;
}
QPushButton:pressed{
    background-color: red;
    color: gold;
    font-size: 30px;
}''')
        
    def change_classic_map(self):
        
        self.toolbar_map_type_label.setText(f'Harita gösterimi türü: {str(self.toolbar_button_marker.text())}')
        self.toolbar_button_heatmap.setStyleSheet('''background-color: white;
    color: black;
    border: 0.7px solid rgb(177, 21, 21);
    border-radius: 4px;
    font-weight: bolder;
    font-size: 24px;
}
QPushButton:hover{
    background-color: rgb(92, 16, 16);
    color: rgb(108, 93, 7);
    font-size: 25;
}
QPushButton:pressed{
    background-color: red;
    color: gold;
    font-size: 30px;
}''')
        
        self.toolbar_button_marker.setStyleSheet('''background-color: orange;
    color: black;
    border: 0.7px solid rgb(177, 21, 21);
    border-radius: 4px;
    font-weight: bolder;
    font-size: 24px;
}
QPushButton:hover{
    background-color: rgb(92, 16, 16);
    color: rgb(108, 93, 7);
    font-size: 25;
}
QPushButton:pressed{
    background-color: red;
    color: gold;
    font-size: 30px;
}''')

    def change_default_map_option(self):
        self.toolbar_button_heatmap.setStyleSheet('''QPushButton{
    background-color: white;
    color: black;
    border: 0.7px solid rgb(177, 21, 21);
    border-radius: 4px;
    font-weight: bolder;
    font-size: 24px;
}
QPushButton:hover{
    background-color: rgb(92, 16, 16);
    color: rgb(108, 93, 7);
    font-size: 25;
}
QPushButton:pressed{
    background-color: red;
    color: gold;
    font-size: 30px;
}''')
        
        self.toolbar_button_marker.setStyleSheet('''QPushButton{
    background-color: orange;
    color: white;
    border: 0.7px solid rgb(177, 21, 21);
    border-radius: 4px;
    font-weight: bolder;
    font-size: 24px;
}
QPushButton:hover{
    background-color: rgb(92, 16, 16);
    color: rgb(108, 93, 7);
    font-size: 25;
}
QPushButton:pressed{
    background-color: red;
    color: gold;
    font-size: 30px;
}''')
        
        self.toolbar_map_type_label.setText(f'Harita gösterimi türü: {str(self.toolbar_button_marker.text())}') 
    
sp = QApplication(sys.argv) 

sw = LoadGui()

def ShowWindow():
    sw.show()

    
