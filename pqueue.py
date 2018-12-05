# CS 107, Fall 2018
# Map Class for HaverQuest

class PriorityQueue:
    """
    An implementation of a priority queue
    """
    def __init__(self):
        self.lst = []

    # Number of items in the queue
    def length(self): return len(self.lst)

    # Clear the queue
    def clear(self): self.lst.clear()

    # Add an element to the priority queue
    def add(self,element,priority):
        i = 0
        while (i < len(self.lst) and self.lst[i][0] > priority):
            i += 1
        self.lst = self.lst[0:i] + [(priority,element)] + self.lst[i:]

    # Remove an element from the queue
    def remove(self,element):
        i = 0
        while (i < len(self.lst) and self.lst[i][1] != element):
            i += 1
        self.lst = self.lst[0:i] + self.lst[i+1:]

    def __iter__(self):
        return iter(self.lst)
    
