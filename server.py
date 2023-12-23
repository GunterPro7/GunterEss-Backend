class Server:
    connection = None,
    user = "",
    def __init__(self, connection, user):
        self.connection = connection
        self.user = user


servers = []

def send_data(data, connection):
    connection.send(data.encode('utf-8'))

def process_data(data, connection):
    dataString = str(data[2:].decode('utf-8'))
    if dataString.startswith("init"):
        playerName = dataString.split(";")[1]
        servers.append(Server(connection, playerName))
    elif dataString.startswith("msg"):
        parts = dataString.split(";")
        playerFrom = parts[1]
        playerTo = parts[2]
        message = "".join(parts[3:])
        for server in servers:
            if server.user.lower() == playerTo.lower():
                send_data("msg;" + playerFrom + ";" + message, server.connection)
                break
    elif dataString.startswith("party"):
        parts = dataString.split(";")
        partyName = parts[1]
        com = parts[2]   # com could be: "create", "join", "invite", "kick", "disband", "msg", "leave"
        if com == "create":
            pass


    pass
    # wenn data mit "init" beginnt, dann spieler herausfinden und connection da rein speichern
    # wenn z.b /msg parameter mitübergeben wurde servers durchlaufen und user heraussuchen