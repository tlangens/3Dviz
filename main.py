#!/usr/bin/env python
'''
Created on Mar 11, 2013

@author: Thomas Langenskiold
'''
import sys
from PyQt4 import QtGui, QtCore
from world import World

class MainWindow(QtGui.QMainWindow):
    def __init__(self):    
        super(MainWindow, self).__init__()
        self.initUI()
    
    def initUI(self):
        # Initialize main window.
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle('3D-Visualisation')
        
        self.frame = ViewFrame(self)
        self.setCentralWidget(self.frame)
        
        openFile = QtGui.QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        
        self.show()

        
    def showDialog(self):
        # Open file
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.frame.loadFile(fname)


    def center(self):
        #Center window on screen
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        
    def keyPressEvent(self, e):
        # Handle key pressing events
        self.frame.keyPress(e)
        
        
class ViewFrame(QtGui.QFrame):
    
    def __init__(self, parent):
        # Create the main frame of the window
        QtGui.QFrame.__init__(self, parent)
       
        self.setFrameShape(QtGui.QFrame.WinPanel)
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setStyleSheet("QWidget { background-color: #222222 }")
        self.world = World()
    
    def keyPress(self, e):
        # Handle key pressing
        # Move eye
        key = e.key()
        if key == QtCore.Qt.Key_Up \
        or key == QtCore.Qt.Key_Down \
        or key == QtCore.Qt.Key_Left \
        or key == QtCore.Qt.Key_Right \
        or key == QtCore.Qt.Key_Q \
        or key == QtCore.Qt.Key_W \
        or key == QtCore.Qt.Key_E \
        or key == QtCore.Qt.Key_A \
        or key == QtCore.Qt.Key_S \
        or key == QtCore.Qt.Key_D:
            self.world.moveEye(key)
        self.update()
        
        # Add or remove walls
        if key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Backspace:
            self.world.editWall(key)
            
        
    def paintEvent(self, event):
        # Handle the paint event. All walls are drawn in the Wall class.
        painter = QtGui.QPainter(self)
        self.world.drawWalls(painter)
        painter.end()
        
    def loadFile(self, fname):
        # Passing on the file to the world class, and updating the frame when world is done loading.
        self.world.loadWalls(fname)
        self.update()


def main():
    # Main loop
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())    

if __name__ == '__main__':
    main()    
