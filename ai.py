from random import randint
from players import *

class InvalidRequestException(Exception):
    pass

class AISquirrel(Squirrel):
    def __init__(self, coordinate, board):
        super(Squirrel, self).__init__(coordinate, board)
        self.nuts = 0
        self.pic = pygame.image.load(os.path.join("imgs/squirrelright.png"))
        self.priority = Priority.player
        super().setSpeed((0,0))
        self.tileType = "squirrel"
        self.aiTicks = 0
        self.STONESPEED = 8

    # Turn *off* the ability to set a speed
    def setSpeed(self,speed):
        return

    # Don't do anything!
    def handleEvent(self,ev):
        return

    # Every half second, the squirrel gets 1 more fuel
    def clockTick(self,fps,num):
        self.aiTicks += num
        if (self.aiTicks > 5):
            self.board.state.incrementFuel(3)
            self.aiTicks -= 5

    def getHealthPacks(self):
        self.board.state.decrementFuel(20)
        x = []
        for hpack in self.board.healthpacks:
            x.append((hpack.getX(),hpack.getY()))
        return x

    def getFerrets(self):
        self.board.state.decrementFuel(5)
        x = []
        for ferret in self.board.ferrets:
            x.append((ferret.getX(),ferret.getY()))
        return x

    def getExit(self):
        self.board.state.decrementFuel(30)
        return (self.board.endTile.getX(),self.board.endTile.getY())

    def abs(self,x):
        if (x < 0): return -x
        return x

    # Uses |x| + |y| fuel
    def move(self,x,y):
        print('at move')
        if (x < -1 or x > 1 or y < -1 or y > 1):
            print("here1")
            raise InvalidRequestException()
        if self.canMoveTo(self.getX() + x, self.getY() + y):
            super().move(x,y)
            self.board.state.decrementFuel(self.abs(x) + self.abs(y))
        else:
            print("here2")
            raise InvalidRequestException()

    # Where x & y are in the range of integers [-1,1]
    def fireStone(self,x,y):
        if (x < -1 or x > 1 or y < -1 or y > 1):
            raise InvalidRequestException()
        
        startingTile = (self.getX()+x,
                        self.getY()+y)

        # Make sure we're not trying to, shoot at something we can't,
        # e.g., a wall.
        if (self.canMoveTo(startingTile[0], startingTile[1])):
            stone = Stone(startingTile,self.board)
            stone.setPosition(startingTile[0], startingTile[1])
            stone.setSpeed((movementVector[0] * self.STONESPEED,
                            movementVector[1] * self.STONESPEED))
            self.board.addTile(stone)
            self.board.registerForClockTick(stone)
            self.board.state.decrementFuel((self.abs(x) + self.abs(y)) * 3)
        else:
            raise InvalidRequestException()

class MyAISquirrel(AISquirrel):
    def __init__(self, coordinate, board):
        super().__init__(coordinate, board)
        self.myTicks = 0
        self.setSpeed((0,0))

    # You may call this method as often as you like: it does not use
    # any fuel.
    def canMove(self,x,y):
        print((self.getX() + x, self.getY() + y))
        return self.canMoveTo(self.getX() + x, self.getY() + y)

    # Use this method to move in any direction one tile. This will use
    # |x| + |y| fuel (i.e., if you call it with (-1, 1) it will use 2)
    def move(self,x,y):
        super().move(x,y)

    # Where x,y are in the range [-1,1] (integers)
    # Uses (|x| + |y|) * 3 fuel
    def fireStone(self,x,y):
        super().fireStone(x,y)

    # Gets the *current* position of all ferrets on the board as a
    # list of (x,y) tuples.
    # 
    # Uses 5 fuel each time it is called
    def getFerrets(self):
        return super().getFerrets()

    # Gets the position of all health packs on the board (which do not
    # move)
    # 
    # Uses 20 fuel each time it is called
    def getFerrets(self):
        return super().getFerrets()

    # Implement the main logic for your AI here. You may not
    # manipulate the other tiles on the board directly: this will be
    # considered cheating. Similarly, you may not manipulate the fuel
    # directly.
    # 
    # Every half second, you will receive 3 more fuel. This is
    # implemented in the parent class's clockTick (which, again, you
    # may not change).
    def clockTick(self,fps,num):
        super().clockTick(fps,num)

        # For example, if I wanted to step to the health pack (default tile)
        if (self.myTicks < 1):
            self.move(1,1)

        self.myTicks += 1

        if (self.myTicks % 4 != 0):
            return

        if (self.myTicks % 40 == 0):
            print('getting the position of all ferrets')
            for ferretPos in self.getFerrets():
                print(ferretPos)

        if (self.myTicks % 80 == 0):
            print('getting the position of all health packs')
            for healthPack in self.getHealthPacks():
                print(healthPack)

        if (self.myTicks % 160 == 0):
            print('getting the position of the exit tile')
            print(self.getExit())

        x = randint(-1, 1)
        y = randint(-1, 1)
        print("I am doing something boring..")
        print(x,y)
        if (self.canMove(x,y)):
            print("Moving..")
            self.move(x,y)
        else:
            print("Not moving..")

        return
