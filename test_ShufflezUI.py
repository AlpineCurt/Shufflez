'''Unit Testing for ShufflezUI'''

import unittest
import ShufflezUI
import ShufflezWidgets
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

app = QtWidgets.QApplication(sys.argv)

class TestPlayerWindowReceiveUpdate(unittest.TestCase):
    
    def setUp(self):
        
        startingRange = '22+, A2s+, KQs, QJs, JTs, T9s, 98s, 87s, ATo+, KQo'
        value = 'TT+, AKs, AKo, AhQh, AdQd'
        bluff = 'AJs-A3s, Ah2h, As2s'
        call = '99-22, KQs, QJs, JTs, T9s, 98s, 87s, AcQc, AsQs'
        noAction = 'AQo-ATo, KQo, Ad2d, Ac2c'
        lockedCombos = 'JdJs, KhQh, Ad7d, AcQd, AcQh'
        
        self.player = ShufflezUI.PlayerWindow()
        
        self.updatePack = ShufflezWidgets.UpdatePack()
        self.updatePack.origin = ''
        self.updatePack.value = ShufflezWidgets.RangeText.rangeToList(value)
        self.updatePack.bluff = ShufflezWidgets.RangeText.rangeToList(bluff)
        self.updatePack.call = ShufflezWidgets.RangeText.rangeToList(call)
        self.updatePack.noAction = ShufflezWidgets.RangeText.rangeToList(noAction)
        self.updatePack.startingCombos = ShufflezWidgets.RangeText.rangeToList(startingRange)
        self.updatePack.lockedCombos = ShufflezWidgets.RangeText.rangeToList(lockedCombos)
        self.updatePack.unlockedCombos = set()
        self.updatePack.lockStatus = False
        self.updatePack.preflopStatus = False
        self.updatePack.updateActionsOnly = False
        self.updatePack.selectedAction = ''
        self.updatePack.board = [[9, 1], [5, 0], [6, 1]]
    
    def test_setUp(self):
        '''setUp should be valid.'''
        
        self.assertTrue(self.updatePack.test_pass())
    
    def test_receiveUpdateFromGameHistory(self):
        
        self.updatePack.origin = 'GameHistory'
        self.player.receiveUpdate(self.updatePack)