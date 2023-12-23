import server

class Party:
    name = "",
    owner = "",
    members = []

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.members.append(owner)

    def addMember(self, playerName):
        self.members.append(playerName)

    def removeMember(self, playerName):
        self.members.remove(playerName)

    def membersToString(self):
        string = ""

        for member in self.members:
            string += member + ";"

        return string[:-1]

    def broadCast(self, message):
        for member in self.members:
            connection = server.getServerByUserName(member).connection
            server.send_data("party;" + self.name + ";log;" + message, connection)
