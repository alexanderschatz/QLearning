import numpy as np
import random

import globalV

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
            elif(self.actions[actionIndex] == 'r' and currentState[0] == globalV.COLUMNS-1):
                return False
            elif(self.actions[actionIndex] == 'u' and currentState[1] == 0):
                return False
            elif(self.actions[actionIndex] == 'd' and currentState[1] == globalV.ROWS-1):
                return False
        else:
            #if the action was chosen based on a max value, said value is biased negatively to prevent the AI from choosing it again
            if(self.actions[actionIndex] == 'l' and currentState[0] == 0):
                self.qTable[self.stateCoords[currentState], actionIndex] -= 1
                return False
            elif(self.actions[actionIndex] == 'r' and currentState[0] == globalV.COLUMNS-1):
                self.qTable[self.stateCoords[currentState], actionIndex] -= 1
                return False
            elif(self.actions[actionIndex] == 'u' and currentState[1] == 0):
                self.qTable[self.stateCoords[currentState], actionIndex] -= 1
                return False
            elif(self.actions[actionIndex] == 'd' and currentState[1] == globalV.ROWS-1):
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