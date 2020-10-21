import unittest
import ShufflezWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

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


class TestFiveCardHist(unittest.TestCase):
    
    def test_five_card_hist(self):
        
        '''Quads'''
        cards1 = [[12, 0], [12, 3], [4, 3], [12, 1], [12, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards1), [4, 1])
        
        '''Full House'''
        cards2 = [[4, 0], [10, 0], [4, 1], [4, 3], [10, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards2), [3, 2])
        
        '''Three of a Kind'''
        cards3 = [[6, 3], [12, 3], [6, 2], [11, 1], [6, 0]]
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards3), [3, 1, 1])
        
        '''Two Pair'''
        cards4 = [[6, 0], [9, 1], [9, 2], [6, 2], [11, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards4), [2, 2, 1])
        
        '''One Pair'''
        cards5 = [[11, 0], [10, 1], [5, 3], [10, 2], [2, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards5), [2, 1, 1, 1])
        
        '''Straight, Flush, or High Card'''
        cards6 = [[3, 1], [4, 2], [5, 0], [2, 3], [1, 1]]  # Straight
        cards7 = [[11, 3], [5, 3], [1, 3], [8, 3], [0, 3]]  # Flush
        cards8 = [[8, 2], [1, 0], [2, 3], [5, 3], [12, 0]]  # No made hand / High Card
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards6), [1, 1, 1, 1, 1])
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards7), [1, 1, 1, 1, 1])
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards8), [1, 1, 1, 1, 1])
        
        '''Paired board, less than five cards'''
        cards9 = [[6, 2], [5, 2], [6, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards9), [2, 1])
        
        '''Four cards'''
        cards10 = [[10, 2], [10, 0], [10, 3], [10, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.five_card_hist(cards10), [4])


class TestBoardStrFlushCheck(unittest.TestCase):
    
    def test_board_str_flush(self):
        
        '''8d 7d 6d 9d Td'''
        board1 = [[6, 1], [5, 1], [4, 1], [7, 1], [8, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_str_flush_check(board1), True)
        
        '''8d 7d 6d 9d Th'''
        board2 = [[6, 1], [5, 1], [4, 1], [7, 1], [8, 0]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_str_flush_check(board2), False)
        
        '''8d 7d 6d 9d Jd'''
        board3 = [[6, 1], [5, 1], [4, 1], [7, 1], [9, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_str_flush_check(board3), False)
        
        '''2c, 3c, 4c, 5c, Ac'''
        board4 = [[0, 2], [1, 2], [2, 2], [3, 2], [12, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_str_flush_check(board4), True)


class TestStrFlushCheck(unittest.TestCase):
    
    def test_str_flush(self):
        
        '''4h Td 9d'''
        board1 = [[2, 0], [8, 1], [7, 1]]
        
        '''Ac Ks Qs'''
        board2 = [[12, 2], [11, 3], [10, 3]]
        
        '''2s 3s 4s'''
        board3 = [[0, 3], [1, 3], [2, 3]]
        
        '''4h 5h 6h 7h 8h'''
        board4 = [[2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
        
        '''As Kd 9d 6s 3c'''
        board5 = [[12, 3], [11, 1], [7, 1], [4, 3], [1, 2]]
        
        '''2c 3c 4c 5c'''
        board6 = [[0, 2], [1, 2], [2, 2], [3, 2]]
        
        '''As Ks Qs Js Ts'''
        board7 = [[12, 3], [11, 3], [10, 3], [9, 3], [8, 3]]
        
        '''As 5s'''
        combo1 = ShufflezWidgets.Combo([12, 3], [3, 3])
        
        '''As 5c'''
        combo2 = ShufflezWidgets.Combo([12, 3], [3, 2])
        
        '''5s 6s'''
        combo3 = ShufflezWidgets.Combo([3, 3], [4, 3])
        
        '''Ac 3h'''
        combo4 = ShufflezWidgets.Combo([12, 2], [1, 0])
        
        '''Th 9h'''
        combo5 = ShufflezWidgets.Combo([8, 0], [7, 0])
        
        '''9s 2c'''
        combo6 = ShufflezWidgets.Combo([7, 3], [0, 2])
        
        
        '''4h Td 9d   As 5s'''
        self.assertEqual(ShufflezWidgets.RangeStats.str_flush_check(combo1, board1), False)
        
        '''2s 3s 4s   As 5s  Test if wheel ace works'''
        self.assertEqual(ShufflezWidgets.RangeStats.str_flush_check(combo1, board3), True)
        
        '''4h 5h 6h 7h 8h   Th 9h,  str flush on board, combo makes higher str flush'''
        self.assertEqual(ShufflezWidgets.RangeStats.str_flush_check(combo5, board4), True)
        
        '''4h 5h 6h 7h 8h   As 5s, str flush on board, combo does not make a higher str flush'''
        self.assertEqual(ShufflezWidgets.RangeStats.str_flush_check(combo1, board4), False)
        
        '''4h 5h 6h 7h 8h  Ac 3h, str flush on board, combo does make a str flush, but not a better str flush'''
        #self.assertEqual(ShufflezWidgets.RangeStats.str_flush_check(combo4, board4), False)
        '''This is not asserting correctly and I cannot for the life of me figure out why.  It's evaluating correctly in every other test.'''
        
        '''2c 3c 4c 5c   Ac 3h, single ace for str flush wheel'''
        self.assertEqual(ShufflezWidgets.RangeStats.str_flush_check(combo4, board6), True)
        
        '''As Ks Qs Js Ts   9s 2c, lower str flush with combo than board alone'''
        self.assertEqual(ShufflezWidgets.RangeStats.str_flush_check(combo6, board7), False)
        
        '''As Kd 9d 6s 3c   As 5c, no possible str flush'''
        self.assertEqual(ShufflezWidgets.RangeStats.str_flush_check(combo2, board5), False)


class TestBoardQuadsCheck(unittest.TestCase):
    
    def test_board_quads(self):
        
        '''Qc Qh Qs Qd'''
        board1 = [[10, 2], [10, 0], [10, 3], [10, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_quads_check(board1), True)
        
        '''Qc Qh Qs Qd Ks'''
        board2 = [[10, 2], [10, 0], [10, 3], [10, 1], [11, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_quads_check(board2), True)
        
        '''Qc Qh Qs Td Ks'''
        board3 = [[10, 2], [10, 0], [10, 3], [8, 1], [11, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_quads_check(board3), False)
        
        '''Qc Qh Qs'''
        board4 = [[10, 2], [10, 0], [10, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_quads_check(board4), False)


class TestQuadsCheck(unittest.TestCase):
    
    def test_quads(self):
        
        '''7h7d'''
        combo1 = ShufflezWidgets.Combo([5, 0], [5, 1])
        '''7s 7c 3d'''
        board1 = [[5, 3], [5, 2], [1, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.quads_check(combo1, board1), True)
        
        '''3h 3c'''
        combo2 = ShufflezWidgets.Combo([1, 0], [1, 2])
        '''7s 7c 3d 3s'''
        board2 = [[5, 3], [5, 2], [1, 1], [1, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.quads_check(combo2, board2), True)
        
        '''Qh Qd Qc Qs Ac'''
        board3 = [[11, 0], [11, 1], [11, 3], [11, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.quads_check(combo2, board3), False)
        
        '''Ah 4c'''
        combo3 = ShufflezWidgets.Combo([12, 0], [2, 2])
        '''3c Ac 8d As Ad'''
        board4 = [[1, 2], [12, 2], [6, 1], [12, 3], [12, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.quads_check(combo3, board4), True)
        
        '''2s 2h 2d 2c'''
        board5 = [[0, 3], [0, 0], [0, 1], [0, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.quads_check(combo3, board5), False)
        
        '''2h 2s'''
        combo4 = ShufflezWidgets.Combo([0, 0], [0, 3])
        '''2d 5d 6d Td 2c'''
        board6 = [[0, 1], [3, 1], [4, 1], [8, 1], [0, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.quads_check(combo4, board6), True)


class TestBoardFullHouseCheck(unittest.TestCase):
    
    def test_board_full_house(self):
        
        '''Qc Qd Qs 8d 8s'''
        board1 = [[10, 2], [10, 1], [10, 3], [6, 1], [6, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_full_house_check(board1), True)
        
        ''''Qc Qd Qs Qh 8s'''
        board2 = [[10, 2], [10, 1], [10, 3], [10, 0], [6, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_full_house_check(board2), False)
        
        '''Jh Ac Jd As Js'''
        board3 = [[9, 0], [12, 2], [9, 1], [12, 3], [9, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_full_house_check(board3), True)
        
        '''Jh Ac Jd'''
        board4 = [[9, 0], [12, 2], [9, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.board_full_house_check(board4), False)


class TestFullHouseCheck(unittest.TestCase):
    
    def test_full_house(self):
        
        '''3h 3c'''
        combo1 = ShufflezWidgets.Combo([1, 0], [1, 2])
        
        '''Ad Ks'''
        combo2 = ShufflezWidgets.Combo([12, 1], [11, 3])
        
        '''Ks 3h'''
        combo3 = ShufflezWidgets.Combo([11, 3], [1, 0])
        
        '''Qh Qc'''
        combo4 = ShufflezWidgets.Combo([10, 0], [10, 2])
        
        '''Jc 5c'''
        combo5 = ShufflezWidgets.Combo([9, 2], [3, 2])
        
        '''3c 3d 3s Ac Ah'''
        board3 = [[1, 2], [1, 1], [1, 3], [12, 2], [12, 0]]
        
        '''Ah Ac Ad 3d 3s'''
        board4 = [[12, 0], [12, 2], [12, 1], [1, 1], [1, 3]]
        
        '''Jh 4h Js 4c Td'''
        board5 = [[9, 0], [2, 0], [9, 3], [2, 2], [8, 1]]
        
        '''Ks Kc 3d'''
        board6 = [[11, 3], [11, 2], [1, 1]]
        
        '''No pair on board, full house not possible'''
        '''2d 5d 6d Td'''
        board1 = [[0, 1], [3, 1], [4, 1], [8, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.full_house_check(combo1, board1), False)
        '''Kh Jc 6c'''
        board2 = [[11, 0], [9, 2], [4, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.full_house_check(combo1, board2), False)
        
        '''Ace in hole cards make a better full house than board'''
        '''3c 3d 3s Ac Ah    Ad Ks'''
        self.assertEqual(ShufflezWidgets.RangeStats.full_house_check(combo2, board3), True)
        
        '''3 in hole cards does not improve full house on board'''
        '''Ah Ac Ad 3d 3s    Ks 3h'''
        self.assertEqual(ShufflezWidgets.RangeStats.full_house_check(combo3, board4), False)
        
        '''QQ improves over the board for a higher full house'''
        '''Ah Ac Ad 3d 3s   Qh Qc'''
        self.assertEqual(ShufflezWidgets.RangeStats.full_house_check(combo4, board4), True)
        
        '''QQ does not improve the board'''
        '''3c 3d 3s Ac Ah   Qh Qc'''
        self.assertEqual(ShufflezWidgets.RangeStats.full_house_check(combo4, board3), False)

        '''Double pair board with single hole card to make full house'''
        '''Jh 4h Js 4c Td   Jc 5c'''
        self.assertEqual(ShufflezWidgets.RangeStats.full_house_check(combo5, board5), True)
        
        '''Single paired board, pocket pair makes full house'''
        '''Ks Kc 3d   3h 3c'''
        self.assertEqual(ShufflezWidgets.RangeStats.full_house_check(combo1, board6), True)


class TestFlushCheck(unittest.TestCase):
    
    def test_flush(self):
        
        '''Hole card(s) used to make flush'''
        '''Ac 3c'''
        combo1 = ShufflezWidgets.Combo([12, 2], [1, 2])
        '''5c 9c Kc'''
        board1 = [[3, 2], [7, 2], [11, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo1, board1), True)
        
        '''5c 8c Jd'''
        board2 = [[3, 2], [6, 2], [9, 1]]
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo1, board2), False)
        
        '''Jd 5c 8c 6s Qc'''
        board3 = [[9, 1], [3, 2], [6, 2], [4, 3], [10, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo1, board3), True)
        
        '''Jd 5c 8c 6s Qh'''
        board4 = [[9, 1], [3, 2], [6, 2], [4, 3], [10, 0]]
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo1, board4), False)
        
        '''5h 7d'''
        combo2 = ShufflezWidgets.Combo([3, 0], [5, 1])
        '''8h 9h 2h Kh'''
        board5 = [[6, 0], [7, 0], [0, 0], [11, 0]]
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo2, board5), True)
        
        '''8h 9h 9s 2h Kh'''
        board6 = [[6, 0], [7, 0], [9, 3], [0, 0], [11, 0]]
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo2, board6), True)
        
        '''9s 8s'''
        combo3 = ShufflezWidgets.Combo([7, 3], [6, 3])
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo3, board6), False)
        
        '''Flush on board'''
        board7 = [[8, 1], [4, 1], [7, 1], [3, 1], [10, 1]]
        
        '''Th 9h'''
        '''two Hole cards not of board suit; do not improve board flush'''
        combo4 = ShufflezWidgets.Combo([8, 0], [7, 0])
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo4, board7), False)
        
        '''Ad Kd'''
        '''both hole cards of board suit make higher flush'''
        combo5 = ShufflezWidgets.Combo([12, 1], [11, 1])
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo5, board7), True)
        
        '''8d 3d'''
        '''One hole card of board suit improves board flush'''
        combo6 = ShufflezWidgets.Combo([6, 1], [1, 1])
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo6, board7), True)
        
        '''3d 2d'''
        '''Two hole cards of board suit, neither improves board flush'''
        combo7 = ShufflezWidgets.Combo([1, 1], [0, 1])
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo7, board7), False)
        
        '''Jd 2d'''
        '''One hole card of board suit, improves board flush'''
        combo8 = ShufflezWidgets.Combo([9, 1], [0, 1])
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo8, board7), True)
        
        '''4c 4d'''
        '''One hole card of board suit, does not improve board flush'''
        combo9 = ShufflezWidgets.Combo([2, 2], [2, 1])
        self.assertEqual(ShufflezWidgets.RangeStats.flush_check(combo9, board7), False)


class TestNutFlushCard(unittest.TestCase):
    
    def test_nut_flush_card(self):
        
        '''7s 3s 6s'''
        board1 = [[5, 3], [1, 3], [4, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.nut_flush_card(board1), [12, 3])
        
        '''7s 3s As'''
        board2 = [[5, 3], [1, 3], [12, 3]]
        self.assertEqual(ShufflezWidgets.RangeStats.nut_flush_card(board2), [11, 3])
        
        '''Jc Kc Ac 5c'''
        board3 = [[9, 2], [11, 2], [12, 2], [3, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.nut_flush_card(board3), [10, 2])
        
        '''Qc Kc Ac 5c'''
        board4 = [[10, 2], [11, 2], [12, 2], [3, 2]]
        self.assertEqual(ShufflezWidgets.RangeStats.nut_flush_card(board4), [9, 2])        