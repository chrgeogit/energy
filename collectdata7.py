import minimalmodbus
import requests as requests
import serial
import time
import ntplib
from time import ctime
import sys
import datetime
import sqlite3
from sqlite3 import Error


class DDS238:
    def __init__(self, modbus_device: str, meter_id: int = 1):
        self.modbus_device = modbus_device
        self.meter_id = meter_id
        self._configure_modbus()

    def _configure_modbus(self):
        instrument = minimalmodbus.Instrument(self.modbus_device, self.meter_id)
        time.sleep(.5)
        instrument.serial.baudrate = 9600
        instrument.serial.bytesize = 8
        instrument.serial.parity = serial.PARITY_NONE
        instrument.serial.stopbits = 1
        instrument.serial.timeout = 1 # seconds

        self._m = instrument


    #@property
    def close_serial(self):
        self._m.serial.close()

    @property
    def voltage(self) -> float:
        """ Returns the voltage in Volts """
        return self._m.read_register(0xC, 1)

    @property
    def current(self) -> float:
        """ Returns the current in Amperes """
        return self._m.read_register(0xD, 2)

    @property
    def frequency(self) -> float:
        """ Returns the frequency in Herz """
        return self._m.read_register(0x11, 2)

    @property
    def power(self) -> float:
        """ Returns the power in Watts. Positive is import. Negative power is exported """
        return self._m.read_register(0xE, 0, signed=True)

    @property
    def reactive_power(self) -> float:
        """ Return the reactive power in VAr """
        return self._m.read_register(0xF)/1000

    @property
    def power_factor(self) -> float:
        """ Returns the power factor (0-1 scalar)"""
        return self._m.read_register(0x10)/1000

    @property
    def import_energy(self) -> float:
        """ Returns the imported energy, in kWh """
        return self._m.read_long(0xA)/100

    @property
    def export_energy(self) -> float:
        """ Returns the exported energy, in kWh """
        return self._m.read_long(0x8)/100

    def change_address(self, address: int, baudrate=9600):
        """ Change the modbus address and the baudrate of the current device. USE AT YOUR OWN RISK ! """
        baudrate_map = {
            1200: 4,
            2400: 3,
            4800: 2,
            9600: 1,
        }
        assert baudrate in baudrate_map
        assert address < 256
        assert address >= 1

        payload = address * 256 + baudrate_map[baudrate]
        # two bytes: address and baudrate
        self._m.write_register(0x15, payload)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


if __name__ == '__main__':
    database = "/home/pi/rs485/db1"

    while True:
        c = ntplib.NTPClient()
        try:
            response = c.request('europe.pool.ntp.org', version=3)
            if response:
                print( " NTP Active " + ctime(response.tx_time))
        except:
            print(" NTP Deactivated")

        print(ctime(response.tx_time))
        x = ctime(response.tx_time)
        #d = DDS238('COM4', 1)
        d = DDS238('/dev/ttyUSB0',1)
        print(f'Frequency: {d.frequency}',flush=True)
        print(f'Voltage: {d.voltage}',flush=True ) 
        v= d.voltage 
        print(f'Current: {d.current}')
        c = d.current        
        print(f'Power: {d.power}')
        p=d.power        
        print(f'Import energy: {d.import_energy}')
        en = d.import_energy        
        print(f'Powerfactor: {d.power_factor}')
        #time.sleep(20)
        d.close_serial()
        try:
            sqliteConnection = sqlite3.connect(database)
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            sqlite_insert_query = '''INSERT INTO mes (volt, current, powewr, energy, date) VALUES (?,?,?,?,?)'''
            count = cursor.execute(sqlite_insert_query,(v,c,p,en,x))
            sqliteConnection.commit()
            print("Record inserted successfully into mes table ", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")
        time.sleep(60)

