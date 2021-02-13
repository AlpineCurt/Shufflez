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
        self.actionBuckets = ShufflezWidgets.ActionBuckets()
        layout.addWidget(self.actionBuckets, 0, 0, Qt.AlignTop)
        
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
        
        '''Connect Signals and Slots'''
        self.rangeDisplay.updateSignal.connect(self.receiveUpdate)
        self.actionBuckets.updateSignal.connect(self.receiveUpdate)
        self.boardDisplay.updateSignal.connect(self.receiveUpdate)
        self.rangeStatsDisplay.rangeStatsMain.updateSignal.connect(self.receiveUpdate)
    
    def receiveUpdate(self, updatePack):
        '''Handles update signals from child Widgets'''
        
        if updatePack.origin == 'RangeDisplay':
            self.actionBuckets.receiveUpdate(updatePack)
            self.rangeStatsDisplay.rangeStatsMain.receiveUpdate(updatePack)
        elif updatePack.origin == 'ActionBuckets':
            self.rangeDisplay.receiveUpdate(updatePack)
        elif updatePack.origin == 'BoardDisplay':
            self.rangeDisplay.receiveUpdate(updatePack)
            self.actionBuckets.receiveUpdate(updatePack)
            self.rangeStatsDisplay.rangeStatsMain.receiveUpdate(updatePack)
        elif updatePack.origin == 'RangeStatsMain':
            self.rangeDisplay.receiveUpdate(updatePack)
            self.actionBuckets.receiveUpdate(updatePack)
            
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setWindowTitle('Shufflez')
    ui.show()
    sys.exit(app.exec_())