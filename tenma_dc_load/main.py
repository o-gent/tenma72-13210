import time
import serial

class DCload():
    """
    Allows programmatic control of the Tenma 72-13210
    """

    def __init__(self, port):
        self.__connection = serial.Serial(port, 115200)
        self.__connection.timeout = 1 # so we don't hang forever if nothing is recieved

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
    dc.set_power(20)
    dc.turn_on()
    for i in range(500):
        dc.set_power(i/4)
        print(dc.get_current())
        time.sleep(0.2)
