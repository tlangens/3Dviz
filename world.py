'''
Created on Mar 12, 2013

@author: tuba
'''
from PyQt4 import QtCore
from wall import Wall
from eye import Eye


class World():
    '''
    This class contains the eye, that is the point from where the world is seen,
    and the list of walls included in the world.
    '''
    
    def __init__(self):
        # Initialize Wall list and Eye
        self.walls = []
        self.eye = Eye(0, 0, Direction.North)
        

    def loadWalls(self, fname):
        # Manage loading of walls from file.
        f = open(fname, 'r')
        with f:
            self.walls = [] # Empty list from any existing walls.
            data = f.readline() # Read firs line, that should contain data for the eye. If this line does not exist, the file is not valid.
            eye = data.split(':')
            self.eye.setCoords([int(eye[0]), int(eye[1])], int(eye[2]))
            data = f.readline() # Read next line, walls should start here, if any exist.
            while data:
                # Add all wall to the wall list one by one until EOF is reached.
                wall = data.split(' ')
                coords1 = wall[0].split(':')
                coords2 = wall[1].split(':')
                self.addWall(Wall([int(coords1[0]), int(coords1[1])], [int(coords2[0]), int(coords2[1])]))
                data = f.readline()
        f.close()
        
        
    def sortWalls(self):
        # Sort walls by distance to eye for drawing.
        def keyfunc(wall):
            c1 = wall.getFirstCoords()
            c2 = wall.getSecondCoords()
            z1 = (c1[0] - self.eye.getX())**2 + (c1[1] - self.eye.getY())**2
            z2 = (c2[0] - self.eye.getX())**2 + (c2[1] - self.eye.getY())**2
            if z1 > z2:
                return z2
            else:
                return z1
        
        self.walls.sort(key=keyfunc, reverse=True)


    def drawWalls(self, painter):
        
        self.sortWalls()
        for wall in self.walls:
            wall.drawWall(painter, self.eye)
            
    def moveEye(self, key):
        # Move eye if move is allowed. Only necessary to check the eight closest walls for collision, 
        # which is easy because the list is already sorted by distance.
        newcoors = self.eye.move(key)
        i = 1
        for wall in reversed(self.walls):
            if wall.getFirstCoords() == [newcoors[0], newcoors[1]] or wall.getSecondCoords() == [newcoors[0], newcoors[1]]:
                return
            i += 1
            if i > 8:
                break
        self.eye.setCoords([newcoors[0], newcoors[1]], newcoors[2])
    
    
    def editWall(self, key):
        point = self.eye.getPoint()
        direction = point[2]
        coords2 = [point[0], point[1]]
        if direction == Direction.North:
            coords2[0] += 1
        elif direction == Direction.East:
            coords2[1] -= 1
        elif direction == Direction.South:
            coords2[0] -= 1
        elif direction == Direction.West:
            coords2[1] += 1
        
        for wall in self.walls:
            if wall.getFirstCoords() == [point[0], point[1]] or wall.getSecondCoords() == [point[0], point[1]]:
                if key == QtCore.Qt.Key_Backspace:
                    self.rmWall(wall)
                    return
                else:
                    if wall.getFirstCoords() == coords2 or wall.getSecondCoords() == coords2:
                        return

        self.addWall(Wall([point[0], point[1]], coords2))
    
    
    def addWall(self, wall):
        self.walls.append(wall)
    
    def rmWall(self, wall):
        self.walls.remove(wall)
        
        
        
class Direction(object):
    North = 1
    East = 2
    South = 3
    West = 4
