

class Sensor5TE():

    @staticmethod
    def sensorModel():
        return '5TE'
    
    @staticmethod
    def sensorReadings():
        return ['id', 'humidity', 'electricConductivity', 'temperature']
    
    def __init__(self, data=None):
        self.id_ = None
        self.humidity = None
        self.electricConductivity = None
        self.temperature = None
        if data is not None:
            self.fromArduino(payload=data)

    def fromArduino(self, payload):
        self.id = payload['id']
        self.humidity = payload['humidity']
        self.electricConductivity = payload['eletricConductivity']
        self.temperature = payload['temperature']

    def toDict(self):
        readings = {}
        readings['sensorModel'] = Sensor5TE.sensorModel()
        readings['id'] = self.id_
        readings['humidity'] = self.humidity
        readings['eletricConductivity'] = self.electricConductivity
        readings['temperature'] = self.temperature

        return readings
