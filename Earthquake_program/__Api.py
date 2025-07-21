import requests 

class CustomData():
    def __init__(self,start,end,lim):
        super().__init__()

        #data-arrays#
        self.city = []
        self.province = []
        self.magnitude = []
        self.district = []
        self.longitude = []
        self.depth = []
        self.latitude = []
        #                   #

        #indexes#

        json_index = 0
        response_index = 0
        #                   #

        #example time-code: (2025-09-16T10:00:00)
        #example lim: (500)
        self.start = start
        self.end = end
        self.lim = lim
        #                   #

    def Parse(self):
        try:        
            custom_response = requests.get(url=f'https://servisnet.afad.gov.tr/apigateway/deprem/apiv2/event/filter?start={self.start}&end={self.end}&limit={self.lim}&offset=5&orderby=timedesc')
            response_index = 1

        except Exception as CustomDataResponseException:
            print(f'CustomData response error: {CustomDataResponseException}')
            response_index = 0
            pass
        
        try:
            self.data = custom_response.json()
            json_index = 1
        
        except Exception as __jsonDecodeError:
            json_index = 0
            print(f'Json decode error: {__jsonDecodeError}')
            pass
        
        try:
            if response_index == 1 and json_index == 1:
                for data in self.data:
                    yield [data['country'],data['province'],data['magnitude']]
        
        except Exception as __DataReturnException:
            print(f'Data return exception: {__DataReturnException}')

__function = CustomData(start='2024-09-16T10:00:00',end='2025-09-16T10:00:00',lim=100)

__generator_object = __function.Parse()

for gen_data in __generator_object:
    print(gen_data)
            
                
            
            




            
