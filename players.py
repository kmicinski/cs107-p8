# Tiles, Players, and NPCs
import pygame, sys, os, json, random
from pygame.locals import *

# The priorities of various elements
class Priority:
    background = 4
    item       = 3
    player     = 2
    arrow      = 1
    wall       = 1

# An exception that gets thrown when a player executes an
# invalid move.
class InvalidMoveException(Exception):
    pass

# The representation of a single tile on the game board
class Tile:
    def __init__(self, tileType):
        # The (x,y) position on the board
        self.xPosition = None
        self.yPosition = None

        # The priority of the tile, lower is higher priority
        self.priority  = Priority.background
        
        # The set of observers on this tile
        self.observers = []

        # The type of this tile. This is a string.
        self.tileType  = tileType

        # The image to render the tile
        self.image     = None
        
        # The set of observers watching for when this tile is collided
        # with. This is a list of objects. Every time this tile
        # "collides" with another tile, each of these collisions
        # observers will have its `handleCollisionWith` method called.
        self.collisionObservers = []

    # Getters and setters
    def getX(self): return self.xPosition
    def getY(self): return self.yPosition
    def getPriority(self): return self.priority
    def setPriority(self, n):
        self.priority = n

    # Is this tile a "Squirrel" object
    def isSquirrel(self): return False

    # Register for collision events
    def registerCollisionObserver(self,o):
        self.collisionObservers.append(o)

    # Register for movement events
    def registerMoveObserver(self,o):
        self.observers.append(o)

    # Fire all of the observers
    def fireCollision(self,collidedTile):
        for observer in self.collisionObservers:
            observer.handleCollisionWith(collidedTile)

    # Get a copy of this object. All object parameters are copied
    # deeply, but image object is reused (i.e., shallow copy).
    def clone(self):
        t = Tile(self.tileType)
        t.xPosition = self.xPosition
        t.priority  = self.priority
        # Should observers be copied..?
        t.observers = self.observers
        t.tileType  = self.tileType
        t.image     = self.image
        return t

    # Set and load the image file for this tile, also firing the
    # observers to update the game board based on this
    def setImage(self,filename):
        try:
            self.image = pygame.image.load(os.path.join(filename))
        except:
            print("Cannot load tile image file {}".format(filename))
            exit(1)
        
        # Now fire observers
        for observer in self.observers:
            observer.handleMove(x, y, x, y)
        return

    # Set the position of the tile, firing all observers
    def setPosition(self,x,y):
        fromX = self.xPosition
        fromY = self.yPosition
        self.xPosition = x
        self.yPosition = y
        for observer in self.observers:
            observer.handleMove(self, fromX, fromY, x, y)
        return
    
    # Get the image for this tile, returns None unless `setImageFile`
    # has been called
    def getImage(self):
        assert(self.image != None)
        return self.image

    # Handle a collision with another tile
    def handleCollisionWith(self, otherTile):
        pass

    # Turn this object into a string
    def __str__(self): return "tile"

# A tile factory that returns new tiles based on the character given
# Takes as input a configuration given as a Python dictionary.
class TileFactory:
    def __init__(self,cfg):
        self.tiles = {}
        
        for tileData in cfg["tiles"]:
            tile = Tile(tileData["type"])
            tile.setImage(tileData["filename"])
            tile.setPriority(tileData["priority"])
            tile.id = tileData["id"]
            self.tiles[tileData["mapCharacter"]] = tile
        return

    # Create a fresh new tile from the character with the specified
    # coordinate
    def fromChar(self,character,x,y):
        tile = self.tiles[character].clone()
        tile.setPosition(x,y)
        return tile

# Abstract Player class representing all of the common properties
# shared by a character
class Player(Tile):
    def __init__(self, coordinate, board):
        super(Player, self).__init__("player")
        self.setPosition(coordinate[0], coordinate[1])

        # A reference to the underlying board
        self.board = board

        # health points
        self.hp = 100

        # An x/y speed vector in "tiles per second"
        self.speed = (0,0)

        # Number of clock ticks since last move
        self.ticks = [0,0]

        # Register for clock ticks
        self.board.registerForClockTick(self)
        
    # Set the speed of some object
    def setSpeed(self,speed):
        # It had better be a two-tuple
        assert(type(speed) == type((1,2)))
        self.speed = speed

    # Several helper functions that will likely be useful in `clockTick`
    def sign(self,num):
        if num >= 0: return 1
        else:        return -1

    def abs(self,num):
        if num >= 0: return num
        else:        return -1*num

    # --------------------------------------------------------------
    # TASK 1 [10 points]
    # --------------------------------------------------------------

    # Handle a clock tick event. This is the main method in the game
    # that will cause player movement. Be sure to use self.move for
    # movement, as some Player subclasses may override movement (e.g.,
    # to subtract fuel). This method takes two arguments:
    # 
    #   - fps <-- The number of frames per second (i.e., number of
    #   times this method is called per second)
    # 
    #   - num <-- The number of frames since the last time this method
    #   was called.
    # 
    #  As a result, this function should move the player the
    #  appropriate amount based on the speed vector. The speed vector
    #  is given in "tiles per second."
    #  
    #  For example, let's say that self.speed = (10,10). This means
    #  that this tile should move 10 tiles to the right every second,
    #  and also 10 tiles down every second. So if `clockTick(10,1)` is
    #  called, this method should move the player right one tile and
    #  down one tile (i.e., (x+1, y+1)). However, let's instead say
    #  that self.speed is (5,5). Then...
    # 
    #    - self.clockTick(10,1) should do nothing the first time it is
    #    called.
    #    
    #    - self.clockTick(10,1) should move the tile right one tile
    #    and down one tile the *second* time it is called.
    # 
    #  This accounts for the fact that objects will move across the
    #  board with variable speeds.
    # 
    #  There are several things to keep in mind here:
    # 
    #  - To actually *perform* the movement, you should use the
    #  self.move(deltaX, deltaY) method, which takes a delta x and
    #  delta y (both in the range [-1,1]) and moves to (x + deltaX, y
    #  + deltaY)
    # 
    #  - Sometimes you can't move. For example, AI players should not
    #  be able to walk through walls. If a player attempts to move to
    #  a tile to which it cannot move, you must set the `canMove`
    #  field to False (it should be set to True) otherwise.
    def clockTick(self,fps,num):
        self.ticks[0] += self.speed[0]/fps*num
        self.ticks[1] += self.speed[1]/fps*num
        move = [0,0]
        if (abs(self.ticks[0]) > 1):
            self.ticks[0] -= 1 * self.sign(self.speed[0])
            move[0]       =  self.sign(self.speed[0])
        if (abs(self.ticks[1]) > 1):
            self.ticks[1] -= 1 * self.sign(self.speed[1])
            move[1]       =  self.sign(self.speed[1])
        self.canMove = self.canMoveTo(self.getX()+move[0],self.getY()+move[1])
        if ((move[0] != 0 or move[1] != 0) and self.canMove):
            self.move(move[0], move[1])

    # Attempt to move the player (+x, +y) units, where x is in the
    # range {-1, 0, 1} and y is in the range {-1, 0, 1}. For example,
    # `move(1,0)` would move the character one tile to the right.
    def move(self, x, y):
        tx = self.xPosition + x
        ty = self.yPosition + y
        # Check to ensure we can move there
        if (x < -1 or x > 1 or y < -1 or y > 1):
            # x and y must be in [-1,1]
            raise InvalidMoveException()
        if (tx >= 0 and tx < self.board.width
            and ty >= 0 and ty < self.board.height
            and
            (not self.board.higherPriorityObjectAt(self,tx,ty))):
            # Actually set the position
            self.setPosition(self.xPosition + x, self.yPosition + y)
        else:
            # Either outside of the boundaries of the board or a wall
            # is there
            raise InvalidMoveException()

    # Check whether or not we can move to (x,y) I.e., is there a wall
    # there, or is it out of bounds?
    def canMoveTo(self,tx,ty):
        # Check to ensure we can move there
        if (tx >= 0                     # x must be in [0,width-1]
            and tx < self.board.getWidth()
            and ty >= 0                 # y must be in [0,height-1]
            and ty < self.board.getHeight()):
            # Not a higher-priority object at that point (i.e., a wall)
            if (not self.board.higherPriorityObjectAt(self,tx,ty)):
                return True
            else:
                return False
        else:
            # Either outside of the boundaries of the board or a wall
            # is there
            return False

    def __str__(self): return "player"


# The "exit" tile in the game, a picture of a nut (i.e., when you get
# here you win).
class Exit(Player):
    def __init__(self, coordinate, board):
        super(Exit, self).__init__(coordinate, board)
        self.setImage("imgs/nuts.png")
        self.priority = Priority.item

    # If we collide with this tile, the player wins the game!
    def handleCollisionWith(self, other):
        # If we collided with the squirrel
        if (other.isSquirrel()):
            self.board.state.setWon()

    def __str__(self): return "nut (exit tile)"

# A stone is a floating sprite on the board that moves and eventually
# might hit another player.
class Stone(Player):
    def __init__(self, coordinate, board):
        super(Stone, self).__init__(coordinate, board)
        self.nuts = 0
        self.pic = pygame.image.load(os.path.join("imgs/stone0.png"))
        self.priority = Priority.player
        self.tileType = "stone"

    def getImage(self):
        return self.pic

    # --------------------------------------------------------------
    # TASK 2 [5 points]
    # --------------------------------------------------------------

    # This method will be called in the same way as `clockTick` on the
    # Player object, as this is a subclass of Player. Your clock tick
    # method should:
    # 
    # - Call the parent's clockTick method
    # 
    # - If the movement failed (e.g., because the stone hit a wall)
    # you should remove this tile from the board. 
    def clockTick(self,fps,num):
        super(Stone,self).clockTick(fps,num)
        if (self.canMove == False):
            # Tried to move and couldn't
            self.board.removeTile(self)
            self.board.unregisterForClockTick(self)
            if self in self.board.stones:
                self.board.stones.remove(self)

    def __str__(self): return "stone"

# A health pack gives the player life once they touch it.
class Health(Player):
    def __init__(self, coordinate, board):
        super(Health, self).__init__(coordinate, board)
        self.nuts = 0
        self.pic = pygame.image.load(os.path.join("imgs/hospital.png"))
        self.priority = Priority.item
        self.setSpeed((0,0))
        self.tileType = "healthpack"

    def getImage(self):
        return self.pic

    def clockTick(self,fps,num):
        super(Health,self).clockTick(fps,num)

    # --------------------------------------------------------------
    # TASK 3 [3 points]
    # --------------------------------------------------------------

    # This method should:
    #   - Check whether the tile being collided with is a squirrel
    #   - If it is, it should increment the fuel by 15 and *then* 
    #   remove the tile from the board.
    #   - If it is not, it should not do anything.
    def handleCollisionWith(self,other):
        if (other.tileType == "squirrel"):
            self.board.state.incrementFuel(15)
            self.board.removeTile(self)

    def __str__(self): return "healthpack"

# The main player in the game (i.e., the squirrel)
class Squirrel(Player):
    def __init__(self, coordinate, board):
        super(Squirrel, self).__init__(coordinate, board)
        self.nuts = 0
        self.pic = pygame.image.load(os.path.join("imgs/squirrelright.png"))
        self.priority = Priority.player
        self.setSpeed((0,0))
        self.movementVector = (1,0)
        self.STONESPEED = 8
        self.tileType = "squirrel"

    # This player is the squirrel
    def isSquirrel(self): return True

    # Handle events from the toplevel
    def handleEvent(self,event):
        if event.type == pygame.KEYDOWN:
            try:
                if event.key == pygame.K_LEFT:
                    self.move(-1, 0)
                    self.movementVector = (-1,0)
                elif event.key == pygame.K_RIGHT:
                    self.move(1, 0)
                    self.movementVector = (1,0)
                elif event.key == pygame.K_UP:
                    self.move(0, -1)
                    self.movementVector = (0,-1)
                elif event.key == pygame.K_DOWN:
                    self.move(0, +1)
                    self.movementVector = (0,1)
                elif event.key == pygame.K_SPACE:
                    self.fireStone()
            except InvalidMoveException:
                # They tried to go somewhere they couldn't, do
                # nothing.
                return

    # --------------------------------------------------------------
    # TASK 4 [10 points]
    # --------------------------------------------------------------

    # Fire a stone
    # 
    # This method should fire a stone. The stone should start at (x +
    # mX, y + mY) where (mX, mY) is the movement vector. For example,
    # if the squirrel is traveling to the right (because the last key
    # pressed was the right) and the squirrel is currently at (3, 2),
    # then the stone should start at (4, 2). Additionally, you must
    # subtract 10 fuel after firing a stone.
    # 
    # Note that you will need to:
    # 
    # - Check that the stone can actually start at that place. For
    # example, if the stone should start at (4, 2) but there is a wall
    # there, then you should not fire a stone.
    # 
    # - Add the stone to the board (otherwise it won't show up)
    # 
    # - Ensure there are at least 10 fuel tokens available
    # 
    # - Ensure that you make the stone register for clock ticks
    # (otherwise it won't move)
    def fireStone(self):
        startingTile = (self.getX()+self.movementVector[0], self.getY()+self.movementVector[1])
        # Make sure we're not trying to, shoot at something we can't,
        # e.g., a wall.
        if (self.canMoveTo(startingTile[0], startingTile[1])):
            stone = Stone(startingTile,self.board)
            stone.setPosition(startingTile[0], startingTile[1])
            stone.setSpeed((self.movementVector[0] * self.STONESPEED, self.movementVector[1] * 4))
            self.board.addTile(stone)
            self.board.registerForClockTick(stone)
            self.board.state.decrementFuel(10)
        return

    def move(self,x,y):
        super().move(x,y)
        
        # Once we've performed the move, we need to update the player
        # statistics. Specifically, we:
        #   - Subtract one fuel
        self.board.state.decrementFuel(1)
        
    def getImage(self):
        return self.pic

    # --------------------------------------------------------------
    # TASK 5 [3 points]
    # --------------------------------------------------------------

    # Handle collisions with other things
    # If you collide with a...
    # 
    #  - ferret <-- Subtract 15 fuel
    #  - stone  <-- Subtract 10 fuel
    def handleCollisionWith(self,other):
        if (other.tileType == "ferret"):
            self.board.state.decrementFuel(15)
        if (other.tileType == "stone"):
            self.board.state.decrementFuel(10)


    def __str__(self): return "squirrel"

# A "square" AI player. This AI player is a ferret that walks around
# the board. 

class SquareAIFerret(Player):
    def __init__(self, coordinate, board):
        super(SquareAIFerret, self).__init__(coordinate, board)
        self.nuts = 0
        self.pic = pygame.image.load(os.path.join("imgs/ferret.png"))
        self.priority = Priority.player
        self.setSpeed((5,0))
        self.numTicks = 0
        self.ticksSinceFire = 0
        self.hp = 30
        self.tileType = "ferret"
        self.STONESPEED = 8

    # --------------------------------------------------------------
    # TASK 6 [7 points]
    # --------------------------------------------------------------

    # Move should implemented in such a way that the ferret AI
    # character walks around the board in a length 5 square. For
    # example, if the ferret starts at (5,5), the first step should be
    # to (6,5), then (7,5) and so on until reaching (10,5). At that
    # point, it should start going downwards to (10,6) until it
    # reaches (10,10), at which point it should go left. It should
    # proceed to (5,10) until finally moving back up towards (5,5 and
    # starting over again).
    # 
    # As a hint: I would suggest adding a `numTicks` member variable
    # to this class and then incrementing it upon each call to `move`.
    def move(self,x,y):
        if (self.numTicks % 5 == 0):
            # Change direction
            if (self.speed == (5,0)):
                self.setSpeed((0,-5))
            elif (self.speed == (0,-5)):
                self.setSpeed((-5,0))
            elif (self.speed == (-5,0)):
                self.setSpeed((0,5))
            elif (self.speed == (0,5)):
                self.setSpeed((5,0))
            self.numTicks = 0

        self.numTicks += 1
        self.ticksSinceFire += 1

        if (self.ticksSinceFire % 7 == 1):
            self.fireStone()
        
        super().move(x,y)

    # --------------------------------------------------------------
    # TASK 7 [5 points]
    # --------------------------------------------------------------
    

    def fireStone(self):
        movementVector = [0,0]
        ri = random.randint(0,7)
        if (ri == 0):
            movementVector = [1,0]
        elif (ri == 1):
            movementVector = [0,1]
        elif (ri == 2):
            movementVector = [-1, 0]
        elif (ri == 3):
            movementVector = [0, -1]
        elif (ri == 4):
            movementVector = [-1, -1]
        elif (ri == 5):
            movementVector = [1, 1]
        elif (ri == 6):
            movementVector = [1, -1]
        elif (ri == 7):
            movementVector = [-1, 1]

        startingTile = (self.getX()+movementVector[0],
                        self.getY()+movementVector[1])

        # Make sure we're not trying to, shoot at something we can't,
        # e.g., a wall.
        if (self.canMoveTo(startingTile[0], startingTile[1])):
            stone = Stone(startingTile,self.board)
            stone.setPosition(startingTile[0], startingTile[1])
            stone.setSpeed((movementVector[0] * self.STONESPEED,
                            movementVector[1] * 4))
            self.board.addTile(stone)
            self.board.registerForClockTick(stone)
            self.board.stones.append(stone)

    # If we collide with a stone, we subtract 15 HP.
    def handleCollisionWith(self, other):
        # If we collided with the squirrel
        if (other.tileType == "stone"):
            self.subtractHp(15)

    def getImage(self):
        return self.pic

    # --------------------------------------------------------------
    # TASK 8 [3 points]
    # --------------------------------------------------------------

    # Subtract HP, potentially killing off the character
    # 
    # Takes a single argument, hp. The result of calling this function
    # should be that:
    # 
    #  - self.hp becomes subtracted by the relevant amount. 
    # 
    #  - If the hp now becomes below 0, this tile should be removed
    #  from the board.
    def subtractHp(self,hp):
        self.hp -= hp
        if (self.hp <= 0):
            # Remove this tile from the board, effectively "killing"
            # the character
            self.board.unregisterForClockTick(self)
            self.board.removeTile(self)

    def __str__(self): return "ferret"
