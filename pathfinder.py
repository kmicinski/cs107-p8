from dllist import *

# A path finder object isolates the logic to perform a path-finding
# problem on:
# 
#   - An underlying `board` object.
# 
#   - A `player` object, which holds the player's current position and
#   other relevant information about the player.
class PathFinder:
    def __init__(self, board, player):
        # The underlying game board on which tiles live
        self.board   = board
        
        # The underlying player object
        self.player  = player

        # The starting coordinates
        self.startX  = player.getX()
        self.startY  = player.getY()
        
        # The width / height of the board
        self.width   = self.board.width
        self.height  = self.board.height

        # A two-dimensional array to store whether or not the tile has
        # been visited.
        self.visited = [[False for x in range(board.height)]
                        for y in range(board.width)]

        # XXX
        self.winning = False

    # Check whether `path` is a valid path
    def checkValidPath(self,path):
        if (not self.canMoveTo(path[0][0], path[0][1])):
            return False
        cur = [path[0][0], path[0][1]]
        rest = path[1:]
        for move in rest:
            cur[0] = cur[0] + move[0]
            cur[1] = cur[1] + move[1]
            if (not self.canMoveTo(cur[0],cur[1])):
                return False
        return True

    # Check whether or not there is a wall (or other solid object) at
    # the coordinates (x,y)
    def wallAt(self,x,y):
        return self.board.higherPriorityObjectAt(self.player,x,y)
    
    # Check whether or not we can move to (x,y) I.e., is there a wall
    # there, or is it out of bounds?
    def canMoveTo(self,tx,ty):
        # Check to ensure we can move there
        if (tx >= 0                     # x must be in [0,width-1]
            and tx < self.width
            and ty >= 0                 # y must be in [0,height-1]
            and ty < self.height):
            # Not a higher-priority object at that point (i.e., a wall)
            if (not self.wallAt(tx,ty)):
                return True
            else:
                return False
        else:
            # Either outside of the boundaries of the board or a wall
            # is there
            return False
        
    def shouldGo(self,x,y):
        return self.canMoveTo(x,y) and self.visited[x][y] == False
        
    def go(self,x,y,lst):
        nxt = [(x,y)] + lst
        self.visited[x][y] = nxt
        if x == self.to[0] and y == self.to[1]:
            self.winning = nxt
        return (x,y)

    def canSolve(self, toCoordinate):
        return (self.findPath(toCoordinate) != False)

    def findPath(self, toCoordinate):
        path = self.solve(toCoordinate)
        if (path == False):
            return False
        path.reverse()
        ret = [(self.startX,self.startY)]
        if (path == False):
            return False
        last = None
        for chunk in path:
            if (last == None):
                last = chunk
            else:
                n = ((chunk[0]-last[0]),
                     (chunk[1]-last[1]))
                last = chunk
                ret.append(n)
        return ret

    def solve(self,toCoordinate):
        self.to = toCoordinate
        queue = [(self.startX,self.startY)]
        self.visited[self.startX][self.startY] = [(self.startX, self.startY)]
        while (len(queue) > 0):
            c = queue[0]
            queue = queue[1:]
            lst = self.visited[c[0]][c[1]]
            mostRecent = lst[0]
            x = mostRecent[0]
            y = mostRecent[1]
            if (self.shouldGo(x+1,y)):
                queue.append(self.go(x+1,y,lst))
            if (self.shouldGo(x-1,y)):
                queue.append(self.go(x-1,y,lst))
            if (self.shouldGo(x,y+1)):
                queue.append(self.go(x,y+1,lst))
            if (self.shouldGo(x,y-1)):
                queue.append(self.go(x,y-1,lst))
            if (self.winning != False):
                break
        return self.winning
