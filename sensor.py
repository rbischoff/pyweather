import socket
import json
import sys
import time
import datetime as dt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Float, DateTime


Base = declarative_base()


class History(Base):
    __tablename__ = 'history'
    date_time = Column(DateTime, primary_key=True)
    sig_strength = Column(Integer)
    temp = Column(Float)
    rain = Column(Float)
    baro = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_direction_deg = Column(Float)
    lumen = Column(Float)


class Sensor:
    def __init__(self, address=('localhost', 10001)):
        self._addr = address
        self._json = ""
        self.data = {}
        self.fetch_data()
        self._engine = create_engine('sqlite:///sensor.db')
        Base.metadata.create_all(self._engine)
        session = sessionmaker()
        session.configure(bind=self._engine)
        self._session = session()
        self.data = json.loads(self._json)

    def fetch_data(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self._addr)
        conn.send(b'\n')
        conn.settimeout(5.0)
        term = '\r\n'
        h_str = ''
        while term not in h_str:
            h = conn.recv(1)
            h_str += h.decode()

        # Ditch the deliminator
        h_str = h_str.replace('\r\n', '')

        # Find the header info
        sizes = h_str.split('Payload size: ')

        try:
            size = int(sizes[1])
        except ValueError:
            print('Invalid size value.', file=sys.stderr)
            return

        j_str = ''
        while len(j_str) < size:
            j = conn.recv(512)
            j_str += j.decode()
        conn.close()
        self._json = j_str
        self.data = json.loads(self._json)
        return j_str

    def update_history(self):
        self.fetch_data()
        hist = History(date_time=dt.datetime.now(), sig_strength=self.data['RSSI'], temp=self.data['Temperature'],
                       rain=self.data['Rain'], baro=self.data['Pressure'], humidity=self.data['Humidity'],
                       wind_speed=self.data['Wind Speed'], wind_direction_deg=self.data['Direction'],
                       lumen=self.data['Lumens'])
        self._session.add(hist)
        self._session.commit()

    def get_current(self):
        ct = dt.datetime.now()
        recent = ct - dt.timedelta(minutes=5)
        result = self._session.query(History).filter(History.date_time > recent).all()
        return result[-1]

if __name__ == '__main__':
    s = Sensor(address=('192.168.0.107', 7001))
    while True:
        s.update_history()
        report = s.get_current()
        print((report.date_time.strftime("%D %T"), report.sig_strength, report.temp, report.rain, report.baro,
               report.humidity, report.wind_speed, report.wind_direction_deg, report.lumen))
        time.sleep(1)




