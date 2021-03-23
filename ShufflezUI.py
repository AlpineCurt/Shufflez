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
        self.setWindowTitle('Shufflez Poker')
        
        self.value = set()
        self.bluff = set()
        self.call = set()
        self.noAction = set()
        self.lockedCombos = set()
        self.startingCombos = set()
        self.board = []
        self.lockStatus = False
        self.preflop = True  # Preflop condiditon determines labeling, and RangeStatsDisplay mode
        self.statsRowSignalsConnected = False
        self.selectedAction = ''
        self.lastUpdateFrom = ''
        
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
        
        self.comboWindows = []
        
        '''Connect Signals and Slots'''
        self.rangeDisplay.updateSignal.connect(self.receiveUpdate)
        self.actionBuckets.updateSignal.connect(self.receiveUpdate)
        self.boardDisplay.updateSignal.connect(self.receiveUpdate)
        self.rangeStatsDisplay.rangeStatsMain.updateSignal.connect(self.receiveUpdate)
        self.rangeDisplay.rangeMatrix.requestComboWindowSignal.connect(self.createComboWindow)  
    
    def updatePackOverwrite(self, updatePack):
        '''self attributes will be replaced by updatePack'''
        
        self.lastUpdateFrom = updatePack.origin
        
        self.value = updatePack.value.copy()
        self.bluff = updatePack.bluff.copy()
        self.call = updatePack.call.copy()
        self.noAction = updatePack.noAction.copy()
        self.startingCombos = updatePack.startingCombos.copy()
        self.lockedCombos = updatePack.lockedCombos.copy()
        self.lockStatus = updatePack.lockStatus
        self.preflop = updatePack.preflopStatus
        self.selectedAction = updatePack.selectedAction
    
    def updatePackMerge(self, updatePack):
        '''self attributes will be modified by updatePack
        Primarily for updates from ComboWindows'''
        
        self.lastUpdateFrom = updatePack.origin
        
        for combo in updatePack.value:
            self.value.add(combo)
            self.bluff.discard(combo)
            self.call.discard(combo)
            self.noAction.discard(combo)
        for combo in updatePack.bluff:
            self.value.discard(combo)
            self.bluff.add(combo)
            self.call.discard(combo)
            self.noAction.discard(combo)
        for combo in updatePack.call:
            self.value.discard(combo)
            self.bluff.discard(combo)
            self.call.add(combo)
            self.noAction.discard(combo)
        for combo in updatePack.noAction:
            self.value.discard(combo)
            self.bluff.discard(combo)
            self.call.discard(combo)
            self.noAction.add(combo)   
        for combo in updatePack.startingCombos:
            self.lockedCombos.discard(combo)
        for combo in updatePack.lockedCombos:
            self.lockedCombos.add(combo)
    
    def receiveUpdate(self, updatePack):
        '''Handles update signals from child Widgets'''
        
        '''Test updatePack for validity'''
        if not updatePack.test_pass:
            print('Error in updatePack')
            return
        
        if len(updatePack.startingCombos) == 0 or updatePack.startingCombos != self.startingCombos:
            '''If we're recalculating RangeStats, we'll need to reconnect the signals of each StatsRow'''
            self.statsRowSignalsConnected = False
        
        if updatePack.origin == 'ComboWindow':
            self.updatePackMerge(updatePack)
        elif updatePack.origin == 'BoardDisplay':
            self.board = updatePack.board
            self.lastUpdateFrom = updatePack.origin
        elif updatePack.origin == 'ActionBuckets':
            self.selectedAction = updatePack.selectedAction
            self.lastUpdateFrom = updatePack.origin
        else:
            self.updatePackOverwrite(updatePack)
        
        self.update()
    
    def connectStatsRowSignals(self):
        '''After RangeStatsMain calculates made hands, each StatsRow requestComboWindow
        signal needs to be connected to createComboWindow'''
        
        if self.statsRowSignalsConnected:
            return
        
        for row in self.rangeStatsDisplay.rangeStatsMain.made_hands.allRows:
            row.requestComboWindowSignal.connect(self.createComboWindow)
            for row2 in row.secondary_StatsRows:
                row2.requestComboWindowSignal.connect(self.createComboWindow)
        for row in self.rangeStatsDisplay.rangeStatsMain.drawing_hands.allRows:
            row.requestComboWindowSignal.connect(self.createComboWindow)
            for row2 in row.secondary_StatsRows:
                row2.requestComboWindowSignal.connect(self.createComboWindow)
        self.statsRowSignalsConnected = True
    
    def createComboWindow(self, updatePack):
        '''Slot when RangeMatrix or a StatsRow emits requestComboWindow signal'''
        
        comboWindow = ShufflezWidgets.ComboWindow(self.position, updatePack)
        
        if comboWindow in self.comboWindows:
            for comWin in self.comboWindows:
                if comboWindow == comWin:
                    comWin.show()
        else:
            self.comboWindows.append(comboWindow)
            self.comboWindows[-1].closeSignal.connect(self.deleteComboWindow)
            self.comboWindows[-1].updateSignal.connect(self.receiveUpdate)
            
    def deleteComboWindow(self, origin):
        '''Slot when a ComboWindow emits a closeSignal'''
        
        for comboWindow in self.comboWindows:
            if comboWindow == origin:
                self.comboWindows.remove(comboWindow)
                del comboWindow
                break
    
    def update(self):
        
        updatePack = ShufflezWidgets.UpdatePack()
        updatePack.origin = 'PlayerWindow'
        updatePack.value = self.value
        updatePack.bluff = self.bluff
        updatePack.call = self.call
        updatePack.noAction = self.noAction
        updatePack.startingCombos = self.startingCombos
        updatePack.lockedCombos = self.lockedCombos
        updatePack.lockStatus = self.lockStatus
        updatePack.preflopStatus = self.preflop
        updatePack.selectedAction = self.selectedAction
        updatePack.board = self.board
        
        '''Specifying which Widgets receive an update to avoid updating redundancy'''
        if self.lastUpdateFrom == 'ComboWindow':
            self.rangeDisplay.receiveUpdate(updatePack)
            self.rangeStatsDisplay.rangeStatsMain.receiveUpdate(updatePack)
            self.actionBuckets.receiveUpdate(updatePack)        
        elif self.lastUpdateFrom == 'RangeDisplay':
            self.actionBuckets.receiveUpdate(updatePack)
            self.rangeStatsDisplay.rangeStatsMain.receiveUpdate(updatePack)
            self.connectStatsRowSignals()
        elif self.lastUpdateFrom == 'BoardDisplay':
            self.rangeDisplay.receiveUpdate(updatePack)
            self.actionBuckets.receiveUpdate(updatePack)
            self.rangeStatsDisplay.rangeStatsMain.receiveUpdate(updatePack)
            self.connectStatsRowSignals()   
        elif self.lastUpdateFrom == 'RangeStatsMain':
            self.rangeDisplay.receiveUpdate(updatePack)
            self.actionBuckets.receiveUpdate(updatePack)   
            self.connectStatsRowSignals()
        elif self.lastUpdateFrom == 'ActionBuckets':
            self.rangeDisplay.receiveUpdate(updatePack)
        else:
            '''GameHistory Update'''
            self.actionBuckets.receiveUpdate(updatePack)
            self.rangeDisplay.receiveUpdate(updatePack)
            self.rangeStatsDisplay.rangeStatsMain.receiveUpdate(updatePack)
            self.connectStatsRowSignals()
            
        for window in self.comboWindows:
            window.receiveComboActions(updatePack)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setWindowTitle('Shufflez')
    ui.show()
    sys.exit(app.exec_())