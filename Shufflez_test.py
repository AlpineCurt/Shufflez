'''This is for testing random snipits of code.
This is not unit testing.'''

import ShufflezCalc
import ShufflezWidgets

'''Jc Th 9d'''
#board = [[9, 2], [8, 0], [7, 1]]
#board = 'String'
#board = [[4, 1], [7, 3], [10, 2], [12, 0], [0, 0]]
#board = [[8, 2], [7, 3], [6, 3]]


'''3d 2h Ac -> 3'''
#board = [[1, 1], [0, 0], [12, 2]]

'''6d 7c 8h 9s Qh -> 9'''
#board = [[4, 1], [5, 2], [6, 0], [7, 3], [10, 0]]

'''Ah Kc Td 9s 8s'''
#board = [[12, 0], [11, 2], [8, 1], [7, 3], [6, 3]]

'''7c 6d 5s Jc Qh -> 6'''
#board = [[5, 2], [4, 1], [3, 3], [9, 2], [10, 0]]

'''Qh Jc 4c 3d 7c -> None'''
#board = [[10, 0], [9, 2], [2, 2], [1, 1], [5, 2]]

#print(ShufflezCalc.nut_straight_rank(board, 2))

'''Qc Js Tc Qd Jd'''
#board = [[10, 2], [9, 2], [8, 2], [10, 1], [9, 1]]
#print('dup free board: ', ShufflezCalc.removeDuplicateRanks(board))

#'''As Ks'''
#combo = ShufflezWidgets.Combo([12, 3], [11, 3])
#'''Qc Jc Tc Qd Jd'''
#board = [[10, 2], [9, 2], [8, 2], [10, 1], [9, 1]]
#print(ShufflezCalc.straight_check(combo, board))


#'''Ah As'''
#combo = ShufflezWidgets.Combo([12, 0], [12, 3])

#'''3s 2s 5d 4s'''
#board = [[1, 3], [0, 3], [3, 1], [2, 3]]

#print(ShufflezCalc.straight_check(combo, board))

'''Kc Qh'''
combo = ShufflezWidgets.Combo([11, 2], [10, 0])        

'''Jc Td 9s'''
board = [[9, 2], [8, 1], [7, 3]]
print(ShufflezCalc.nut_straight_check(combo, board))