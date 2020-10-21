'''
v4
'''

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
#from math import ceil
import ShufflezWidgets

class Ui_MainWindow(QtWidgets.QMainWindow):
    
    '''
    Main program window
    
    This will contain File, Edit, etc.
    Game logic and record goes here.
    Each player window is a child class of this main window.
    '''
    
    def __init__(self):
        super().__init__()
        
        self.layout = MainLayout()
        
        self.resize(200, 100)
        self.move(100, 100)

        self.setCentralWidget(self.layout)


class MainLayout(QtWidgets.QWidget):
    '''Layout of MainWindow.  Widgets for game history will go here.'''
    
    def __init__(self):
        super().__init__()
        
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(5)
        
        test_button = QtWidgets.QPushButton('Test Window')
        test_button.clicked.connect(self.onTestWindowClick)
        layout.addWidget(test_button, 0, 1)
        
        self.setLayout(layout)
        
    def onTestWindowClick(self):
        self.testPlayerWindow = PlayerWindow()
        self.testPlayerWindow.show()


class PlayerWindow(QtWidgets.QWidget):
    
    '''Single Player's range and stats display.
    Contains:  range matrix, stats display, action buttons,
    and board cards.'''
    
    def __init__(self):
        super().__init__()
        
        layout = QtWidgets.QGridLayout()
        
        '''Create ActionBuckets'''
        self.action_buckets = ShufflezWidgets.ActionBuckets()
        layout.addWidget(self.action_buckets, 0, 0, Qt.AlignTop)
        
        '''Create RangeDisplay'''
        self.rangeDisplay = ShufflezWidgets.RangeDisplay()
        layout.addWidget(self.rangeDisplay, 1, 0, Qt.AlignCenter)
        
        '''Create RangeStatsDisplay'''
        self.rangeStats = ShufflezWidgets.RangeStats()
        self.rangeStatsDisplay = ShufflezWidgets.RangeStatsDisplay()
        self.rangeStatsDisplay.setFixedSize(300, self.rangeDisplay.totalHeight)
        layout.addWidget(self.rangeStatsDisplay, 1, 1, Qt.AlignCenter)
        self.rangeStatsDisplay.setWidget(self.rangeStats)
        
        '''Create BoardDisplay'''
        self.boardDisplay = ShufflezWidgets.BoardDisplay()
        layout.addWidget(self.boardDisplay, 0, 1, Qt.AlignCenter)
        
        layout.setVerticalSpacing(0)
        self.setLayout(layout)       
        
        self.preflop = True  # Preflop condiditon determines labeling, and RangeStatsDisplay mode
        
        '''Connect Signals and Slots between Widgets'''
        self.action_buckets.actionSelected.connect(self.rangeDisplay.setAction)
        self.rangeDisplay.sendRangesToActionBuckets.connect(self.action_buckets.receiveRanges)
        self.boardDisplay.sendBoardCards.connect(self.rangeStats.receiveBoard)
        self.boardDisplay.sendBoardCards.connect(self.action_buckets.receiveBoard)
        self.rangeDisplay.sendRangesToRangeStats.connect(self.rangeStats.receiveCombos)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setWindowTitle('Shufflez')
    ui.show()
    sys.exit(app.exec_())