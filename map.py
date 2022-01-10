import numpy as np
import tkinter as tk
import random

import globalV

###################################

#Map defines the playground
class Map(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.columns = globalV.COLUMNS
        self.rows = globalV.ROWS
        self.size = globalV.CELLSIZE
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
        self.canvas = tk.Canvas(self, width=globalV.WIDTH, height=globalV.HEIGHT, background='grey')

        #creates map and grid
        self.createMap()
        self.createGrid()

    #creates a gid, that displays the individual cells
    def createGrid(self):
        for x in range(self.columns, globalV.WIDTH, self.size):
            self.canvas.create_line(x, 0, x, globalV.WIDTH, fill='black')
        for y in range(self.rows, globalV.HEIGHT, self.size):
            self.canvas.create_line(0, y, globalV.HEIGHT, y, fill='black')

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
                i = globalV.MAP_RAW[x][y]
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