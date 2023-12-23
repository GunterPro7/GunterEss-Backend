# Server.py
import socket
import time

host = 'localhost' # Lokale Adresse
port = 5000 # Port zum Zuhören
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Erstellen Sie ein Socket-Objekt
serv.bind((host, port)) # Binden Sie das Socket-Objekt an die Adresse
serv.listen(5) # Hören Sie auf bis zu 5 Verbindungen


conn, addr = serv.accept()
conn.send(b"Willkommen beim Socket-Server")
while True:
    time.sleep(1)
    conn.send(b"Danke fr Ihre Nachricht")
    data = conn.recv(4096)

    if not data: break
    print(data)
