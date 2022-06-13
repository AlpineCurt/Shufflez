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
    Each player window is a child class of this main window.
    '''
    
    def __init__(self):
        super().__init__()
        
        self.resize(1500, 800)
        self.move(100, 100)
        self.setWindowTitle("Shufflez")
        
        self._createMenuBar()
        self._createStatusBar()
        
        mdiArea = QtWidgets.QMdiArea()
        mdiArea.addSubWindow(ShufflezWidgets.RangeWidgetMain())
        mdiArea.addSubWindow(ShufflezWidgets.HandReplayer())

        self.setCentralWidget(mdiArea)
    
    def _createMenuBar(self):
        menuBar = QtWidgets.QMenuBar(self)
        self.setMenuBar(menuBar)
        
        fileMenu = QtWidgets.QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        
        menuBar.addMenu("&Edit")
        
    def _createStatusBar(self):
        self.statusBar = self.statusBar()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())