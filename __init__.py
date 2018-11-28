from tkinter import *
import os
import random
import copy
import logic
import player
import playerL
import playerT
import playerB
import playerR
import graphicsFunc
random.seed(10)
# ---------------------- Control Center ------------------------- #

def init(data):
    data.mode = "start"
    data.images = []
    data.drawPile = [] 
    data.highlighted = []
    data.B = playerB.PlayerB([], "Bottom")
    data.R = playerR.PlayerR([], "Right")
    data.T = playerT.PlayerT([], "Top")
    data.L = playerL.PlayerL([], "Left")
    data.turnOrder = [data.B, data.R, data.T, data.L]
    data.turnInd = random.randint(0, 3)
    graphicsFunc.loadImages(data)
    graphicsFunc.loadSeaFlow(data)
    graphicsFunc.initialHands(data)
    graphicsFunc.loadBack(data)


def mousePressed(event, data):
    if data.mode == "play": playMousePressed(event, data)
    elif data.mode == "pong": graphicsFunc.pongMousePressed(event, data)
    elif data.mode == "chow": graphicsFunc.chowMousePressed(event, data)

def keyPressed(event, data):
    if event.keysym == "p":
        data.mode = "play"
    if data.mode == "play": playKeyPressed(event, data)

def timerFired(data):
    if data.mode == "play": playTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "start":
        canvas.create_text(data.width / 2, data.height / 2, text="press p to play")
    elif data.mode == "play": playRedrawAll(canvas, data)
    elif data.mode == "pong": 
        playRedrawAll(canvas, data)
        graphicsFunc.pongRedrawAll(canvas, data)
    elif data.mode == "chow":
        playRedrawAll(canvas, data)
        graphicsFunc.chowRedrawAll(canvas, data)
    elif data.mode == "win":
        playRedrawAll(canvas, data)
        graphicsFunc.winRedrawAll(canvas, data)


#---------------------- Play Mode -------------------------- #


def playMousePressed(event, data):
    # highlights tile if pressed
    graphicsFunc.tilePressed(event, data)
    # discards highlighted tile, changes turn, draws
    graphicsFunc.discardPressed(event, data)

     

def playKeyPressed(event,data):
    pass

def playTimerFired(data):
    pass

def playRedrawAll(canvas, data):
    # draw background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="green") 
    # draw remaining draw tile count
    canvas.create_text(data.width / 2, data.height / 2, text=len(data.drawPile), font = "Arial 20")
    # draw text indicating whose turn it is
    canvas.create_text(data.width / 2, 2 * data.height / 3, \
        text="Turn: " + data.turnOrder[data.turnInd].name, font = "Arial 20")
    # discard button
    graphicsFunc.discardButton(canvas, data)
    # draw tiles
    for hand in data.turnOrder:
        hand.drawTiles(canvas, data)
        hand.drawMelds(canvas, data)
    # draw discard pile
    graphicsFunc.drawDiscard(canvas, data)



###########################################
# Animation starter code from Course Notes
###########################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 800)