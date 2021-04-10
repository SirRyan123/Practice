# Toontown Rewritten Programming Challenge
# Program written by Ryan Demboski

import random
# randomStreet = random.randint(0,5)
# self.toonLocation = random.choice(self.streets[self.playgrounds[randomStreet]]) 
# (this will be used later for random cog movement and placement of holes and banana peels)

toonNameInput = input("Please name your toon to continue: ")
tempCogName = "Flunky"


class toontownChallenge():
    ENDLINE_CHAR = '\n'

    toonLocation = None
    userChoice = None

    playgrounds = ['Toontown Central', 'Donalds Dock', 'Daisy Garden', 'Minnies Melodyland',
                    'The Brrrgh', 'Donalds Dreamland', 'Sellbot HQ', 'Cashbot HQ', 'Lawbot HQ'
                    'Bossbot HQ', 'Acorn Acres']

    streets = {
                playgrounds[0] : ['Punchline Place', 'Loopy Lane', 'Silly Street'],
                playgrounds[1] : ['Barnacle Boulevard', 'Seaweed Street', 'Lighthouse Lane'],
                playgrounds[2] : ['Oak Street', 'Elm Street', 'Maple Street'],
                playgrounds[3] : ['Baritone Boulevard', 'Tenor Terrace', 'Alto Avenue'],
                playgrounds[4] : ['Sleet Street', 'Walrus Way', 'Polar Place'],
                playgrounds[5] : ['Lullaby Lane', 'Pajama Place']
                }


    #constructor
    def __init__(self, toon, cog):
        self.toon = toon
        self.cog = cog

        self.login()
        self.startGame()
        
    
    #supporting methods
    def getInput(self, *locations):
        print("Places to travel to:")

        for location in locations:
            print(location)
        
        print(self.ENDLINE_CHAR)
        
        decision = input("Where would you like to go?" + self.ENDLINE_CHAR)
        print(self.ENDLINE_CHAR)

        return decision
    

    def startGame(self):
        self.userChoice = self.getInput(self.playgrounds[1], self.playgrounds[2], self.playgrounds[3])

        if (self.userChoice == "Donalds Dock"):
            self.ttcToDd()

        elif (self.userChoice == "Minnies Melodyland"):
            pass

        elif (self.userChoice == "Daisy Garden"):
            pass

        else:
            print("Invalid location. Try again." + self.ENDLINE_CHAR)
            self.startGame()


    def ttcToDd(self):
        #start moving
        self.toonLocation = self.streets[self.playgrounds[0]][0]
        print(self.toon + " is now entering " + self.toonLocation + self.ENDLINE_CHAR)
            
        print("No cog present. Phew!" + self.ENDLINE_CHAR)
            
        self.toonLocation = self.streets[self.playgrounds[1]][0]
        print(self.toon + " is now entering " + self.toonLocation + self.ENDLINE_CHAR)

        print("Still no cog present. Wow!" + self.ENDLINE_CHAR)
            
        self.toonLocation = self.playgrounds[1]
        print(self.toon + " is now entering " + self.toonLocation + self.ENDLINE_CHAR)
        #stop moving
        self.donaldsDock()


    def toontownCentral(self):
        #ttc choice
        self.userChoice = self.getInput(self.playgrounds[1], self.playgrounds[2], self.playgrounds[3])

        if (self.userChoice == "Donalds Dock"):
            self.ttcToDd()

        elif (self.userChoice == "Minnies Melodyland"):
            pass

        elif (self.userChoice == "Daisy Garden"):
            pass

        else:
            print("Invalid location. Try again." + self.ENDLINE_CHAR)
            self.toontownCentral()


    def donaldsDock(self):
        #donalds dock choice
        self.userChoice = self.getInput(self.playgrounds[0], self.playgrounds[2], self.playgrounds[4])

        if (self.userChoice == "Toontown Central"):
            self.DdToTtc()

        elif (self.userChoice == "Minnies Melodyland"):
            pass

        elif (self.userChoice == "Daisy Garden"):
            pass

        else:
           print("Invalid location. Try again." + self.ENDLINE_CHAR)
           self.donaldsDock() 

            

    def DdToTtc(self):
        #start moving
        self.toonLocation = self.streets[self.playgrounds[1]][0]
        print(self.toon + " is now entering " + self.toonLocation + self.ENDLINE_CHAR)
            
        print("No cog present. Phew!" + self.ENDLINE_CHAR)
            
        self.toonLocation = self.streets[self.playgrounds[0]][0]
        print(self.toon + " is now entering " + self.toonLocation + self.ENDLINE_CHAR)

        print("Still no cog present. Wow!" + self.ENDLINE_CHAR)
            
        self.toonLocation = self.playgrounds[0]
        print(self.toon + " is now entering " + self.toonLocation + self.ENDLINE_CHAR)
        #stop moving

        self.toontownCentral()

        
    def login(self):
        self.toonLocation = self.playgrounds[0]

        print(self.ENDLINE_CHAR + "Welcome to Toontown!")
        print(self.toon + " has logged into " + self.toonLocation + self.ENDLINE_CHAR)


    #unused currently
    def logout(self):
        print("Logging out.")
        print("See ya, " + self.toon + "!")


toontownChallenge(toonNameInput, tempCogName)
