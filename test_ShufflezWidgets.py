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


class TestRangeText(unittest.TestCase):
        
    def test_PPConvert(self):
        
        inputString = 'KK+, JJ-88, 66-44, 22'
        comboSet = ShufflezWidgets.RangeText.rangeToList(inputString)
        
        self.assertEqual(len(comboSet), 60)
        
        '''These should be in the comboSet output'''
        combo1 = ShufflezWidgets.Combo([12, 0], [12, 1])  # AhAd
        combo2 = ShufflezWidgets.Combo([6, 2], [6, 0])    # 8c8h
        combo3 = ShufflezWidgets.Combo([11, 1], [11, 3])  # KdKs
        combo4 = ShufflezWidgets.Combo([8, 0], [8, 3])    # ThTs
        combo5 = ShufflezWidgets.Combo([7, 2], [7, 3])    # 9c9s
        combo6 = ShufflezWidgets.Combo([4, 0], [4, 2])    # 6h6c
        combo7 = ShufflezWidgets.Combo([2, 2], [2, 1])    # 4c4d
        combo8 = ShufflezWidgets.Combo([0, 1], [0, 3])    # 2d2s
        
        self.assertIn(combo1, comboSet)
        self.assertIn(combo2, comboSet)
        self.assertIn(combo3, comboSet)
        self.assertIn(combo4, comboSet)
        self.assertIn(combo5, comboSet)
        self.assertIn(combo6, comboSet)
        self.assertIn(combo7, comboSet)
        self.assertIn(combo8, comboSet)
        
        '''These should NOT be in comboSet output'''
        combo9 = ShufflezWidgets.Combo([10, 0], [10, 1])  # QhQd
        combo10 = ShufflezWidgets.Combo([5, 2], [5, 1])   # 7c7d
        combo11 = ShufflezWidgets.Combo([5, 2], [5, 3])   # 7c7s
        combo12 = ShufflezWidgets.Combo([1, 0], [1, 2])   # 3h3c
        
        self.assertNotIn(combo9, comboSet)
        self.assertNotIn(combo10, comboSet)
        self.assertNotIn(combo11, comboSet)
        self.assertNotIn(combo12, comboSet)
    
    def test_SuitedConvert(self):
        
        inputString = 'A6s+, KJs, K9s, K4s, QTs+, Q4s, J9s, J3s, 95s-93s, 74s, 64s-63s, 32s'
        comboSet = ShufflezWidgets.RangeText.rangeToList(inputString)
        
        self.assertEqual(len(comboSet), 92)
        
        '''These should be in the comboSet output'''
        combo1 = ShufflezWidgets.Combo([12, 0], [11, 0])  # AhKh
        combo2 = ShufflezWidgets.Combo([10, 1], [9, 1])   # QdJd
        combo3 = ShufflezWidgets.Combo([10, 2], [9, 2])   # QcJc
        combo4 = ShufflezWidgets.Combo([9, 3], [7, 3])    # Js9s
        combo5 = ShufflezWidgets.Combo([12, 1], [4, 1])   # Ad6d
        combo6 = ShufflezWidgets.Combo([9, 2], [1, 2])    # Jc3c
        combo7 = ShufflezWidgets.Combo([1, 0], [0, 0])    # 3h2h
        
        self.assertIn(combo1, comboSet)
        self.assertIn(combo2, comboSet)
        self.assertIn(combo3, comboSet)
        self.assertIn(combo4, comboSet)
        self.assertIn(combo5, comboSet)
        self.assertIn(combo6, comboSet)
        self.assertIn(combo7, comboSet)
        
        '''These should NOT be in comboSet output'''
        combo8 = ShufflezWidgets.Combo([8, 1], [7, 1])    # Td9d
        combo9 = ShufflezWidgets.Combo([1, 1], [0, 0])    # 3d2h
        combo10 = ShufflezWidgets.Combo([10, 0], [10, 1])  # QhQd
        combo11 = ShufflezWidgets.Combo([11, 3], [8, 3])  # KsTs
        combo12 = ShufflezWidgets.Combo([12, 0], [12, 1])  # AhAd
        combo13 = ShufflezWidgets.Combo([10, 1], [9, 3])   # QdJs
        
        self.assertNotIn(combo8, comboSet)
        self.assertNotIn(combo9, comboSet)
        self.assertNotIn(combo10, comboSet)
        self.assertNotIn(combo11, comboSet)
        self.assertNotIn(combo12, comboSet)
        self.assertNotIn(combo13, comboSet)
    
    def test_offsuitConvert(self):
        
        inputString = 'ATo+, K9o-K8o, QTo, Q7o-Q6o, J8o, J3o, T5o, T3o, 97o, 87o, 73o-72o, 64o, 42o'
        comboSet = ShufflezWidgets.RangeText.rangeToList(inputString)
        
        self.assertEqual(len(comboSet), 228)
        
        '''These should be in the comboSet output'''
        combo1 = ShufflezWidgets.Combo([12, 0], [11, 2])  # AhKd
        combo2 = ShufflezWidgets.Combo([12, 1], [10, 0])  # AdQh
        combo3 = ShufflezWidgets.Combo([12, 1], [10, 3])  # AdQs
        combo4 = ShufflezWidgets.Combo([11, 3], [6, 0])   # Ks8h
        combo5 = ShufflezWidgets.Combo([7, 2], [5, 0])    # 9c7h
        combo6 = ShufflezWidgets.Combo([8, 3], [1, 1])    # Ts3d
        combo7 = ShufflezWidgets.Combo([5, 1], [0, 2])    # 7h2c
        
        self.assertIn(combo1, comboSet)
        self.assertIn(combo2, comboSet)
        self.assertIn(combo3, comboSet)
        self.assertIn(combo4, comboSet)
        self.assertIn(combo5, comboSet)
        self.assertIn(combo6, comboSet)
        self.assertIn(combo7, comboSet)
        
        '''These should NOT be in comboSet output'''
        combo8 = ShufflezWidgets.Combo([8, 1], [7, 1])    # Td9d
        combo9 = ShufflezWidgets.Combo([1, 1], [0, 0])    # 3d2h
        combo10 = ShufflezWidgets.Combo([10, 0], [10, 1])  # QhQd
        combo11 = ShufflezWidgets.Combo([11, 3], [8, 3])  # KsTs
        combo12 = ShufflezWidgets.Combo([12, 0], [12, 1])  # AhAd
        combo13 = ShufflezWidgets.Combo([10, 1], [9, 3])   # QdJs
        combo14 = ShufflezWidgets.Combo([12, 0], [11, 0])  # AhKh
        combo15 = ShufflezWidgets.Combo([10, 1], [9, 1])   # QdJd
        combo16 = ShufflezWidgets.Combo([10, 2], [9, 2])   # QcJc
        combo17 = ShufflezWidgets.Combo([9, 3], [7, 3])    # Js9s
        combo18 = ShufflezWidgets.Combo([12, 1], [4, 1])   # Ad6d
        combo19 = ShufflezWidgets.Combo([9, 2], [1, 2])    # Jc3c
        combo20 = ShufflezWidgets.Combo([1, 0], [0, 0])    # 3h2h
        combo21 = ShufflezWidgets.Combo([10, 0], [10, 1])  # QhQd
        combo22 = ShufflezWidgets.Combo([5, 2], [5, 1])   # 7c7d
        combo23 = ShufflezWidgets.Combo([5, 2], [5, 3])   # 7c7s
        combo24 = ShufflezWidgets.Combo([1, 0], [1, 2])   # 3h3c
        combo25 = ShufflezWidgets.Combo([11, 0], [10, 2])   # KhQc
        combo26 = ShufflezWidgets.Combo([4, 1], [3, 0])   # 6d5h
        
        
        self.assertNotIn(combo8, comboSet)
        self.assertNotIn(combo9, comboSet)
        self.assertNotIn(combo10, comboSet)
        self.assertNotIn(combo11, comboSet)
        self.assertNotIn(combo12, comboSet)
        self.assertNotIn(combo13, comboSet)
        self.assertNotIn(combo14, comboSet) 
        self.assertNotIn(combo15, comboSet) 
        self.assertNotIn(combo16, comboSet) 
        self.assertNotIn(combo17, comboSet) 
        self.assertNotIn(combo18, comboSet) 
        self.assertNotIn(combo19, comboSet) 
        self.assertNotIn(combo20, comboSet) 
        self.assertNotIn(combo21, comboSet) 
        self.assertNotIn(combo22, comboSet) 
        self.assertNotIn(combo23, comboSet) 
        self.assertNotIn(combo24, comboSet) 
        self.assertNotIn(combo25, comboSet) 
        self.assertNotIn(combo26, comboSet)
    
    def test_SingleComboConvert(self):
        
        inputString = '5d5s,Jh7h,Ts7d'
        comboSet = ShufflezWidgets.RangeText.rangeToList(inputString)
        
        self.assertEqual(len(comboSet), 3)
        
        '''These should be in the comboSet output'''
        combo1 = ShufflezWidgets.Combo([3, 1], [3, 3])  # 5d5s
        combo2 = ShufflezWidgets.Combo([9, 0], [5, 0])  # Jh7h
        combo3 = ShufflezWidgets.Combo([8, 3], [5, 1])  # Ts7d
        
        self.assertIn(combo1, comboSet)
        self.assertIn(combo2, comboSet)
        self.assertIn(combo3, comboSet)
        
        '''These should NOT be in comboSet output'''
        combo4 = ShufflezWidgets.Combo([8, 1], [7, 1])    # Td9d
        combo5 = ShufflezWidgets.Combo([1, 1], [0, 0])    # 3d2h
        combo6 = ShufflezWidgets.Combo([10, 0], [10, 1])  # QhQd
        combo7 = ShufflezWidgets.Combo([11, 3], [8, 3])  # KsTs
        combo8 = ShufflezWidgets.Combo([12, 0], [12, 1])  # AhAd
        
        self.assertNotIn(combo4, comboSet)
        self.assertNotIn(combo5, comboSet)
        self.assertNotIn(combo6, comboSet)
        self.assertNotIn(combo7, comboSet)
        self.assertNotIn(combo8, comboSet)
    
    def test_CombinedRange(self):
        
        inputString = '22+, A2s+, K8s+, Q8s+, J9s+, T8s+, 97s+, 87s, 76s, 65s, 54s, A9o+, KJo+, QJo'
        comboSet = ShufflezWidgets.RangeText.rangeToList(inputString)
        
        self.assertEqual(len(comboSet), 298)
        
        '''These should be in the comboSet output'''
        combo1 = ShufflezWidgets.Combo([12, 0], [11, 2])  # AhKd
        combo2 = ShufflezWidgets.Combo([12, 1], [10, 0])  # AdQh
        combo3 = ShufflezWidgets.Combo([12, 1], [10, 3])  # AdQs
        combo4 = ShufflezWidgets.Combo([12, 0], [11, 0])  # AhKh
        combo5 = ShufflezWidgets.Combo([10, 1], [9, 1])   # QdJd
        combo6 = ShufflezWidgets.Combo([10, 2], [9, 2])   # QcJc
        combo7 = ShufflezWidgets.Combo([9, 3], [7, 3])    # Js9s
        combo8 = ShufflezWidgets.Combo([12, 1], [4, 1])   # Ad6d
        combo9 = ShufflezWidgets.Combo([12, 0], [12, 1])  # AhAd
        combo10 = ShufflezWidgets.Combo([6, 2], [6, 0])    # 8c8h
        combo11 = ShufflezWidgets.Combo([11, 1], [11, 3])  # KdKs
        combo12 = ShufflezWidgets.Combo([8, 0], [8, 3])    # ThTs
        combo13 = ShufflezWidgets.Combo([7, 2], [7, 3])    # 9c9s
        combo14 = ShufflezWidgets.Combo([4, 0], [4, 2])    # 6h6c
        combo15 = ShufflezWidgets.Combo([2, 2], [2, 1])    # 4c4d
        combo16 = ShufflezWidgets.Combo([0, 1], [0, 3])    # 2d2s
        
        self.assertIn(combo1, comboSet)
        self.assertIn(combo2, comboSet)
        self.assertIn(combo3, comboSet)
        self.assertIn(combo4, comboSet)
        self.assertIn(combo5, comboSet)
        self.assertIn(combo6, comboSet)
        self.assertIn(combo7, comboSet)
        self.assertIn(combo8, comboSet)
        self.assertIn(combo9, comboSet)
        self.assertIn(combo10, comboSet)
        self.assertIn(combo11, comboSet)
        self.assertIn(combo12, comboSet)
        self.assertIn(combo13, comboSet)
        self.assertIn(combo14, comboSet)
        self.assertIn(combo15, comboSet)
        self.assertIn(combo16, comboSet)
        
        '''These should NOT be in comboSet output'''
        combo17 = ShufflezWidgets.Combo([8, 1], [7, 3])    # Td9s
        combo18 = ShufflezWidgets.Combo([1, 1], [0, 0])    # 3d2h
        combo19 = ShufflezWidgets.Combo([4, 1], [3, 0])   # 6d5h
        combo20 = ShufflezWidgets.Combo([5, 1], [0, 2])    # 7h2c
        combo21 = ShufflezWidgets.Combo([9, 2], [1, 2])    # Jc3c
        combo22 = ShufflezWidgets.Combo([1, 0], [0, 0])    # 3h2h
        
        self.assertNotIn(combo17, comboSet)
        self.assertNotIn(combo18, comboSet)
        self.assertNotIn(combo19, comboSet)
        self.assertNotIn(combo20, comboSet)
        self.assertNotIn(combo21, comboSet)
        self.assertNotIn(combo22, comboSet)


class TestUpdatePack(unittest.TestCase):
    
    def setUp(self):
        
        self.updatePack = ShufflezWidgets.UpdatePack()
        
        startingCombos = '22+, AQs+, A5s-A2s, KTs+, QTs+, JTs, T9s, 98s, 87s, AQo+'
        self.updatePack.startingCombos = ShufflezWidgets.RangeText.rangeToList(startingCombos)
        value = 'TT+, AQs+, AQo+'
        self.updatePack.value = ShufflezWidgets.RangeText.rangeToList(value)
        bluff = 'A5s-A2s'
        self.updatePack.bluff = ShufflezWidgets.RangeText.rangeToList(bluff)
        call = '99-22'
        self.updatePack.call = ShufflezWidgets.RangeText.rangeToList(call)
        noAction = 'KTs+, QTs+, JTs, T9s, 98s, 87s'
        self.updatePack.noAction = ShufflezWidgets.RangeText.rangeToList(noAction)        
    
    def test_pass(self):
        '''setUp case is a valid UpdatePack'''
        self.assertTrue(self.updatePack.test_pass())
    
    def test_fail1(self):
        value = 'TT+, AQs+, AQo+, J8o'
        self.updatePack.value = ShufflezWidgets.RangeText.rangeToList(value)
        '''Value range contains combos not in startingCombos'''
        self.assertFalse(self.updatePack.test_pass())
    
    def test_fail2(self):
        bluff = 'A6s-A2s'
        self.updatePack.bluff = ShufflezWidgets.RangeText.rangeToList(bluff)
        '''Bluff range contains combos not in startingCombos'''
        self.assertFalse(self.updatePack.test_pass())
    
    def test_fail3(self):
        call = '32s'
        self.updatePack.call = ShufflezWidgets.RangeText.rangeToList(call)
        '''Call range contains combos not in startingCombos'''
        self.assertFalse(self.updatePack.test_pass())
        
    def test_fail4(self):
        noAction = 'KTs+, QTs+, JTs, T9s, 98s, 87s, 85s'
        self.updatePack.noAction = ShufflezWidgets.RangeText.rangeToList(noAction)
        '''noAction range contains combos not in startingCombos'''
        self.assertFalse(self.updatePack.test_pass())
    
    def test_fail5(self):
        bluff = 'AQs, A5s-A2s'
        self.updatePack.bluff = ShufflezWidgets.RangeText.rangeToList(bluff)
        '''Bluff range contains combos also in value range'''
        self.assertFalse(self.updatePack.test_pass())
    
    def test_fail6(self):
        call = 'AA, 99-22'
        self.updatePack.call = ShufflezWidgets.RangeText.rangeToList(call)
        '''Call range contains combos also in value range'''
        self.assertFalse(self.updatePack.test_pass())
    
    def test_fail7(self):
        noAction = 'KTs+, QTs+, JTs, T9s, 98s, 87s, AhAs'
        self.updatePack.noAction = ShufflezWidgets.RangeText.rangeToList(noAction)
        '''noAction range contains combos also in value range'''
        self.assertFalse(self.updatePack.test_pass())
    
    def test_fail8(self):
        call = '99-22, Ah2h'
        self.updatePack.call = ShufflezWidgets.RangeText.rangeToList(call)
        '''Call range contains combos also in bluff range'''
        self.assertFalse(self.updatePack.test_pass())
    
    def test_fail9(self):
        noAction = 'KTs+, QTs+, JTs, T9s, 98s, 87s, As4s'
        self.updatePack.noAction = ShufflezWidgets.RangeText.rangeToList(noAction)
        '''noAction range contains combos also in bluff range'''
        self.assertFalse(self.updatePack.test_pass())
    
    def test_fail10(self):
        noAction = 'KTs+, QTs+, JTs, T9s, 98s, 87s, 3d3c'
        self.updatePack.noAction = ShufflezWidgets.RangeText.rangeToList(noAction)
        '''noAction range contains combos also in call range'''
        self.assertFalse(self.updatePack.test_pass())
        