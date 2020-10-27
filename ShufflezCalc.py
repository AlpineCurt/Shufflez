'''
Contains all functions for "Poker Math" such as:
-Calculating made hands for RangeStats
-Checking if a combo and a board make a made hand
'''

from itertools import combinations

def removeBlockedCombos(combos, board):
    '''
    Removes from combos parameter any Combo objects that are not
    possible given the board.  Returns a list of Combo objects.
    '''
    
    unblockedCombos = []
    
    for combo in combos:
        if combo.cardA not in board and combo.cardB not in board:
            unblockedCombos.append(combo)
    
    return unblockedCombos

def removeDuplicateRanks(board, hole_cards = None):
    '''
    Returns a list of cards [rank, suit] without any cards of the 
    same rank.  Prioritizes the first card it encounters.
    hole_cards needs to be a list of card lists i.e.
    [[rank, suit], [rank, suit]]
    '''
    dup_free_board = []
    ranks_present = set()
    for card in board:
        if card[0] not in ranks_present:
            ranks_present.add(card[0])
            dup_free_board.append(card)
    
    if hole_cards != None:
        for card in hole_cards:
            if card[0] not in ranks_present:
                ranks_present.add(card[0])
                dup_free_board.append(card)        
    
    return dup_free_board

def card_histogram(combos):
    '''
    Returns a histogram of card ranks as a list. combos parameter is a list
    [rank, suit] lists.
    Returned List is sorted by highest numbe of repeating rank to lowest
    regardless of the value of the ranks.
    i.e. [4, 1] or [3, 2] or [3, 1, 1] or [1, 1, 1, 1, 1]
    Used for quickly determining made hand type and/or if a 
    made hand is present.
    combos parameter is a list of cards in list form.  i.e. [10, 2]
    '''
    
    hist = {}
    for combo in combos:
        if combo[0] in hist:
            hist[combo[0]] += 1
        else:
            hist[combo[0]] = 1
    
    hist_list = []
    for i in hist:
        hist_list.append(hist.get(i))
    
    hist_list = sorted(hist_list, reverse = True)
    
    return hist_list

def board_str_flush_check(board):
    '''Returns true if five cards in board parameter make
    a straight flush'''
    
    if card_histogram(board) != [1, 1, 1, 1, 1]:
        return False
    
    test_board = sorted(board, key=lambda card: card[0], reverse=True)
    
    '''Add wheen ace if needed'''
    if test_board[0][0] == 12:
        test_board.append([-1, test_board[0][1]])        
        
    ci = 0
    
    while len(test_board) - ci >= 5:
    
        '''Check if all stuits are equal'''
        suits = [test_board[ci][1], test_board[ci + 1][1], test_board[ci + 2][1],
                 test_board[ci + 3][1], test_board[ci + 4][1]]
        
        if suits[1:] == suits[:-1]:
            if test_board[ci][0] - test_board[ci + 4][0] == 4:
                return True
        ci +=1
    
    return False

def str_flush_check(combo, board):
    '''Returns True if at least one hold card is used to make a straight flush.
    Hole card used must be higher than a straight flush on the board (if one is present).
    combo is a Combo object.  board is a list of [rank, suit] lists.'''
    
    test_combo = [combo.cardA, combo.cardB]
    
    '''Add wheel Ace if ace(s) are present.'''
    for card in test_combo:
        if card[0] == 12:
            test_combo.append([-1, card[1]])
    
    '''Check for Straight Flush on the board.'''
    board_str_flush_high_rank = 0
    
    if len(board) == 5:
        
        '''Sort from highest rank to lowest'''
        test_board = sorted(board, key=lambda card: card[0], reverse=True)
        
        '''Add wheel Ace if needed'''
        if test_board[0][0] == 12:
            test_board.append([-1, test_board[0][1]])
        
        '''Check if all suits are equal'''
        for card in test_board:
            '''all() interperates 0 as false, so convert h (0 value) to 4'''
            if card[1] == 0:
                card[1] = 4
        if all(test_board[1]):
            
            ci = 0  # card index
            
            while len(test_board) - ci >= 5:
                if test_board[ci][0] - test_board[ci + 4][0] == 4:
                    '''straight flush on board found'''
                    board_str_flush_high_rank = test_board[ci][0]
                    break
                ci += 1
        for card in test_board:
            '''convert h back to 0'''
            if card[1] == 4:
                card[1] = 0
    
    '''Combine combo cards and board cards'''
    test_board = board.copy()
    for card in test_combo:
        test_board.append(card)
    
    '''Assign each card in test_board to correct suit list.
    Index of suits_list is equal to its suit.
    0 = h, 1 = d, 2 = c, 3 = s'''
    suits_list = [[], [], [], []]
    for card in test_board:
        suits_list[card[1]].append(card)
    
    '''Check for 5 or more of a single suit'''
    for suit in suits_list:
        if len(suit) >= 5:
            suit_sort = sorted(suit, key=lambda card: card[0], reverse=True)
            
            ci = 0  # card index
            while len(suit) - ci >= 5:
                five_card_test = [suit_sort[ci], suit_sort[ci + 1], suit_sort[ci + 2],
                                  suit_sort[ci + 3], suit_sort[ci + 4]]
                if five_card_test[0][0] - five_card_test[4][0] == 4 and five_card_test[0][0] > board_str_flush_high_rank:
                    '''Straight Flush Found; check if hole card used'''
                    for card in test_combo:
                        if card in five_card_test:
                            return True
                
                ci += 1
    return False

def board_quads_check(board):
    '''Returns True if quads are present on the board.'''
    
    if 4 in card_histogram(board):
        return True
    else:
        return False

def quads_check(combo, board):
    '''Returns true if at least one hole card is used to
    make four of a kind.'''
    
    '''Check for Quads on the board'''
    if len(board) >= 4:
        board_sorted = sorted(board, key=lambda card: card[0], reverse=True)
        
        ci = 0  # card index
        
        while len(board_sorted) - ci >= 4:
            four_card_test = [board_sorted[ci][0], board_sorted[ci + 1][0], board_sorted[ci + 2][0],
                              board_sorted[ci + 3][0]]
            '''Check if all same rank'''
            if four_card_test[1:] == four_card_test[:-1]:
                return False
            
            ci += 1
    
    '''Combine combo and board, and sort'''
    test_board = board.copy()
    test_board.append(combo.cardA)
    test_board.append(combo.cardB)
    
    test_board = sorted(test_board, key=lambda card: card[0], reverse=True)
    
    '''Check for Quads in entire card list'''
    
    ci = 0
    
    while len(test_board) - ci >= 4:
        four_card_test = [test_board[ci][0], test_board[ci + 1][0], test_board[ci + 2][0],
                          test_board[ci + 3][0]]
        if four_card_test[1:] == four_card_test[:-1]:
            return True
        ci += 1
        
    return False


def board_full_house_check(board):
    '''Returns True if a full house is present on the board.'''
    
    if card_histogram(board) == [3, 2]:
        return True
    else:
        return False

def full_house_check(combo, board):
    '''Returns True if at least one hole card is used to make a full house,
    or improve a full house on the board.'''
    
    '''Check for at least one pair.  If every card rank is different,
    no full house is possible.'''
    board_check = card_histogram(board)
    for i in board_check:
        if i >= 2:
            break
    else:
        return False
    
    '''Check if full house on board, make note of ranks of trips and pair'''
    trips_rank, pair_rank = None, None
    
    if board_full_house_check(board):
        board_sort = sorted(board, key=lambda card: card[0], reverse=True)
        if board_sort[2][0] > board_sort[3][0]:
            trips_rank, pair_rank = board_sort[0][0], board_sort[-1][0]
        else:
            trips_rank, pair_rank = board_sort[-1][0], board_sort[0][0]

    '''List for checking if hole card used'''
    test_combo = [combo.cardA, combo.cardB]
    
    '''Combine combo with board'''
    test_board = board.copy()
    test_board.append(combo.cardA)
    test_board.append(combo.cardB)
    
    test_board = combinations(test_board, 5)
    
    '''Test each combination of five cards for a full house'''
    for i in list(test_board):
        if card_histogram(i) == [3, 2]:
            for card in test_combo:
                if card in i:
                    '''Check that either trips or pair is higher than board trips or pair'''
                    if trips_rank == None:
                        return True
                    else:
                        i_sorted = sorted(i, key=lambda card: card[0], reverse=True)
                        if i_sorted[2][0] > i_sorted[3][0]:
                            i_trips_rank, i_pair_rank = i_sorted[0][0], i_sorted[-1][0]
                        else:
                            i_trips_rank, i_pair_rank = i_sorted[-1][0], i_sorted[0][0]
                        if i_trips_rank == trips_rank and i_pair_rank > pair_rank:
                            return True
                        elif i_trips_rank > trips_rank:
                            return True
    return False

def board_flush_check(board):
    '''Returns True if a flush is on the board'''
    
    if card_histogram(board) == [1, 1, 1, 1, 1]:
        suits = [board[0][1], board[1][1], board[2][1],
                 board[3][1], board[4][1]]
        if suits[1:] == suits[:-1]:
            return True
    return False

def flush_check(combo, board):
    '''Returns True if at least one hole card is used to make a flush, or
    improve a flush on the board'''
    
    test_combo = [combo.cardA, combo.cardB]
    
    '''Check for flush on board'''
    board_flush_low_card = -1
    if board_flush_check(board):
        board_flush_low_card = min(board[0][0], board[1][0], board[2][0],
                                    board[3][0], board[4][0])
    
    '''Combine combo with board cards'''
    test_board = board.copy()
    test_board.append(combo.cardA)
    test_board.append(combo.cardB)
    
    '''Sort by suit'''
    test_board = sorted(test_board, key=lambda card: card[1])
    
    '''Check every group of five cards'''
    ci = 0
    
    while len(test_board) - ci >= 5:
        five_card_test = [test_board[ci], test_board[ci + 1], test_board[ci + 2],
                                  test_board[ci + 3], test_board[ci + 4]]
        suits_list = [five_card_test[0][1], five_card_test[1][1], five_card_test[2][1],
                          five_card_test[3][1], five_card_test[4][1]]
        if suits_list[1:] == suits_list[:-1]:
            for card in test_combo:
                if card in five_card_test and card[0] > board_flush_low_card:
                    return True
        ci += 1
    
    return False

def nut_flush_check(combo, board):
    '''Returns True if combo is used to make the nut flush
    given the board.  Does not care if the combo actually makes a flush.
    This method is run after ShufflezCalc.flush_check() and assumes the combo
    makes a flush.'''
    
    nut_card = nut_flush_card(board, 1)
    
    if combo.cardA == nut_card or combo.cardB == nut_card:
        return True
    else:
        return False

def second_nut_flush_check(combo, board):
    '''Returns True if combo is used to make the second nut flush
    given the board.  Does not care if the combo actually makes a flush.
    This method is run after ShufflezCalc.flush_check() and assumes the combo
    makes a flush.'''
    
    nut_card = nut_flush_card(board, 2)
    
    if combo.cardA == nut_card or combo.cardB == nut_card:
        return True
    else:
        return False
    
def third_nut_flush_check(combo, board):
    '''Returns True if combo is used to make the nut flush
    given the board.  Does not care if the combo actually makes a flush.
    This method is run after ShufflezCalc.flush_check() and assumes the combo
    makes a flush.'''
    
    nut_card = nut_flush_card(board, 3)
    
    if combo.cardA == nut_card or combo.cardB == nut_card:
        return True
    else:
        return False

def nut_flush_card(board, nut_rank):
    '''Finds the specified nut flush card.  nut_rank is the nth nut flush card
    you're looking for.  nut_rank of 1 will return the card that makes the
    highest possible flush.  nut_rank of 2 will return 2nd nut flush card and so on.'''
    
    if len(board) < 3 or len(board) > 5:
        return None
    
    '''Find the flush suit'''
    suits = [[], [], [], []]
    
    nut_found = 0
    
    for card in board:
        suits[card[1]].append(card)
    for i, n in enumerate(suits):
        if len(n) >= 3:
            suit = i
            suits_sorted = sorted(n, key=lambda card: card[0], reverse=True)
            rank = None
            for x in range(12, 0, -1):
                for card in suits_sorted:
                    if x in card:
                        break
                else:
                    if nut_found == nut_rank - 1:
                        rank = x
                        break
                    else:
                        nut_found += 1
    return [rank, suit]

def straight_check(combo, board):
    '''Returns true if at least one hole card is used to make a
    straight, or improve a straight on the board.'''
    
    '''Check if straight is possible with the board'''
    if nut_straight_rank(board, 1) == None:
        return False
    
    '''If straight on board, get highest hand rank'''
    if board_straight_check(board):
        board_sorted = sorted(board, key=lambda card: card[0], reverse=True)
        board_max_rank = board_sorted[0][0]
    else:
        board_max_rank = -2
    
    test_combo = [combo.cardA, combo.cardB]
    
    '''Add wheel ace to test_combo if necessary'''
    for card in test_combo:
        if card[0] == 12:
            test_combo.append([-1, card[1]])
    
    '''Combine combo cards with board cards and remove duplicate ranks'''
    test_board = removeDuplicateRanks(board, [combo.cardA, combo.cardB])
    test_board = sorted(test_board, key=lambda card: card[0], reverse=True)
    
    '''Add wheel ace if necessary'''
    if test_board[0][0] == 12:
        test_board.append([-1, test_board[0][1]])
    
    '''Check every group of five cards'''
    ci = 0
    
    while len(test_board) - ci >= 5:
        five_card_test = [test_board[ci], test_board[ci + 1], test_board[ci + 2], 
                          test_board[ci + 3], test_board[ci + 4]]
        if card_histogram(five_card_test) == [1, 1, 1, 1, 1]:
            if five_card_test[0][0] - five_card_test[4][0] == 4:
                for card in test_combo:
                    if card in five_card_test and card[0] > board_max_rank:
                        return True
        ci += 1
    return False

def nut_straight_check(combo, board):
    '''Returns True if one of the hole cards is used to make
    the nut straight.  Does not care if the hole cards actually
    make a straight.  Dependent on being used after straight_check().'''
    
    nut_rank = nut_straight_rank(board, 1)
    
    if nut_rank == combo.cardA[0] or nut_rank == combo.cardB[0]:
        return True
    else:
        return False

def second_nut_straight_check(combo, board):
    '''Returns True if one of the hole cards is used to make
    the second nut straight.  Does not care if the hole cards
    actually make a straight.  Dependent on being used after
    straight_check and after nut_straight_check'''
    
    second_nut_rank = nut_straight_rank(board, 2)
    
    if second_nut_rank == combo.cardA[0] or second_nut_rank == combo.cardB[0]:
        return True
    else:
        return False

def board_straight_check(board):
    '''Returns True is a straight is present on the board.
    Does not check for flushes or straight flushes.'''
    
    if len(board) < 5:
        return False
    if card_histogram(board) != [1, 1, 1, 1, 1]:
        return False
    
    '''Sort by rank'''
    test_board = sorted(board, key=lambda card: card[0], reverse=True)
    
    '''Add wheel ace if necessary'''
    if test_board[0][0] == 12:
        test_board.append([-1, test_board[0][1]])
    
    '''Check each sequence of five cards'''
    ci = 0
    while len(test_board) - ci >= 5:
        if test_board[ci][0] - test_board[ci + 4][0] == 4:
            return True
        ci += 1
    return False

def nut_straight_rank(board, rank_needed):
    '''Returns an integer of the rank required to make
    the nut straight.  rank_needed is the nth nut straight
    rank you're looking for.  i.e. nut_rank of 1 will return
    the rank that makes a nut straight.  Only returns 1st or
    second nut ranks.
    
    If rank_needed is 1 and None gets returned, it means a
    straight is not possible on that board.'''
    
    if rank_needed != 1 and rank_needed != 2:
        return None
    
    board_sorted = sorted(board, key=lambda card: card[0], reverse=True)
    
    '''Add wheel ace if necessary'''
    if board_sorted[0][0] == 12:
        board_sorted.append([-1, board_sorted[0][1]])
    
    '''Remove Duplicate ranks'''
    test_board = board_sorted.copy()
    board_sorted.clear()
    
    board_sorted = removeDuplicateRanks(test_board)
    
    '''Test each ordered group of three cards to see if they
    make a straight possible'''
    ci = 0
    while len(board_sorted) - ci >= 3:
        three_card_test = [board_sorted[ci], board_sorted[ci + 1], board_sorted[ci + 2]]
        if card_histogram(three_card_test) == [1, 1, 1] and three_card_test[0][0] - three_card_test[2][0] <= 4:
            board_top_rank = three_card_test[0][0]
            gap = three_card_test[0][0] - three_card_test[2][0]
            board_ranks = [three_card_test[0][0], three_card_test[1][0], three_card_test[2][0]]
            break
        ci += 1
    else:
        return None
    
    nut_rank = None
    second_nut_rank = None
    
    if gap == 2:
        rank_test_start = board_top_rank + 2
    elif gap == 3:
        rank_test_start = board_top_rank + 1
    elif gap == 4:
        rank_test_start = board_top_rank - 1
    else:
        return 'Error finding nut straight rank: Gap too large'
    
    '''Start at rank_test_start and count backwards'''
    for rank_test in range(rank_test_start, 0, -1):
        if rank_test not in board_ranks and rank_test <= 12:
            if nut_rank == None:
                nut_rank = rank_test
            else:
                if board_sorted[-1][0] == -1 and len(board) == 3:
                    second_nut_rank = None
                elif board_sorted[0][0] == 12 and len(board) < 5:
                    second_nut_rank = None
                elif gap == 4 and board_sorted[-1][0] == three_card_test[2][0]:
                    second_nut_rank = None
                else:
                    second_nut_rank = rank_test
                break
    
    if rank_needed == 1:
        return nut_rank
    elif rank_needed == 2:
        return second_nut_rank

def three_of_a_kind_check(combo, board):
    '''Returns True if at least one of the hole cards
    is used to make three of a kind.'''
    
    test_combo = [combo.cardA, combo.cardB]
    
    test_board = board.copy()
    test_board.append(combo.cardA)
    test_board.append(combo.cardB)
    
    test_board = sorted(test_board, key=lambda card: card[0], reverse=True)
    
    ci = 0
    
    while len(test_board) - ci >= 3:
        three_card_test = [test_board[ci], test_board[ci + 1], test_board[ci + 2]]
        if card_histogram(three_card_test) == [3]:
            if test_combo[0] in three_card_test or test_combo[1] in three_card_test:
                return True
        ci += 1
    return False

def board_three_of_a_kind_check(board):
    '''Returns True if three of a kind is present on the board.
    Is this necessary?  If true, any pairing of a hole card makes
    a full house which will get picked up by an earlier check.'''
    
    if 3 in card_histogram(board):
        return True
    else:
        return False

def set_check(combo, board):
    '''Returns True if both hole cards are used to make
    three of a kind.
    combo is a single Combo object; board is a list of cards as lists'''
    
    test_combo = [combo.cardA, combo.cardB]
    
    test_board = board.copy()
    test_board.append(combo.cardA)
    test_board.append(combo.cardB)

    test_board = sorted(test_board, key=lambda card: card[0], reverse=True)

    ci = 0

    while len(test_board) - ci >= 3:
        three_card_test = [test_board[ci], test_board[ci + 1], test_board[ci + 2]]
        if card_histogram(three_card_test) == [3]:
            if test_combo[0] in three_card_test and test_combo[1] in three_card_test:
                return True
        ci += 1
    return False

def two_pair_check(combo, board):
    '''Returns True if both hole cards are used to make Two Pair.
    Two Pair is invalid if board is paired higher than either hole card.'''
    
    '''Find any pairs on the board'''
    single_board_ranks = []
    paired_board_ranks = [0]
    
    for card in board:
        if card[0] not in single_board_ranks:
            single_board_ranks.append(card[0])
        else:
            paired_board_ranks.append(card[0])
    
    paired_board_ranks = sorted(paired_board_ranks, reverse=True)
    
    '''If either hole card's rank is less than higest board pair, no two pair possible.'''
    if combo.cardA[0] < paired_board_ranks[0] or combo.cardB[0] < paired_board_ranks[0]:
        return False
    
    if combo.cardA[0] in single_board_ranks and combo.cardB[0] in single_board_ranks:
        return True
    
    return False

def overpair_check(combo, board):
    '''Returns True if hole cards are paired and higher rank than highest
    board card. Does not check for made hand on board.
    Dependent on being used after checking for higher made hands.'''
    
    if combo.cardA[0] != combo.cardB[0]:
        return False
    
    board_high_rank = 0
    for card in board:
        if card[0] > board_high_rank:
            board_high_rank = card[0]
    
    if combo.cardA[0] > board_high_rank:
        return True
    else:
        return False