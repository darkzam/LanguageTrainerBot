
import discord
import datetime

class SesionLectura:

    def __init__(self, members):
        self.id = 0
        self.partyMembers = []
        self.tempTurns = []

        for member in members:
            self.partyMembers.append(member)
            self.tempTurns.append(member)
        
        self.roundCounter = 0
        self.turnCounter = 0
        self.turnMember = None

    def start(self):

        message = ""

        self.roundCounter += 1

        if len(self.tempTurns) == len(self.partyMembers):
            message = "Round: " + str(self.roundCounter) + " starting!\n"
        
        return message
        
    def nextTurn(self):

        message = ""

        if len(self.partyMembers) > 0:

            if len(self.tempTurns) > 0:

                if len(self.tempTurns) == len(self.partyMembers):
                    message = "Round: " + str(self.roundCounter) + " starting!\n"
                
                if len(self.tempTurns) == 1:
                    message = message + "Last turn of Round: " + str(self.roundCounter) + "\n"    

                self.turnMember = self.tempTurns.pop(0)
                             
                self.turnCounter += 1

                message = message + "<@"+ self.turnMember.id + "> It's your turn."
            
            else:
                
                message = "Round " + str(self.roundCounter) + " has finished!"
                
                for member in self.partyMembers:
                    self.tempTurns.append(member)

                self.roundCounter += 1

        else:
            message = "Party has not started."

        return message
    
    def getJson(self):

        dataSesion = {}
        dataSesion['id'] = 0
        dataSesion['totalTurns'] = self.turnCounter
        dataSesion['totalRounds'] = self.roundCounter

        dataPartyMembers = []

        for member in self.partyMembers:
            dataMember = {}
            dataMember['id'] = member.id
            dataMember['username'] = member.name
           ## dataMember['created_at'] = datetime.datetime.strtime("%y-%m-%d-%H-%M")
            dataPartyMembers.append(dataMember)
        
        dataSesion['partyMembers'] = dataPartyMembers


        return dataPartyMembers