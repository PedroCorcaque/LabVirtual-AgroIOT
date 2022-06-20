from lib.sensors import *

class SensorsFactory:
    SENSORS = {
        '5TE': Sensor5TE,
    }

    @staticmethod
    def getSensorObject(model, data):
        model = model.lower()
        if model in SensorsFactory.SENSORS.keys():
            return SensorsFactory.SENSORS[model](data=data)
        else:
            return None

    
    
