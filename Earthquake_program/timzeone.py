import datetime

class current_date():
    def __init__(self):  
        self.year = None
        self.month = None
        self.day = None

    def returner():
        date = datetime.date.today().strftime('%d/%m/%y')
        date = date.replace('/','-')

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

