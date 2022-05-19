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
        
        rangeWidgetMain_button = QtWidgets.QPushButton('RangeWidgetMain')
        rangeWidgetMain_button.clicked.connect(self.onRangeWidgetMainButtonClick)
        layout.addWidget(rangeWidgetMain_button, 0, 1)
        
        handReplayer_button = QtWidgets.QPushButton('HandReplayer')
        handReplayer_button.clicked.connect(self.onHandReplayerButtonClick)
        layout.addWidget(handReplayer_button, 1, 1)
        
        playerSetUp_button = QtWidgets.QPushButton('PlayerSetUp')
        playerSetUp_button.clicked.connect(self.onPlayerSetUpButtonClick)
        layout.addWidget(playerSetUp_button, 2, 1)
        
        self.setLayout(layout)
        
    def onRangeWidgetMainButtonClick(self):
        self.testRangeWidgetMain = ShufflezWidgets.RangeWidgetMain('UTG')
        self.testRangeWidgetMain.show()
    
    def onHandReplayerButtonClick(self):
        self.testHandReplayer = ShufflezWidgets.HandReplayer()
        self.testHandReplayer.show()
    
    def onPlayerSetUpButtonClick(self):
        self.testPlayerSetUp = ShufflezWidgets.PlayerSetUp('BTN')
        self.testPlayerSetUp.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setWindowTitle('Shufflez')
    ui.show()
    sys.exit(app.exec_())