import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import random
import time

import map, player, qlearn, globalV


author = "A.Schatz, alexander.schatz@th-widau.de"

###################################

if __name__ == '__main__':
    #initialize classes
    game = map.Map()
    player = player.Player()
    q = qlearn.qLearning(game.getRewardDictionary(), player.getActions(), game.getStateCoords())

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
