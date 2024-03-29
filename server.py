import time

from Party import Party


class Server:
    connection = None,
    user = "",

    def __init__(self, connection, user):
        self.connection = connection
        self.user = user


servers = []
parties = []


def send_data(data, connection):
    connection.send(data.encode('utf-8'))
    print("    <-- " + data)


def getServerByUserName(userName):
    global servers
    userName_ = userName.lower()
    for server in servers:
        if server.user.lower() == userName_:
            return server
    return None

def log_to_file(message, filename='log.txt'):
    with open(filename, 'a') as file:
        file.write(message + '\n')

def removeServerByConnection(connection):
    servers.remove(getServerByConnection(connection))

def getServerByConnection(connection):  # TODO check ob python == auf Instance überprüft
    global servers
    for server in servers:
        if server.connection == connection:
            return server
    return None


def getPartyByName(partyName):
    global parties
    for party in parties:
        if party.name == partyName:
            return party


def process_data(data, connection):
    global servers, parties
    dataString = str(data[2:].decode('utf-8'))
    if dataString.startswith("init"):
        playerName = dataString.split(";")[1]
        servers.append(Server(connection, playerName))

    elif dataString.startswith("msg"):
        parts = dataString.split(";")
        playerFrom = parts[1]
        playerTo = parts[2]
        message = "".join(parts[3:])
        server = getServerByUserName(playerTo)
        if server is not None:
            send_data("msg;" + playerFrom + ";" + message, server.connection)

    elif dataString.startswith("party"):
        server_self = getServerByConnection(connection)
        if server_self is None:
            print("This should not happen!")
        parts = dataString.split(";")
        partyName = parts[1]
        party = getPartyByName(partyName)
        com = parts[2]  # com could be: "create", "join", "invite", "kick", "disband", "msg", "leave"
        if com == "create":
            # TODO check backend side if party name already exists and send respond if could create or not
            parties.append(Party(partyName, parts[3]))
        elif com == "invite":
            # TODO check if permission
            playerToInvite = parts[3]
            if playerToInvite in party.members:
                send_data("party;" + partyName + ";log;This Player is already in the Party!", connection)
                return
            server = getServerByUserName(playerToInvite)
            if server is not None:
                send_data("party;" + partyName + ";invited;" + server_self.user, server.connection)
            else:
                send_data(
                    "party;" + partyName + ";log;The Player " + playerToInvite + " has not been found or does not use "
                                                                                 "GunterEss!",
                    connection)

        elif com == "join":
            # TODO check backend side if player has been invited, if no dont let him join
            if server_self.user in party.members:
                return
            party.addMember(server_self.user)
            party.broadCast(server_self.user, messageType="playerjoin", crossingOver=server_self.user)

            send_data("party;" + partyName + ";joinedInit;" + party.membersToString(), connection)

        elif com == "kick":
            if server_self.user != party.owner:
                send_data("party;" + partyName + ";log;You are not the owner of the party " + partyName + "!", connection)
                return
            playerToKick = parts[3]
            server = getServerByUserName(playerToKick)
            party.removeMember(playerToKick)
            party.broadCast(playerToKick, messageType="playerkick", crossingOver=playerToKick)
            send_data("party;" + partyName + ";kick;" + server_self.user, server.connection)

        elif com == "disband":
            if server_self.user != party.owner:
                send_data("party;" + partyName + ";log;You are not the owner of the party " + partyName + "!",
                          connection)
                return
            party.broadCast(server_self.user, messageType="partydisband", crossingOver=server_self.user)
            parties.remove(party)
        elif com == "msg":
            party.broadCast(server_self.user + ": " + parts[3], crossingOver=server_self.user)
        elif com == "leave":
            playerToRemove = server_self.user
            party.removeMember(playerToRemove)
            if len(party.members) == 0:
                parties.remove(party)
                return
            if party.owner == playerToRemove:
                newOwner = party.members[0]
                party.owner = newOwner
                party.broadCast(newOwner, messageType="transfer")
                time.sleep(0.25)
            party.broadCast(playerToRemove, messageType="playerleave", crossingOver=playerToRemove)
        elif com == "transfer":
            if server_self.user != party.owner:
                return
            newOwner = parts[3]
            if newOwner not in party.members:
                send_data("party;" + partyName + ";log;" + newOwner + " is not in the party!", connection)
            party.owner = newOwner
            party.broadCast(newOwner, messageType="transfer")
