import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import random
import time

author = "A. Schatz, alexander.schatz@th-widau.de"

#width and height of canvas
WIDTH = 800
HEIGHT = 800

#number of columns and rows of the playground
COLUMNS = 16
ROWS = 16

#size of each cell(Tile) in pixel
CELLSIZE = 50

#raw map that defines the layout of the playground
MAP_RAW = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
           [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
           [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
           [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
           [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2]]

###################################


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
        if(self.x == COLUMNS-1):
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
        if(self.y == ROWS-1):
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

###################################

#Map defines the playground
class Map(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.columns = COLUMNS
        self.rows = ROWS
        self.size = CELLSIZE
        self.mapSize = self.columns * self.rows

        #initializes lastPlayerPos and the finish position  as tupel
        self.lastPlayerPos = (0, 0)
        self.finish = (0, 0)

        #initializes empty matrix
        self.mapMatrix = np.zeros((self.columns, self.rows))

        #initializes dictionaries that map the coordinates to the rewards and to the stateIndex
        self.rewardDictionary = {}
        self.stateCoords = {}

        #defines color dictionary that defines the color based on the reward of the Tile
        self.colorDictionary = {1: 'red', 0.001: 'yellow', -1: 'blue', 0: 'grey', 'player': 'green'}

        #defines the canvas
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, background='grey')

        #creates map and grid
        self.createMap()
        self.createGrid()

    #creates a gid, that displays the individual cells
    def createGrid(self):
        for x in range(self.columns, WIDTH, self.size):
            self.canvas.create_line(x, 0, x, WIDTH, fill='black')
        for y in range(self.rows, HEIGHT, self.size):
            self.canvas.create_line(0, y, HEIGHT, y, fill='black')

    def getRewardDictionary(self):
        return self.rewardDictionary

    def getStateCoords(self):
        return self.stateCoords

    def getFinish(self):
        return self.finish

    def createMap(self): #creates the map, colors Tiles based on reward
        reward = 0
        index = 0
        for x in range(0, self.columns):
            for y in range(0, self.rows):
                #define reward based on raw map
                i = MAP_RAW[x][y]
                if(i == 0): reward = -1
                elif(i == 1): reward = 0.001
                elif(i == 2): 
                    reward = 1
                    self.finish = (x, y) #defines finish position

                #map rewards to coordinates and state indices to coordinates
                self.rewardDictionary.update({(x, y): reward})
                self.stateCoords.update({(x, y): index})
                index += 1

                #draw Tiles on canvas
                self.canvas.create_rectangle(x*self.size, y*self.size, x*self.size+self.size, y*self.size+self.size, fill=self.colorDictionary[reward])
        
        self.canvas.pack(padx=1, pady=1)
        pass

    #redraws the player on canvas and redraws the tile the player was before moving
    def updateMap(self, playerPos):

        #redraw Rectangle on lastPlayerPos
        x = self.lastPlayerPos[0]
        y = self.lastPlayerPos[1]
        self.canvas.create_rectangle(x*self.size, y*self.size, x*self.size+self.size, y*self.size+self.size, fill=self.colorDictionary[self.rewardDictionary[(x, y)]])

        #draw Player on playerPos
        x = playerPos[0]
        y = playerPos[1]
        self.canvas.create_rectangle(x*self.size, y*self.size, x*self.size+self.size, y*self.size+self.size, fill=self.colorDictionary['player'])
        
        #updateLastPlayerPos
        self.lastPlayerPos = playerPos
        pass
###################################

###################################

#qLearning is the algorithm thas is used to train the AI
class qLearning():
    #parameter needed: dictionary where rewards are mapped to the stateIndex
    #                  array with possible actions
    #                  dictionary where coordinates are mapped to the stateIndex
    def __init__(self, stateRewards, actions, stateCoords): 
        self.stateCoords = stateCoords
        self.stateRewards = stateRewards
        self.actions = actions

        #initialize old player position (last state)
        self.oldPlayerPos = (0, 0)
        #boolean that defines if this is the first run
        self.firstRun = True

        #initialize qLearning parameter
        self.learningRate = 0.4 
        self.discount = 0.9 #the discount determines how much the AI strives for high rewards
        self.epsilon = 0.1  #epsilon is a percentage that determines the exploration rate

        pass

    #initializes the qTable // qTable has the form: states vs actions; it defines the possible reward of taking an action at a certain state
    def initializeQTable(self):
        actionSize = len(self.actions)
        stateSize = len(self.stateRewards)
        self.qTable = np.zeros([stateSize, actionSize])

        #the values are assigned as random, because the AI has no prior knowledge about the environment
        for x in range(stateSize):
            for y in range(actionSize):
                self.qTable[x, y] = random.random()

        pass

    def getQTable(self):
        return self.qTable

    #returns a False if an action is invalid // invalid actions are defined as stepping beyond the bounds of the environment
    def isActionValid(self, actionIndex, currentState, isRandomAction):
        if(isRandomAction):
            #if the action was chosen randomly only False is returned
            if(self.actions[actionIndex] == 'l' and currentState[0] == 0):
                return False
            elif(self.actions[actionIndex] == 'r' and currentState[0] == COLUMNS-1):
                return False
            elif(self.actions[actionIndex] == 'u' and currentState[1] == 0):
                return False
            elif(self.actions[actionIndex] == 'd' and currentState[1] == ROWS-1):
                return False
        else:
            #if the action was chosen based on a max value, said value is biased negatively to prevent the AI from choosing it again
            if(self.actions[actionIndex] == 'l' and currentState[0] == 0):
                self.qTable[self.stateCoords[currentState], actionIndex] -= 1
                return False
            elif(self.actions[actionIndex] == 'r' and currentState[0] == COLUMNS-1):
                self.qTable[self.stateCoords[currentState], actionIndex] -= 1
                return False
            elif(self.actions[actionIndex] == 'u' and currentState[1] == 0):
                self.qTable[self.stateCoords[currentState], actionIndex] -= 1
                return False
            elif(self.actions[actionIndex] == 'd' and currentState[1] == ROWS-1):
                self.qTable[self.stateCoords[currentState], actionIndex] -= 1
                return False

        #else return True
        return True

    #getInput returns the new action
    def getInput(self, currentPos, actionTakenIndex):
        #it takes the current player position (current state) and the last taken action

        #for readbility outcomeStateIndex and oldStateIndex are defined here
        outcomeStateIndex = self.stateCoords[currentPos]
        oldStateIndex = self.stateCoords[self.oldPlayerPos]

        #if firstRun is True the qTable is initialized
        if (self.firstRun):
            self.initializeQTable()
            self.firstRun = False
        else:
            #else take the reward from the current player Position
            reward = self.stateRewards[currentPos]

            #update qTable based on:
            # Q'(s_t, a_t) = Q(s_t, a_t) + alpha * (r_t + gamma * max_a(Q(s_t+1, a)) - Q(s_t, a_t))
                
                # Q'(s_t, a_t)      .. new qValue at state s_t with action a_t
                # Q(s_t, a_t)       .. old qValue at state s_t with action a_t
                # aplha             .. learning rate
                # r_t               .. reward
                # gamma             .. discount factor
                # max_a(Q(s_t+1, a)).. estimate of optimal future value
            
            # https://www.practicalai.io/teaching-ai-play-simple-game-using-q-learning/
            # https://en.wikipedia.org/wiki/Q-learning

            self.qTable[oldStateIndex, actionTakenIndex] = self.qTable[oldStateIndex, actionTakenIndex] + self.learningRate * \
                (reward + self.discount * max(self.qTable[outcomeStateIndex]) - self.qTable[oldStateIndex, actionTakenIndex])

        #update old player position
        self.oldPlayerPos = currentPos

        #define new action // overwrite actinTakenIndex with new actionIndex
        if(random.random() <= self.epsilon):
            #exploration mode: next action s chosen randomly
            actionTakenIndex = random.randint(0, len(self.actions)-1)

            #choose a different action if chosen action is invalid
            while self.isActionValid(actionTakenIndex, currentPos, True) == False:
                actionTakenIndex = random.randint(0, len(self.actions)-1)

        else:
            #optimal mode: next action is chosen based on max possible qValue
            actionTakenIndex = np.where(self.qTable == max(self.qTable[outcomeStateIndex]))[1][0]

            #choose a different action if chosen action is invalid
            while self.isActionValid(actionTakenIndex, currentPos, False) == False:
                actionTakenIndex = np.where(self.qTable == max(self.qTable[outcomeStateIndex]))[1][0]

        #return new action
        return actionTakenIndex
###################################


if __name__ == '__main__':
    #initialize classes
    game = Map()
    player = Player()
    q = qLearning(game.getRewardDictionary(), player.getActions(), game.getStateCoords())

    #define counter
    moveCounter = 0
    gameCounter = 1

    #define array that holds the moveCounter for the display of a learning curve
    gameMovex = []

    print("###################################################")
    print("AI learns to take a path using Q-Learning algorithm")
    print("###################################################")
    print()
    print("by " + author)
    print()
    print("This program starts a game, where an artificial player (AI) has the task to find an optimal way through a marshland. \n" +
          "The player is displayed with the color green. The finish the player has to reach is displayed with the color red. \n"+
           "The save path is displayed with the color red. Each tile that hast the color blue is defined as an unsave path. \n" +
           "The AI has no prior knowledge of what is good and what is bad.")
    print()
    print("The Q-Learning algorithm is a reinforcement learning algorithm, that reward the AI for good actions \n" +
           "(staying on the path, reaching the goal) and punishes it for doing bad things (stepping into the marsh).")
    print()
    print("The AI will learn over the course of 100 games which path to follow to savely reach the goal.")
    print()
    print("###################################################")
    print()
    print("Do you want to observe the movement of the AI? [y, n]")
    print("(this may take a while)")
    print()
    
    watch = input("")

    print()
    print("###################################################")
    print()

    while True:
        #play 100 game
        if(gameCounter > 100):
            break

        if(player.getPos() == game.getFinish()):
            #if player has reached the finish: reset player and moveCounter; print the amount of steps taken; increase gameCounter
            print("Game " + str(gameCounter) + " won after " + str(moveCounter) + " steps.")
            player.resetPlayer()
            gameMovex.append(moveCounter)
            moveCounter = 0
            gameCounter += 1
        else:
            #else: define new action; let player execute chosen new action; increase moveCounter
            actionIndex = q.getInput(player.getPos(), player.getLastAction())
            player.doAction(player.getActions()[actionIndex])
            moveCounter += 1

        if(watch == "y"):
            #render the playground; 
            game.update()
            game.updateMap(player.getPos())
            tk.Tk.after(game, 10) #sleep 10ms between each step

    print()
    print("###################################################")
    print()
    print("Do you want to see the learning curve? [y, n]")
    print()
    
    watch = input("")
    if(watch == 'y'):
        #display the learning curve
        plt.plot(gameMovex)
        plt.xlabel("number of games")
        plt.ylabel("number of steps")
        plt.show()

    print()
    print("###################################################")
    print()
