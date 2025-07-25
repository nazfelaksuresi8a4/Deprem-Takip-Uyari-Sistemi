import json

class CityList():
    def __init__(self):
        super().__init__()

    def List(self):
        self.cityFile = r'tum_iller.json'
        self.readed_file = open(self.cityFile,'r',encoding='utf-8').read()

        return self.readed_file

class ProvinceList():
    def __init__(self):
        super().__init__()
        self.cityFile = r'tum_iller.json'
        self.readed_file = open(self.cityFile,'r',encoding='utf-8').read()

        return self.readed_file
