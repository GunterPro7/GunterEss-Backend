import threading
import time

import server

def handle_client(conn, addr):
    empfange_daten_bool = True
    verbindung_abgebrochen = False

    def empfange_daten(connection):
        nonlocal empfange_daten_bool
        empfange_daten_bool = False
        try:
            data = connection.recv(4096)
        except Exception:
            print("--> Verbindung zu einem Client unterbrochen, wird beendet.")
            connection_close(connection)
            return
        empfange_daten_event(data, connection)
        empfange_daten_bool = True

    def empfange_daten_event(data, connection):
        print("-->" + str(data))
        server.process_data(data, connection)

    def connection_close(connection):
        nonlocal verbindung_abgebrochen
        server.removeServerByConnection(connection)
        verbindung_abgebrochen = True

    def sende_daten(data, connection):
        connection.send(data.encode('utf-8'))

    while not verbindung_abgebrochen:
        time.sleep(1)
        if empfange_daten_bool:
            conn_thread = threading.Thread(target=empfange_daten, args=(conn,))
            conn_thread.start()