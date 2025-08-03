import datetime
from PyQt5.QtCore import QDate
class current_date():
    def __init__(self,value):  
        self.value = value

    def returner(self):
        date = QDate()

        y = QDate().currentDate().getDate()[0]
        m = QDate().currentDate().getDate()[1] - self.value
        d = QDate().currentDate().getDate()[2]

        date.setDate(y,m,d)

        return date

class current_time():
    def __init__(self):
        self.hour = None
        self.minute = None
        self.second = None
    
    def returner():
        time = datetime.datetime.now().strftime('%H/%M/%S')
        time = time.replace('/','-')
        
        return time
    
#date_data = current_date.returner()
#time_data = current_time.returner()

