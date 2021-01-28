'''
Main Program to run application.
'''

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
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
        self.testPlayerWindow = PlayerWindow('UTG')
        self.testPlayerWindow.show()


class PlayerWindow(QtWidgets.QWidget):
    
    '''Single Player's range and stats display.
    Contains:  range matrix, stats display, action buttons,
    and board cards.'''
    
    def __init__(self, position=None):
        super().__init__()
        
        layout = QtWidgets.QGridLayout()
        
        self.position = position
        
        '''Create ActionBuckets'''
        self.action_buckets = ShufflezWidgets.ActionBuckets()
        layout.addWidget(self.action_buckets, 0, 0, Qt.AlignTop)
        
        '''Create RangeDisplay'''
        self.rangeDisplay = ShufflezWidgets.RangeDisplay(self.position)
        layout.addWidget(self.rangeDisplay, 1, 0, Qt.AlignCenter)
        
        '''Create RangeStatsDisplay'''
        self.rangeStatsDisplay = ShufflezWidgets.RangeStatsDisplay(self.position)
        self.rangeStatsDisplay.setMinimumSize(335, self.rangeDisplay.totalHeight)
        self.rangeStatsDisplay.scrollArea.setFixedSize(330, self.rangeDisplay.totalHeight - 25)
        layout.addWidget(self.rangeStatsDisplay, 1, 1, Qt.AlignTop)
        
        '''Create BoardDisplay'''
        self.boardDisplay = ShufflezWidgets.BoardDisplay()
        layout.addWidget(self.boardDisplay, 0, 1, Qt.AlignCenter)
        
        layout.setVerticalSpacing(0)
        self.setLayout(layout)
        
        self.preflop = True  # Preflop condiditon determines labeling, and RangeStatsDisplay mode
        
        '''Connect Signals and Slots between Widgets'''
        self.action_buckets.actionSelected.connect(self.rangeDisplay.setAction)
        self.rangeDisplay.sendRangesToActionBuckets.connect(self.action_buckets.receiveRanges)
        self.boardDisplay.sendBoardCards.connect(self.rangeStatsDisplay.rangeStatsMain.receiveBoard)
        self.boardDisplay.sendBoardCards.connect(self.action_buckets.receiveBoard)
        self.rangeDisplay.sendRangesToRangeStats.connect(self.rangeStatsDisplay.rangeStatsMain.receiveCombos)
        self.rangeStatsDisplay.rangeStatsMain.sendComboActionsToRangeDisplay.connect(self.rangeDisplay.receiveActionList)
        self.rangeStatsDisplay.rangeStatsMain.lockRangeMatrix.connect(self.rangeDisplay.receiveLockStatus)
        self.rangeStatsDisplay.rangeStatsMain.sendLockedToRangeDisplay.connect(self.rangeDisplay.receiveLockedCombos)
        self.boardDisplay.sendPreflopStatus.connect(self.rangeDisplay.receivePreflopStatus)
        self.rangeDisplay.sendLockedCombosToRangeStatsMain.connect(self.rangeStatsDisplay.rangeStatsMain.receiveLockedCombosFromRangeDisplay)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setWindowTitle('Shufflez')
    ui.show()
    sys.exit(app.exec_())