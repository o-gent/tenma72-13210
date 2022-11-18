import time
from typing import List
import serial

class DCload():
    """
    Allows programmatic control of the Tenma 72-13210
    """

    def __init__(self, port):
        self.__connection = serial.Serial(port, 115200)
        self.__connection.timeout = 1 # so we don't hang forever if nothing is recieved
        
        self.__voltage = 0.0
        self.__current = 0.0
        self.__resistance = 0.0
        self.__power = 0.0
        self.__set_voltage = 0.0
        self.__set_current = 0.0
        self.__set_resistance = 0.0
        self.__set_power = 0.0

    def __call__(self):
        return self.get_readings()
    
    def get_readings(self) -> List[float]:
        self.__voltage = self.get_voltage()
        self.__current = self.get_current()
        self.__power = self.get_power()
        #self.__resistance = self.get_resistance()
        return [
            self.__voltage,
            self.__current,
            self.__power,
            self.__resistance
        ]

    def write(self, command:str):
        """ write correct format to serial from string """
        towrite = f'{command}\n'
        self.__connection.write(towrite.encode())

    def read(self) -> str:
        """ read incoming serial and decode from bytes"""
        result = self.__connection.readline()
        return result.decode()

    def str_to_val(self, reading: str, unit: str) -> float:
        """ convert incoming readings to float """
        return float(reading.split(unit)[0])

    def turn_on(self):
        """ starts the programmed load """
        self.write(":INP 1")

    def turn_off(self):
        """ turns off the programmed load """
        self.write(":INP 0")

    def get_value(self, type: str, unit: str):
        """ read source values """
        self.write(f":MEAS:{type}?")
        return self.str_to_val(self.read(), unit)
    
    def get_set_value(self, type:str, unit:str):
        """ read sink values """
        self.write(f":{type}?")
        return self.str_to_val(self.read(), unit)

    def get_voltage(self) -> float:
        return self.get_value("VOLT", "V")
    
    def get_current(self) -> float:
        return self.get_value("CURR", "A")

    def get_resistance(self) -> float:
        return self.get_value("RES", "OHM")

    def get_power(self) -> float:
        return self.get_value("POW", "W")

    def get_set_voltage(self) -> float:
        return self.get_set_value("VOLT", "V")

    def get_set_current(self) -> float:
        return self.get_set_value("CURR", "A")

    def get_set_resistance(self) -> float:
        return self.get_set_value("RES", "OHM")

    def get_set_power(self) -> float:
        return self.get_set_value("POW", "W")

    def set_voltage(self, param: float):
        """ dc load target """
        self.write(f":VOLT {param}V")

    def set_current(self, param: float):
        """ dc load target """
        self.write(f":CURR {param}A")

    def set_resistance(self, param: float):
        """ dc load target """
        self.write(f":RES {param}OHM")

    def set_power(self, param: float):
        """ dc load target """
        self.write(f":POW {param}W")


if __name__ == "__main__":
    dc = DCload("COM8")
    print(dc.get_voltage())
    dc.set_power(10)
    dc.turn_on()
    import csv

    with open(f"data_{time.strftime('%Y%m%d-%H%M%S')}.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['voltage', 'current', 'power', 'resistance'])
        i = 0
        while True:
            results = dc()
            print(results)
            csvwriter.writerow(results)
            i += 1
            if i > 300:
                i = 0
                dc.set_power(10)
            if i == 150:
                dc.set_power(5)

