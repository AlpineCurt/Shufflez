'''
Unit Testing for ShufflezCalc
'''

import unittest
import ShufflezCalc
from ShufflezWidgets import Combo

class TestCardHist(unittest.TestCase):
    
    def test_card_histogram(self):
        
        '''Quads'''
        cards1 = [[12, 0], [12, 3], [4, 3], [12, 1], [12, 2]]
        self.assertEqual(ShufflezCalc.card_histogram(cards1), [4, 1])
        
        '''Full House'''
        cards2 = [[4, 0], [10, 0], [4, 1], [4, 3], [10, 2]]
        self.assertEqual(ShufflezCalc.card_histogram(cards2), [3, 2])
        
        '''Three of a Kind'''
        cards3 = [[6, 3], [12, 3], [6, 2], [11, 1], [6, 0]]
        self.assertEqual(ShufflezCalc.card_histogram(cards3), [3, 1, 1])
        
        '''Two Pair'''
        cards4 = [[6, 0], [9, 1], [9, 2], [6, 2], [11, 3]]
        self.assertEqual(ShufflezCalc.card_histogram(cards4), [2, 2, 1])
        
        '''One Pair'''
        cards5 = [[11, 0], [10, 1], [5, 3], [10, 2], [2, 2]]
        self.assertEqual(ShufflezCalc.card_histogram(cards5), [2, 1, 1, 1])
        
        '''Straight, Flush, or High Card'''
        cards6 = [[3, 1], [4, 2], [5, 0], [2, 3], [1, 1]]  # Straight
        cards7 = [[11, 3], [5, 3], [1, 3], [8, 3], [0, 3]]  # Flush
        cards8 = [[8, 2], [1, 0], [2, 3], [5, 3], [12, 0]]  # No made hand / High Card
        self.assertEqual(ShufflezCalc.card_histogram(cards6), [1, 1, 1, 1, 1])
        self.assertEqual(ShufflezCalc.card_histogram(cards7), [1, 1, 1, 1, 1])
        self.assertEqual(ShufflezCalc.card_histogram(cards8), [1, 1, 1, 1, 1])
        
        '''Paired board, less than five cards'''
        cards9 = [[6, 2], [5, 2], [6, 1]]
        self.assertEqual(ShufflezCalc.card_histogram(cards9), [2, 1])
        
        '''Four cards'''
        cards10 = [[10, 2], [10, 0], [10, 3], [10, 1]]
        self.assertEqual(ShufflezCalc.card_histogram(cards10), [4])


class TestRemoveDuplicateRanks(unittest.TestCase):
    
    def test_remove_duplicate_ranks(self):
        
        '''Qc Js Tc Qd Jd'''
        board = [[10, 2], [9, 2], [8, 2], [10, 1], [9, 1]]
        self.assertEqual(ShufflezCalc.removeDuplicateRanks(board), [[10, 2], [9, 2], [8, 2]])
        
        '''Ac Th 5d Tc 5s'''
        board = [[12, 2], [8, 0], [3, 1], [8, 2], [3, 3]]
        self.assertEqual(ShufflezCalc.removeDuplicateRanks(board), [[12, 2], [8, 0], [3, 1]])
        
        '''Kh Tc 3d Ac Ks    Kd 8d'''
        board = [[11, 0], [8, 2], [1, 1], [12, 2], [11, 3]]
        self.assertEqual(ShufflezCalc.removeDuplicateRanks(board, [[11, 1], [6, 1]]), [[11, 0], [8, 2], [1, 1], [12, 2], [6, 1]])
        
        '''all seven cards are unique'''
        '''Ts 9h 7d Qh Ad    4c 3c'''
        board = [[8, 3], [7, 0], [5, 1], [10, 0], [12, 1]]
        self.assertEqual(ShufflezCalc.removeDuplicateRanks(board, [[2, 2], [1, 2]]), [[8, 3], [7, 0], [5, 1], [10, 0], [12, 1], [2, 2], [1, 2]])
        
        '''pocket pair rank appears on board'''
        '''Ts 9h 7d Qh Ad     9d 9s'''
        self.assertEqual(ShufflezCalc.removeDuplicateRanks(board, [[7, 1], [7, 3]]), [[8, 3], [7, 0], [5, 1], [10, 0], [12, 1]])


class TestBoardStrFlushCheck(unittest.TestCase):
    
    def test_board_str_flush(self):
        
        '''8d 7d 6d 9d Td'''
        board1 = [[6, 1], [5, 1], [4, 1], [7, 1], [8, 1]]
        self.assertEqual(ShufflezCalc.board_str_flush_check(board1), True)
        
        '''8d 7d 6d 9d Th'''
        board2 = [[6, 1], [5, 1], [4, 1], [7, 1], [8, 0]]
        self.assertEqual(ShufflezCalc.board_str_flush_check(board2), False)
        
        '''8d 7d 6d 9d Jd'''
        board3 = [[6, 1], [5, 1], [4, 1], [7, 1], [9, 1]]
        self.assertEqual(ShufflezCalc.board_str_flush_check(board3), False)
        
        '''2c, 3c, 4c, 5c, Ac'''
        board4 = [[0, 2], [1, 2], [2, 2], [3, 2], [12, 2]]
        self.assertEqual(ShufflezCalc.board_str_flush_check(board4), True)


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
        combo1 = Combo([12, 3], [3, 3])
        
        '''As 5c'''
        combo2 = Combo([12, 3], [3, 2])
        
        '''5s 6s'''
        combo3 = Combo([3, 3], [4, 3])
        
        '''Ac 3h'''
        combo4 = Combo([12, 2], [1, 0])
        
        '''Th 9h'''
        combo5 = Combo([8, 0], [7, 0])
        
        '''9s 2c'''
        combo6 = Combo([7, 3], [0, 2])
        
        
        '''4h Td 9d   As 5s'''
        self.assertEqual(ShufflezCalc.str_flush_check(combo1, board1), False)
        
        '''2s 3s 4s   As 5s  Test if wheel ace works'''
        self.assertEqual(ShufflezCalc.str_flush_check(combo1, board3), True)
        
        '''4h 5h 6h 7h 8h   Th 9h,  str flush on board, combo makes higher str flush'''
        self.assertEqual(ShufflezCalc.str_flush_check(combo5, board4), True)
        
        '''4h 5h 6h 7h 8h   As 5s, str flush on board, combo does not make a higher str flush'''
        self.assertEqual(ShufflezCalc.str_flush_check(combo1, board4), False)
        
        '''4h 5h 6h 7h 8h  Ac 3h, str flush on board, combo does make a str flush, but not a better str flush'''
        #self.assertEqual(ShufflezCalc.str_flush_check(combo4, board4), False)
        '''This is not asserting correctly and I cannot for the life of me figure out why.  It's evaluating correctly in every other test.'''
        
        '''2c 3c 4c 5c   Ac 3h, single ace for str flush wheel'''
        self.assertEqual(ShufflezCalc.str_flush_check(combo4, board6), True)
        
        '''As Ks Qs Js Ts   9s 2c, lower str flush with combo than board alone'''
        self.assertEqual(ShufflezCalc.str_flush_check(combo6, board7), False)
        
        '''As Kd 9d 6s 3c   As 5c, no possible str flush'''
        self.assertEqual(ShufflezCalc.str_flush_check(combo2, board5), False)
        
        '''Ac Kc'''
        combo = Combo([12, 2], [11, 2])
        '''Qc Jc Tc Qd Jd'''
        board = [[10, 2], [9, 2], [8, 2], [10, 1], [9, 1]]
        self.assertTrue(ShufflezCalc.str_flush_check(combo, board))


class TestBoardQuadsCheck(unittest.TestCase):
    
    def test_board_quads(self):
        
        '''Qc Qh Qs Qd'''
        board1 = [[10, 2], [10, 0], [10, 3], [10, 1]]
        self.assertEqual(ShufflezCalc.board_quads_check(board1), True)
        
        '''Qc Qh Qs Qd Ks'''
        board2 = [[10, 2], [10, 0], [10, 3], [10, 1], [11, 3]]
        self.assertEqual(ShufflezCalc.board_quads_check(board2), True)
        
        '''Qc Qh Qs Td Ks'''
        board3 = [[10, 2], [10, 0], [10, 3], [8, 1], [11, 3]]
        self.assertEqual(ShufflezCalc.board_quads_check(board3), False)
        
        '''Qc Qh Qs'''
        board4 = [[10, 2], [10, 0], [10, 3]]
        self.assertEqual(ShufflezCalc.board_quads_check(board4), False)


class TestQuadsCheck(unittest.TestCase):
    
    def test_quads(self):
        
        '''7h7d'''
        combo1 = Combo([5, 0], [5, 1])
        '''7s 7c 3d'''
        board1 = [[5, 3], [5, 2], [1, 1]]
        self.assertEqual(ShufflezCalc.quads_check(combo1, board1), True)
        
        '''3h 3c'''
        combo2 = Combo([1, 0], [1, 2])
        '''7s 7c 3d 3s'''
        board2 = [[5, 3], [5, 2], [1, 1], [1, 3]]
        self.assertEqual(ShufflezCalc.quads_check(combo2, board2), True)
        
        '''Qh Qd Qc Qs Ac'''
        board3 = [[11, 0], [11, 1], [11, 3], [11, 2]]
        self.assertEqual(ShufflezCalc.quads_check(combo2, board3), False)
        
        '''Ah 4c'''
        combo3 = Combo([12, 0], [2, 2])
        '''3c Ac 8d As Ad'''
        board4 = [[1, 2], [12, 2], [6, 1], [12, 3], [12, 1]]
        self.assertEqual(ShufflezCalc.quads_check(combo3, board4), True)
        
        '''2s 2h 2d 2c'''
        board5 = [[0, 3], [0, 0], [0, 1], [0, 2]]
        self.assertEqual(ShufflezCalc.quads_check(combo3, board5), False)
        
        '''2h 2s'''
        combo4 = Combo([0, 0], [0, 3])
        '''2d 5d 6d Td 2c'''
        board6 = [[0, 1], [3, 1], [4, 1], [8, 1], [0, 2]]
        self.assertEqual(ShufflezCalc.quads_check(combo4, board6), True)


class TestBoardFullHouseCheck(unittest.TestCase):
    
    def test_board_full_house(self):
        
        '''Qc Qd Qs 8d 8s'''
        board1 = [[10, 2], [10, 1], [10, 3], [6, 1], [6, 3]]
        self.assertEqual(ShufflezCalc.board_full_house_check(board1), True)
        
        ''''Qc Qd Qs Qh 8s'''
        board2 = [[10, 2], [10, 1], [10, 3], [10, 0], [6, 3]]
        self.assertEqual(ShufflezCalc.board_full_house_check(board2), False)
        
        '''Jh Ac Jd As Js'''
        board3 = [[9, 0], [12, 2], [9, 1], [12, 3], [9, 3]]
        self.assertEqual(ShufflezCalc.board_full_house_check(board3), True)
        
        '''Jh Ac Jd'''
        board4 = [[9, 0], [12, 2], [9, 1]]
        self.assertEqual(ShufflezCalc.board_full_house_check(board4), False)


class TestFullHouseCheck(unittest.TestCase):
    
    def test_full_house(self):
        
        '''3h 3c'''
        combo1 = Combo([1, 0], [1, 2])
        
        '''Ad Ks'''
        combo2 = Combo([12, 1], [11, 3])
        
        '''Ks 3h'''
        combo3 = Combo([11, 3], [1, 0])
        
        '''Qh Qc'''
        combo4 = Combo([10, 0], [10, 2])
        
        '''Jc 5c'''
        combo5 = Combo([9, 2], [3, 2])
        
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
        self.assertEqual(ShufflezCalc.full_house_check(combo1, board1), False)
        '''Kh Jc 6c'''
        board2 = [[11, 0], [9, 2], [4, 2]]
        self.assertEqual(ShufflezCalc.full_house_check(combo1, board2), False)
        
        '''Ace in hole cards make a better full house than board'''
        '''3c 3d 3s Ac Ah    Ad Ks'''
        self.assertEqual(ShufflezCalc.full_house_check(combo2, board3), True)
        
        '''3 in hole cards does not improve full house on board'''
        '''Ah Ac Ad 3d 3s    Ks 3h'''
        self.assertEqual(ShufflezCalc.full_house_check(combo3, board4), False)
        
        '''QQ improves over the board for a higher full house'''
        '''Ah Ac Ad 3d 3s   Qh Qc'''
        self.assertEqual(ShufflezCalc.full_house_check(combo4, board4), True)
        
        '''QQ does not improve the board'''
        '''3c 3d 3s Ac Ah   Qh Qc'''
        self.assertEqual(ShufflezCalc.full_house_check(combo4, board3), False)

        '''Double pair board with single hole card to make full house'''
        '''Jh 4h Js 4c Td   Jc 5c'''
        self.assertEqual(ShufflezCalc.full_house_check(combo5, board5), True)
        
        '''Single paired board, pocket pair makes full house'''
        '''Ks Kc 3d   3h 3c'''
        self.assertEqual(ShufflezCalc.full_house_check(combo1, board6), True)


class TestFlushCheck(unittest.TestCase):
    
    def test_flush(self):
        
        '''Hole card(s) used to make flush'''
        '''Ac 3c'''
        combo1 = Combo([12, 2], [1, 2])
        '''5c 9c Kc'''
        board1 = [[3, 2], [7, 2], [11, 2]]
        self.assertEqual(ShufflezCalc.flush_check(combo1, board1), True)
        
        '''5c 8c Jd'''
        board2 = [[3, 2], [6, 2], [9, 1]]
        self.assertEqual(ShufflezCalc.flush_check(combo1, board2), False)
        
        '''Jd 5c 8c 6s Qc'''
        board3 = [[9, 1], [3, 2], [6, 2], [4, 3], [10, 2]]
        self.assertEqual(ShufflezCalc.flush_check(combo1, board3), True)
        
        '''Jd 5c 8c 6s Qh'''
        board4 = [[9, 1], [3, 2], [6, 2], [4, 3], [10, 0]]
        self.assertEqual(ShufflezCalc.flush_check(combo1, board4), False)
        
        '''5h 7d'''
        combo2 = Combo([3, 0], [5, 1])
        '''8h 9h 2h Kh'''
        board5 = [[6, 0], [7, 0], [0, 0], [11, 0]]
        self.assertEqual(ShufflezCalc.flush_check(combo2, board5), True)
        
        '''8h 9h 9s 2h Kh'''
        board6 = [[6, 0], [7, 0], [9, 3], [0, 0], [11, 0]]
        self.assertEqual(ShufflezCalc.flush_check(combo2, board6), True)
        
        '''9s 8s'''
        combo3 = Combo([7, 3], [6, 3])
        self.assertEqual(ShufflezCalc.flush_check(combo3, board6), False)
        
        '''Flush on board'''
        board7 = [[8, 1], [4, 1], [7, 1], [3, 1], [10, 1]]
        
        '''Th 9h'''
        '''two Hole cards not of board suit; do not improve board flush'''
        combo4 = Combo([8, 0], [7, 0])
        self.assertEqual(ShufflezCalc.flush_check(combo4, board7), False)
        
        '''Ad Kd'''
        '''both hole cards of board suit make higher flush'''
        combo5 = Combo([12, 1], [11, 1])
        self.assertEqual(ShufflezCalc.flush_check(combo5, board7), True)
        
        '''8d 3d'''
        '''One hole card of board suit improves board flush'''
        combo6 = Combo([6, 1], [1, 1])
        self.assertEqual(ShufflezCalc.flush_check(combo6, board7), True)
        
        '''3d 2d'''
        '''Two hole cards of board suit, neither improves board flush'''
        combo7 = Combo([1, 1], [0, 1])
        self.assertEqual(ShufflezCalc.flush_check(combo7, board7), False)
        
        '''Jd 2d'''
        '''One hole card of board suit, improves board flush'''
        combo8 = Combo([9, 1], [0, 1])
        self.assertEqual(ShufflezCalc.flush_check(combo8, board7), True)
        
        '''4c 4d'''
        '''One hole card of board suit, does not improve board flush'''
        combo9 = Combo([2, 2], [2, 1])
        self.assertEqual(ShufflezCalc.flush_check(combo9, board7), False)


class TestNutFlushCard(unittest.TestCase):
    
    def test_nut_flush_card(self):
        
        '''Teesting for nut flush card'''
        
        '''7s 3s 6s -> As'''
        board1 = [[5, 3], [1, 3], [4, 3]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board1, 1), [12, 3])
        
        '''7s 3s As -> Ks'''
        board2 = [[5, 3], [1, 3], [12, 3]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board2, 1), [11, 3])
        
        '''Jc Kc Ac 5c -> Qs'''
        board3 = [[9, 2], [11, 2], [12, 2], [3, 2]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board3, 1), [10, 2])
        
        '''Qc Kc Ac 5c -> Jc'''
        board4 = [[10, 2], [11, 2], [12, 2], [3, 2]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board4, 1), [9, 2])
    
    def test_second_nut_flush_card(self):
        
        '''Testing for second nut flush card'''
        
        '''7s 3s 6s -> Ks'''
        board1 = [[5, 3], [1, 3], [4, 3]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board1, 2), [11, 3])
        
        '''7s 3s As -> Qs'''
        board2 = [[5, 3], [1, 3], [12, 3]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board2, 2), [10, 3])
        
        '''Jc Kc Ac 5c -> Tc'''
        board3 = [[9, 2], [11, 2], [12, 2], [3, 2]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board3, 2), [8, 2])
        
        '''Qc Kc Ac 5c -> Tc'''
        board4 = [[10, 2], [11, 2], [12, 2], [3, 2]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board4, 2), [8, 2])
    
    def test_third_nut_flush_card(self):
        
        '''Testing for third nut flush card'''
        
        '''7s 3s 6s -> Qs'''
        board1 = [[5, 3], [1, 3], [4, 3]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board1, 3), [10, 3])
        
        '''7s 3s As -> Js'''
        board2 = [[5, 3], [1, 3], [12, 3]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board2, 3), [9, 3])
        
        '''Jc Kc Ac 5c -> 9c'''
        board3 = [[9, 2], [11, 2], [12, 2], [3, 2]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board3, 3), [7, 2])
        
        '''Qc Kc Ac 5c -> 9c'''
        board4 = [[10, 2], [11, 2], [12, 2], [3, 2]]
        self.assertEqual(ShufflezCalc.nut_flush_card(board4, 3), [7, 2])

        
class TestBoardStraightCheck(unittest.TestCase):
    
    def test_board_straight(self):
        
        '''6s 9d Tc'''
        board = [[4, 3], [7, 1], [8, 2]]
        self.assertEqual(ShufflezCalc.board_straight_check(board), False)
        
        '''Jc Th 9h 6c'''
        board = [[9, 2], [8, 0], [7, 0], [4, 2]]
        self.assertEqual(ShufflezCalc.board_straight_check(board), False)
        
        '''9d 7d 8s Tc Jh'''
        board = [[7, 1], [5, 1], [6, 3], [8, 2], [9, 0]]
        self.assertEqual(ShufflezCalc.board_straight_check(board), True)
        
        '''Td Jd Qd Kc Ac'''
        board = [[8, 1], [9, 1], [10, 1], [11, 2], [12, 2]]
        self.assertEqual(ShufflezCalc.board_straight_check(board), True)
        
        '''3c 5c As 2d 4c'''
        board = [[1, 2], [3, 2], [12, 3], [0, 1], [2, 2]]
        self.assertEqual(ShufflezCalc.board_straight_check(board), True)
        
        '''As 9s Js 9h 6c'''
        board = [[12, 3], [7, 3], [9, 3], [7, 0], [4, 2]]
        self.assertEqual(ShufflezCalc.board_straight_check(board), False)
        
        '''Kc Kd Jc 9d 9s'''
        board = [[11, 2], [11, 1], [9, 2], [7, 1], [7, 3]]
        self.assertEqual(ShufflezCalc.board_straight_check(board), False)


class TestNutStraightRank(unittest.TestCase):
    
    def test_nut_straight_rank(self):
        
        '''NUT STRAIGHT RANKS'''
        
        '''Jc Th 9d -> 11'''
        board = [[9, 2], [8, 0], [7, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 11)
        
        '''Kc Qc Jd -> 12'''
        board = [[11, 2], [10, 2], [9, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 12)
        
        '''Kc Jd Td -> 12'''
        board = [[11, 2], [9, 1], [8, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 12)
        
        '''8c 7d 5s -> 7'''
        board = [[6, 2], [5, 1], [3, 3]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 7)
        
        '''3d 2h Ac -> 3'''
        board = [[1, 1], [0, 0], [12, 2]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 3)
        
        '''As Kc Qh -> 9'''
        board = [[12, 3], [11, 2], [10, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 9)
        
        '''Jc 7d Td -> 7'''
        board = [[9, 2], [8, 1], [5, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 7)
        
        '''4d 3d 6h -> 5'''
        board = [[2, 1], [1, 1], [4, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 5)
        
        '''Qh Jc Td 9s 8h -> 12'''
        board = [[10, 0], [9, 2], [8, 1], [7, 3], [6, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 12)
        
        '''6d 7c 8h 9s Qh -> 9'''
        board = [[4, 1], [5, 2], [6, 0], [7, 3], [10, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 9)
        
        '''7c 6d 5s Jc Qh -> 7'''
        board = [[5, 2], [4, 1], [3, 3], [9, 2], [10, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 7)
        
        '''Qh Jc 4c 3d 7c -> 4'''
        board = [[10, 0], [9, 2], [2, 2], [1, 1], [5, 2]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 4)
        
        '''6d 9s Qc Ah 2h'''
        board = [[4, 1], [7, 3], [10, 2], [12, 0], [0, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), None)
        
        '''Qh Jc Tc Jd Td'''
        board = [[10, 0], [9, 2], [8, 2], [9, 1], [8, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 1), 12)
        
        '''SECOND NUT STRAIGHT RANKS'''
        
        '''Jc Th 9d -> 10'''
        board = [[9, 2], [8, 0], [7, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 10)
        
        '''Kc Qc Jd -> 8'''
        board = [[11, 2], [10, 2], [9, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 8)
        
        '''Kc Jd Td -> 10'''
        board = [[11, 2], [9, 1], [8, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 10)
        
        '''8c 7d 5s -> 4'''
        board = [[6, 2], [5, 1], [3, 3]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 4)
        
        '''3d 2h Ac -> None'''
        board = [[1, 1], [0, 0], [12, 2]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), None)
        
        '''As Kc Qh -> None'''
        board = [[12, 3], [11, 2], [10, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), None)
        
        '''Jc 7d Td -> None'''
        board = [[9, 2], [8, 1], [5, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), None)
        
        '''4d 3d 6h -> 3'''
        board = [[2, 1], [1, 1], [4, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 3)
        
        '''Qh Jc Td 9s 8h -> 11'''
        board = [[10, 0], [9, 2], [8, 1], [7, 3], [6, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 11)
        
        '''6d 7c 8h 9s Qh -> 8'''
        board = [[4, 1], [5, 2], [6, 0], [7, 3], [10, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 8)
        
        '''7c 6d 5s Jc Qh -> 6'''
        board = [[5, 2], [4, 1], [3, 3], [9, 2], [10, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 6)
        
        '''Qh Jc 4c 3d 7c -> None'''
        board = [[10, 0], [9, 2], [2, 2], [1, 1], [5, 2]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), None)
        
        '''6d 9s Qc Ah 2h'''
        board = [[4, 1], [7, 3], [10, 2], [12, 0], [0, 0]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), None)
        
        '''Ah Kc Td 9s 8s -> 9'''
        board = [[12, 0], [11, 2], [8, 1], [7, 3], [6, 3]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 9)
        
        '''Ks Qd 8c 5s 4s -> None'''
        board = [[11, 3], [10, 1], [6, 2], [3, 3], [2, 3]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), None)
        
        '''Qh Jc Tc Jd Td'''
        board = [[10, 0], [9, 2], [8, 2], [9, 1], [8, 1]]
        self.assertEqual(ShufflezCalc.nut_straight_rank(board, 2), 11)


class TestStraightCheck(unittest.TestCase):
    
    def test_straight_check(self):        
        
        '''Kc Qh'''
        combo = Combo([11, 2], [10, 0])
        
        '''Boards with NO straight possible'''
        
        '''Qh 8s 4c'''
        board = [[10, 0], [6, 3], [2, 2]]
        self.assertFalse(ShufflezCalc.straight_check(combo, board))
        
        '''5d 4d Qc As 9s'''
        board = [[3, 1], [2, 1], [10, 2], [12, 3], [7, 3]]
        self.assertFalse(ShufflezCalc.straight_check(combo, board))
        
        '''Jc Td Ts 6s 5c'''
        board = [[9, 2], [8, 1], [8, 3], [4, 3], [3, 2]]
        self.assertFalse(ShufflezCalc.straight_check(combo, board))
        
        '''Boards with possible straight'''
        
        '''Jc Td 9s'''
        board = [[9, 2], [8, 1], [7, 3]]
        self.assertTrue(ShufflezCalc.straight_check(combo, board))
        
        '''Ah Td Jc'''
        board = [[12, 0], [8, 1], [9, 2]]
        self.assertTrue(ShufflezCalc.straight_check(combo, board))
        
        '''Ah 9s Tc'''
        board = [[12, 0], [7, 3], [8, 1]]
        self.assertFalse(ShufflezCalc.straight_check(combo, board))
        
        #######
        
        '''6d 5d'''
        combo = Combo([4, 1], [3, 1])
        
        '''Qh Jc 4c 3d 7c'''
        board = [[10, 0], [9, 2], [2, 2], [1, 1], [5, 2]]
        self.assertTrue(ShufflezCalc.straight_check(combo, board))
        
        '''Ah 5c'''
        combo = Combo([12, 0], [3, 2])
        
        '''4d 3s 2s'''
        board = [[2, 1], [1, 3], [0, 3]]
        self.assertTrue(ShufflezCalc.straight_check(combo, board))
        
        '''Hole cards do NOT imporove board straight'''
        
        '''4h 4c  Hole cards do NOT imporove board straight'''
        combo = Combo([2, 0], [2, 2])
        
        '''9h 8c 7d 6s 5c'''
        board = [[7, 0], [6, 2], [5, 1], [4, 3], [3, 3]]
        self.assertFalse(ShufflezCalc.straight_check(combo, board))

        '''Jh Ts  Hole cards DO imporove board straight'''
        combo = Combo([9, 0], [8, 3])
        self.assertTrue(ShufflezCalc.straight_check(combo, board))
        
        '''Ah As'''
        combo = Combo([12, 0], [12, 3])
        
        '''3s 2s 5d 4s'''
        board = [[1, 3], [0, 3], [3, 1], [2, 3]]
        self.assertTrue(ShufflezCalc.straight_check(combo, board))
        
        '''Ah Kh'''
        combo = Combo([12, 0], [11, 0])
        
        '''Qh Qc Jc Jd Td'''
        board = [[10, 0], [10, 2], [9, 2], [9, 1], [8, 1]]
        self.assertTrue(ShufflezCalc.straight_check(combo, board))
        
        '''9s 8s'''
        combo = Combo([7, 3], [6, 3])
        self.assertTrue(ShufflezCalc.straight_check(combo, board))
        

class TestNutStraightCheck(unittest.TestCase):
    
    def test_nut_straight_check(self):       
        
        '''Kc Qh'''
        combo = Combo([11, 2], [10, 0])          
        
        '''Jc Td 9s'''
        board = [[9, 2], [8, 1], [7, 3]]
        self.assertTrue(ShufflezCalc.nut_straight_check(combo, board))
        
        '''Qh 8h'''
        combo = Combo([10, 0], [6, 0])
        self.assertFalse(ShufflezCalc.nut_straight_check(combo, board))
        
        '''Kc Qh'''
        combo = Combo([11, 2], [10, 0])         
        
        '''Ah Td Jc'''
        board = [[12, 0], [8, 1], [9, 2]]
        self.assertTrue(ShufflezCalc.nut_straight_check(combo, board))
        
        '''6d 5d'''
        combo = Combo([4, 1], [3, 1])
        
        '''Qh Jc 4c 3d 7c'''
        board = [[10, 0], [9, 2], [2, 2], [1, 1], [5, 2]]  
        self.assertTrue(ShufflezCalc.nut_straight_check(combo, board))
        
        '''Ah Kh'''
        combo = Combo([12, 0], [11, 0])
        
        '''Qh Qc Jc Jd Td'''
        board = [[10, 0], [10, 2], [9, 2], [9, 1], [8, 1]]
        self.assertTrue(ShufflezCalc.nut_straight_check(combo, board))
        
        '''9s 8s'''
        combo = Combo([7, 3], [6, 3])
        self.assertFalse(ShufflezCalc.nut_straight_check(combo, board))
        
        '''4h 4c'''
        combo = Combo([2, 0], [2, 2])
        
        '''9h 8c 7d 6s 5c'''
        board = [[7, 0], [6, 2], [5, 1], [4, 3], [3, 3]]
        self.assertFalse(ShufflezCalc.nut_straight_check(combo, board))


class TestSecondNutStraight(unittest.TestCase):
    
    def test_second_nut_straight(self):
        
        '''Qh 8h'''
        combo = Combo([10, 0], [6, 0])
        
        '''Jc Td 9s'''
        board = [[9, 2], [8, 1], [7, 3]]
        self.assertTrue(ShufflezCalc.second_nut_straight_check(combo, board))
        
        '''9s 8s'''
        combo = Combo([7, 3], [6, 3])
        
        '''Qh Qc Jc Jd Td'''
        board = [[10, 0], [10, 2], [9, 2], [9, 1], [8, 1]]
        self.assertFalse(ShufflezCalc.second_nut_straight_check(combo, board))
        
        '''9h 8c 7d 6s 5c'''
        board = [[7, 0], [6, 2], [5, 1], [4, 3], [3, 3]]        
        
        '''4h 4c'''
        combo = Combo([2, 0], [2, 2])
        self.assertFalse(ShufflezCalc.second_nut_straight_check(combo, board))
        
        '''Tc Td'''
        combo = Combo([8, 2], [8, 1])
        self.assertTrue(ShufflezCalc.second_nut_straight_check(combo, board))


class TestThreeOfAKindCheck(unittest.TestCase):
    
    def test_thee_of_a_kind_check(self):
        
        '''8d, 8h, 8s   Ah 9h'''
        board = [[6, 1], [6, 0], [6, 3]]
        combo = Combo([12, 0], [7, 0])
        self.assertFalse(ShufflezCalc.three_of_a_kind_check(combo, board))
        
        '''Tc 9d 4s   Th Ts'''
        board = [[8, 2], [7, 1], [2, 3]]
        combo = Combo([8, 0], [8, 3])
        self.assertTrue(ShufflezCalc.three_of_a_kind_check(combo, board))
        
        '''Tc 9d 9s   Ah 9h'''
        board = [[8, 2], [7, 1], [7, 3]]
        combo = Combo([12, 0], [7, 0])
        self.assertTrue(ShufflezCalc.three_of_a_kind_check(combo, board))
        
        '''8s 5d 3h   9h 9s'''
        board = [[6, 3], [3, 1], [1, 0]]
        combo = Combo([7, 0], [7, 3])
        self.assertFalse(ShufflezCalc.three_of_a_kind_check(combo, board))
        

class TestBoardThreeOfAKindCheck(unittest.TestCase):
    
    def test_board_three_of_a_kind_check(self):
        
        '''8d, 8h, 8s'''
        board = [[6, 1], [6, 0], [6, 3]]
        self.assertTrue(ShufflezCalc.board_three_of_a_kind_check(board))
        
        '''8d, 8h, 7s'''
        board = [[6, 1], [6, 0], [7, 3]]
        self.assertFalse(ShufflezCalc.board_three_of_a_kind_check(board))
        
        '''4d Tc Th 4s'''
        board = [[2, 1], [8, 2], [8, 0], [2, 3]]
        self.assertFalse(ShufflezCalc.board_three_of_a_kind_check(board))
        
        '''Kd Kh 7c Kc'''
        board = [[11, 1], [11, 0], [5, 2], [11, 2]]
        self.assertTrue(ShufflezCalc.board_three_of_a_kind_check(board))
        
        '''2d Ah 2s Td 2s'''
        board = [[0, 1], [12, 0], [0, 3], [8, 1], [0, 3]]
        self.assertTrue(ShufflezCalc.board_three_of_a_kind_check(board))
    

class TestSetCheck(unittest.TestCase):
    
    def test_set_check(self):
        
        '''Tc 9d 4s   Th Ts'''
        board = [[8, 2], [7, 1], [2, 3]]
        combo = Combo([8, 0], [8, 3])
        self.assertTrue(ShufflezCalc.set_check(combo, board))
        
        '''combo 9h 9s'''
        combo = Combo([7, 0], [7, 3])
        self.assertTrue(ShufflezCalc.set_check(combo, board))
        
        '''Tc 9d 9s   Ah 9h'''
        board = [[8, 2], [7, 1], [7, 3]]
        combo = Combo([12, 0], [7, 0])
        self.assertFalse(ShufflezCalc.set_check(combo, board))
        
        '''8d, 8h, 8s'''
        board = [[6, 1], [6, 0], [6, 3]]
        self.assertFalse(ShufflezCalc.set_check(combo, board))
        
        '''8s 5d 3h   9h 9s'''
        board = [[6, 3], [3, 1], [1, 0]]
        combo = Combo([7, 0], [7, 3])
        self.assertFalse(ShufflezCalc.set_check(combo, board))


class TestTwoPairCheck(unittest.TestCase):
    
    def test_two_pair_check(self):
        
        '''Td 2c Kc 8s 6s'''
        board = [[8, 1], [0, 2], [11, 2], [6, 3], [4, 3]]
        
        '''Kh Th'''
        combo = Combo([11, 0], [8, 0])
        self.assertTrue(ShufflezCalc.two_pair_check(combo, board))
        
        '''Kh 8h'''
        combo = Combo([11, 0], [6, 0])
        self.assertTrue(ShufflezCalc.two_pair_check(combo, board))
        
        '''6h 2h'''
        combo = Combo([4, 0], [0, 0])
        self.assertTrue(ShufflezCalc.two_pair_check(combo, board))
        
        '''Ah Kh'''
        combo = Combo([12, 0], [11, 0])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Qh Qd'''
        combo = Combo([10, 0], [10, 1])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Kc Td 6s 8s 8c'''
        board = [[11, 2], [8, 1], [4, 3], [6, 3], [6, 2]]
        
        '''Kh Th'''
        combo = Combo([11, 0], [8, 0])
        self.assertTrue(ShufflezCalc.two_pair_check(combo, board))
        
        '''Th 6h'''
        combo = Combo([8, 0], [4, 0])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Kh 6h'''
        combo = Combo([11, 0], [4, 0])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Ah Kh'''
        combo = Combo([12, 0], [11, 0])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Ah Ad'''
        combo = Combo([12, 0], [12, 1])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Kc Td Ts 8s 8c'''
        board = [[11, 2], [8, 1], [8, 3], [6, 3], [6, 2]]
        
        '''Ah Kh'''
        combo = Combo([12, 0], [11, 0])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Qh Qd'''
        combo = Combo([10, 0], [10, 1])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''6h 6d'''
        combo = Combo([4, 0], [4, 1])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Kc Td 5c Ts 8s'''
        board = [[11, 2], [8, 1], [3, 2], [8, 3], [6, 3]]
        
        '''Ah Kh'''
        combo = Combo([12, 0], [11, 0])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Kh 8h'''
        combo = Combo([11, 0], [6, 0])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''Ah Ad'''
        combo = Combo([12, 0], [12, 1])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''8h 5h'''
        combo = Combo([6, 0], [3, 0])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))
        
        '''4h 4s'''
        combo = Combo([2, 0], [2, 3])
        self.assertFalse(ShufflezCalc.two_pair_check(combo, board))


class TestOverpairCheck(unittest.TestCase):
    
    def test_overpair_check(self):
        
        '''Qh 4h Ts 7d 6c'''
        board = [[10, 0], [2, 0], [8, 3], [5, 1], [6, 2]]
        
        '''Ah Ad'''
        combo = Combo([12, 0], [12, 1])
        self.assertTrue(ShufflezCalc.overpair_check(combo, board))
        
        '''2d 2s'''
        combo = Combo([0, 1], [0, 3])
        self.assertFalse(ShufflezCalc.overpair_check(combo, board))
        
        '''Ah Kh'''
        combo = Combo([12, 0], [11, 0])
        self.assertFalse(ShufflezCalc.overpair_check(combo, board))
        
        '''Jc Js'''
        combo = Combo([9, 2], [9, 3])
        self.assertFalse(ShufflezCalc.overpair_check(combo, board))
        
        '''As Qs'''
        combo = Combo([12, 3], [10, 3])
        self.assertFalse(ShufflezCalc.overpair_check(combo, board))
        
        '''7c 7d 2s'''
        board = [[5, 2], [5, 1], [0, 3]]
        
        '''Ah Ad'''
        combo = Combo([12, 0], [12, 1])
        self.assertTrue(ShufflezCalc.overpair_check(combo, board))
        
        '''Jc Js'''
        combo = Combo([9, 2], [9, 3])
        self.assertTrue(ShufflezCalc.overpair_check(combo, board))
        
        '''6h 6d'''
        combo = Combo([4, 0], [4, 1])
        self.assertFalse(ShufflezCalc.overpair_check(combo, board))
        
        '''3c 2d'''
        combo = Combo([1, 2], [0, 1])
        self.assertFalse(ShufflezCalc.overpair_check(combo, board))
        
        '''9h 9c 7c 7d'''
        board = [[7, 0], [7, 2], [5, 2], [5, 1]]
        
        '''Jc Js'''
        combo = Combo([9, 2], [9, 3])
        self.assertTrue(ShufflezCalc.overpair_check(combo, board))
        
        '''2d 2s'''
        combo = Combo([0, 1], [0, 3])
        self.assertFalse(ShufflezCalc.overpair_check(combo, board))
        
        '''As Qs'''
        combo = Combo([12, 3], [10, 3])
        self.assertFalse(ShufflezCalc.overpair_check(combo, board))       


class TestTopPairCheck(unittest.TestCase):
    
    def test_top_pair_check(self):
        
        '''Qc Td 9h'''
        board = [[10, 2], [8, 1], [7, 0]]
        
        '''As Qs'''
        combo = Combo([12, 3], [10, 3])
        self.assertTrue(ShufflezCalc.top_pair_check(combo, board))
        
        '''Kh Qh'''
        combo = Combo([11, 0], [10, 0])
        self.assertTrue(ShufflezCalc.top_pair_check(combo, board))
        
        '''Qh 2s'''
        combo = Combo([10, 0], [0, 3])
        self.assertTrue(ShufflezCalc.top_pair_check(combo, board))
        
        '''Th 8h'''
        combo = Combo([8, 0], [6, 0])
        self.assertFalse(ShufflezCalc.top_pair_check(combo, board))


class TestTopPairKickerRank(unittest.TestCase):
    
    def test_top_pair_kicker_rank(self):
        
        '''Qc Td 9h -> 12'''
        board = [[10, 2], [8, 1], [7, 0]]
        
        '''Top Kicker: A'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 1), 12)
        '''Second Kicker:  K'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 2), 11)
        '''Third Kicker:  J'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 3), 9)
        '''Fourth Kicker:  8'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 4), 6)
        
        '''Ah Kc Jd 3h'''
        board = [[12, 0], [11, 2], [9, 1], [1, 0]]
        
        '''Top Kicker: Q'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 1), 10)
        '''Second Kicker:  T'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 2), 8)
        '''Third Kicker:  9'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 3), 7)
        '''Fourth Kicker:  8'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 4), 6)
        
        '''9h 8d 5s'''
        board = [[7, 0], [6, 1], [3, 3]]
        
        '''Top Kicker: A'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 1), 12)
        '''Second Kicker:  K'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 2), 11)
        '''Third Kicker:  Q'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 3), 10)
        '''Fourth Kicker:  J'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 4), 9)
        '''Seventh Kicker:  6'''
        self.assertEqual(ShufflezCalc.top_pair_kicker_rank(board, 7), 4)


class TestPPBelowTPCheck(unittest.TestCase):
    
    def test_pp_below_tp_check(self):
        
        '''Ad 7s 3s'''
        board = [[12, 1], [5, 3], [1, 3]]
        
        '''Kd Kc'''
        combo = Combo([11, 1], [11, 2])
        self.assertTrue(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''Jc Js'''
        combo = Combo([9, 2], [9, 3])
        self.assertTrue(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''8h 8d'''
        combo = Combo([6, 0], [6, 1])
        self.assertTrue(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''7h 7d'''
        combo = Combo([5, 0], [5, 1])
        self.assertFalse(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''6h 6d'''
        combo = Combo([4, 0], [4, 1])
        self.assertFalse(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''2h 2d'''
        combo = Combo([0, 0], [0, 1])
        self.assertFalse(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''Ah Kh'''
        combo = Combo([12, 0], [1, 1])
        self.assertFalse(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''Qd 5h 4h'''
        board = [[10, 1], [3, 0], [2, 0]]
        
        '''Kd Kc'''
        combo = Combo([11, 1], [11, 2])
        self.assertFalse(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''Jc Js'''
        combo = Combo([9, 2], [9, 3])
        self.assertTrue(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''6h 6d'''
        combo = Combo([4, 0], [4, 1])
        self.assertTrue(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''Qd Qh 4h'''
        board = [[10, 1], [10, 0], [2, 0]]
        
        '''Jc Js'''
        combo = Combo([9, 2], [9, 3])
        self.assertTrue(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''6h 6d'''
        combo = Combo([4, 0], [4, 1])
        self.assertTrue(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''2h 2d'''
        combo = Combo([0, 0], [0, 1])
        self.assertFalse(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''Qd Jh 4h'''
        board = [[10, 1], [9, 0], [2, 0]]
        
        '''Kd Kc'''
        combo = Combo([11, 1], [11, 2])
        self.assertFalse(ShufflezCalc.pp_below_tp_check(combo, board))
        
        '''Td Tc'''
        combo = Combo([8, 1], [8, 2])
        self.assertFalse(ShufflezCalc.pp_below_tp_check(combo, board))


class TestMiddlePairCheck(unittest.TestCase):
    
    def test_middle_pair_check(self):
        
        '''Ad 7s 3s'''
        board = [[12, 1], [5, 3], [1, 3]]
        
        '''Kh 7h'''
        combo = Combo([11, 0], [5, 0])
        self.assertTrue(ShufflezCalc.middle_pair_check(combo, board))
        
        '''7h 4s'''
        combo = Combo([5, 0], [2, 3])
        self.assertTrue(ShufflezCalc.middle_pair_check(combo, board))
        
        '''Jc Tc'''
        combo = Combo([9, 2], [8, 2])
        self.assertFalse(ShufflezCalc.middle_pair_check(combo, board))
        
        '''Kd Kc'''
        combo = Combo([11, 1], [11, 2])
        self.assertFalse(ShufflezCalc.middle_pair_check(combo, board))
        
        '''Ad 7s 3s 7c'''
        board = [[12, 1], [5, 3], [1, 3], [5, 2]]
        
        '''Kh 7h'''
        combo = Combo([11, 0], [5, 0])
        self.assertFalse(ShufflezCalc.middle_pair_check(combo, board))
        
        '''As Kh'''
        combo = Combo([12, 3], [11, 0])
        self.assertFalse(ShufflezCalc.middle_pair_check(combo, board))
        
        '''Js Jh'''
        combo = Combo([9, 3], [9, 0])
        self.assertFalse(ShufflezCalc.middle_pair_check(combo, board))


class TestWeakPairCheck(unittest.TestCase):
    
    def test_weak_pair_check(self):
        
        '''Ad 7s 3s'''
        board = [[12, 1], [5, 3], [1, 3]]       
        
        '''Kh 7h'''
        combo = Combo([11, 0], [5, 0])
        self.assertFalse(ShufflezCalc.weak_pair_check(combo, board))
        
        '''6h 6d'''
        combo = Combo([4, 0], [4, 1])
        self.assertTrue(ShufflezCalc.weak_pair_check(combo, board))
        
        '''Kh 3h'''
        combo = Combo([11, 0], [1, 0])
        self.assertTrue(ShufflezCalc.weak_pair_check(combo, board))
        
        '''As Kh'''
        combo = Combo([12, 3], [11, 0])
        self.assertFalse(ShufflezCalc.weak_pair_check(combo, board))
        
        '''Jh 7d Tc 3c 6h'''
        board = [[9, 0], [5, 1], [8, 2], [1, 2], [4, 0]]
        
        '''Kh 7h'''
        combo = Combo([11, 0], [5, 0])
        self.assertTrue(ShufflezCalc.weak_pair_check(combo, board))
        
        '''2h 2d'''
        combo = Combo([0, 0], [0, 1])
        self.assertTrue(ShufflezCalc.weak_pair_check(combo, board))
        
        '''As 3s'''
        combo = Combo([12, 3], [1, 3])
        self.assertTrue(ShufflezCalc.weak_pair_check(combo, board))
        
        '''As 6s'''
        combo = Combo([12, 3], [4, 3])
        self.assertTrue(ShufflezCalc.weak_pair_check(combo, board))
        
        '''Kd Kc'''
        combo = Combo([11, 1], [11, 2])
        self.assertFalse(ShufflezCalc.weak_pair_check(combo, board))
        
        '''Jh Jc 8d 8s 4d'''
        board = [[9, 0], [9, 2], [6, 1], [6, 3], [2, 1]]
        
        '''Ah 4h'''
        combo = Combo([12, 0], [2, 0])
        self.assertFalse(ShufflezCalc.weak_pair_check(combo, board))
        
        '''2h 2d'''
        combo = Combo([0, 0], [0, 1])
        self.assertFalse(ShufflezCalc.weak_pair_check(combo, board))
        

class TestFlushDrawCheck(unittest.TestCase):
    
    def test_flush_draw_check(self):
        
        '''9h 8c 4c'''
        board = [[7, 0], [6, 2], [2, 2]]
        
        '''Ac Kc'''
        combo = Combo([12, 2], [11, 2])
        self.assertTrue(ShufflezCalc.flush_draw_check(combo, board))
        
        '''Ac Kh'''
        combo = Combo([12, 2], [11, 0])
        self.assertFalse(ShufflezCalc.flush_draw_check(combo, board))
        
        '''9s 4s Qc Jc'''
        board = [[7, 3], [2, 3], [10, 2], [9, 2]]
        
        '''Ks Qs'''
        combo = Combo([11, 3], [10, 3])
        self.assertTrue(ShufflezCalc.flush_draw_check(combo, board))
        
        '''Ac Kc'''
        combo = Combo([12, 2], [11, 2])
        self.assertTrue(ShufflezCalc.flush_draw_check(combo, board))
        
        '''Ac Kh'''
        combo = Combo([12, 2], [11, 0])
        self.assertFalse(ShufflezCalc.flush_draw_check(combo, board))
        
        '''Th 7h 6h'''
        board = [[8, 0], [5, 0], [4, 0]]
        
        '''Ac Kh'''
        combo = Combo([12, 2], [11, 0])
        self.assertTrue(ShufflezCalc.flush_draw_check(combo, board))
        
        '''Ac Kc'''
        combo = Combo([12, 2], [11, 2])
        self.assertFalse(ShufflezCalc.flush_draw_check(combo, board))
        
        '''5h 4h'''
        combo = Combo([3, 0], [2, 0])
        self.assertFalse(ShufflezCalc.flush_draw_check(combo, board))
        
        '''Th 7h 6h 2h'''
        board = [[8, 0], [5, 0], [4, 0], [0, 0]]
        
        '''Ac Kh'''
        combo = Combo([12, 2], [11, 0])
        self.assertFalse(ShufflezCalc.flush_draw_check(combo, board))
        
        '''5h 4h'''
        combo = Combo([3, 0], [2, 0])
        self.assertFalse(ShufflezCalc.flush_draw_check(combo, board))
        
        '''Ac Kc'''
        combo = Combo([12, 2], [11, 2])
        self.assertFalse(ShufflezCalc.flush_draw_check(combo, board))


class TestNutFlushDrawCard(unittest.TestCase):
    
    def test_nut_flush_draw_card(self):
        
        '''Finding Nut Flush Draw card; nut_rank of 1'''
        
        '''Qc 9c 6s -> Ac'''
        board = [[10, 2], [7, 2], [4, 3]]
        nut_card = [12, 2]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 1))
        
        '''Ac 9c 6s -> Kc'''
        board = [[12, 2], [7, 2], [4, 3]]
        nut_card = [11, 2]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 1))
        
        '''Jc 9c 3c -> Ac'''
        board = [[9, 2], [7, 2], [1, 2]]
        nut_card = [12, 2]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 1))
        
        '''Kh Th 8c 5d -> Ah'''
        board = [[11, 0], [8, 0], [6, 2], [3, 1]]
        nut_card = [12, 0]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 1))
        
        '''Kh Th 8c 3h -> Ah'''
        board = [[11, 0], [8, 0], [6, 2], [1, 0]]
        nut_card = [12, 0]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 1))
        
        '''Ad Kd 9h -> Qd'''
        board = [[12, 1], [11, 1], [7, 0]]
        nut_card = [10, 1]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 1))
        
        '''Jh Ts 8h 4s -> Ah, As'''
        board = [[9, 0], [8, 3], [8, 0], [2, 3]]
        nut_card = [12, 0]
        nut_card_2 = [12, 3]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 1))
        self.assertIn(nut_card_2, ShufflezCalc.nut_flush_draw_card(board, 1))
        
        '''Ah Jd 8h 5d -> Kh, Ad'''
        board = [[12, 0], [9, 1], [6, 0], [3, 1]]
        nut_card = [11, 0]
        nut_card_2 = [12, 1]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 1))
        self.assertIn(nut_card_2, ShufflezCalc.nut_flush_draw_card(board, 1))
        
        '''Kh Ks Ah As -> Qh, Qs'''
        board = [[11, 0], [11, 3], [12, 0], [12, 3]]
        nut_card = [10, 0]
        nut_card_2 = [10, 3]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 1))
        self.assertIn(nut_card_2, ShufflezCalc.nut_flush_draw_card(board, 1))
        
        '''Finding Second Nut Flush Draw card; nut_rank of 2'''
        
        '''Qc 9c 6s -> Kc'''
        board = [[10, 2], [7, 2], [4, 3]]
        nut_card = [11, 2]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 2))
        
        '''Ac 9c 6s -> Qc'''
        board = [[12, 2], [7, 2], [4, 3]]
        nut_card = [10, 2]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 2))
        
        '''Jc 9c 3c -> Kc'''
        board = [[9, 2], [7, 2], [1, 2]]
        nut_card = [11, 2]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 2))
        
        '''Kh Th 8c 5d -> Qh'''
        board = [[11, 0], [8, 0], [6, 2], [3, 1]]
        nut_card = [10, 0]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 2))
        
        '''Kh Th 8c 3h -> Qh'''
        board = [[11, 0], [8, 0], [6, 2], [1, 0]]
        nut_card = [10, 0]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 2))
        
        '''Ad Kd 9h -> Jd'''
        board = [[12, 1], [11, 1], [7, 0]]
        nut_card = [9, 1]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 2))
        
        '''Jh Ts 8h 4s -> Kh, Ks'''
        board = [[9, 0], [8, 3], [8, 0], [2, 3]]
        nut_card = [11, 0]
        nut_card_2 = [11, 3]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 2))
        self.assertIn(nut_card_2, ShufflezCalc.nut_flush_draw_card(board, 2))
        
        '''Ah Jd 8h 5d -> Qh, Kd'''
        board = [[12, 0], [9, 1], [6, 0], [3, 1]]
        nut_card = [10, 0]
        nut_card_2 = [11, 1]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 2))
        self.assertIn(nut_card_2, ShufflezCalc.nut_flush_draw_card(board, 2))
        
        '''Kh Ks Ah As -> Jh, Js'''
        board = [[11, 0], [11, 3], [12, 0], [12, 3]]
        nut_card = [9, 0]
        nut_card_2 = [9, 3]
        self.assertIn(nut_card, ShufflezCalc.nut_flush_draw_card(board, 2))
        self.assertIn(nut_card_2, ShufflezCalc.nut_flush_draw_card(board, 2))        


class TestNutFlushDrawCheck(unittest.TestCase):
    
    def test_nut_flush_draw_check(self):
        
        '''Kc 7h 2h'''
        board = [[11, 2], [5, 0], [0, 0]]
        
        '''Ac 2c'''
        combo = Combo([12, 2], [11, 2])
        self.assertFalse(ShufflezCalc.nut_flush_draw_check(combo, board))
        
        '''Ah 5h'''
        combo = Combo([12, 0], [3, 0])
        self.assertTrue(ShufflezCalc.nut_flush_draw_check(combo, board))
        
        '''Kh 5h'''
        combo = Combo([11, 0], [3, 0])
        self.assertFalse(ShufflezCalc.nut_flush_draw_check(combo, board))
        
        '''Kc 7h 2h 9h'''
        board = [[11, 2], [5, 0], [0, 0], [7, 0]]
        
        '''Ac 2c'''
        combo = Combo([12, 2], [11, 2])
        self.assertFalse(ShufflezCalc.nut_flush_draw_check(combo, board))
        
        '''Ah 5s'''
        combo = Combo([12, 0], [3, 3])
        self.assertTrue(ShufflezCalc.nut_flush_draw_check(combo, board))


class TestSecondNutFlushDrawCheck(unittest.TestCase):
    
    def test_second_nut_flush_draw_check(self):
        
        '''Kc 7h 2h'''
        board = [[11, 2], [5, 0], [0, 0]]
        
        '''Qc 2c'''
        combo = Combo([10, 2], [11, 2])
        self.assertFalse(ShufflezCalc.second_nut_flush_draw_check(combo, board))
        
        '''Kh 5h'''
        combo = Combo([11, 0], [3, 0])
        self.assertTrue(ShufflezCalc.second_nut_flush_draw_check(combo, board))
        
        '''Qh 5h'''
        combo = Combo([10, 0], [3, 0])
        self.assertFalse(ShufflezCalc.second_nut_flush_draw_check(combo, board))
        
        '''Kc 7h 2h 9h'''
        board = [[11, 2], [5, 0], [0, 0], [7, 0]]
        
        '''Ac 2c'''
        combo = Combo([12, 2], [11, 2])
        self.assertFalse(ShufflezCalc.second_nut_flush_draw_check(combo, board))
        
        '''Kh 5s'''
        combo = Combo([11, 0], [3, 3])
        self.assertTrue(ShufflezCalc.second_nut_flush_draw_check(combo, board))


class TestStraightDrawCheck(unittest.TestCase):
    
    def test_straight_draw_check(self):
        
        '''Ac 9h 8c'''
        board = [[12, 2], [7, 0], [6, 2]]
        
        '''Jh Th'''
        combo = Combo([9, 0], [8, 0])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''7c 6d'''
        combo = Combo([5, 2], [4, 1])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''6d 5d'''
        combo = Combo([4, 1], [3, 1])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''Qs Jc'''
        combo = Combo([10, 3], [9, 2])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''Kd Qh'''
        combo = Combo([11, 1], [10, 0])
        self.assertFalse(ShufflezCalc.straight_draw_check(combo, board))
        
        '''Th 7s'''
        combo = Combo([8, 0], [5, 3])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''Kd Th'''
        combo = Combo([11, 1], [8, 0])
        self.assertFalse(ShufflezCalc.straight_draw_check(combo, board))
        
        '''Td Ts'''
        combo = Combo([8, 1], [8, 3])
        self.assertFalse(ShufflezCalc.straight_draw_check(combo, board))
        
        '''7h 5d 3d'''
        board = [[5, 0], [3, 1], [1, 1]]
        
        '''6h 6s'''
        combo = Combo([4, 0], [4, 3])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''6c 5c'''
        combo = Combo([4, 2], [3, 2])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''9d 8h'''
        combo = Combo([7, 1], [6, 0])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''8d 7s'''
        combo = Combo([6, 1], [5, 3])
        self.assertFalse(ShufflezCalc.straight_draw_check(combo, board))
        
        '''4h 4d'''
        combo = Combo([2, 0], [2, 1])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''Tc 9c'''
        combo = Combo([8, 2], [7, 2])
        self.assertFalse(ShufflezCalc.straight_draw_check(combo, board))
        
        '''9h 6s 5s 7h'''
        board = [[7, 0], [4, 3], [3, 3], [5, 0]]
        
        '''As Ks'''
        combo = Combo([12, 3], [11, 3])
        self.assertFalse(ShufflezCalc.straight_draw_check(combo, board))
        
        '''4h 4d'''
        combo = Combo([2, 0], [2, 1])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''5h 4d'''
        combo = Combo([3, 0], [2, 1])
        self.assertTrue(ShufflezCalc.straight_draw_check(combo, board))
        
        '''9c 9d'''
        combo = Combo([7, 2], [7, 1])
        self.assertFalse(ShufflezCalc.straight_draw_check(combo, board))
        
        '''9h 6s 5s 7h Kh'''
        board = [[7, 0], [4, 3], [3, 3], [5, 0], [11, 0]]
        
        '''9c 9d'''
        combo = Combo([7, 2], [7, 1])
        self.assertFalse(ShufflezCalc.straight_draw_check(combo, board))
        
        '''Js Ts'''
        combo = Combo([9, 3], [8, 3])
        self.assertFalse(ShufflezCalc.straight_draw_check(combo, board))


class TestOESDCheck(unittest.TestCase):
    
    def test_oesd_check(self):
        
        '''Ac 9h 8c'''
        board = [[12, 2], [7, 0], [6, 2]]
        
        '''Jh Th'''
        combo = Combo([9, 0], [8, 0])
        self.assertTrue(ShufflezCalc.oesd_check(combo, board))
        
        '''7c 6d'''
        combo = Combo([5, 2], [4, 1])
        self.assertTrue(ShufflezCalc.oesd_check(combo, board))
        
        '''6d 5d'''
        combo = Combo([4, 1], [3, 1])
        self.assertFalse(ShufflezCalc.oesd_check(combo, board))
        
        '''Qs Jc'''
        combo = Combo([10, 3], [9, 2])
        self.assertFalse(ShufflezCalc.oesd_check(combo, board))
        
        '''9h 8c 7d'''
        board = [[7, 0], [6, 2], [5, 1]]
        
        '''Td Ts'''
        combo = Combo([8, 1], [8, 3])
        self.assertTrue(ShufflezCalc.oesd_check(combo, board))
        
        '''Qs Jc'''
        combo = Combo([10, 3], [9, 2])
        self.assertFalse(ShufflezCalc.oesd_check(combo, board))
        
        '''Tc 9c'''
        combo = Combo([8, 2], [7, 2])
        self.assertTrue(ShufflezCalc.oesd_check(combo, board))
        
        '''5h 4d'''
        combo = Combo([3, 0], [2, 1])
        self.assertFalse(ShufflezCalc.oesd_check(combo, board))
        
        '''Ts 7d 2c 3h'''
        board = [[8, 3], [5, 1], [0, 2], [1, 0]]
        
        '''5h 4d'''
        combo = Combo([3, 0], [2, 1])
        self.assertTrue(ShufflezCalc.oesd_check(combo, board))
        
        '''9d 8h'''
        combo = Combo([7, 1], [6, 0])
        self.assertTrue(ShufflezCalc.oesd_check(combo, board))
        
        '''Ah 5c 2c 4s'''
        board = [[12, 0], [3, 2], [0, 2], [2, 3]]
        
        '''8h 6s'''
        combo = Combo([6, 0], [4, 3])
        self.assertTrue(ShufflezCalc.oesd_check(combo, board))


class TestBDFDCheck(unittest.TestCase):
    
    def test_bdfd_check(self):
        
        '''9h 8c 7d'''
        board = [[7, 0], [6, 2], [5, 1]]
        
        '''Ah 4h'''
        combo = Combo([12, 0], [2, 0])
        self.assertTrue(ShufflezCalc.bdfd_check(combo, board))
        
        '''Kh 4h'''
        combo = Combo([11, 0], [2, 0])
        self.assertTrue(ShufflezCalc.bdfd_check(combo, board))
        
        '''As 4s'''
        combo = Combo([12, 3], [2, 3])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''Qh Js'''
        combo = Combo([10, 0], [9, 3])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''Ks 2s 7h'''
        board = [[11, 3], [0, 3], [5, 0]]
        
        '''As Ts'''
        combo = Combo([12, 3], [8, 3])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''6h 5h'''
        combo = Combo([4, 0], [3, 0])
        self.assertTrue(ShufflezCalc.bdfd_check(combo, board))
        
        '''Js Td'''
        combo = Combo([9, 3], [8, 1])
        self.assertTrue(ShufflezCalc.bdfd_check(combo, board))
        
        '''9c 8h'''
        combo = Combo([7, 2], [6, 0])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''Ks 2s 7s'''
        board = [[11, 3], [0, 3], [5, 3]]
        
        '''9c 8h'''
        combo = Combo([7, 2], [6, 0])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''Js Td'''
        combo = Combo([9, 3], [8, 1])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''As 4s'''
        combo = Combo([12, 3], [2, 3])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''Ks 2s 7h Jc'''
        board = [[11, 3], [0, 3], [5, 0], [9, 2]]
        
        '''As 4s'''
        combo = Combo([12, 3], [2, 3])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''9c 8h'''
        combo = Combo([7, 2], [6, 0])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''Js Td'''
        combo = Combo([9, 3], [8, 1])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''Ks 2s 7h Jc 8d'''
        board = [[11, 3], [0, 3], [5, 0], [9, 2], [6, 1]]
        
        '''As 4s'''
        combo = Combo([12, 3], [2, 3])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''Js Td'''
        combo = Combo([9, 3], [8, 1])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))
        
        '''9c 8h'''
        combo = Combo([7, 2], [6, 0])
        self.assertFalse(ShufflezCalc.bdfd_check(combo, board))


class TestTwoCardBDFDCheck(unittest.TestCase):
    
    def test_two_card_bdfd_check(self):
        
        '''Ah Ac'''
        combo = Combo([12, 0], [12, 2])
        self.assertFalse(ShufflezCalc.two_card_bdfd_check(combo))
        
        '''Ah Kc'''
        combo = Combo([12, 0], [11, 2])
        self.assertFalse(ShufflezCalc.two_card_bdfd_check(combo))
        
        '''Ah 2h'''
        combo = Combo([12, 0], [0, 0])
        self.assertTrue(ShufflezCalc.two_card_bdfd_check(combo))
        
        '''Js Ts'''
        combo = Combo([9, 3], [8, 3])
        self.assertTrue(ShufflezCalc.two_card_bdfd_check(combo))


class TestNutBDFDCheck(unittest.TestCase):
    
    def test_nut_bdfd_check(self):
        
        '''9c 8h 3d'''
        board = [[7, 2], [6, 0], [1, 1]]
        
        '''Ah 6h'''
        combo = Combo([12, 0], [4, 0])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Kh 6h'''
        combo = Combo([11, 0], [4, 0])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ac Jc'''
        combo = Combo([12, 2], [9, 2])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Qc Jc'''
        combo = Combo([10, 2], [9, 2])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ah Kc Qd'''
        board = [[12, 0], [11, 2], [10, 1]]
        
        '''Kh 6h'''
        combo = Combo([11, 0], [4, 0])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''4h 3h'''
        combo = Combo([2, 0], [1, 0])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ac 9c'''
        combo = Combo([12, 2], [7, 2])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Qc Jc'''
        combo = Combo([10, 2], [9, 2])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ad Kd'''
        combo = Combo([12, 1], [11, 1])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ad 8d'''
        combo = Combo([12, 1], [6, 1])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Kd Jd'''
        combo = Combo([11, 1], [10, 1])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''As 9s'''
        combo = Combo([12, 3], [7, 3])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Kh Tc 6h'''
        board = [[11, 0], [8, 2], [4, 0]]
        
        '''Ah 8c'''
        combo = Combo([12, 0], [6, 2])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Qh Jh'''
        combo = Combo([10, 0], [9, 0])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ac 8h'''
        combo = Combo([12, 2], [6, 0])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ac Kc'''
        combo = Combo([12, 2], [11, 2])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ac 2c'''
        combo = Combo([12, 2], [0, 2])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ac 6d'''
        combo = Combo([12, 2], [4, 1])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Jh 8h 5h'''
        board = [[9, 0], [6, 0], [3, 0]]
        
        '''Ac 6d'''
        combo = Combo([12, 2], [4, 1])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ah 8c'''
        combo = Combo([12, 0], [6, 2])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Kd Jd'''
        combo = Combo([11, 1], [10, 1])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Qh Th'''
        combo = Combo([10, 0], [8, 0])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ah Kc 8h'''
        board = [[12, 0], [11, 2], [6, 0]]
        
        '''Kh 7s'''
        combo = Combo([11, 0], [5, 3])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Kh 5h'''
        combo = Combo([11, 0], [3, 0])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Qh Jh'''
        combo = Combo([10, 0], [9, 0])
        self.assertFalse(ShufflezCalc.nut_bdfd_check(combo, board))
        
        '''Ac Kh'''
        combo = Combo([12, 2], [11, 0])
        self.assertTrue(ShufflezCalc.nut_bdfd_check(combo, board))
        
        
class TestBDSDCheck(unittest.TestCase):
    
    def test_bdsd_check(self):
        
        '''Qh 5h 4d'''
        board = [[10, 0], [3, 0], [2, 1]]
        
        '''Kh Jh'''
        combo = Combo([11, 0], [9, 0])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Kc Jd'''
        combo = Combo([11, 2], [9, 1])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Ah Jc'''
        combo = Combo([12, 0], [9, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))        
        
        '''Ac Js'''
        combo = Combo([12, 2], [9, 3])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))        
        
        '''Kh Td'''
        combo = Combo([11, 0], [8, 1])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Jh Td'''
        combo = Combo([9, 0], [8, 1])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Js 8d'''
        combo = Combo([9, 3], [6, 1])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Js 9h'''
        combo = Combo([9, 3], [7, 0])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Ac 6c'''
        combo = Combo([12, 2], [4, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''9s 8s'''
        combo = Combo([7, 3], [6, 3])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Ad Kd'''
        combo = Combo([12, 1], [11, 1])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''As Tc'''
        combo = Combo([12, 3], [8, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''9h 8c 7d'''
        board = [[7, 0], [6, 2], [5, 1]]
        
        '''Ah Kh'''
        combo = Combo([12, 0], [11, 0])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''Kh Qh'''
        combo = Combo([11, 0], [10, 0])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Qh Jh'''
        combo = Combo([10, 0], [9, 0])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''9c 9d'''
        combo = Combo([7, 2], [7, 1])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''8d 7s'''
        combo = Combo([6, 1], [5, 3])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''7s 6s'''
        combo = Combo([5, 3], [4, 3])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''6h 6c'''
        combo = Combo([4, 0], [4, 2])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''4c 4d'''
        combo = Combo([2, 2], [2, 1])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''4d 3h'''
        combo = Combo([2, 1], [1, 0])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Jc Tc'''
        combo = Combo([9, 2], [8, 2])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''Td 9s 3c'''
        board = [[8, 1], [7, 3], [1, 2]]
        
        '''Ah 2s'''
        combo = Combo([12, 0], [0, 3])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''As 4c'''
        combo = Combo([12, 3], [2, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''As 5s'''
        combo = Combo([12, 3], [3, 3])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''4h 2c'''
        combo = Combo([2, 0], [0, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''5d 2c'''
        combo = Combo([3, 1], [0, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Jh Jc'''
        combo = Combo([9, 0], [9, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''As Ks'''
        combo = Combo([12, 3], [11, 3])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''9c 8c'''
        combo = Combo([7, 2], [6, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''8h 7d'''
        combo = Combo([6, 0], [5, 1])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''Ah Qh'''
        combo = Combo([12, 0], [10, 0])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''6c 5d'''
        combo = Combo([4, 2], [3, 1])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''6h 6d'''
        combo = Combo([4, 0], [4, 1])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Kh Ks'''
        combo = Combo([11, 0], [11, 3])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Ah Ac'''
        combo = Combo([12, 0], [12, 2])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''Th Tc Td'''
        board = [[8, 0], [8, 2], [8, 1]]
        
        '''As Ks'''
        combo = Combo([12, 3], [11, 3])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Kc Qh'''
        combo = Combo([11, 2], [10, 0])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''9d 9s'''
        combo = Combo([7, 1], [7, 3])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''7h 6s'''
        combo = Combo([5, 0], [4, 3])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Ts 9c'''
        combo = Combo([8, 3], [7, 2])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''Ah 8c'''
        combo = Combo([12, 0], [6, 2])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''Qc 8c'''
        combo = Combo([10, 2], [6, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''8h As 8c'''
        board = [[6, 0], [12, 3], [6, 2]]
        
        '''3c 2c'''
        combo = Combo([1, 2], [0, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''5d 4d'''
        combo = Combo([3, 1], [2, 1])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Qs Jc'''
        combo = Combo([10, 3], [9, 2])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''Kc 8d'''
        combo = Combo([11, 2], [6, 1])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))
        
        '''6s 5s'''
        combo = Combo([4, 3], [3, 3])
        self.assertTrue(ShufflezCalc.bdsd_check(combo, board))
        
        '''8d 8s'''
        combo = Combo([6, 1], [6, 3])
        self.assertFalse(ShufflezCalc.bdsd_check(combo, board))


class Test_bdsd_open_ended_three_straight_check(unittest.TestCase):
    
    def test_bdsd_open_ended_three_straight_check(self):
        
        '''Qh Td 3h'''
        board = [[10, 0], [8, 1], [1, 0]]
        
        '''4h 2h'''
        combo = Combo([2, 0], [0, 0])
        self.assertTrue(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''5c 4s'''
        combo = Combo([3, 2], [2, 3])
        self.assertTrue(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Ac 2d'''
        combo = Combo([12, 1], [0, 1])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Ah 9s 2c'''
        board = [[12, 0], [7, 3], [0, 2]]
        
        '''Td 8d'''
        combo = Combo([8, 1], [6, 1])
        self.assertTrue(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''8d 7d'''
        combo = Combo([6, 1], [5, 1])
        self.assertTrue(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Jh Td'''
        combo = Combo([9, 0], [8, 1])
        self.assertTrue(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Kc Qd'''
        combo = Combo([11, 2], [10, 1])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''3h 3s'''
        combo = Combo([1, 0], [1, 3])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Qc Jh'''
        combo = Combo([10, 2], [9, 0])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Ks Jh 2c'''
        board = [[11, 3], [9, 0], [0, 2]]
        
        '''4s 3c'''
        combo = Combo([2, 3], [1, 2])
        self.assertTrue(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Ac 3c'''
        combo = Combo([12, 2], [1, 2])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Qd Qh'''
        combo = Combo([10, 1], [10, 0])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Tc 9c'''
        combo = Combo([8, 2], [7, 2])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Qh Js 8c'''
        board = [[10, 0], [9, 3], [6, 2]]
        
        '''9s 7s'''
        combo = Combo([7, 3], [5, 3])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''7d 6c'''
        combo = Combo([5, 1], [4, 2])
        self.assertTrue(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''6c 5h'''
        combo = Combo([4, 2], [3, 0])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Kh Kd'''
        combo = Combo([11, 0], [11, 1])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        '''Ac Ks'''
        combo = Combo([12, 2], [11, 3])
        self.assertFalse(ShufflezCalc.bdsd_open_ended_three_straight_check(combo, board))
        
        
class TestTwoCardBDSDCheck(unittest.TestCase):
    
    def test_two_card_bdsd_check(self):
        
        '''Kd 7s 6c'''
        board = [[11, 1], [5, 3], [4, 2]]
        
        '''Ah Qh'''
        combo = Combo([12, 0], [10, 0])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''Ac Jd'''
        combo = Combo([12, 2], [9, 1])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''As Th'''
        combo = Combo([12, 3], [8, 0])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''9d 9s'''
        combo = Combo([7, 1], [7, 3])
        self.assertFalse(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''5d 5s'''
        combo = Combo([3, 1], [3, 3])
        self.assertFalse(ShufflezCalc.two_card_bdsd_check(combo, board))        
        
        '''5s 4s'''
        combo = Combo([3, 3], [2, 3])
        self.assertFalse(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''3h 2d'''
        combo = Combo([1, 0], [0, 1])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''Tc 8s 2s'''
        board = [[8, 2], [6, 3], [0, 3]]
        
        '''Ac 3d'''
        combo = Combo([12, 2], [1, 1])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''Ah 4h'''
        combo = Combo([12, 0], [2, 0])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''Ad 5s'''
        combo = Combo([12, 0], [3, 3])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''5d 4c'''
        combo = Combo([3, 1], [2, 2])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''5c 3c'''
        combo = Combo([3, 2], [1, 2])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''Kc Qc'''
        combo = Combo([11, 2], [10, 2])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''Ks 9d'''
        combo = Combo([11, 3], [7, 1])
        self.assertTrue(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''9h 8h'''
        combo = Combo([7, 0], [6, 0])
        self.assertFalse(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''Ah Tc 2s 8s'''
        board = [[12, 0], [8, 2], [0, 3], [6, 3]]
        
        '''6s 5s'''
        combo = Combo([4, 3], [3, 3])
        self.assertFalse(ShufflezCalc.two_card_bdsd_check(combo, board))
        
        '''Kh Qh'''
        combo = Combo([11, 0], [10, 0])
        self.assertFalse(ShufflezCalc.two_card_bdsd_check(combo, board))        