'''Unit Testing for ShufflezUI'''

import unittest
import ShufflezUI
import ShufflezWidgets
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

app = QtWidgets.QApplication(sys.argv)

class TestRangeWidgetMainReceiveUpdate(unittest.TestCase):
    
    def setUp(self):
        
        startingRange = '22+, A2s+, KQs, QJs, JTs, T9s, 98s, 87s, ATo+, KQo' # 210 combos
        value = 'TT+, AKs, AKo, AhQh, AdQd' # 48 combos
        bluff = 'AJs-A3s, Ah2h, As2s'  # 38 combos
        call = '99-22, KQs, QJs, JTs, T9s, 98s, 87s, AcQc, AsQs' # 74 combos
        noAction = 'AQo-ATo, KQo, Ad2d, Ac2c'  # 50 combos
        lockedCombos = 'JdJs, KhQh, Ad7d, AcQd, AcQh' # 5 combos
        
        self.player = ShufflezWidgets.RangeWidgetMain()
        
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
        
        combo2h2c = ShufflezWidgets.Combo([0, 0], [0, 2])   # Call
        comboAsKs = ShufflezWidgets.Combo([12, 3], [11, 3]) # Value
        comboAc3c = ShufflezWidgets.Combo([12, 2], [1, 2])  # Bluff
        comboKdQh = ShufflezWidgets.Combo([11, 1], [10, 0]) # noAction
        
        '''ACTION BUCKETS'''
        
        '''Value'''
        self.assertEqual(len(self.player.actionBuckets.value), 48)
        self.assertNotIn(combo2h2c, self.player.actionBuckets.value)
        self.assertIn(comboAsKs, self.player.actionBuckets.value)
        self.assertNotIn(comboAc3c, self.player.actionBuckets.value)
        self.assertNotIn(comboKdQh, self.player.actionBuckets.value)
        
        '''Bluff'''
        self.assertEqual(len(self.player.actionBuckets.bluff), 38)
        self.assertNotIn(combo2h2c, self.player.actionBuckets.bluff)
        self.assertNotIn(comboAsKs, self.player.actionBuckets.bluff)
        self.assertIn(comboAc3c, self.player.actionBuckets.bluff)
        self.assertNotIn(comboKdQh, self.player.actionBuckets.bluff)
        
        '''Call'''
        self.assertEqual(len(self.player.actionBuckets.call), 74)
        self.assertIn(combo2h2c, self.player.actionBuckets.call)
        self.assertNotIn(comboAsKs, self.player.actionBuckets.call)
        self.assertNotIn(comboAc3c, self.player.actionBuckets.call)
        self.assertNotIn(comboKdQh, self.player.actionBuckets.call)
        
        '''noAction'''
        self.assertEqual(len(self.player.actionBuckets.noAction), 50)
        self.assertNotIn(combo2h2c, self.player.actionBuckets.noAction)
        self.assertNotIn(comboAsKs, self.player.actionBuckets.noAction)
        self.assertNotIn(comboAc3c, self.player.actionBuckets.noAction)
        self.assertIn(comboKdQh, self.player.actionBuckets.noAction)
        
        '''RANGE DISPLAY'''
        
        self.assertEqual(len(self.player.rangeDisplay.startingCombos), 210)
        
        '''Value'''
        self.assertEqual(len(self.player.rangeDisplay.value), 48)
        self.assertNotIn(combo2h2c, self.player.rangeDisplay.value)
        self.assertIn(comboAsKs, self.player.rangeDisplay.value)
        self.assertNotIn(comboAc3c, self.player.rangeDisplay.value)
        self.assertNotIn(comboKdQh, self.player.rangeDisplay.value)
        
        '''Bluff'''
        self.assertEqual(len(self.player.rangeDisplay.bluff), 38)
        self.assertNotIn(combo2h2c, self.player.rangeDisplay.bluff)
        self.assertNotIn(comboAsKs, self.player.rangeDisplay.bluff)
        self.assertIn(comboAc3c, self.player.rangeDisplay.bluff)
        self.assertNotIn(comboKdQh, self.player.rangeDisplay.bluff)
        
        '''Call'''
        self.assertEqual(len(self.player.rangeDisplay.call), 74)
        self.assertIn(combo2h2c, self.player.rangeDisplay.call)
        self.assertNotIn(comboAsKs, self.player.rangeDisplay.call)
        self.assertNotIn(comboAc3c, self.player.rangeDisplay.call)
        self.assertNotIn(comboKdQh, self.player.rangeDisplay.call)
        
        '''noAction'''
        self.assertEqual(len(self.player.rangeDisplay.noAction), 50)
        self.assertNotIn(combo2h2c, self.player.rangeDisplay.noAction)
        self.assertNotIn(comboAsKs, self.player.rangeDisplay.noAction)
        self.assertNotIn(comboAc3c, self.player.rangeDisplay.noAction)
        self.assertIn(comboKdQh, self.player.rangeDisplay.noAction)
        
        '''RANGE STATS MAIN'''
        
        self.assertEqual(len(self.player.rangeStatsDisplay.rangeStatsMain.startingCombos), 210)
        
        '''Value'''
        self.assertEqual(len(self.player.rangeStatsDisplay.rangeStatsMain.value), 48)
        self.assertNotIn(combo2h2c, self.player.rangeStatsDisplay.rangeStatsMain.value)
        self.assertIn(comboAsKs, self.player.rangeStatsDisplay.rangeStatsMain.value)
        self.assertNotIn(comboAc3c, self.player.rangeStatsDisplay.rangeStatsMain.value)
        self.assertNotIn(comboKdQh, self.player.rangeStatsDisplay.rangeStatsMain.value)
        
        '''Bluff'''
        self.assertEqual(len(self.player.rangeStatsDisplay.rangeStatsMain.bluff), 38)
        self.assertNotIn(combo2h2c, self.player.rangeStatsDisplay.rangeStatsMain.bluff)
        self.assertNotIn(comboAsKs, self.player.rangeStatsDisplay.rangeStatsMain.bluff)
        self.assertIn(comboAc3c, self.player.rangeStatsDisplay.rangeStatsMain.bluff)
        self.assertNotIn(comboKdQh, self.player.rangeStatsDisplay.rangeStatsMain.bluff)
        
        '''Call'''
        self.assertEqual(len(self.player.rangeStatsDisplay.rangeStatsMain.call), 74)
        self.assertIn(combo2h2c, self.player.rangeStatsDisplay.rangeStatsMain.call)
        self.assertNotIn(comboAsKs, self.player.rangeStatsDisplay.rangeStatsMain.call)
        self.assertNotIn(comboAc3c, self.player.rangeStatsDisplay.rangeStatsMain.call)
        self.assertNotIn(comboKdQh, self.player.rangeStatsDisplay.rangeStatsMain.call)
        
        '''noAction'''
        self.assertEqual(len(self.player.rangeStatsDisplay.rangeStatsMain.noAction), 50)
        self.assertNotIn(combo2h2c, self.player.rangeStatsDisplay.rangeStatsMain.noAction)
        self.assertNotIn(comboAsKs, self.player.rangeStatsDisplay.rangeStatsMain.noAction)
        self.assertNotIn(comboAc3c, self.player.rangeStatsDisplay.rangeStatsMain.noAction)
        self.assertIn(comboKdQh, self.player.rangeStatsDisplay.rangeStatsMain.noAction)        
        
        