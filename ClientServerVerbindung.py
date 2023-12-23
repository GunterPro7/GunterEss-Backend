# Server.py
import socket
import time
import threading

import handleClient
import server

host = 'localhost' # Lokale Adresse
port = 5000 # Port zum Zuhören
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Erstellen Sie ein Socket-Objekt
serv.bind((host, port)) # Binden Sie das Socket-Objekt an die Adresse
serv.listen(5) # Hören Sie auf bis zu 5 Verbindungen





while True:
    print("Auf neue Verbindung warten...")
    conn, addr = serv.accept()
    thread = threading.Thread(target=handleClient.handle_client, args=(conn, addr))
    thread.start()