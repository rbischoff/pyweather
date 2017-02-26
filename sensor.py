import socket
import json
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
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._json = self.fetch_data()
        self._engine = create_engine('sqlite:///sensor.db')
        Base.metadata.create_all(self._engine)
        session = sessionmaker()
        session.configure(bind=self._engine)
        self._session = session()
        self.data = json.loads(self._json)

    def fetch_data(self):
        self._conn.connect(self._addr)
        jsonstr = self._conn.recv(512)
        self._conn.close()
        return jsonstr.decode()

    def update_history(self):
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
        print(result)

if __name__ == '__main__':
    s = Sensor()
    s.update_history()
    s.get_current()
    print(s.data)


