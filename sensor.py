import socket
import json


class Sensor:
    def __init__(self, address=('localhost', 10001)):
        self._addr = address
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._json = self.fetch_data()
        self.data = json.loads(self._json)

    def fetch_data(self):
        self._conn.connect(self._addr)
        jsonstr = self._conn.recv(512)
        self._conn.close()
        return jsonstr.decode()

if __name__ == '__main__':
    s = Sensor()
    print(s.data)


