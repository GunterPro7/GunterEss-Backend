# Server.py
import socket
import time
import threading
import server

host = 'localhost' # Lokale Adresse
port = 5000 # Port zum Zuhören
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Erstellen Sie ein Socket-Objekt
serv.bind((host, port)) # Binden Sie das Socket-Objekt an die Adresse
serv.listen(5) # Hören Sie auf bis zu 5 Verbindungen

empfange_daten_bool = True
def empfange_daten():
    global empfange_daten_bool, conn
    empfange_daten_bool = False
    data = conn.recv(4096)
    empfange_daten_event(data)
    empfange_daten_bool = True

def empfange_daten_event(data):
    global conn
    server.process_data(data, conn)

def sende_daten(data):
    global conn
    conn.send(data.encode('utf-8'))

conn, addr = serv.accept()
sende_daten("Willkommen beim Socket-Server")
while True:
    time.sleep(1)
    sende_daten("test huhu")
    if empfange_daten_bool:
        conn_thread = threading.Thread(target=empfange_daten)
        conn_thread.start()
