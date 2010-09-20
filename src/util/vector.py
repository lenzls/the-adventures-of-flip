'''
Created on 13.09.2010

@author: simon
'''

class Vector():

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    # + operator
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    # - operator
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    # * operator (used for resizing the vector)
    def __mul__(self, factor):
        return Vector(self.x * factor, self.y * factor)

    # / operator (used for resizing the vector)
    def __div__(self, factor):
        return Vector(self.x / factor, self.y / factor)

    # += operator
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    # -= operator
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise Exception('Invalid Key!') 

    def getTuple(self):
        return (self.x, self.y)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
