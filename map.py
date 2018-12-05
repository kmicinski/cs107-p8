# CS 107, Fall 2018
# Map Class for HaverQuest

class Map:
    def __init__(self, tileFactory, filename, width, height):
        """A Map object represents a matrix of tiles that forms the
        "background layer" for a given level. Maps can be input via
        the `loadMap` method below, which parses a map in a specified
        format.
        """
        self.id = id
        self.tileFactory = tileFactory
        self.filename = filename
        self.tiles = [["\0" for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height

    def loadMap(self):
        """Parse the map file (self.filename) and load the map into memory.

        Maps begin with an n-by-k matrix of characters. See the
        README.md for the full specification of the map file format.

        """
        try:
            file = open(self.filename)
            lineno = 0 # Store lineno for error reporting to a user
            y = 0      # y is different than lineno as some lines may be comments
            for line in file:
                lineno = lineno + 1
                # If this line starts with #, it is a comment, skip the rest of this iteration
                # Interpret this as a command
                if (y >= self.height):
                    parts = line.split()
                    
                else:
                    if (len(line) > 0 and line[0] == '#'): continue
                    if (len(line) < self.width):
                        print("Line {} of map is malformed".format(lineno))
                        exit(1)
                    for x in range(self.width):
                        self.tiles[x][y] = self.tileFactory.fromChar(line[x], x, y)
                y += 1
            file.close()
        except:
            print("Could not load map file {}".format(self.filename))
            exit(1)

    def loadToBoard(self,board):
        """
        Load all of the tiles and put them on the board
        :type board: Board the board on which to add this tile
        """
        for x in range(self.width):
            for y in range(self.height):
                board.addTile(self.tiles[x][y])
        return
