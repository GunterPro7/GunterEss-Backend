import threading
import time

import server

def handle_client(conn, addr):
    empfange_daten_bool = True

    def empfange_daten(connection):
        global empfange_daten_bool
        empfange_daten_bool = False
        data = connection.recv(4096)
        empfange_daten_event(data, connection)
        empfange_daten_bool = True

    def empfange_daten_event(data, connection):
        print(data)
        server.process_data(data, connection)

    def sende_daten(data, connection):
        connection.send(data.encode('utf-8'))

    while True:
        time.sleep(1)
        if empfange_daten_bool:
            conn_thread = threading.Thread(target=empfange_daten, args=(conn,))
            conn_thread.start()