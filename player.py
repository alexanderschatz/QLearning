import globalV

###################################

#Player defines a player with its position, possible actions and the last action
class Player(): 
    def __init__(self):
        self.resetPlayer() 
        pass

    def getPos(self): #return player position as a tupel
        return (self.x, self.y)

    def getActions(self): #return array of possible player actions
        return self.actions

    def setPos(self, newPos): #set new player position from tupel
        self.x = newPos[0]
        self.y = newPos[1]
        pass

    def resetPlayer(self): #resets the player position // is called in __init__ // initializes actions and last action
        self.setPos((0, 0))
        self.actions = ['l', 'r', 'u', 'd']
        self.lastAction = 0
        pass

    #player actions that change the position of player in the matrix
    ##############################
    def left(self):
        if(self.x == 0):
            return False
        else:
            self.x -= 1
            return True

    def right(self):
        if(self.x == globalV.COLUMNS-1):
            return False
        else:
            self.x += 1
            return True

    def up(self):
        if(self.y == 0):
            return False
        else:
            self.y -= 1
            return True

    def down(self):
        if(self.y == globalV.ROWS-1):
            return False
        else:
            self.y += 1
            return True
    ###########################

    def doAction(self, action): #executes action // updates last action
        if(action == 'l'):
            self.left()
        elif(action == 'r'):
            self.right()
        elif(action == 'u'):
            self.up()
        elif(action == 'd'):
            self.down()

        self.lastAction = self.actions.index(action)
        pass

    def getLastAction(self): #returns last player action
        return self.lastAction
###################################