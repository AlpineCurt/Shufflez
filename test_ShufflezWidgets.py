'''Unit Testing for ShufflezWidgets'''

import unittest
import ShufflezWidgets

class TestCombo(unittest.TestCase):
    
    def setUp(self):
        
        '''AhAd'''
        self.combo1 = ShufflezWidgets.Combo([12, 0], [12, 1])
        
        '''8c8h'''
        self.combo2 = ShufflezWidgets.Combo([6, 2], [6, 0])
        
        '''Th2h'''
        self.combo3 = ShufflezWidgets.Combo([8, 0], [0, 0])
        
        '''9c8c'''
        self.combo4 = ShufflezWidgets.Combo([7, 2], [6, 2])
        
        '''AhKs'''
        self.combo5 = ShufflezWidgets.Combo([12, 0], [11, 3])
        
        '''7c2d'''
        self.combo6 = ShufflezWidgets.Combo([5, 2], [0, 1])
        
        '''2d7c'''
        self.combo7 = ShufflezWidgets.Combo([0, 1], [5, 2])
    
    def test_findComboRect(self):
        '''Pocket pairs'''
        self.assertEqual(self.combo1.getComboRect(), 'AA')
        self.assertEqual(self.combo2.getComboRect(), '88')
        
        '''Suited Combos'''
        self.assertEqual(self.combo3.getComboRect(), 'T2s')
        self.assertEqual(self.combo4.getComboRect(), '98s')
        
        '''Offsuit Combos'''
        self.assertEqual(self.combo5.getComboRect(), 'AKo')
        self.assertEqual(self.combo6.getComboRect(), '72o')
    
    def test_text(self):
        self.assertEqual(self.combo1.getText(), 'AhAd')
        self.assertEqual(self.combo2.getText(), '8h8c')
        self.assertEqual(self.combo3.getText(), 'Th2h')
        self.assertEqual(self.combo4.getText(), '9c8c')
        self.assertEqual(self.combo5.getText(), 'AhKs')
        self.assertEqual(self.combo6.getText(), '7c2d')
        self.assertEqual(self.combo7.getText(), '7c2d')   