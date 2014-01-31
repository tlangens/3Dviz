'''
Created on Mar 15, 2013

@author: tuba
'''

import math
from PyQt4 import QtGui, QtCore

        
class Direction(object):
    North = 1
    East = 2
    South = 3
    West = 4


class Wall(object):
    
    def __init__(self, coordinates1, coordinates2):
        self.coords1 = coordinates1
        self.coords2 = coordinates2
        
    def getFirstCoords(self):
        return self.coords1
    
    def getSecondCoords(self):
        return self.coords2
    
    def drawWall(self, painter, eye):
        flen = eye.getFocalLength()
        direction = eye.getDirection()
        
        distance = (math.sqrt((self.coords1[0] - eye.getX())**2 + (self.coords1[1] - eye.getY())**2) + 
                    math.sqrt((self.coords2[0] - eye.getX())**2 + (self.coords2[1] - eye.getY())**2)) / 2
        distance = 170 - 7*distance
        if distance < 22:                   # draw distance now until darker than background color
            return
        
        # Transform coordinates so that they can be calculated with in the same way.
        if direction == Direction.North:
            c10 = self.coords1[0]
            c11 = self.coords1[1]
            c20 = self.coords2[0]
            c21 = self.coords2[1]
            eyex = eye.getX()
            eyey = eye.getY()
        elif direction == Direction.East:
            c10 = -self.coords1[1]
            c11 = self.coords1[0]
            c20 = -self.coords2[1]
            c21 = self.coords2[0]
            eyex = -eye.getY()
            eyey = eye.getX()
        elif direction == Direction.South:
            c10 = -self.coords1[0]
            c11 = -self.coords1[1]
            c20 = -self.coords2[0]
            c21 = -self.coords2[1]
            eyex = -eye.getX()
            eyey = -eye.getY()
        elif direction == Direction.West:
            c10 = self.coords1[1]
            c11 = -self.coords1[0]
            c20 = self.coords2[1]
            c21 = -self.coords2[0]
            eyex = eye.getY()
            eyey = -eye.getX()
        
        # Check if walls are in front of- or behind eye. If behind, return.
        AH1x = c10 - eyex
        AH1z = c11 - eyey
        if AH1z > 0:
            BH1x = AH1x * (flen/AH1z)
        else:
            return
        
        BV1 = flen * (flen/(AH1z))
        
        AH2x = c20 - eyex
        AH2z = c21 - eyey
        if AH2z > 0:
            BH2x = AH2x * (flen/AH2z)
        else:
            return
        
        BV2 = flen * (flen/AH2z)
        
        # Convert coordinates to screen coordinates.
        Hratio = 1024.0/(2*flen)        # view-width is twice the focal length, 1024 is frame width
        Vratio = 700.0/(2*flen)         # view height also twice the focal length. These may be changed
        x1 = (BH1x * Hratio) + 512      # and affects the percieved width and heights of the walls.
        x2 = (BH2x * Hratio) + 512
        y1a = (-BV1 * Vratio) + 350
        y1b = (BV1 * Vratio) + 350
        y2a = (BV2 * Vratio) + 350
        y2b = (-BV2 * Vratio) + 350
        
        # Create polygon object and draw.
        wall = QtGui.QPolygon([QtCore.QPoint(x1, y1a), QtCore.QPoint(x1, y1b),
                               QtCore.QPoint(x2, y2a), QtCore.QPoint(x2, y2b)])
        
        color = QtGui.QColor(distance, distance, distance)
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawPolygon(wall)
