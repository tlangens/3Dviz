'''
Created on Mar 15, 2013

@author: tuba
'''

from PyQt4 import QtCore

        
class Direction(object):
    North = 1
    East = 2
    South = 3
    West = 4



class Eye():
    
    def __init__(self, x, y, direction):
        self.xcoor = x
        self.ycoor = y
        self.direction = direction
        self.flen = 2.0                     # Focal length. This is the distance from the eye to the picture. 
                                            # Can be set to anything, and affects the percieved width of the walls.
        
    def setCoords(self, coords, direction):
        self.xcoor = coords[0]
        self.ycoor = coords[1]
        self.direction = direction
        
    def getX(self):
        return self.xcoor
    
    def getY(self):
        return self.ycoor
    
    def getDirection(self):
        return self.direction
    
    def getFocalLength(self):
        return self.flen
    
    def getPoint(self):
        # Get the point that is being looked at, which is now set to 2 squares in front of the eye.
        direction = self.direction
        ycoor = self.ycoor
        xcoor = self.xcoor

        if direction == Direction.North:
            ycoor += 2
        elif direction == Direction.East:
            xcoor += 2
        elif direction == Direction.South:
            ycoor -= 2
        elif direction == Direction.West:
            xcoor -= 2
            
        return [xcoor, ycoor, direction]
    
    def move(self, key):
        # Returns the point to which the eye is about to move. 
        direction = self.direction
        ycoor = self.ycoor
        xcoor = self.xcoor
        
        if key == QtCore.Qt.Key_Left or key == QtCore.Qt.Key_Q:
            if direction == Direction.North:
                direction = Direction.West
            elif direction == Direction.East:
                direction = Direction.North
            elif direction == Direction.South:
                direction = Direction.East
            elif direction == Direction.West:
                direction = Direction.South
                
        elif key == QtCore.Qt.Key_Right or key == QtCore.Qt.Key_E:
            if direction == Direction.North:
                direction = Direction.East
            elif direction == Direction.East:
                direction = Direction.South
            elif direction == Direction.South:
                direction = Direction.West
            elif direction == Direction.West:
                direction = Direction.North
                
        elif key == QtCore.Qt.Key_Up or key == QtCore.Qt.Key_W:
            if direction == Direction.North:
                ycoor+=1
            elif direction == Direction.East:
                xcoor+=1
            elif direction == Direction.South:
                ycoor-=1
            elif direction == Direction.West:
                xcoor-=1
            
        elif key == QtCore.Qt.Key_Down or key == QtCore.Qt.Key_S:
            if direction == Direction.North:
                ycoor-=1
            elif direction == Direction.East:
                xcoor-=1
            elif direction == Direction.South:
                ycoor+=1
            elif direction == Direction.West:
                xcoor+=1
                
        elif key == QtCore.Qt.Key_A:
            if direction == Direction.East:
                ycoor+=1
            elif direction == Direction.South:
                xcoor+=1
            elif direction == Direction.West:
                ycoor-=1
            elif direction == Direction.North:
                xcoor-=1
            
        elif key == QtCore.Qt.Key_D:
            if direction == Direction.East:
                ycoor-=1
            elif direction == Direction.South:
                xcoor-=1
            elif direction == Direction.West:
                ycoor+=1
            elif direction == Direction.North:
                xcoor+=1
                
        return [xcoor, ycoor, direction]
