import socket
import threading

import handleClient

print("Backend Server Starting...")
print("------------------")
print("Messages received from Client: --> *")
print("Messages sent to Client: <-- *")
print("------------------")


localhost = True

if localhost:
    host = 'localhost'
else:
    host = '49.12.101.156'

port = 5000
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((host, port))
serv.listen(5)

while True:
    print("Waiting for another Client")
    conn, addr = serv.accept()
    thread = threading.Thread(target=handleClient.handle_client, args=(conn, addr))
    thread.start()