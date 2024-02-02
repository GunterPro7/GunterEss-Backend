import threading
import time

import server

def handle_client(conn, addr):
    def empfange_daten(connection, empfange_daten_bool_event, verbindung_abgebrochen_event):
        empfange_daten_bool_event.set()
        try:
            data = connection.recv(4096)
        except Exception:
            print("--> Verbindung zu einem Client unterbrochen, wird beendet.")
            connection_close(connection, verbindung_abgebrochen_event)
            return
        empfange_daten_event(data, connection)
        empfange_daten_bool_event.clear()

    def empfange_daten_event(data, connection):
        print("-->" + str(data))
        server.process_data(data, connection)

    def connection_close(connection, verbindung_abgebrochen_event):
        server.removeServerByConnection(connection)
        verbindung_abgebrochen_event.set()

    def sende_daten(data, connection):
        connection.send(data.encode('utf-8'))

    empfange_daten_bool_event = threading.Event()
    verbindung_abgebrochen_event = threading.Event()

    while not verbindung_abgebrochen_event.is_set():
        time.sleep(1)
        if empfange_daten_bool_event.is_set():
            continue
        conn_thread = threading.Thread(target=empfange_daten, args=(conn, empfange_daten_bool_event,
                                                                    verbindung_abgebrochen_event))
        conn_thread.start()
