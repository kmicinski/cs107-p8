# CS 107, Fall 2018
# Representation of the game board

import pygame
from pqueue import PriorityQueue
from levelState import *
from players    import *

# Holds the master game board, with a whole bunch of tiles
# 
# This class has several fields:
# 
#   - cfg -- A configuration object, specifies board layout and maps,
#   etc..
# 
#   - width / height (natural numbers) -- The width / height of the
#   game board
# 
#   - board -- A two-dimensional array of priority queues representing
#   the tiles at each (x,y) coordinate on the board.
# 
#   - dirty -- A two-dimensional array saying--for each (x,y)
#   coordinate on the board--whether it needs to be drawn again or
#   not.
#   
class GameBoard:
    def __init__(self, cfg, width, height):
        self.cfg    = cfg
        # Set up the state of the game board using the LevelState
        # object. This is the main class that holds things like the
        # amount of fuel that the player has left.
        initialFuel = 30 # A default value of fuel to use if one is
                         # not specified in config.json
        
        try:
          initialFuel = self.cfg["initialfuel"]
        except:
          pass
        self.state  = LevelState(initialFuel)
        # The actual board, represented as an width-by-height matrix
        # (array of arrays)
        self.board  = [[0 for x in range(height)] for y in range(width)]
        # A "dirty" matrix. This is used for efficiency: don't redraw
        # tiles that don't need to be redrawn.
        self.dirty  = [[True for x in range(height)] for y in range(width)]
        # Set the width/height
        self.width  = width
        self.height = height
        
        # Build the board as a matrix of priority queues
        for x in range(width):
            for y in range(height):
                self.board[x][y] = PriorityQueue()

        # The set of things that want to listen to clock ticks.
        self.clockTickListeners = []
        self.ferrets = []
        self.healthpacks = []
        self.stones = []

    def getWidth(self): return self.width
    def getHeight(self): return self.height

    # Render all of the tiles at (x,y)
    def renderAt(self, screen, x, y):
        actualX = self.cfg["tileSize"] * x
        actualY = self.cfg["tileSize"] * y
        # Iterate through the tiles at (x,y) in priority order
        for priorityItem in self.board[x][y].lst:
            screen.blit(priorityItem[1].getImage(), (actualX, actualY))

        # Since all the images in this tile have been blitted, clean
        # the dirty bit
        self.dirty[x][y] = False
        return

    # Add the tile to the board, coordinate is drawn from tile's (x,y)
    # position
    def addTile(self, tile):
        self.board[tile.getX()][tile.getY()].add(tile, tile.getPriority())
        self.dirty[tile.getX()][tile.getY()] = True
        tile.registerMoveObserver(self)

    def removeTile(self,tile):
        self.board[tile.getX()][tile.getY()].remove(tile)
        self.dirty[tile.getX()][tile.getY()] = True

    # Return true if a higher-priority object is on the board at the
    # specified place
    def higherPriorityObjectAt(self, tile, x, y):
        for t in self.board[x][y]:
            if (t[0] < tile.getPriority()):
                return True
        return False

    # Handle a move from one coordinate to another
    def handleMove(self, tile, fromX, fromY, toX, toY):
        # If fromX/Y are None (since they have never been set before)
        if (fromX != None and fromY != None):
            self.board[fromX][fromY].remove(tile)

        self.board[toX][toY].add(tile, tile.getPriority())

        # Dirty the screen, also process collisions
        if (fromX != toX or fromY != toY):
            if (fromX and fromY):
                self.dirty[fromX][fromY] = True
            self.dirty[toX][toY] = True
            for observer in self.board[toX][toY]:
                if (observer[1].getPriority() >= tile.getPriority()):
                    observer[1].handleCollisionWith(tile)
                #if tile.getPriority() >= observer[1].getPriority():
                #    tile.handleCollisionWith(observer[1])

    # Register for clock tick events
    def registerForClockTick(self,observer):
        self.clockTickListeners.append(observer)

    # Register for clock tick events
    def unregisterForClockTick(self,observer):
        self.clockTickListeners.remove(observer)

    # Clock tick event
    # This is called from game.py
    def clockTick(self,fps,num):
        for observer in self.clockTickListeners:
            observer.clockTick(fps,num)
    

    # Set up all of the enemies on the board
    # Assume enemies is a list (array) of dictionaries
    def setupCharacters(self,enemiesDict):
        for enemy in enemiesDict:
            if enemy["type"] == "squareferret":
                ferret = SquareAIFerret([enemy["startX"], enemy["startY"]], self)
                self.addTile(ferret)
                self.ferrets.append(ferret)
            elif enemy["type"] == "healthpack":
                hp = Health([enemy["startX"], enemy["startY"]],self)
                self.addTile(hp)
                self.healthpacks.append(hp)

    # Render the whole screen
    def renderScreen(self,screen):
        # Walk through all of the x,y coordinates, redraw the screen
        # if necessary. Take care to avoid drawing when the screen is
        # not dirty
        for x in range(self.width):
            for y in range(self.height):
                self.renderAt(screen, x, y)

        # Draw life
        font = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = font.render('Fuel: ' + str(self.state.hp),
                                  False, (255, 255, 255))
        screen.blit(textsurface,(0,0))

        if (self.state.gameOver()):
            screen.fill((0,0,0))
            font = pygame.font.SysFont('Comic Sans MS', 80)
            wl   = 'Lose :-('
            if (self.state.hasWon()):
                wl = 'Win :-)'
            textsurface = font.render('You ' + wl,
                                      False, (0, 255, 0))
            screen.blit(textsurface,(100,200))
            

        # Redraw the whole screen
        pygame.display.flip()
                
