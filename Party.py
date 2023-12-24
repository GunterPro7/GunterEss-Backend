import server


class Party:
    name = "",
    owner = "",
    members = []

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.members = [owner]

    def addMember(self, playerName):
        self.members.append(playerName)

    def removeMember(self, playerName):
        self.members.remove(playerName)

    def membersToString(self):
        string = ""

        for member in self.members:
            string += member + ";"

        return string[:-1]

    def broadCast(self, message, messageType="log", crossingOver=""):
        for member in self.members:
            if member == crossingOver:
                continue
            connection = server.getServerByUserName(member).connection
            server.send_data("party;" + self.name + ";" + messageType + ";" + message, connection)
