import socket


def test_server():
    str = "{\"Temperature\": 80.5, \"Humidity\": 34.0, \"Pressure\": 23.0, \"Altitude\": 0.5, " \
          "\"Lumens\": 8.5, \"Wind Speed\": 34.5, \"Direction\": 20, \"Rain\": 4, \"RSSI\": -23}"
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn.bind(('localhost', 10001))
    conn.listen(10)

    while True:
        try:
            (clientsocket, address) = conn.accept()
            clientsocket.send(bytes(str, encoding='ascii'))
        except KeyboardInterrupt:
            conn.close()
            break

if __name__ == '__main__':
    test_server()
