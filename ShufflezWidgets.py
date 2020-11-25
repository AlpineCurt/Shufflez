'''
Tools and UI Widgets for Shufflez Program.

v3 9/25/2020
Restructuring RangeMatrix as a QGridLayout of ComboRect Objects

v4 10/2/2020
Restructuring RangeMatrix as a custom grid of ComboRect Objects
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from math import ceil
import ShufflezCalc as ShCalc
from random import randint

"""RANGE MATRIX and related classes"""

class RangeDisplay(QtWidgets.QWidget):
    '''
    Contains RangeMatrix, RangeText, and clear button.
    '''
    
    sendRangesToActionBuckets = QtCore.pyqtSignal(list)  # Mouse over signal
    sendRangesToRangeStats = QtCore.pyqtSignal(list)   # Mouse release signal
    
    def __init__(self):
        super().__init__()
        
        layout = QtWidgets.QVBoxLayout()
        
        spacing = 5
        
        self.rangeMatrix = RangeMatrix()
        layout.addWidget(self.rangeMatrix, Qt.AlignTop)
        
        self.rangeText = RangeText()
        self.rangeText.setFixedSize(self.rangeMatrix.matrixWidth, self.rangeText.boxHeight)
        layout.addWidget(self.rangeText, Qt.AlignCenter)
        
        self.clearButton = QtWidgets.QPushButton('Clear')
        self.clearButton.setFixedWidth(55)
        self.clearButton.setFixedHeight(25)
        self.clearButton.clicked.connect(self.onClearClick)
        layout.addWidget(self.clearButton)
        
        layout.setSpacing(spacing)
        
        self.totalHeight = self.rangeMatrix.matrixHeight + spacing + self.rangeText.height() + self.clearButton.height()
        
        sizepolicy = QtWidgets.QSizePolicy()
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHorizontalStretch(0)
        self.setSizePolicy(sizepolicy)
        
        self.setLayout(layout)
        
        '''Attributes'''
        self.selecting = False
        
        self.action = ''
        
        self.value = []
        self.bluff = []
        self.call = []
        self.noAction = []
        self.valueLock = []
        self.bluffLock = []
        self.callLock = []
        
        '''Connect Signals and Slots'''
        self.rangeMatrix.comboRectClicked.connect(self.setSelecting)
        self.rangeMatrix.mouseOver.connect(self.comboRectMouseMove)
        self.rangeText.enterPressed.connect(self.setRangeFromText)
    
    def receiveActionList(self, actionList):
        '''Slot to respond when RangeStatsMain sends a list of combos
        for each action (value, bluff, call).'''
        
        self.rangeMatrix.clearGrid()
        
        self.value = actionList[0]
        self.bluff = actionList[1]
        self.call = actionList[2]
        self.noAction = actionList[3]
        
        self.update()
    
    def setSelecting(self, comboRectName):
        
        for combo in self.rangeMatrix.matrix:
            if combo.name == comboRectName:
                if len(combo.value) == combo.totalCombos and self.action == 'value':
                    self.selecting = False
                elif len(combo.bluff) == combo.totalCombos and self.action == 'bluff':
                    self.selecting = False
                elif len(combo.call) == combo.totalCombos and self.action == 'call':
                    self.selecting = False
                elif len(combo.noAction) == combo.totalCombos and self.action == '':
                    self.selecting = False
                else:
                    self.selecting = True
                break
        self.rangeMatrix.selecting = self.selecting

    def setAction(self, action):
        self.action = action
        self.update()
        
    def comboRectMouseMove(self, comboList):
        '''
        Slot to repsond to mouseMoveEvent
        '''
        for combo in comboList:
            self.comboActionSort(combo)
        self.update()
        
    def comboActionSort(self, combo):
        '''
        Places or removes combo from correct action Set depending on
        if we're selecting or not and the current selected action.
        Used by comboRectMouseMove.
        '''
        
        if self.selecting:
            for com in self.value:
                if combo.text == com.text:
                    self.value.remove(com)
            for com in self.bluff:
                if combo.text == com.text:
                    self.bluff.remove(com)
            for com in self.call:
                if combo.text == com.text:
                    self.call.remove(com)
            for com in self.noAction:
                if combo.text == com.text:
                    self.noAction.remove(com)
                
            if self.action == 'value':   # Now place combo in correct Set
                self.value.append(combo)
            elif self.action == 'bluff':
                self.bluff.append(combo)
            elif self.action == 'call':
                self.call.append(combo)
            elif self.action == '':
                self.noAction.append(combo)
                
        elif not self.selecting:
            for com in self.value:
                if combo.text == com.text:
                    self.value.remove(com)
            for com in self.bluff:
                if combo.text == com.text:
                    self.bluff.remove(com)
            for com in self.call:
                if combo.text == com.text:
                    self.call.remove(com)
            for com in self.noAction:
                if combo.text == com.text:
                    self.noAction.remove(com)
    
    def onClearClick(self):
        '''Slot for Clear button clicked signal'''
        
        if self.action == 'value':
            self.value.clear()
        elif self.action == 'bluff':
            self.bluff.clear()
        elif self.action == 'call':
            self.call.clear()
        else:
            self.value.clear()
            self.bluff.clear()
            self.call.clear()
            self.noAction.clear()
            self.rangeMatrix.clearGrid()
        
        self.rangeText.clear()
        
        self.sendRangesToRangeStats.emit([self.value, self.bluff, self.call, self.noAction])
        
        self.update()
        
    def setRangeFromText(self, range_list):
        '''Slot to respond to Enter pressed on RangeText.'''
        
        for combo in range_list:
            '''Remove combo if it's already in an action Set'''
            for com in self.value:
                if combo.text == com.text:
                    self.value.remove(com)
                    break
            for com in self.bluff:
                if combo.text == com.text:
                    self.bluff.remove(com)
                    break
            for com in self.call:
                if combo.text == com.text:
                    self.call.remove(com)
            for com in self.noAction:
                if combo.text == com.text:
                    self.noAction.remove(com)
            
            '''Add the combo to the selected action Set'''
            if self.action == 'value':
                self.value.append(combo)
            elif self.action == 'bluff':
                self.bluff.append(combo)
            elif self.action == 'call':
                self.call.append(combo)
            else:
                self.noAction.append(combo)
        
        self.update()
        self.sendRangesToRangeStats.emit([self.value, self.bluff, self.call, self.noAction])
    
    def mouseReleaseEvent(self, e):
        self.selecting = False
        self.sendRangesToRangeStats.emit([self.value, self.bluff, self.call, self.noAction])
        super().mouseReleaseEvent(e)
    
    def update(self):
        
        '''Update RangeMatrix'''
        self.rangeMatrix.clearGrid()
        self.rangeMatrix.setValue(self.value)
        self.rangeMatrix.setBluff(self.bluff)
        self.rangeMatrix.setCall(self.call)
        self.rangeMatrix.setNoAction(self.noAction)
        self.rangeMatrix.update()
        
        '''Update ActionBuckets'''
        self.sendRangesToActionBuckets.emit([self.value, self.bluff, self.call, self.noAction])
        
        '''Update RangeText'''
        self.rangeText.clear()
        if self.action == 'value':
            self.rangeText.setText(self.rangeText.rangeListToString(self.value))
        elif self.action == 'bluff':
            self.rangeText.setText(self.rangeText.rangeListToString(self.bluff))
        elif self.action == 'call':
            self.rangeText.setText(self.rangeText.rangeListToString(self.call))
        else:
            allActionCombos = []
            allActionCombos.extend(self.value)
            allActionCombos.extend(self.bluff)
            allActionCombos.extend(self.call)
            allActionCombos.extend(self.noAction)
            self.rangeText.setText(self.rangeText.rangeListToString(allActionCombos))
        
        super().update()
    
    def paintEvent(self, e):
        '''To set breakpoint for checking current State.'''
        pass


class RangeMatrix(QtWidgets.QWidget):
    '''
    Widget that displays a 13x13 grid of hand combos and
    displays designated ranges in different colors.
    '''
    
    comboRectClicked = QtCore.pyqtSignal(str)
    mouseOver = QtCore.pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        
        boxLen = 30        # Length in pixels of each grid square
        self.boxLen = boxLen
        offset = [0, 0]   # Pixel width, length of border, if any
        
        self.matrixHeight = boxLen * 13 + offset[1] * 2
        self.matrixWidth = boxLen * 13 + offset[0] * 2
        
        '''Consruct Grid of ComboRects'''
        gridref = [['AA',   6], ['AKs',  4], ['AQs',  4], ['AJs',  4], ['ATs',  4], ['A9s',  4], ['A8s',  4], ['A7s',  4], ['A6s',  4], ['A5s',  4], ['A4s',  4], ['A3s',  4], ['A2s', 4], 
                   ['AKo', 12], ['KK',   6], ['KQs',  4], ['KJs',  4], ['KTs',  4], ['K9s',  4], ['K8s',  4], ['K7s',  4], ['K6s',  4], ['K5s',  4], ['K4s',  4], ['K3s',  4], ['K2s', 4],
                   ['AQo', 12], ['KQo', 12], ['QQ',   6], ['QJs',  4], ['QTs',  4], ['Q9s',  4], ['Q8s',  4], ['Q7s',  4], ['Q6s',  4], ['Q5s',  4], ['Q4s',  4], ['Q3s',  4], ['Q2s', 4],
                   ['AJo', 12], ['KJo', 12], ['QJo', 12], ['JJ',   6], ['JTs',  4], ['J9s',  4], ['J8s',  4], ['J7s',  4], ['J6s',  4], ['J5s',  4], ['J4s',  4], ['J3s',  4], ['J2s', 4],
                   ['ATo', 12], ['KTo', 12], ['QTo', 12], ['JTo', 12], ['TT',   6], ['T9s',  4], ['T8s',  4], ['T7s',  4], ['T6s',  4], ['T5s',  4], ['T4s',  4], ['T3s',  4], ['T2s', 4],
                   ['A9o', 12], ['K9o', 12], ['Q9o', 12], ['J9o', 12], ['T9o', 12], ['99',   6], ['98s',  4], ['97s',  4], ['96s',  4], ['95s',  4], ['94s',  4], ['93s',  4], ['92s', 4],
                   ['A8o', 12], ['K8o', 12], ['Q8o', 12], ['J8o', 12], ['T8o', 12], ['98o', 12], ['88',   6], ['87s',  4], ['86s',  4], ['85s',  4], ['84s',  4], ['83s',  4], ['82s', 4],
                   ['A7o', 12], ['K7o', 12], ['Q7o', 12], ['J7o', 12], ['T7o', 12], ['97o', 12], ['87o', 12], ['77',   6], ['76s',  4], ['75s',  4], ['74s',  4], ['73s',  4], ['72s', 4],
                   ['A6o', 12], ['K6o', 12], ['Q6o', 12], ['J6o', 12], ['T6o', 12], ['96o', 12], ['86o', 12], ['76o', 12], ['66',   6], ['65s',  4], ['64s',  4], ['63s',  4], ['62s', 4],
                   ['A5o', 12], ['K5o', 12], ['Q5o', 12], ['J5o', 12], ['T5o', 12], ['95o', 12], ['85o', 12], ['75o', 12], ['65o', 12], ['55',   6], ['54s',  4], ['53s',  4], ['52s', 4],
                   ['A4o', 12], ['K4o', 12], ['Q4o', 12], ['J4o', 12], ['T4o', 12], ['94o', 12], ['84o', 12], ['74o', 12], ['64o', 12], ['54o', 12], ['44',   6], ['43s',  4], ['42s', 4],
                   ['A3o', 12], ['K3o', 12], ['Q3o', 12], ['J3o', 12], ['T3o', 12], ['93o', 12], ['83o', 12], ['73o', 12], ['63o', 12], ['53o', 12], ['43o', 12], ['33'  , 6], ['32s', 4],
                   ['A2o', 12], ['K2o', 12], ['Q2o', 12], ['J2o', 12], ['T2o', 12], ['92o', 12], ['82o', 12], ['72o', 12], ['62o', 12], ['52o', 12], ['42o', 12], ['32o', 12],  ['22', 6]]
        
        self.matrix = self.buildGrid(boxLen, gridref, offset)
        
        '''RGB values for display colors.  Changable in Settings. '''
        self.grey_pen = [190, 190, 190]
        
        self.suited_blank = [250, 244, 185]
        self.suited_grey = [235, 235, 235]
        
        self.pocketPair_blank = [192, 233, 155]
        self.pocketPair_grey = [225, 225, 225]
        
        self.offsuit_blank = [216, 237, 255]
        self.offsuit_grey = [225, 225, 225]
        
        self.valueBrush = [255, 77, 77]
        self.bluffBrush = [255, 166, 166]
        self.callBrush = [103, 178, 45]
        self.noActionBrush = [250, 206, 60]
        
        '''Tracks if user is clicking and dragging to select comboRects'''
        self.selecting = False
        
        '''QtWidget Settings'''
        self.setMinimumSize(boxLen * 13 + 1 + offset[0] * 2, boxLen * 13 + 1 + offset[1] * 2)
        
    def buildGrid(self, boxLen, gridref, offset):
        '''
        Creates list of combo Rects that make up the 13 x 13 range matrix.
        Primarily used during __init__ to create Grid.
        If Signals and Slots need to be added to each ComboRect, it's done here.
        '''
        
        matrix = []
        
        row = 0
        col = 0
        
        for combo in gridref:
            rect = ComboRect(boxLen * col + offset[0],
                             boxLen * row + offset[1],
                             boxLen, boxLen, combo[1], combo[0])
            matrix.append(rect)
            col += 1
            if col % 13 == 0:
                row += 1
                col = 0
        
        return matrix
    
    def clearGrid(self):
        '''Clears each ComboRect's value, bluff, and call Sets.'''
        
        for combo in self.matrix:
            combo.value.clear()
            combo.bluff.clear()
            combo.call.clear()
            combo.valueLock.clear()
            combo.bluffLock.clear()
            combo.callLock.clear()            
            combo.noAction.clear()
        self.update()
    
    def setValue(self, valueCombos):
        '''
        Places each combo into the correct ComboRect's value Set.
        '''
        
        for combo in valueCombos:
            for rect in self.matrix:
                if combo.comboRect == rect.name:
                    rect.value.add(combo)
                    break
    
    def setBluff(self, bluffCombos):
        '''
        Places each combo into the correct ComboRect's bluff Set.
        '''
        
        for combo in bluffCombos:
            for rect in self.matrix:
                if combo.comboRect == rect.name:
                    rect.bluff.add(combo)
                    break
    
    def setCall(self, callCombos):
        '''
        Places each combo into the correct ComboRect's call Set.
        '''
        
        for combo in callCombos:
            for rect in self.matrix:
                if combo.comboRect == rect.name:
                    rect.call.add(combo)
                    break
    
    def setNoAction(self, noActionCombos):
        '''
        Places each combo into the correct ComboRect's noAction set.
        '''
        
        for combo in noActionCombos:
            for rect in self.matrix:
                if combo.comboRect == rect.name:
                    rect.noAction.add(combo)
                    break
    
    def mousePressEvent(self, e):
        
        '''Determine which ComboRect was clicked and emit the name of it'''
        for combo in self.matrix:
            if combo.rect.contains(e.x(), e.y()):
                self.comboRectClicked.emit(combo.name)
                self.mouseOver.emit(combo.comboList)
                break
    
    def mouseMoveEvent(self, e):
        
        '''Emit list of combos of moused over ComboRect'''
        for combo in self.matrix:
            if combo.rect.contains(e.x(), e.y()):
                self.mouseOver.emit(combo.comboList)
                break
    
    def paintEvent(self, e):
        
        painter = QtGui.QPainter(self)
        black_pen = QtGui.QPen(Qt.black, 1, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin)
        grey_pen = QtGui.QPen(Qt.gray, 1, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin)
        grey_pen.setColor(QtGui.QColor(self.grey_pen[0], self.grey_pen[1], self.grey_pen[2]))
        painter.setPen(black_pen)
        
        suited_blank = QtGui.QBrush()
        suited_blank.setColor(QtGui.QColor(self.suited_blank[0], self.suited_blank[1], self.suited_blank[2]))
        suited_blank.setStyle(Qt.SolidPattern)
        
        suited_grey = QtGui.QBrush()
        suited_grey.setColor(QtGui.QColor(self.suited_grey[0], self.suited_grey[1], self.suited_grey[2]))
        suited_grey.setStyle(Qt.SolidPattern)
        
        pocketPair_blank = QtGui.QBrush()
        pocketPair_blank.setColor(QtGui.QColor(self.pocketPair_blank[0], self.pocketPair_blank[1], self.pocketPair_blank[2]))
        pocketPair_blank.setStyle(Qt.SolidPattern)
        
        pocketPair_grey = QtGui.QBrush()
        pocketPair_grey.setColor(QtGui.QColor(self.pocketPair_grey[0], self.pocketPair_grey[1], self.pocketPair_grey[2]))
        pocketPair_grey.setStyle(Qt.SolidPattern)
        
        offsuit_blank = QtGui.QBrush()
        offsuit_blank.setColor(QtGui.QColor(self.offsuit_blank[0], self.offsuit_blank[1], self.offsuit_blank[2]))
        offsuit_blank.setStyle(Qt.SolidPattern)
        
        offsuit_grey = QtGui.QBrush()
        offsuit_grey.setColor(QtGui.QColor(self.offsuit_grey[0], self.offsuit_grey[1], self.offsuit_grey[2]))
        offsuit_grey.setStyle(Qt.SolidPattern)
        
        valueBrush = QtGui.QBrush()
        valueBrush.setColor(QtGui.QColor(self.valueBrush[0], self.valueBrush[1], self.valueBrush[2]))
        valueBrush.setStyle(Qt.SolidPattern)
        
        bluffBrush = QtGui.QBrush()
        bluffBrush.setColor(QtGui.QColor(self.bluffBrush[0], self.bluffBrush[1], self.bluffBrush[2]))
        bluffBrush.setStyle(Qt.SolidPattern)
        
        callBrush = QtGui.QBrush()
        callBrush.setColor(QtGui.QColor(self.callBrush[0], self.callBrush[1], self.callBrush[2]))
        callBrush.setStyle(Qt.SolidPattern)
        
        noActionBrush = QtGui.QBrush()
        noActionBrush.setColor(QtGui.QColor(self.noActionBrush[0], self.noActionBrush[1], self.noActionBrush[2]))
        noActionBrush.setStyle(Qt.SolidPattern)
        
        for combo in self.matrix:
            
            '''Fill with base color'''
            if combo.selectable:
                if combo.totalCombos == 4:
                    painter.fillRect(combo.rect, suited_blank)
                elif combo.totalCombos == 6:
                    painter.fillRect(combo.rect, pocketPair_blank)
                elif combo.totalCombos == 12:
                    painter.fillRect(combo.rect, offsuit_blank)
            else:
                if combo.totalCombos == 4:
                    painter.fillRect(combo.rect, suited_grey)
                elif combo.totalCombos == 6:
                    painter.fillRect(combo.rect, pocketPair_grey)
                elif combo.totalCombos == 12:
                    painter.fillRect(combo.rect, offsuit_grey)
                    
            '''Fill proportionally for combos in each action Set'''
            div = combo.boxLen / combo.totalCombos
            newX = combo.rect.x()
            newY = combo.rect.y() + combo.boxLen
            newWidth = combo.boxLen
            newLen = 0         
            
            for com in combo.noAction:
                newY -= div
                newLen += div
            painter.fillRect(ceil(newX), ceil(newY), newWidth, newLen, noActionBrush)
            newLen = 0
            
            for com in combo.call:
                newY -= div
                newLen += div
            painter.fillRect(ceil(newX), ceil(newY), newWidth, newLen, callBrush)
            newLen = 0
            
            for com in combo.bluff:
                newY -= div
                newLen += div
            painter.fillRect(ceil(newX), ceil(newY), newWidth, newLen, bluffBrush)
            newLen = 0
            
            for com in combo.value:
                newY -= div
                newLen += div
            painter.fillRect(ceil(newX), ceil(newY), newWidth, newLen, valueBrush)
            
            '''Outline each ComboRect'''
            if not combo.selectable:
                painter.setPen(grey_pen)
            painter.drawRect(combo.rect)
            
            '''Label each combo Rect'''
            painter.drawText(combo.rect, Qt.AlignCenter, combo.name)


class ComboRect(QtWidgets.QWidget):
    '''
    Widget each combo in a range matrix.
    Used by RangeMatrix.
    '''
    
    def __init__(self, x, y, width, height, totalCombos, name):
        super().__init__()
        
        '''Rect for drawing in paintEvent'''
        self.boxLen = height
        self.rect = QtCore.QRect(x, y, width, height)
        
        '''Attributes'''
        self.totalCombos = totalCombos
        self.name = name
        
        rank_value = ["2", "3", "4", "5", "6", "7", "8",
                      "9", "T", "J", "Q", "K", "A"]
        
        self.rankA = rank_value.index(name[0])
        self.rankB = rank_value.index(name[1])
        
        self.comboList = self.buildCombos()
        
        '''Can the user click it?  Is it part of the current selectable range?'''
        self.selectable = True
        
        '''Used to determine if we are selecing or deselecting when clicked.'''
        self.selected = False
        
        '''Set for each action for displaying correct amount of grid square.'''
        self.value = set()
        self.bluff = set()
        self.call = set()
        self.noAction = set()
        self.valueLock = set()
        self.bluffLock = set()
        self.callLock = set()        
    
    def buildCombos(self):
        '''
        Creates a list of Combo Objects that belong to the ComboRect.
        '''
        combos = []
        
        pp_combos = [[0, 2], [0, 1], [0, 3], [2, 1], [2, 3], [1, 3]]
        
        suited_combos = [[0, 0], [1, 1], [2, 2], [3, 3]]
        
        offsuit_combos = [[0, 2], [0, 1], [0, 3], [2, 1], [2, 3], [1, 3],
                          [2, 0], [1, 0], [1, 2], [3, 0], [3, 2], [3, 1]]
        
        if len(self.name) == 2:
            '''pocket pairs'''
            for i in pp_combos:
                combos.append(Combo([self.rankA, i[0]], [self.rankB, i[1]]))
        
        elif self.name[-1] == 's':
            '''suited combos'''
            for i in suited_combos:
                combos.append(Combo([self.rankA, i[0]], [self.rankB, i[1]]))
        
        elif self.name[-1] == 'o':
            for i in offsuit_combos:
                combos.append(Combo([self.rankA, i[0]], [self.rankB, i[1]]))
        
        return combos
    

class RangeText(QtWidgets.QTextEdit):
    '''Basic text box for range as a string input/output. Needed to override keypress event.'''
    
    enterPressed = QtCore.pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        
        sizepolicy = QtWidgets.QSizePolicy()
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHorizontalStretch(0)
        self.setSizePolicy(sizepolicy)
        
        self.boxHeight = 50
        
        self.rank_value = ["2", "3", "4", "5", "6", "7", "8",
                      "9", "T", "J", "Q", "K", "A"]
        self.suit_value = ['h', 'd', 'c', 's']
        
        self.text = ''
    
    def pocket_pair_convert(self, pp_range, combo_list):
        '''Appends to combo_list a Combo object for every combo in
        a pocket pair range.
        Used by rangeToList'''
        
        '''checks if listed as XX+ and sets upper limit as Aces (12)'''
        if pp_range[-1] == "+":
            
            upper_limit = 12
            lower_limit = self.rank_value.index(pp_range[0])
        
        else:
            limit1 = self.rank_value.index(pp_range[0])   # hand rank of first listing
            limit2 = self.rank_value.index(pp_range[-1])  # hand rank of second listing
            
            upper_limit = max(limit1, limit2)
            lower_limit = min(limit1, limit2)
        
        '''Iterate through each rank in the range and create all six Combo objects'''
        
        pp_combos = [[0, 2], [0, 1], [0, 3], [2, 1], [2, 3], [1, 3]]
        
        while upper_limit >= lower_limit:
            
            for combo in pp_combos:
                combo_list.append(Combo([upper_limit, combo[0]], [upper_limit, combo[1]]))
            
            upper_limit -= 1
    
    def suited_convert(self, suited_range, combo_list):
        '''Appends to combo_list a Combo object for every combo
        in a suited combo range
        Used by rangeToList'''
        
        if suited_range[-1] == "+":
            '''checks if listed as + and sets upper limit'''
            
            upper_limit = self.rank_value.index(suited_range[0]) - 1
            lower_limit = self.rank_value.index(suited_range[1])
            
        elif len(suited_range) == 3:
            '''Individual suited listing'''
            
            upper_limit = self.rank_value.index(suited_range[1])
            lower_limit = self.rank_value.index(suited_range[1])      
                
        else:
            '''These should be suited ranges'''
            
            limit1 = self.rank_value.index(suited_range[1])   # hand rank of first listing
            limit2 = self.rank_value.index(suited_range[-2])  # hand rank of second listing
            
            upper_limit = max(limit1, limit2)
            lower_limit = min(limit1, limit2)
        
        while upper_limit >= lower_limit:
            '''Go through each card rank in range and create the four suited combos'''
                        
            card1 = self.rank_value.index(suited_range[0])
            card2 = upper_limit
            
            suited_combos = [[0, 0], [1, 1], [2, 2], [3, 3]]
            
            for combo in suited_combos:
                combo_list.append(Combo([card1, combo[0]], [card2, combo[1]]))
    
            upper_limit -= 1
            
    def offsuit_convert(self, offsuit_range, combo_list):
        '''Appends to combo_list a Combo object for every combo
        in a offsuit combo range
        Used by rangeToList'''
        
        if offsuit_range[-1] == "+":
            '''checks if listed as + and sets upper limit'''
            
            upper_limit = self.rank_value.index(offsuit_range[0]) - 1
            lower_limit = self.rank_value.index(offsuit_range[1])
            
        elif len(offsuit_range) == 3:
            '''Individual suited listing'''
            
            upper_limit = self.rank_value.index(offsuit_range[1])
            lower_limit = self.rank_value.index(offsuit_range[1])      
                
        else:
            '''These should be suited ranges'''
            
            limit1 = self.rank_value.index(offsuit_range[1])   # hand rank of first listing
            limit2 = self.rank_value.index(offsuit_range[-2])  # hand rank of second listing
            
            upper_limit = max(limit1, limit2)
            lower_limit = min(limit1, limit2)
        
        while upper_limit >= lower_limit:
            '''Go through each card rank in range and create the four suited combos'''
                        
            card1 = self.rank_value.index(offsuit_range[0])
            card2 = upper_limit
            
            offsuit_combos = [[0, 2], [0, 1], [0, 3], [2, 1], [2, 3], [1, 3],
                              [2, 0], [1, 0], [1, 2], [3, 0], [3, 2], [3, 1]]
            
            for combo in offsuit_combos:
                combo_list.append(Combo([card1, combo[0]], [card2, combo[1]]))
    
            upper_limit -= 1
    
    def single_combo_convert(self, combo, combo_list):
        '''Converts a single combo string into Combo Object.'''
        
        card1 = [self.rank_value.index(combo[0]), self.suit_value.index(combo[1])]
        card2 = [self.rank_value.index(combo[2]), self.suit_value.index(combo[3])]
        
        combo_list.append(Combo(card1, card2))

    def rangeToList(self):
        '''
        Converts user input range from text to a list of Combo objects.
        '''
        
        combo_list = []
        
        '''Main Funcion'''
        try:
            
            '''Remove commas and spaces and turn into a list'''
            input_range = self.text.split(',')
            working_range = []
            
            for i in input_range:
                if i[0] == " ":
                    working_range.append(i[1:])
                else:
                    working_range.append(i)
            
            '''Iterate through working_range'''
            for i in working_range:
                
                if i[0] == i[1]:
                    '''Checks if pocket pair'''
                    self.pocket_pair_convert(i, combo_list)
                
                elif "o" in i:
                    '''Checks if offsuit item'''
                    self.offsuit_convert(i, combo_list)
                
                elif i[2] == "s":
                    '''Checks if suited item'''
                    self.suited_convert(i, combo_list)
                
                else:
                    '''Anything left should be individual combos'''
                    self.single_combo_convert(i, combo_list)
            
            return combo_list
            
        except:
            return []
    
    def rangeListToString(self, InputComboList):
        '''
        Converts a list of Combo Objects into the string representing that range.
        '''
        
        '''List representing RangeMatrix.matrix'''
        comboCounts = []
        for i in range(169):
            comboCounts.append([])      
        
        '''Place each combo object in its correct comboCount location'''
        for combo in InputComboList:
            comboCounts[combo.gridIndex].append(combo)
            
        rangeText = ''
        
        '''Build Pocket Pair text'''
        pp = ''        
        i = 0    # Tracks progress through comboCounts
        high = None
        low = None
        singleCombos = []
        
        while i <= 169:
            
            '''Find high value of pocket pair range'''
            for n in range(i, 169, 14):
                if len(comboCounts[n]) == 6:
                    '''All 6 pocket pair combos are present'''
                    high = comboCounts[n][0].cardA[0]
                    low = comboCounts[n][0].cardA[0]
                    i = n
                    i += 14
                    break
                elif len(comboCounts[n]) > 0 and len(comboCounts[n]) < 6:
                    '''Less than 6 pocket pair combos means they are listed as individual combos'''
                    for singleCombo in comboCounts[n]:
                        singleCombos.append(singleCombo.text)
            else:
                break
            if i > 168 and high == 0:
                rangeText += '22, '
                break
            
            '''Find low value of pocket pair range'''
            for n in range(i, 169, 14):
                if len(comboCounts[n]) == 6:
                    '''All 6 pocket pair combos are present'''
                    low = comboCounts[n][0].cardA[0]
                    i += 14
                    if low == 0:
                        '''all six combos of 22 will be lowest possible low value'''
                        break
                else:
                    break
                
            
            '''Convert rank values to text, format it, and add to string output'''
            highText = self.rank_value[high] * 2
            lowText = self.rank_value[low] * 2
            
            if highText == lowText:
                pp += highText + ', '
            elif highText == 'AA':
                pp += lowText + '+, '
            else:
                pp += highText + '-' + lowText + ', '
            
            rangeText += pp
            
            '''Increment and repeat to find next pocket pair range'''
            i += 14
            high = None
            low = None
            highText = ''
            lowText = ''
            pp = ''
        
        '''Append single combos to string output'''
        for combo in singleCombos:
            rangeText += combo + ', '
            
        '''Reset all Trackers'''
        i = 0
        high = None
        low = None
        singleCombos = []
        suitedText = ''
        
        '''Build Suited Combo Text'''
        
        rowHighs = ['AKs', 'KQs', 'QJs', 'JTs', 'T9s', '98s', '87s', '76s', '65s', '54s', '43s', '32s']
        rowHighIdx = 0
        
        while i <= 12:                       # Loop for each row
            begin = (13 * i) + (1 + i)       # starting index of comboCounts of current row
            end = 13 * (i + 1)               # ending index of comboCounts of current row
            for n in range(begin, end, 1):   # Loop for current row
                
                '''Find the High and/or Low value of suited range'''
                if len(comboCounts[n]) == 4 and high == None:
                    '''All 4 suited combos are present'''
                    high = comboCounts[n][0].comboRect
                    low = comboCounts[n][0].comboRect
                elif len(comboCounts[n]) == 4:
                    '''All 4 suited combos present in next ComboRect.
                    This will loop and set a new low value each time.'''
                    low = comboCounts[n][0].comboRect
                else:
                    '''Suited range has ended; convert to text'''
                    if len(comboCounts[n]) > 0:
                        for singleCombo in comboCounts[n]:
                            singleCombos.append(singleCombo)
                    if high == low and high != None:
                        suitedText += high + ', '
                    elif high == rowHighs[rowHighIdx]:
                        suitedText += low + '+, '
                    elif high != None:
                        suitedText += high + '-' + low + ', '
                    high = None
                    low = None
                if n + 1 == end and high != None:
                    '''This catches if last combo in row is selected.'''
                    if high == low:
                        suitedText += high + ', '
                    else:
                        if high == rowHighs[rowHighIdx]:
                            suitedText += low + '+, '
                        else:
                            suitedText += high + '-' + low + ', '
            rangeText += suitedText
            suitedText = ''
            high = None
            low = None
            rowHighIdx += 1
            i += 1
        
        '''Append single combos to string output'''
        for combo in singleCombos:
            rangeText += combo.text + ', '
        
        '''Reset all Trackers'''
        i = 0
        high = None
        low = None
        singleCombos = []
        offsuitText = ''
        
        '''Build Offsuit Combo Text'''
        # i is the column being checked.  AKo is 0
        rowHighs = ['AKo', 'KQo', 'QJo', 'JTo', 'T9o', '98o', '87o', '76o', '65o', '54o', '43o', '32o']
        rowHighIdx = 0        
        
        while i <= 12:                         # Loop for each column
            begin = (i + 1) * 13 + i
            end = 157 + i
            for n in range(begin, end, 13):    # Loop for currernt column
                '''Find High and/or low of offsuit range'''
                
                if len(comboCounts[n]) == 12 and high == None:
                    '''All 12 offsuit combos are present'''
                    high = comboCounts[n][0].comboRect
                    low = comboCounts[n][0].comboRect
                elif len(comboCounts[n]) == 12:
                    '''All 12 offsuit combos present in next ComboRect.
                    This will loop and set a new low value each time.'''
                    low = comboCounts[n][0].comboRect
                else:
                    '''offsuit range has ended; convert to text'''
                    if len(comboCounts[n]) > 0:
                        for singleCombo in comboCounts[n]:
                            singleCombos.append(singleCombo)
                    if high == low and high != None:
                        offsuitText += high + ', '
                    elif high == rowHighs[rowHighIdx]:
                        offsuitText += low + '+, '
                    elif high != None:
                        offsuitText += high + '-' + low + ', '
                    high = None
                    low = None
                if n + 1 == end and high != None:
                    '''This catches if last combo in row is selected.'''
                    if high == low:
                        offsuitText += high + ', '
                    else:
                        if high == rowHighs[rowHighIdx]:
                            offsuitText += low + '+, '
                        else:
                            offsuitText += high + '-' + low + ', '
            rangeText += offsuitText
            offsuitText = ''
            high = None
            low = None
            rowHighIdx += 1
            i += 1
        
        rangeText = rangeText[:-2]  # cut off the last ', '
        return rangeText
    
    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.text = self.toPlainText()
            range_list = self.rangeToList()
            self.enterPressed.emit(range_list)
        else:
            super().keyPressEvent(e)


"""RANGE STATS DISPLAY and related classes"""
           
class RangeStatsDisplay(QtWidgets.QWidget):
    '''
    QScrollArea Widget that displays saved preflop ranges or
    post flop made hand percentages.
    '''
    
    def __init__(self):
        super().__init__()
        
        layout = QtWidgets.QGridLayout()
        
        self.rangeStatsMain = RangeStatsMain()
        
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.rangeStatsMain)
        layout.addWidget(self.scrollArea, 0, 0, Qt.AlignCenter)
        
        self.clearButton = QtWidgets.QPushButton('Clear')
        self.clearButton.setFixedWidth(55)
        self.clearButton.setFixedHeight(25)
        self.clearButton.clicked.connect(self.rangeStatsMain.clearActions)
        layout.addWidget(self.clearButton, 1, 0)
        
        self.setLayout(layout)

class RangeStatsMain(QtWidgets.QWidget):
    '''
    Parent widget of RangeStats; and displays them.  This widget
    handles receives signals of range changes and passes them to
    each of its RangeStats child widgets.  Similarly, this widget
    emits signals indicating any changes in combos' action assignment.
    Intended to be the primary child widget of RangeStatsDisplay.
    '''
    
    sendComboActionsToRangeDisplay = QtCore.pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        
        self.combos = []
        self.board = []
        
        self.value = []
        self.bluff = []
        self.call = []
        self.noAction = []
        self.valueLock = []
        self.bluffLock = []
        self.callLock = []        
        
        self.made_hands = RangeStats()
        self.made_hands.setParent(self)
        
        self.drawing_hands = RangeStats()
        self.drawing_hands.setParent(self)
        
    def connectStatsRowSignals(self):
        '''Used after calculating made and/or drawing hands to
        connect every StatsRow signal to receiveComboActions.'''
        
        for row in self.made_hands.allRows:
            row.sendCombosToRangeStatsMain.connect(self.receiveComboActions)
            for row2 in row.secondary_StatsRows:
                row2.sendCombosToRangeStatsMain.connect(self.receiveComboActions)
        
        for row in self.drawing_hands.allRows:
            row.sendCombosToRangeStatsMain.connect(self.receiveComboActions)
            for row2 in row.secondary_StatsRows:
                row2.sendCombosToRangeStatsMain.connect(self.receiveComboActions)
    
    def receiveBoard(self, boardCards):
        '''Slot for BoardDisplay sendBoardCards signal'''
        self.board = boardCards
        self.made_hands.calc_made_hands(self.combos, self.board)
        self.drawing_hands.calc_drawing_hands(self.combos, self.board)
        self.connectStatsRowSignals()
        self.made_hands.update()
        self.drawing_hands.update()
        
        self.update()
    
    def receiveCombos(self, combos):
        '''Slot for RangeDisplay sendRangesToRangeStats signal'''
        self.value = combos[0]
        self.bluff = combos[1]
        self.call = combos[2]
        self.noAction = combos[3]
        
        '''Combine value, bluff, call, noAction into single combo list.'''
        combined_combos = []
        for combo_list in combos:
            combined_combos.extend(combo_list)
        self.combos = combined_combos
        
        if len(self.combos) == 0:
            self.made_hands.collapse_all()
            self.drawing_hands.collapse_all()
        
        self.made_hands.calc_made_hands(self.combos, self.board)
        self.drawing_hands.calc_drawing_hands(self.combos, self.board)
        self.connectStatsRowSignals()
        self.made_hands.update()
        self.drawing_hands.update()
        
        self.update()
    
    def receiveComboActions(self, actionList):
        '''
        actionList is a list of lists [value, bluff, call].
        This will go through every statsRow object within each RangeStats
        object and if the combo exists within that statsRow, the combo
        will be assigned to the correct action within that statsRow.
        '''
        
        for combo in actionList[0]:
            '''Value combos'''
            if combo not in self.value:
                self.value.append(combo)
            if combo in self.bluff:
                self.bluff.remove(combo)
            if combo in self.call:
                self.call.remove(combo)
            if combo in self.noAction:
                self.noAction.remove(combo)
            for row in self.made_hands.allRows:
                if combo in row.combos:
                    if combo not in row.value:
                        row.value.add(combo)
                    row.bluff.discard(combo)
                    row.call.discard(combo)
                    for row2 in row.secondary_StatsRows:
                        if combo in row2.combos:
                            if combo not in row2.value:
                                row2.value.add(combo)
                            row2.bluff.discard(combo)
                            row2.call.discard(combo)
            for row in self.drawing_hands.allRows:
                if combo in row.combos:
                    if combo not in row.value:
                        row.value.add(combo)
                    row.bluff.discard(combo)
                    row.call.discard(combo)
                    for row2 in row.secondary_StatsRows:
                        if combo in row2.combos:
                            if combo not in row2.value:
                                row2.value.add(combo)
                            row2.bluff.discard(combo)
                            row2.call.discard(combo)
        
        for combo in actionList[1]:
            '''Bluff Combos'''
            if combo not in self.bluff:
                self.bluff.append(combo)
            if combo in self.value:
                self.value.remove(combo)
            if combo in self.call:
                self.call.remove(combo)
            if combo in self.noAction:
                self.noAction.remove(combo)
            for row in self.made_hands.allRows:
                if combo in row.combos:
                    if combo not in row.bluff:
                        row.bluff.add(combo)
                    row.value.discard(combo)
                    row.call.discard(combo)
                    for row2 in row.secondary_StatsRows:
                        if combo in row2.combos:
                            if combo not in row2.bluff:
                                row2.bluff.add(combo)
                            row2.value.discard(combo)
                            row2.call.discard(combo)
            for row in self.drawing_hands.allRows:
                if combo in row.combos:
                    if combo not in row.bluff:
                        row.bluff.add(combo)
                    row.value.discard(combo)
                    row.call.discard(combo)
                    for row2 in row.secondary_StatsRows:
                        if combo in row2.combos:
                            if combo not in row2.bluff:
                                row2.bluff.add(combo)
                            row2.value.discard(combo)
                            row2.call.discard(combo)
        
        for combo in actionList[2]:
            '''Call Combos'''
            if combo not in self.call:
                self.call.append(combo)
            if combo in self.bluff:
                self.bluff.remove(combo)
            if combo in self.value:
                self.value.remove(combo)
            if combo in self.noAction:
                self.noAction.remove(combo)
            for row in self.made_hands.allRows:
                if combo in row.combos:
                    if combo not in row.call:
                        row.call.add(combo)
                    row.value.discard(combo)
                    row.bluff.discard(combo)
                    for row2 in row.secondary_StatsRows:
                        if combo in row2.combos:
                            if combo not in row2.call:
                                row2.call.add(combo)
                            row2.value.discard(combo)
                            row2.bluff.discard(combo)
            for row in self.drawing_hands.allRows:
                if combo in row.combos:
                    if combo not in row.call:
                        row.call.add(combo)
                    row.value.discard(combo)
                    row.bluff.discard(combo)
                    for row2 in row.secondary_StatsRows:
                        if combo in row2.combos:
                            if combo not in row2.call:
                                row2.call.add(combo)
                            row2.value.discard(combo)
                            row2.bluff.discard(combo)
        for combo in actionList[3]:
            '''noAction combos'''
            self.noAction.append(combo)
        
        self.sendComboActionsToRangeDisplay.emit([self.value, self.bluff, self.call, self.noAction])
        self.update()
    
    def clearActions(self):
        '''Clears action assignments for all StatsRows and sets all
        combos to noAciton.'''
        
        self.value.clear()
        self.bluff.clear()
        self.call.clear()
        self.noAction.clear()
        
        for combo in self.combos:
            self.noAction.append(combo)
        
        for row in self.made_hands.allRows:
            row.value.clear()
            row.bluff.clear()
            row.call.clear()
            row.noAction.clear()
            for row2 in row.secondary_StatsRows:
                row2.value.clear()
                row2.bluff.clear()
                row2.call.clear()
                row2.noAction.clear()
        
        for row in self.drawing_hands.allRows:
            row.value.clear()
            row.bluff.clear()
            row.call.clear()
            row.noAction.clear()
            for row2 in row.secondary_StatsRows:
                row2.value.clear()
                row2.bluff.clear()
                row2.call.clear()
                row2.noAction.clear()
        
        self.sendComboActionsToRangeDisplay.emit([self.value, self.bluff, self.call, self.noAction])
        self.update()
    
    def reposition_range_stats(self):
        x, y = 0, 0
        spacing = 10  # Gap in pixels between each RangeStats widget
        self.made_hands.setParent(self)
        self.made_hands.show()
        self.made_hands.move(x, y)
        
        y += self.made_hands.display_height
        if len(self.made_hands.allRows) > 0:
            y += spacing
        
        self.drawing_hands.setParent(self)
        self.drawing_hands.show()
        self.drawing_hands.move(x, y)
        
        self.setMinimumSize(max(self.made_hands.display_width, self.drawing_hands.display_width),
                            self.made_hands.display_height + self.drawing_hands.display_height + spacing + 1)
    
    def update(self):
        self.made_hands.reconfigHeight()
        self.drawing_hands.reconfigHeight()
        self.reposition_range_stats()
        
        super().update()
        
class RangeStats(QtWidgets.QWidget):
    '''
    Widget that calculates, organizes, and displays the StatsRow Widgets.
    Intended to be a child widget of RangeStatsMain
    '''
    
    def __init__(self):
        super().__init__()
        
        self.allRows = []
        
        self.combos = []
        self.board = []
        
        self.value = []
        self.bluff = []
        self.call = []
        self.noAction = []
        self.valueLock = []
        self.bluffLock = []
        self.callLock = []
        
        self.display_height = 0
        self.display_width = 0
        
        '''Tracks each child StatsRow.extended status.'''
        self.made_hands = self.made_hand_extended_tracker()
        self.drawing_hands = self.drawing_hands_extended_tracker()
    
    def rowExtendReceive(self):
        '''Slot to respond to StatsRow extendSignal'''
        
        self.saveExtendedStatus()
        self.update()
    
    def made_hand_extended_tracker(self):
        '''
        Returns a dict of key='Made Hand Name' and
        value=Boolean representing if it is extended or not.
        Used by self.__init__.
        As new hand types are added to self.calc they get added
        here first as the dict created here is used to make made_hands
        dict in self.calc.
        '''
        
        made_hands = {}
        made_hands['Straight Flush'] = False
        made_hands['Four of a Kind'] = False
        made_hands['Full House'] = False
        made_hands['Flush'] = False
        made_hands['Straight'] = False
        made_hands['Three of a Kind'] = False
        made_hands['Two Pair'] = False
        made_hands['Overpair'] = False
        made_hands['Top Pair'] = False
        made_hands['PP Below TP'] = False
        made_hands['Middle Pair'] = False
        made_hands['Weak Pair'] = False
        made_hands['Ace High'] = False
        made_hands['Overcards'] = False
        
        return made_hands
    
    def drawing_hands_extended_tracker(self):
        '''
        Returns a dict of key='Drawing Hand Name' and
        value=Boolean representing if it is extended or not.
        Used by self.__init__.
        As new hand types are added to self.calc_drawing_hands they get added
        here first as the dict created here is used to make drawing_hands
        dict in self.calc_drawing_hands.
        '''
        
        drawing_hands = {}
        drawing_hands['Flush Draw'] = False
        drawing_hands['Straight Draw'] = False
        drawing_hands['BD Flush Draw'] = False
        drawing_hands['BD Str Draw'] = False
        
        return drawing_hands
    
    def combo_draws_extended_tracker(self):
        '''
        Returns a dict of key='Combo Draw Name' and
        value=Boolean representing if it is extended or not.
        Used by self.__init__.
        As new hand types are added to self.calc_combo_draws they get added
        here first as the dict created here is used to make combo_draw
        dict in self.calc_combo_draws.
        '''
        
        combo_draws = {}
        
        return combo_draws
    
    def collapse_all(self):
        '''Sets all extended statuses to False.'''
        
        for hand in self.made_hands:
            self.made_hands[hand] = False
        
        for hand in self.drawing_hands:
            self.drawing_hands[hand] = False
    
    def saveExtendedStatus(self):
        '''Used when a child StatsRow object extends or collapses
        to remember its state.'''
        
        for row in self.allRows:
            for hand in self.made_hands:
                if row.name == hand:
                    self.made_hands[hand] = row.extended
                    break
            for hand in self.drawing_hands:
                if row.name == hand:
                    self.drawing_hands[hand] = row.extended
                    break
            
    def setExtendedStatus(self):
        '''Sets each child StatsRow's extended status from
        self.made_hands dict.  Used during self.update'''
        
        for row in self.allRows:
            for hand in self.made_hands:
                if row.name == hand:
                    row.extended = self.made_hands[hand]
                    row.calcHeight()
                    break
            for hand in self.drawing_hands:
                if row.name == hand:
                    row.extended = self.drawing_hands[hand]
                    row.calcHeight()
                    break

    def calc_made_hands(self, combos, board):
        '''Clear allRows and recalculate made hand stats.'''
        
        for row in self.allRows:
            row.hide()
        self.allRows.clear()
        if len(board) >= 3:
            self.allRows = self.find_made_hands(combos, board)
        for row in self.allRows:
            row.extendSignal.connect(self.rowExtendReceive)
            if len(row.secondary_StatsRows) > 0:
                row.extendable = True
                row.calcHeight()
                for secondary_row in row.secondary_StatsRows:
                    secondary_row.setParent(row)
    
    def calc_drawing_hands(self, combos, board):
        '''Clear allRows and recalculate drawing hand stats.'''
        
        for row in self.allRows:
            row.hide()
        self.allRows.clear()
        if len(board) >= 3:
            self.allRows = self.find_drawing_hands(combos, board)
        for row in self.allRows:
            row.extendSignal.connect(self.rowExtendReceive)
            if len(row.secondary_StatsRows) > 0:
                row.extendable = True
                row.calcHeight()
                for secondary_row in row.secondary_StatsRows:
                    secondary_row.setParent(row)
        
    def find_made_hands(self, combos, board):
        '''
        Main Made Hand Stats Sovler.
        Returns a list of StatsRow Objects.
        combos is a list or set of combo objects.
        board is a list or set of lists which represent a card as
        [rank, suit].  rank is 0-12, suit is 0-3
        0 = h, 1 = d, 2 = c, 3 = s
        '''
        
        unBlockedCombos = ShCalc.removeBlockedCombos(combos, board)
        total_combos = len(unBlockedCombos)
        
        made_hands = {}
        for hand in self.made_hands:
            made_hands[hand] = []
        
        flush = {}
        flush['Nut Flush'] = []
        flush['2nd Nut Flush'] = []
        flush['3rd Nut Flush'] = []
        flush['Weak Flush'] = []
        
        straight = {}
        straight['Nut Straight'] = []
        straight['2nd Nut Straight'] = []
        straight['Weak Straight'] = []
        
        three_of_a_kind = {}
        three_of_a_kind['Set'] = []
        three_of_a_kind['Trips'] = []
        
        top_pair = {}
        top_pair['Top Kicker'] = []
        top_pair['Second Kicker'] = []
        top_pair['Third Kicker'] = []
        top_pair['Middle Kicker'] = []
        top_pair['Weak Kicker'] = []
        
        
        '''Check board for made hands to disallow lesser hand types from being checked'''
        
        '''Iterate through each made hand type in order from highest to lowest.
        We want each combo to be assigned to only ONE of these main made hand types
        (except Ace High and Overcards).   If the hand type has secondary StatsRows
        (i.e. 2nd nut flush, TP weak kicker), they are assigned here.'''
        
        for combo in unBlockedCombos:
            
            '''Straight Flush'''
            if ShCalc.str_flush_check(combo, board):
                made_hands['Straight Flush'].append(combo)
                continue
            if ShCalc.board_str_flush_check(board):
                continue
            
            '''Quads'''    
            if ShCalc.quads_check(combo, board):
                made_hands['Four of a Kind'].append(combo)
                continue
            if ShCalc.board_quads_check(board):
                continue
            
            '''Full House'''
            if ShCalc.full_house_check(combo, board):
                made_hands['Full House'].append(combo)
                continue
            if ShCalc.board_full_house_check(board):
                continue
            
            '''Flush'''
            if ShCalc.flush_check(combo, board):
                made_hands['Flush'].append(combo)
                '''Assign combo to type of flush'''
                if ShCalc.nut_flush_check(combo, board):
                    flush['Nut Flush'].append(combo)
                elif ShCalc.second_nut_flush_check(combo, board):
                    flush['2nd Nut Flush'].append(combo)
                elif ShCalc.third_nut_flush_check(combo, board):
                    flush['3rd Nut Flush'].append(combo)
                else:
                    flush['Weak Flush'].append(combo)
                continue
                
            if ShCalc.board_flush_check(board):
                continue
            
            '''Straight'''
            if ShCalc.straight_check(combo, board):
                made_hands['Straight'].append(combo)
                '''Assign combo to type of straight'''
                if ShCalc.nut_straight_check(combo, board):
                    straight['Nut Straight'].append(combo)
                elif ShCalc.second_nut_straight_check(combo, board):
                    straight['2nd Nut Straight'].append(combo)
                else:
                    straight['Weak Straight'].append(combo)
                continue
            
            if ShCalc.board_straight_check(board):
                continue
            
            '''Three of a Kind'''
            if ShCalc.three_of_a_kind_check(combo, board):
                made_hands['Three of a Kind'].append(combo)
                if ShCalc.set_check(combo, board):
                    three_of_a_kind['Set'].append(combo)
                else:
                    three_of_a_kind['Trips'].append(combo)
                continue
            
            if ShCalc.board_three_of_a_kind_check(board):
                continue
            
            '''Two Pair'''
            if ShCalc.two_pair_check(combo, board):
                made_hands['Two Pair'].append(combo)
                continue
                
            '''Overpair'''
            if ShCalc.overpair_check(combo, board):
                made_hands['Overpair'].append(combo)
                continue
            
            '''Top Pair'''
            if ShCalc.top_pair_check(combo, board):
                made_hands['Top Pair'].append(combo)
                if ShCalc.top_pair_top_kicker(combo, board):
                    top_pair['Top Kicker'].append(combo)
                elif ShCalc.top_pair_second_kicker(combo, board):
                    top_pair['Second Kicker'].append(combo)
                elif ShCalc.top_pair_third_kicker(combo, board):
                    top_pair['Third Kicker'].append(combo)
                elif ShCalc.top_pair_middle_kicker(combo, board):
                    top_pair['Middle Kicker'].append(combo)
                else:
                    top_pair['Weak Kicker'].append(combo)
                continue
            
            '''PP Below TP'''
            if ShCalc.pp_below_tp_check(combo, board):
                made_hands['PP Below TP'].append(combo)
                continue
            
            '''Middle Pair'''
            if ShCalc.middle_pair_check(combo, board):
                made_hands['Middle Pair'].append(combo)
                continue
            
            '''Weak Pair'''
            if ShCalc.weak_pair_check(combo, board):
                made_hands['Weak Pair'].append(combo)
                continue
            
            '''Ace High'''
            if ShCalc.ace_high_check(combo):
                made_hands['Ace High'].append(combo)
            
            '''Overcards'''
            if ShCalc.overcards_check(combo, board):
                made_hands['Overcards'].append(combo)
        
        
        '''Construct a list of StatsRow objects for each dict of made hands'''
        flush_total_combos = len(made_hands['Flush'])
        if flush_total_combos > 0:
            flush_stats = RangeStats.dictToStatsRows(flush, total_combos)
            made_hands['Flush'].append(flush_stats)
        
        straight_total_combos = len(made_hands['Straight'])
        if straight_total_combos > 0:
            straight_stats = RangeStats.dictToStatsRows(straight, total_combos)
            made_hands['Straight'].append(straight_stats)
        
        three_of_a_kind_total_combos = len(made_hands['Three of a Kind'])
        if three_of_a_kind_total_combos > 0:
            three_of_a_kind_stats = RangeStats.dictToStatsRows(three_of_a_kind, total_combos)
            made_hands['Three of a Kind'].append(three_of_a_kind_stats)
        
        top_pair_total_combos = len(made_hands['Top Pair'])
        if top_pair_total_combos > 0:
            top_pair_stats = RangeStats.dictToStatsRows(top_pair, total_combos)
            made_hands['Top Pair'].append(top_pair_stats)
        
        finalStats = RangeStats.dictToStatsRows(made_hands, total_combos)
         
        return finalStats
    
    def find_drawing_hands(self, combos, board):
        '''
        Main Drawing Hand Stats Sovler.
        Returns a list of StatsRow Objects.
        combos is a list or set of combo objects.
        board is a list or set of lists which represent a card as
        [rank, suit].  rank is 0-12, suit is 0-3
        0 = h, 1 = d, 2 = c, 3 = s
        '''
        
        unBlockedCombos = ShCalc.removeBlockedCombos(combos, board)
        total_combos = len(unBlockedCombos)
        
        flush_draw = {}
        flush_draw['Nut Flush Draw'] = []
        flush_draw['Second Nut FD'] = []
        flush_draw['Weak Flush Draw'] = []
        
        straight_draw = {}
        straight_draw['OESD'] = []
        straight_draw['Gutshot'] = []
        
        bdfd = {}
        bdfd['Nut, 2 Card'] = []
        bdfd['Nut, 1 Card'] = []
        bdfd['Non-Nut, 2 Card'] = []
        bdfd['Non-Nut, 1 Card'] = []
        
        bdsd = {}
        bdsd['OpenEnd 3 Str'] = []
        bdsd['BDSD 2 Card'] = []
        bdsd['BDSD 1 Card'] = []
        
        drawing_hands = {}
        for hand in self.drawing_hands:
            drawing_hands[hand] = []
        
        for combo in unBlockedCombos:
            
            '''Flush Draw'''
            if ShCalc.flush_draw_check(combo, board):
                drawing_hands['Flush Draw'].append(combo)
                if ShCalc.nut_flush_draw_check(combo, board):
                    flush_draw['Nut Flush Draw'].append(combo)
                elif ShCalc.second_nut_flush_draw_check(combo, board):
                    flush_draw['Second Nut FD'].append(combo)
                else:
                    flush_draw['Weak Flush Draw'].append(combo)
            
            '''Straight Draw'''
            if ShCalc.straight_draw_check(combo, board):
                drawing_hands['Straight Draw'].append(combo)
                if ShCalc.oesd_check(combo, board):
                    straight_draw['OESD'].append(combo)
                else:
                    straight_draw['Gutshot'].append(combo)
            
            '''Back Door Flush Draw'''
            if ShCalc.bdfd_check(combo, board):
                drawing_hands['BD Flush Draw'].append(combo)
                if ShCalc.nut_bdfd_check(combo, board):
                    if ShCalc.two_card_bdfd_check(combo):
                        bdfd['Nut, 2 Card'].append(combo)
                    else:
                        bdfd['Nut, 1 Card'].append(combo)
                else:
                    if ShCalc.two_card_bdfd_check(combo):
                        bdfd['Non-Nut, 2 Card'].append(combo)
                    else:
                        bdfd['Non-Nut, 1 Card'].append(combo)
            
            '''Back Door Straight Draw'''
            if ShCalc.bdsd_check(combo, board):
                drawing_hands['BD Str Draw'].append(combo)
                if ShCalc.bdsd_open_ended_three_straight_check(combo, board):
                    bdsd['OpenEnd 3 Str'].append(combo)
                elif ShCalc.two_card_bdsd_check(combo, board):
                    bdsd['BDSD 2 Card'].append(combo)
                else:
                    bdsd['BDSD 1 Card'].append(combo)
        
        
        '''Construct a list of StatsRow objects for each dict of made hands'''
        flush_draw_total_combos = len(drawing_hands['Flush Draw'])
        if flush_draw_total_combos > 0:
            flush_draw_stats = RangeStats.dictToStatsRows(flush_draw, total_combos)
            drawing_hands['Flush Draw'].append(flush_draw_stats)
        
        straight_draw_combos = len(drawing_hands['Straight Draw'])
        if straight_draw_combos > 0:
            straight_draw_stats = RangeStats.dictToStatsRows(straight_draw, total_combos)
            drawing_hands['Straight Draw'].append(straight_draw_stats)
        
        bdfd_combos = len(drawing_hands['BD Flush Draw'])
        if bdfd_combos > 0:
            bdfd_stats = RangeStats.dictToStatsRows(bdfd, total_combos)
            drawing_hands['BD Flush Draw'].append(bdfd_stats)
        
        bdsd_combos = len(drawing_hands['BD Str Draw'])
        if bdsd_combos > 0:
            bdsd_stats = RangeStats.dictToStatsRows(bdsd, total_combos)
            drawing_hands['BD Str Draw'].append(bdsd_stats)

        finalStats = RangeStats.dictToStatsRows(drawing_hands, total_combos)
         
        return finalStats
    
    @staticmethod
    def dictToStatsRows(made_hands, total_combos):
        '''made_hands parameter is a dictionary of made hands where
        the key is a string of the made hand type name, and the value is a list
        of combo objects that belong to that made hand type.
        Used by RangeStats.calc() to construct lists of StatsRow objects.'''
        
        stats_row_list = []
        tot_comb = total_combos
        
        for hand_type in made_hands:
            if len(made_hands[hand_type]) > 0:
                secondary_rows = []
                if isinstance(made_hands[hand_type][-1], list):
                    secondary_rows = made_hands[hand_type][-1]
                    del made_hands[hand_type][-1]
                hand_name = hand_type
                hand_combos = made_hands[hand_type]
                stats_row_list.append(StatsRow(hand_name, hand_combos, tot_comb, secondary_rows))
        
        return stats_row_list    
    
    def reconfigHeight(self):
        '''Used by self.update() and when a StatsRow object extends or collapses.
        Sets new MinimumSize for the widget.'''
        
        self.display_height = 0
        self.display_width = 0
        
        if len(self.allRows) > 0:
            newHeight = 0
            for row in self.allRows:
                if row.extended:
                    newHeight += row.height + 1
                    for secondary_row in row.secondary_StatsRows:
                        newHeight += row.height + 1
                else:
                    newHeight += row.height + 1
            self.display_height = newHeight
            self.display_width = self.allRows[0].width + 1
            self.setMinimumSize(self.allRows[0].width + 1, newHeight)
            self.parent().reposition_range_stats()
    
    def setRowPosition(self):
        '''Set x, y position for each visible StatsRow object'''
        x, y = 0, 0
        for row in self.allRows:
            row.setParent(self)
            
            row.move(x, y)
            row.show()
            if row.extended:
                for secondary_row in row.secondary_StatsRows:
                    sec_row_height = secondary_row.drawHeight
                    secondary_row.show()
                    y += secondary_row.drawHeight
                y += sec_row_height
            else:
                y += row.drawHeight
        
    def update(self):
        
        self.setExtendedStatus()
        self.setRowPosition()
        self.reconfigHeight()
        
        super().update()
    
    def paintEvent(self, e):
        '''so i can stop it and check the stack data'''
        pass


class StatsRow(QtWidgets.QWidget):
    '''
    One row of RangeStats.  Displays made hand type, combos,
    action selection squares.  Is collapsable and extendable.
    '''
    
    extendSignal = QtCore.pyqtSignal()
    sendCombosToRangeStatsMain = QtCore.pyqtSignal(list)
    
    def __init__(self, name, combo_list, total_combos, secondary_rows = []):
        super().__init__()
        
        width, height = 275, 25
        
        self.width, self.height = width, height
        self.drawHeight = self.height
        
        self.name = name    # Name of name hand.
        self.combos = combo_list  # Primary list of Combo Objects
        self.totalCombos = total_combos
        
        '''Format secondary StatsRows'''
        self.secondary_StatsRows = secondary_rows  # List of subdivision StatsRow objects
        for i, row in enumerate(self.secondary_StatsRows):
            row.move(row.x(), (i + 1) * height)
            row.hide()
        
        self.value = set()
        self.bluff = set()
        self.call = set()
        self.noAction = set()
        self.valueLock = set()
        self.bluffLock = set()
        self.callLock = set()
        
        border_height = height
        for row in self.secondary_StatsRows:
            border_height += height
        self.border = QtCore.QRect(0, 0, width, border_height)
        
        tri_x = width - 10                    # X coord for starting point of tirangle collapsed indicator
        tri_y = 8                                  # Y corrd for 'centering' the triable in the row        
        
        '''Triangle collapsed indicator'''
        self.triCollapsed = QtGui.QPainterPath()
        self.triCollapsed.moveTo(tri_x, tri_y)
        self.triCollapsed.lineTo(tri_x + 10, tri_y)
        self.triCollapsed.lineTo(int((tri_x + 10 / 2)), tri_y + 10)
        self.triCollapsed.closeSubpath()
        
        '''Triangle extended indicator'''
        self.triExtended = QtGui.QPainterPath()
        self.triExtended.moveTo(tri_x, tri_y + 10)
        self.triExtended.lineTo(tri_x + 10, tri_y + 10)
        self.triExtended.lineTo(int((tri_x + 10 / 2)), tri_y)
        self.triExtended.closeSubpath()
        
        '''Value, Bluff, and Call Rects'''
        rectScale = .75       # % of StatsRow height
        rectSpacing = 5       # pixels between actionRects
        rectX = (height - rectScale * height) / 2  # Starting x coord for left most rect
        rectY = (height - rectScale * height) / 2  # Y coord for rects
        
        self.valueRect = QtCore.QRect(rectX, rectY, height * rectScale, height * rectScale)
        rectX += height * rectScale + rectSpacing
        self.bluffRect = QtCore.QRect(rectX, rectY, height * rectScale, height * rectScale)
        rectX += height * rectScale + rectSpacing
        self.callRect = QtCore.QRect(rectX, rectY, height * rectScale, height * rectScale)
        rectX += height * rectScale   # Used later for label positioning
        
        '''Lables'''
        font = QtGui.QFont()
        font.setPixelSize(13)
        
        rectLabelGap = 6     # Gap in pixels between last actionRect and name label
        
        self.nameLabel = QtWidgets.QLabel(self.name, self)
        self.nameLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.nameLabel.setFont(font)
        nameLabelSize = self.nameLabel.size()
        nameLabelHeight = self.nameLabel.fontMetrics().boundingRect(self.nameLabel.text()).height()
        nameLabelY = (height - nameLabelHeight) / 2
        nameLabelX = rectX + rectLabelGap
        self.nameLabel.move(nameLabelX, nameLabelY)
        
        freqComboGap = 5  # Gap in pixels between frequency, combo and triangle indicators
        
        freq = round(len(self.combos) / self.totalCombos * 100, 1)
        if freq.is_integer():
            freq = round(freq)    
        self.freqLabel = QtWidgets.QLabel(str(freq) + '%', self)
        self.freqLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.freqLabel.setFont(font)
        freqLabelWidth = self.freqLabel.fontMetrics().boundingRect(self.freqLabel.text()).width()
        freqLabelX = tri_x - freqComboGap - freqLabelWidth
        self.freqLabel.move(freqLabelX, nameLabelY)
        
        self.comboLabel = QtWidgets.QLabel('(' + str(len(self.combos)) + ')', self)
        self.comboLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.comboLabel.setFont(font)
        comboLabelWidth = self.comboLabel.fontMetrics().boundingRect(self.comboLabel.text()).width()
        comboLabelX = self.width * (2/3)
        self.comboLabel.move(comboLabelX, nameLabelY)
        
        '''RGB values for display'''
        self.valueBrush = [255, 77, 77]
        self.bluffBrush = [255, 166, 166]
        self.callBrush = [103, 178, 45]
        
        self.extendable = False
        self.extended = False
        
        self.setMinimumSize(width + 1, height + 1)
    
    def calcHeight(self):
        '''
        Recalculates and updates self.height and sets widget
        minimumsize.
        Used by mousePressEvent and RangeStats for drawing.
        '''
        spacing = 5   # pixel gap between stats rows
        height = self.height
        if self.extended:
            for row in self.secondary_StatsRows:
                height += self.height
        else:
            height = self.height
        
        self.drawHeight = height
        self.setMinimumSize(self.width + 3, self.drawHeight + 3)
    
    def clearActions(self):
        '''Clears combos from all action lists'''
        self.value.clear()
        self.bluff.clear()
        self.call.clear()
    
    def setValue(self):
        '''Called when valueRect is clicked'''
        self.clearActions()
        for combo in self.combos:
            self.value.add(combo)
        self.sendCombosToRangeStatsMain.emit([self.value, self.bluff, self.call, self.noAction])
    
    def setBluff(self):
        '''Called when bluffRect is clicked'''
        self.clearActions()
        for combo in self.combos:
            self.bluff.add(combo)
        self.sendCombosToRangeStatsMain.emit([self.value, self.bluff, self.call, self.noAction])
    
    def setCall(self):
        '''Called when callRect is clicked'''
        self.clearActions()
        for combo in self.combos:
            self.call.add(combo)
        self.sendCombosToRangeStatsMain.emit([self.value, self.bluff, self.call, self.noAction])
    
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.valueRect.contains(e.x(), e.y()):
                self.setValue()
            elif self.bluffRect.contains(e.x(), e.y()):
                self.setBluff()
            elif self.callRect.contains(e.x(), e.y()):
                self.setCall()
            else:
                if self.extendable:
                    if not self.extended:
                        self.extended = True
                        self.calcHeight()
                        for row in self.secondary_StatsRows:
                            row.show()
                    else:
                        self.extended = False
                        self.calcHeight()
                        for row in self.secondary_StatsRows:
                            row.hide()
                    self.extendSignal.emit()
            self.update()
        
    def paintEvent(self, e):
        
        painter = QtGui.QPainter(self)
        black_pen = QtGui.QPen(Qt.black, 1, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin)
        grey_pen = QtGui.QPen(Qt.gray, 1, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin)
        painter.setPen(black_pen)
        
        value = QtGui.QBrush()
        value.setColor(QtGui.QColor(self.valueBrush[0], self.valueBrush[1], self.valueBrush[2]))
        value.setStyle(Qt.SolidPattern)
        
        bluff = QtGui.QBrush()
        bluff.setColor(QtGui.QColor(self.bluffBrush[0], self.bluffBrush[1], self.bluffBrush[2]))
        bluff.setStyle(Qt.SolidPattern)
        
        call = QtGui.QBrush()
        call.setColor(QtGui.QColor(self.callBrush[0], self.callBrush[1], self.callBrush[2]))
        call.setStyle(Qt.SolidPattern)        
        
        triBrush = QtGui.QBrush()
        triBrush.setColor(QtGui.QColor(0, 0, 0))
        triBrush.setStyle(Qt.SolidPattern)        
        
        '''Draw ActionRects'''
        if len(self.value) > 0:
            painter.fillRect(self.valueRect, value)
        if len(self.bluff) > 0:
            painter.fillRect(self.bluffRect, bluff)
        if len(self.call) > 0:
            painter.fillRect(self.callRect, call)
        
        painter.drawRect(self.valueRect)
        painter.drawRect(self.bluffRect)
        painter.drawRect(self.callRect)
        
        painter.drawText(self.valueRect, Qt.AlignCenter, 'V')
        painter.drawText(self.bluffRect, Qt.AlignCenter, 'B')
        painter.drawText(self.callRect, Qt.AlignCenter, 'C')
        
        '''Draw the correct triangle'''
        if self.extendable:
            if not self.extended:
                painter.fillPath(self.triCollapsed, triBrush)
                painter.drawPath(self.triCollapsed)
            elif self.extended:
                painter.fillPath(self.triExtended, triBrush)
                painter.drawPath(self.triExtended)
        
        '''Draw Border'''
        if self.extended:
            painter.drawRect(self.border)

"""ACTIONBUCKETS and related classes"""
        
class ActionBuckets(QtWidgets.QWidget):
    '''
    Widget for displaying Value, Bluff, and Call Buttons and
    each's stats.
    '''
    
    actionSelected = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        width, height = 62, 25
        ol_w = 5
        
        '''Establish Layout'''
        layout = QtWidgets.QGridLayout()
        
        '''Create and Add ActionButtons to layout'''
        self.valueButton = ActionButton(width, height, ol_w, 'Value')
        self.bluffButton = ActionButton(width, height, ol_w, 'Bluff')
        self.callButton = ActionButton(width, height, ol_w, 'Call')
        
        layout.addWidget(self.valueButton, 0, 0, Qt.AlignCenter)
        layout.addWidget(self.bluffButton, 0, 1, Qt.AlignCenter)
        layout.addWidget(self.callButton, 0, 2, Qt.AlignCenter)
        
        self.valueButton.clicked.connect(self.buttonClicked)
        self.bluffButton.clicked.connect(self.buttonClicked)
        self.callButton.clicked.connect(self.buttonClicked)
        
        '''Create, format, and add Combo and Frequency labels to layout'''
        self.valComLabel = QtWidgets.QLabel('0')
        self.bluffComLabel = QtWidgets.QLabel('0')
        self.callComLabel = QtWidgets.QLabel('0')
        
        comboFont = QtGui.QFont()
        comboFont.setPixelSize(15)
        
        self.valComLabel.setFont(comboFont)
        self.bluffComLabel.setFont(comboFont)
        self.callComLabel.setFont(comboFont)
        
        layout.addWidget(self.valComLabel, 1, 0, Qt.AlignCenter)
        layout.addWidget(self.bluffComLabel, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.callComLabel, 1, 2, Qt.AlignCenter)
        
        self.valFreqLabel = QtWidgets.QLabel('0%')
        self.bluffFreqLabel = QtWidgets.QLabel('0%')
        self.callFreqLabel = QtWidgets.QLabel('0%')
        
        self.valFreqLabel.setFont(comboFont)
        self.bluffFreqLabel.setFont(comboFont)
        self.callFreqLabel.setFont(comboFont)
        
        layout.addWidget(self.valFreqLabel, 2, 0, Qt.AlignCenter)
        layout.addWidget(self.bluffFreqLabel, 2, 1, Qt.AlignCenter)
        layout.addWidget(self.callFreqLabel, 2, 2, Qt.AlignCenter)
        
        '''Create, format, and add the Value : Bluff and Continue Frequency labels'''
        self.valueBluffLabel = QtWidgets.QLabel('Value : Bluff')
        self.contFreqLabel = QtWidgets.QLabel('Continue Freq')
        
        comboFont.setPixelSize(13)
        self.valueBluffLabel.setFont(comboFont)
        self.contFreqLabel.setFont(comboFont)
        
        layout.addWidget(self.valueBluffLabel, 0, 3, Qt.AlignLeft)
        layout.addWidget(self.contFreqLabel, 1, 3, Qt.AlignLeft)
        
        self.valueBluffRatio = QtWidgets.QLabel('0 : 0')
        self.contFreqNum = QtWidgets.QLabel('')
        
        comboFont.setBold(True)
        comboFont.setPixelSize(15)
        self.valueBluffRatio.setFont(comboFont)
        self.contFreqNum.setFont(comboFont)
        
        layout.addWidget(self.valueBluffRatio, 0, 4, Qt.AlignLeft)
        layout.addWidget(self.contFreqNum, 1, 4, Qt.AlignLeft)
        
        '''Total Combos and Unassigned Combos Labels'''
        self.noActionLabel = QtWidgets.QLabel('Unassigned Combos: 0')
        self.totalCombosLabel = QtWidgets.QLabel('Total Combos: 0')
        
        comboFont.setPixelSize(13)
        comboFont.setBold(False)
        self.noActionLabel.setFont(comboFont)
        self.totalCombosLabel.setFont(comboFont)
        
        layout.addWidget(self.noActionLabel, 4, 0, 1, 3, Qt.AlignLeft)
        layout.addWidget(self.totalCombosLabel, 4, 3, 1, 2, Qt.AlignLeft)
        layout.setRowMinimumHeight(3, 5)
        
        '''Format the QGridLayout'''
        layout.setVerticalSpacing(0)
        
        sizepolicy = QtWidgets.QSizePolicy()
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHorizontalStretch(0)
        self.setSizePolicy(sizepolicy)
        
        self.setLayout(layout)
        
        '''Attrubutes'''
        self.value = set()
        self.bluff = set()
        self.call = set()
        self.noAction = set()
        self.valueLock = set()
        self.bluffLock = set()
        self.callLock = set()
        self.totalCombos = 0
        self.board = []
        
    def buttonClicked(self, action):
        
        if self.valueButton.action != action:
            self.valueButton.selected = False
        if self.bluffButton.action != action:
            self.bluffButton.selected = False
        if self.callButton.action != action:
            self.callButton.selected = False
        
        '''Emit signal to tell RangeStats and RangeDisplay which action is selected.'''
        if self.valueButton.selected:
            self.actionSelected.emit('value')
        elif self.bluffButton.selected:
            self.actionSelected.emit('bluff')
        elif self.callButton.selected:
            self.actionSelected.emit('call')
        else:
            self.actionSelected.emit('')
        
        self.update()
    
    def receiveRanges(self, ranges):
        '''Slot for RangeDisplay signal that sends updates rangeSets'''
        
        self.value = ranges[0]
        self.bluff = ranges[1]
        self.call = ranges[2]
        self.noAction = ranges[3]
        
        self.update()
    
    def receiveBoard(self, board):
        '''Slot for receiving board info from BoardDisplay'''
        
        self.board = board
        self.update()
    
    def update(self):
        
        '''Update Combo Numbers'''
        self.value = ShCalc.removeBlockedCombos(self.value, self.board)
        self.bluff = ShCalc.removeBlockedCombos(self.bluff, self.board)
        self.call = ShCalc.removeBlockedCombos(self.call, self.board)
        self.noAction = ShCalc.removeBlockedCombos(self.noAction, self.board)
        
        self.totalCombos = len(self.value) + len(self.bluff) + len(self.call) + len(self.noAction)
        
        self.valComLabel.setText(str(len(self.value)))
        self.bluffComLabel.setText(str(len(self.bluff)))
        self.callComLabel.setText(str(len(self.call)))
        
        '''Update Frequency Numbers'''
        if self.totalCombos != 0:
            
            valueFreq = round(len(self.value) / self.totalCombos * 100, 1)
            if valueFreq.is_integer():
                valueFreq = round(valueFreq)
            self.valFreqLabel.setText(str(valueFreq) + '%')
            
            bluffFreq = round(len(self.bluff) / self.totalCombos * 100, 1)
            if bluffFreq.is_integer():
                bluffFreq = round(bluffFreq)
            self.bluffFreqLabel.setText(str(bluffFreq) + '%')
            
            callFreq = round(len(self.call) / self.totalCombos * 100, 1)
            if callFreq.is_integer():
                callFreq = round(callFreq)
            self.callFreqLabel.setText(str(callFreq) + '%')
            
        else:
            self.valFreqLabel.setText('0%')
            self.bluffFreqLabel.setText('0%')
            self.callFreqLabel.setText('0%')
        
        '''Update Value : Bluff Ratio'''
        if len(self.value) >= len(self.bluff) and len(self.bluff) != 0:
            valueNum = str(round(len(self.value) / len(self.bluff), 2))
            if valueNum[-1] == '0':
                valueNum = valueNum[0]
            bluffNum = '1'
        elif len(self.bluff) >= len(self.value) and len(self.value) != 0:
            valueNum = '1'
            bluffNum = str(round(len(self.bluff) / len(self.value), 2))
            if bluffNum[-1] == '0':
                bluffNum = bluffNum[0]
        else:
            valueNum = str(len(self.value))
            bluffNum = str(len(self.bluff))
        ratio_text = valueNum + ' : ' + bluffNum
        self.valueBluffRatio.setText(ratio_text)
        
        '''Update Continue Frequency'''
        if len(self.board) < 3 or self.totalCombos == 0:
            self.contFreqNum.setText('')
        else:
            contCombos = len(self.value) + len(self.bluff) + len(self.call)
            contFreq = round(contCombos / self.totalCombos * 100, 1)
            if contFreq.is_integer():
                contFreq = round(contFreq)
            self.contFreqNum.setText(str(contFreq) + '%')
        
        '''Update noActionLabel and totalCombosLabel'''
        if self.totalCombos != 0:
            noActionNum = str(len(self.noAction))
            noActionFreq = round(len(self.noAction) / self.totalCombos * 100, 1)
            if noActionFreq.is_integer():
                noActionFreq = round(noActionFreq)
            noActionNumText = 'Unassigned Combos:  ' + noActionNum + ' (' + str(noActionFreq) + '%' + ')'
            self.noActionLabel.setText(noActionNumText)
            
            totalCombosText = 'Total Combos:  ' + str(self.totalCombos)
            self.totalCombosLabel.setText(totalCombosText)
        else:
            self.noActionLabel.setText('Unassigned Combos:  0')
            self.totalCombosLabel.setText('Total Combos:  0')
        
        super().update()


class ActionButton(QtWidgets.QWidget):
    '''
    Value, Bluff, or Call Button.
    Used by ActionBuckets class.
    '''
    
    clicked = QtCore.pyqtSignal(str)
    
    def __init__(self, width, height, ol_w, action):
        super().__init__()
        
        self.selected = False
        self.action = action
        self.button = QtCore.QRect(ol_w, ol_w, width, height)
        self.outline = QtCore.QRect(0, 0, width + 2 * ol_w, height + 2 * ol_w)
        self.label = QtCore.QRect((width / 6), (height / 6), width * (2 / 3), height * (2 / 3))
        
        self.valueBrush = [255, 77, 77]
        self.bluffBrush = [255, 166, 166]
        self.callBrush = [103, 178, 45]
        self.outlineSelection = [153, 204, 255]
        
        self.labelSize = 16
        
        self.setMinimumSize(self.outline.width(), self.outline.height())
        
    def mouseReleaseEvent(self, e):
        
        self.selected = not self.selected
        self.clicked.emit(self.action)
    
    def paintEvent(self, e):
        
        painter = QtGui.QPainter(self)
        
        value = QtGui.QBrush()
        value.setColor(QtGui.QColor(self.valueBrush[0], self.valueBrush[1], self.valueBrush[2]))
        value.setStyle(Qt.SolidPattern)
        
        bluff = QtGui.QBrush()
        bluff.setColor(QtGui.QColor(self.bluffBrush[0], self.bluffBrush[1], self.bluffBrush[2]))
        bluff.setStyle(Qt.SolidPattern)
        
        call = QtGui.QBrush()
        call.setColor(QtGui.QColor(self.callBrush[0], self.callBrush[1], self.callBrush[2]))
        call.setStyle(Qt.SolidPattern)
        
        selected = QtGui.QBrush()
        selected.setColor(QtGui.QColor(self.outlineSelection[0], self.outlineSelection[1], self.outlineSelection[2]))
        selected.setStyle(Qt.SolidPattern)
        
        if self.selected:
            painter.fillRect(self.outline, selected)
            
        if self.action == 'Value':
            painter.fillRect(self.button, value)
        elif self.action == 'Bluff':
            painter.fillRect(self.button, bluff)
        else:
            painter.fillRect(self.button, call)
            
        painter.drawRect(self.button)
        
        font = QtGui.QFont()
        font.setPixelSize(self.labelSize)
        painter.setFont(font)
        
        painter.drawText(self.button, Qt.AlignCenter, self.action)


"""BOARD DISPLAY and associated Widgets"""

class BoardDisplay(QtWidgets.QWidget):
    '''
    Widget for selecting and displaying board cards.
    Used in PlayerWindow Widget.
    '''
    
    '''Signal for RangeStats to receive board card changes'''
    sendBoardCards = QtCore.pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        
        layout = QtWidgets.QGridLayout()
        
        flopSpacing = 0        # Column width between flop cards
        turnRiverSpacing = 10   # Column width between turn and river cards
        
        self.scale = .6  ### Size of Cards changed here ###
        
        self.board = []
        
        '''Add Labels to grid'''
        flopLabel = QtWidgets.QLabel('Flop')
        turnLabel = QtWidgets.QLabel('Turn')
        riverLabel = QtWidgets.QLabel('River')
        
        layout.addWidget(flopLabel, 0, 2, Qt.AlignCenter)
        layout.addWidget(turnLabel, 0, 6, Qt.AlignCenter)
        layout.addWidget(riverLabel, 0, 8, Qt.AlignCenter)
        
        '''Add Cards to GridLayout'''
        self.flop1 = BoardCard(self.scale)
        self.flop2 = BoardCard(self.scale)
        self.flop3 = BoardCard(self.scale)
        self.turn = BoardCard(self.scale)
        self.river = BoardCard(self.scale)
        
        layout.addWidget(self.flop1, 1, 0, Qt.AlignCenter)
        layout.addWidget(self.flop2, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.flop3, 1, 4, Qt.AlignCenter)
        layout.addWidget(self.turn, 1, 6, Qt.AlignCenter)
        layout.addWidget(self.river, 1, 8, Qt.AlignCenter)
        
        '''Set grid spacing'''
        layout.setColumnMinimumWidth(1, flopSpacing)
        layout.setColumnMinimumWidth(3, flopSpacing)
        layout.setColumnMinimumWidth(5, turnRiverSpacing)
        layout.setColumnMinimumWidth(7, turnRiverSpacing)
        
        '''Connect card click signals'''
        self.flop1.cardClicked.connect(self.onCardClick)
        self.flop2.cardClicked.connect(self.onCardClick)
        self.flop3.cardClicked.connect(self.onCardClick)
        self.turn.cardClicked.connect(self.onCardClick)
        self.river.cardClicked.connect(self.onCardClick)
        self.setLayout(layout)
        
        self.boardSelection = BoardSelection()
    
    def onCardClick(self):
        '''Update Dialog board cards with currently selected cards'''
        self.boardSelection.clear()
        self.boardSelection.board = self.board.copy()
        for card in self.boardSelection.board:
            self.boardSelection.switchSelection.emit(card)
        
        if self.boardSelection.exec():
            self.board = self.boardSelection.board
            self.sendBoardCards.emit(self.board)
            self.update()
    
    def update(self):
        
        '''Clear each card's rank and suit'''
        self.flop1.revealedCard = self.flop1.getCard(0, 4, self.scale)
        self.flop2.revealedCard = self.flop2.getCard(0, 4, self.scale)
        self.flop3.revealedCard = self.flop3.getCard(0, 4, self.scale)
        self.turn.revealedCard = self.turn.getCard(0, 4, self.scale)
        self.river.revealedCard = self.river.getCard(0, 4, self.scale)
        
        '''Update with New Rank and Suit'''
        if len(self.board) > 0:
            self.flop1.revealedCard = self.flop1.getCard(self.board[0][0], self.board[0][1], self.scale)
        if len(self.board) > 1:
            self.flop2.revealedCard = self.flop2.getCard(self.board[1][0], self.board[1][1], self.scale)
        if len(self.board) > 2:
            self.flop3.revealedCard = self.flop3.getCard(self.board[2][0], self.board[2][1], self.scale)
        if len(self.board) > 3:
            self.turn.revealedCard = self.turn.getCard(self.board[3][0], self.board[3][1], self.scale)
        if len(self.board) > 4:
            self.river.revealedCard = self.river.getCard(self.board[4][0], self.board[4][1], self.scale)    
        
        super().update()
    
    def paintEvent(self, e):
        '''For checking stack data'''
        pass


class BoardCard(QtWidgets.QWidget):
    '''
    A single card displayed in BoardDisplay or BoardSelection.
    '''
    
    cardClicked = QtCore.pyqtSignal(list)
    
    def __init__(self, scale, rank = 0, suit = 4):
        '''Rank is integer between 0 and 12 meaning 2 thru Ace.
        Suit is integer between 0 and 3 meaning h, d, c, s respectively'''
        super().__init__()
        
        self.selected = False  #  If selected, will be displayed with grey shading
        self.revealed = True  # If not revealed, will show card backside
        
        self.name = ''
        
        self.scale = scale
        
        self.rank = rank  
        self.suit = suit  # If suit is 4, card is 'blank' or unknown
        
        self.revealedCard = self.getCard(rank, suit, scale)
        
        self.selectRect = QtCore.QRect(0, 0, 81 * scale, 117 * scale)
        
        self.setMinimumSize(81 * scale + 1, 117 * scale + 1)
        
    def getCard(self, column, row, scale):
        '''
        Returns a scaled pixmap of the correct card to display
        Used during __init__
        '''
        
        card_col = 81 * column
        card_row = 117 * row        
        
        scaled_width = round(scale * 81, 0)
        scaled_height = round(scale * 117, 0)
        size = QtCore.QSize(scaled_width, scaled_height)
        
        card = QtGui.QPixmap('cards_sheet.gif')
        card1 = card.copy(card_col - 1, card_row - 1, 81 + 1, 117 + 1)
        
        return card1.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    def swtichSelection(self, card):
        if card[0] == self.rank and card[1] == self.suit:
            self.selected = not self.selected
        self.update()
    
    def mouseReleaseEvent(self, e):
        self.cardClicked.emit([self.rank, self.suit])
        
    def paintEvent(self, e):
        
        painter = QtGui.QPainter(self)
        
        selectedBrush = QtGui.QBrush()
        selectedBrush.setColor(QtGui.QColor(0, 0, 0))
        selectedBrush.setStyle(Qt.Dense4Pattern)        
        
        painter.drawPixmap(0, 0, self.revealedCard)
        
        if self.selected:
            painter.fillRect(self.selectRect, selectedBrush)
            
    
class BoardSelection(QtWidgets.QDialog):
    '''Dialog window that pops up to select board cards'''
    
    switchSelection = QtCore.pyqtSignal(list)
    
    def __init__(self, board=[]):
        super().__init__()
        
        self.setModal(True)
        self.setWindowTitle('Select Board Cards')
        self.resize(620, 325)
        
        scale = .57
        size = QtCore.QSize(round(scale * 1053, 0), round(scale * 1468, 0))
        
        layout = self.buildCardGrid(scale)
        layout.setSpacing(1)
        
        self.ok_button = QtWidgets.QPushButton("OK", self)
        self.ok_button.setDefault(True)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button, 4, 0, 4, 2, Qt.AlignLeft)
        
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setDefault(False)
        layout.addWidget(self.cancel_button, 4, 2, 4, 2, Qt.AlignLeft)
        
        self.clear_button = QtWidgets.QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear)
        layout.addWidget(self.clear_button, 4, 5, 4, 2, Qt.AlignLeft)
        
        self.random_flop_button = QtWidgets.QPushButton("Random Flop", self)
        self.random_flop_button.clicked.connect(self.random_flop)
        layout.addWidget(self.random_flop_button, 4, 7, 4, 2)
        
        self.random_turn_button = QtWidgets.QPushButton("Random Turn", self)
        self.random_turn_button.clicked.connect(self.random_turn)
        layout.addWidget(self.random_turn_button, 4, 9, 4, 2)
        
        self.random_river_button = QtWidgets.QPushButton("Random River", self)
        self.random_river_button.clicked.connect(self.random_river)
        layout.addWidget(self.random_river_button, 4, 11, 4, 2)
        
        self.board = board
        
        self.setLayout(layout)
    
    def reject(self):
        self.clear()
        super().reject()
        
    def buildCardGrid(self, scale):
        '''
        Constructs the 13 x 4 grid of all cards.
        Used during __init__
        '''
        
        layout = QtWidgets.QGridLayout()
        
        for i in range(4):
            for n in range(13):
                card = BoardCard(scale, n, i)
                card.cardClicked.connect(self.cardClicked)
                self.switchSelection.connect(card.swtichSelection)
                layout.addWidget(card, i, n)
        
        return layout
    
    def cardClicked(self, card):
        '''
        Slot for when a BoardCard is clicked and emits the card info.
        This function determines what to do next.
        card parameter needs to be a list of numebrs representing rank and suit:
        [0 thru 13, 0 thru 3]
        '''
        
        if card in self.board:
            self.board.remove(card)
            self.switchSelection.emit(card)
        elif len(self.board) < 5:
            self.board.append(card)
            self.switchSelection.emit(card)

    def clear(self):
        '''Unselects all cards'''
        
        for card in self.board:
            self.switchSelection.emit(card)
        self.board = []
    
    def random_card(self):
        '''Selects a random rank, suit and checks if that card exists
        in self.board.  If not, returns the card.'''
        
        while True:
            card = [randint(0, 12), randint(0, 3)]
            if card not in self.board:
                return card
    
    def random_flop(self):
        '''Clears the board selection and selects three random cards.'''
        
        self.clear()
        for i in range(3):
            card = self.random_card()
            self.board.append(card)
            self.switchSelection.emit(card)
    
    def random_turn(self):
        '''
        If no cards selected: chooses four random cards.
        If flop cards present, selects random fourth card.
        '''
        
        if len(self.board) == 0:
            for i in range(4):
                card = self.random_card()
                self.board.append(card)
                self.switchSelection.emit(card)
        elif len(self.board) == 3:
            card = self.random_card()
            self.board.append(card)
            self.switchSelection.emit(card)
        elif len(self.board) == 4:
            self.switchSelection.emit(self.board[-1])
            del self.board[-1]
            card = self.random_card()
            self.board.append(card)
            self.switchSelection.emit(card)
        elif len(self.board) == 5:
            for i in range(2):
                self.switchSelection.emit(self.board[-1])
                del self.board[-1]
            card = self.random_card()
            self.board.append(card)
            self.switchSelection.emit(card)
    
    def random_river(self):
        '''
        If no cards are selected, chooses five random cards:
        If flop present, chooses two random cards.
        if turn present, chooses one random card.
        '''
        
        if len(self.board) == 0:
            for i in range(5):
                card = self.random_card()
                self.board.append(card)
                self.switchSelection.emit(card)
        elif len(self.board) == 3:
            for i in range(2):
                card = self.random_card()
                self.board.append(card)
                self.switchSelection.emit(card)
        elif len(self.board) == 4:
            card = self.random_card()
            self.board.append(card)
            self.switchSelection.emit(card)
        elif len(self.board) == 5:
            self.switchSelection.emit(self.board[-1])
            del self.board[-1]
            card = self.random_card()
            self.board.append(card)
            self.switchSelection.emit(card)
        
"""COMBO WINDOW and Related Classes"""

class ComboWindow(QtWidgets.QWidget):
    '''Window that lists individual combos and allows the user to
    assign an action to each.'''
    
    def __init__(self):
        pass


"""Data Storage and Range Info Transfer Objects"""

class Combo():
    '''
    Individual Combo, i.e. AsTh
    Parameter cards are [rank, suit]
    Rank is integer 0 - 12, where 0 is 2 and 12 is Ace
    Suit is 0 - 3 where 0 = h, 1 = d, 2 = c, 3 = s
    '''
    
    def __init__(self, cardA = [], cardB = []):
        
        '''[rank 0 - 12, suit 0 - 3]'''
        self.cardA = cardA
        self.cardB = cardB
        
        self.comboRect = self.getComboRect()
        
        self.text = self.getText()  # String Name of the combo
        
        self.gridIndex = self.getGridIndex()  # Index location in the 169 item list of ComboRects
    
    def __hash__(self):
        
        return hash(self.text)
    
    def getComboRect(self):
        '''
        Determine which RangeMatrix ComboRect this combo belongs in.
        Returns a list of integers [col, row] where col and row are the column
        and row of its location in a RangeMatrix.'''
        
        comboRectText = ''
        
        rank_value = ["2", "3", "4", "5", "6", "7", "8",
                      "9", "T", "J", "Q", "K", "A"]
        suit_value = ['h', 'd', 'c', 's']
        
        if self.cardA[0] == self.cardB[0]:
            comboRectText += rank_value[self.cardA[0]]
            comboRectText += rank_value[self.cardB[0]]
        else:
            cardA = max(self.cardA[0], self.cardB[0])
            cardB = min(self.cardA[0], self.cardB[0])
            comboRectText += rank_value[cardA]
            comboRectText += rank_value[cardB]
            if self.cardA[1] == self.cardB[1]:
                comboRectText += 's'
            else:
                comboRectText += 'o'
        return comboRectText
    
    def getText(self):
        '''
        Returns text version of combo, i.e. 'Ah7c'
        '''
        rank_value = ["2", "3", "4", "5", "6", "7", "8",
                      "9", "T", "J", "Q", "K", "A"]
        suit_value = ['h', 'd', 'c', 's']
        
        cardA = rank_value[self.cardA[0]]
        cardA += suit_value[self.cardA[1]]
        
        cardB = rank_value[self.cardB[0]]
        cardB += suit_value[self.cardB[1]]
        
        if self.cardA[0] == self.cardB[0]:
            if self.cardA[1] < self.cardB[1]:
                return cardA + cardB
            else:
                return cardB + cardA
            
        elif self.cardA[0] < self.cardB[0]:
            return cardB + cardA
        else:
            return cardA + cardB
    
    def getGridIndex(self):
        '''
        Returns the Combo's Index location within 169 item list
        that represents the 13x13 range matrix.
        '''
        
        gridref = ['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s', 
                   'AKo', 'KK', 'KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s',
                   'AQo', 'KQo', 'QQ', 'QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s',
                   'AJo', 'KJo', 'QJo', 'JJ', 'JTs', 'J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'J4s', 'J3s', 'J2s',
                   'ATo', 'KTo', 'QTo', 'JTo', 'TT', 'T9s', 'T8s', 'T7s', 'T6s', 'T5s', 'T4s', 'T3s', 'T2s',
                   'A9o', 'K9o', 'Q9o', 'J9o', 'T9o', '99', '98s', '97s', '96s', '95s', '94s', '93s', '92s',
                   'A8o', 'K8o', 'Q8o', 'J8o', 'T8o', '98o', '88', '87s', '86s', '85s', '84s', '83s', '82s',
                   'A7o', 'K7o', 'Q7o', 'J7o', 'T7o', '97o', '87o', '77', '76s', '75s', '74s', '73s', '72s',
                   'A6o', 'K6o', 'Q6o', 'J6o', 'T6o', '96o', '86o', '76o', '66', '65s', '64s', '63s', '62s',
                   'A5o', 'K5o', 'Q5o', 'J5o', 'T5o', '95o', '85o', '75o', '65o', '55', '54s', '53s', '52s',
                   'A4o', 'K4o', 'Q4o', 'J4o', 'T4o', '94o', '84o', '74o', '64o', '54o', '44', '43s', '42s',
                   'A3o', 'K3o', 'Q3o', 'J3o', 'T3o', '93o', '83o', '73o', '63o', '53o', '43o', '33', '32s',
                   'A2o', 'K2o', 'Q2o', 'J2o', 'T2o', '92o', '82o', '72o', '62o', '52o', '42o', '32o', '22']
        
        return gridref.index(self.comboRect)