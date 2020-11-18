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

def top_pair_check(combo, board):
    '''Returns True if one of the hole cards is used to make top pair.
    Does not check for made hand on baord.  Dependent on being used
    after checking for other made hands.'''
    
    '''If board top rank is paired, no top pair is possible'''
    board_sorted = sorted(board, key=lambda card: card[0], reverse=True)
    
    if board_sorted[0][0] == board_sorted[1][0]:
        return False
    
    '''Pocket pair cannnot be top pair'''
    if combo.cardA[0] == combo.cardB[0]:
        return False
    
    test_combo = [combo.cardA, combo.cardB]
    
    if combo.cardA[0] == board_sorted[0][0]:
        return True
    elif combo.cardB[0] == board_sorted[0][0]:
        return True
    else:
        return False

def top_pair_kicker_rank(board, rank_needed):
    '''Returns an integer of the rank that would make the desired type
    of top pair.  rank_needed is the nth top pair kicker rank needed.
    i.e. 1 will return kicker rank needed for TPTK.  2 will return
    top pair, second kicker and so on.'''
    
    board_ranks = set()
    
    for card in board:
        board_ranks.add(card[0])
    
    desired_rank = rank_needed - 1
    rank_count = 0
    
    for i in range(12, 0, -1):
        if i not in board_ranks:
            if desired_rank == rank_count:
                return i
            else:
                rank_count += 1

def top_pair_top_kicker(combo, board):
    '''Returns True if the hole cards make top pair top kicker given
    the board.  Dependent on top_pair_check already being done.'''
    
    kicker_rank = top_pair_kicker_rank(board, 1)
    
    if kicker_rank == combo.cardA[0] or kicker_rank == combo.cardB[0]:
        return True
    else:
        return False

def top_pair_second_kicker(combo, board):
    '''Returns True if the hole cards make top pair second kicker
    given the board.  Dependent on top_pair_check and
    top_pair_top_kicker already being done.'''
    
    kicker_rank = top_pair_kicker_rank(board, 2)
    
    if kicker_rank == combo.cardA[0] or kicker_rank == combo.cardB[0]:
        return True
    else:
        return False    

def top_pair_third_kicker(combo, board):
    '''Returns True if the hole cards make top pair second kicker
    given the board.  Dependent on top_pair_check and
    top_pair_top_kicker/second_kicker already being done.'''
    
    kicker_rank = top_pair_kicker_rank(board, 3)
    
    if kicker_rank == combo.cardA[0] or kicker_rank == combo.cardB[0]:
        return True
    else:
        return False
    
def top_pair_middle_kicker(combo, board):
    '''Returns True if the hole cards make top pair middle kicker
    given the board. Middle kicker is 4th-6th kicker'''
    
    kickers = set()
    kickers.add(top_pair_kicker_rank(board, 4))
    kickers.add(top_pair_kicker_rank(board, 5))
    kickers.add(top_pair_kicker_rank(board, 6))
    
    if combo.cardA[0] in kickers or combo.cardB[0] in kickers:
        return True
    else:
        return False

def pp_below_tp_check(combo, board):
    '''Returns True if hole cards are paired but the rank is below
    the highest board card, but above the second highest board card.'''
    
    '''If hole cards are not paired, no pp possible.'''
    if combo.cardA[0] != combo.cardB[0]:
        return False
    
    dup_free_board = removeDuplicateRanks(board)
    board_sorted = sorted(dup_free_board, key=lambda card: card[0], reverse=True)
    
    board_high_rank = board_sorted[0][0]
    if len(board_sorted) > 1:
        board_second_high_rank = board_sorted[1][0]
    else:
        board_second_high_rank = board_sorted[0][0]
    
    if combo.cardA[0] < board_high_rank and combo.cardA[0] > board_second_high_rank:
        return True
    else:
        return False

def middle_pair_check(combo, board):
    '''Returns True if one of the hole cards pairs with the second
    highest rank on the board.  Middle pair is not possible if the
    board's second highest rank is paired on the board.'''
    
    if combo.cardA[0] == combo.cardB[0]:
        return False
    
    board_sorted = sorted(board, key=lambda card: card[0], reverse=True)
    board_high_rank = None
    board_second_rank = None
    
    for card in board_sorted:
        if board_high_rank == None:
            board_high_rank = card[0]
        elif card[0] != board_high_rank and board_second_rank == None:
            board_second_rank = card[0]
        elif card[0] == board_second_rank:
            return False
    
    if combo.cardA[0] == board_second_rank or combo.cardB[0] == board_second_rank:
        return True
    else:
        return False

def weak_pair_check(combo, board):
    '''Returns True if any hole card pairs with the third board rank
    or lower.  Pocket pairs below second board rank are considered
    weak pairs.  If board is double paired, weak pairs are not possible.'''
    
    '''Determine if board is double paired.'''
    if len(board) > 4:
        if card_histogram(board) == [2, 2, 1] or card_histogram(board) == [2, 2]:
            return False
    
    weak_ranks = set()
    strong_ranks = set()
    
    board_sorted = sorted(board, key=lambda card: card[0], reverse=True)
    board_high_rank = None
    board_second_rank = None
    
    for card in board_sorted:
        if len(strong_ranks) < 2:
            if card[0] not in strong_ranks:
                strong_ranks.add(card[0])
        else:
            weak_ranks.add(card[0])
    
    if combo.cardA[0] in weak_ranks or combo.cardB[0] in weak_ranks:
        return True
    elif combo.cardA[0] == combo.cardB[0] and combo.cardA[0] < min(strong_ranks):
        return True
    else:
        return False

def ace_high_check(combo):
    '''Returns True if only one hole card is an Ace.  Dependent on every
    other made hand check being performed first.'''
    
    if combo.cardA[0] == combo.cardB[0]:
        return False
    if combo.cardA[0] == 12 or combo.cardB[0] == 12:
        return True
    else:
        return False

def overcards_check(combo, board):
    '''Returns True if both hole card ranks are greater than highest
    board rank.  Dependent on every other made hand check being
    performed first.'''
    
    if len(board) == 5:
        return False
    
    board_sorted = sorted(board, key=lambda card: card[0], reverse=True)
    high_rank = board_sorted[0][0]
    
    if combo.cardA[0] > high_rank and combo.cardB[0] > high_rank:
        return True
    else:
        return False

def flush_draw_check(combo, board):
    '''Returns True if one or both hole cards are used to make
    a four card flush'''
    
    '''Draws not possible on river.'''
    if len(board) == 5:
        return False
    
    '''If board has 4 or 5 of same suit, no FD is possible.'''
    suits_list = [[], [], [], []]
    for card in board:
        suits_list[card[1]].append(card)
    for suit in suits_list:
        if len(suit) >= 4:
            return False
    
    test_combo = [combo.cardA, combo.cardB]
    
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
        
    '''Check for 4 of a single suit'''
    for suit in suits_list:
        if len(suit) == 4:
            if combo.cardA in suit or combo.cardB in suit:
                return True
    return False

def nut_flush_draw_check(combo, board):
    '''Returns True if at least one hole card is used to make
    the nut flush draw.  Dependent on being used after a combo
    passes flush draw check.'''
    
    nut_cards = nut_flush_draw_card(board, 1)
    
    if combo.cardA in nut_cards or combo.cardB in nut_cards:
        return True
    else:
        return False

def second_nut_flush_draw_check(combo, board):
    
    nut_cards = nut_flush_draw_card(board, 2)
    
    if combo.cardA in nut_cards or combo.cardB in nut_cards:
        return True
    else:
        return False    

def nut_flush_draw_card(board, nut_rank):
    '''Returns a list containing cards as a list [rank, suit] that
    would make the specified nut_rank flush.  nut_rank of 1 will
    find card(s) that make the nut flush draw.  nut_rank of 2 will
    find card(s) that make second nut flush draw.'''
    
    if len(board) == 5:
        return None
    
    nut_draw_cards = []
    
    '''Sort by suit'''
    suits = [[], [], [], []]
    
    
    for card in board:
        suits[card[1]].append(card)
    
    
    for i, n in enumerate(suits):
        nut_found = 0
        if len(n) == 2 or len(n) == 3:
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
                        nut_draw_cards.append([rank, suit])
                        break
                    else:
                        nut_found += 1
    return nut_draw_cards

def straight_draw_check(combo, board):
    '''Returns True if either or both hole cards create four to a straight.
    Hole card must be included in the four to a straight; four to a
    straight on the board does not count.'''
    
    '''No draws on the river'''
    if len(board) == 5:
        return False
    
    '''At least one hole card rank must differ from board ranks'''
    board_ranks = []
    for card in board:
        board_ranks.append(card[0])
    if combo.cardA[0] in board_ranks and combo.cardB[0] in board_ranks:
        return False
    
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
        
    '''Check every group of four cards'''
    ci = 0
    while len(test_board) - ci >= 4:
        four_card_test = [test_board[ci], test_board[ci + 1], test_board[ci + 2], 
                          test_board[ci + 3]]
        if 3 <= four_card_test[0][0] - four_card_test[3][0] <= 4:
            for card in test_combo:
                if card in four_card_test:
                    return True
        ci += 1
    return False

def oesd_check(combo, board):
    '''Returns True if the hole cards and the board make an
    Open Ended Straight Draw.  OESD is defined as haivng two
    different ranks that could complete the straight.  This
    function assumes the combo has passed straight_draw_check.'''
    
    '''Combine combo cards with board cards and remove duplicate ranks'''
    test_board = removeDuplicateRanks(board, [combo.cardA, combo.cardB])
    test_board = sorted(test_board, key=lambda card: card[0], reverse=True)    
    
    '''Add wheel ace if necessary'''
    if test_board[0][0] == 12:
        test_board.append([-1, test_board[0][1]])
    
    test_board_ranks = []
    for card in test_board:
        test_board_ranks.append(card[0])
    
    draw_count = 0  # track number of cards that could make a straight
    found_draws = set()
    
    ci = 0
    
    '''Plug in each missing rank and see if it makes a straight'''
    while len(test_board_ranks) - ci >= 4:
        four_card_test = [test_board_ranks[ci], test_board_ranks[ci + 1], test_board_ranks[ci + 2], 
                          test_board_ranks[ci + 3]]
        for i in range(12, -2, -1):
            if i not in four_card_test:
                board_ranks = four_card_test.copy()
                board_ranks.append(i)
                board_ranks = sorted(board_ranks, reverse=True)
                if board_ranks[0] - board_ranks[4] == 4:
                    if i not in found_draws:
                        found_draws.add(i)
                        draw_count += 1
        ci += 1
        
    if draw_count == 2:
        return True
    else:
        return False

def bdfd_check(combo, board):
    '''Returns True if at least one of the hole cards is used
    to make a backdoor flush draw.  Only possible on the flop.'''
    
    if len(board) != 3:
        return False
    
    if board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return False
    
    test_board = board.copy()
    test_board.append(combo.cardA)
    test_board.append(combo.cardB)
    
    suits_list = [[], [], [], []]
    
    for card in test_board:
        suits_list[card[1]].append(card)
    
    for suit in suits_list:
        if len(suit) == 3:
            return True
    
    return False

def two_card_bdfd_check(combo):
    '''Returns True if the hole cards are the same suit. Intended
    to be used only after a combo has passed bdfd_check()'''
    
    if combo.cardA[1] == combo.cardB[1]:
        return True
    else:
        return False
    
def nut_bdfd_check(combo, board):
    '''Returns True if the hole card combo is drawing to the nut flush.
    Dependent on combo already having passed bdfd_check()'''
    
    if len(board) != 3:
        return False
    
    '''Find Nut Flush card for each suit'''
    suit_nuts = [12, 12, 12, 12]
    board_sorted = sorted(board, key=lambda card: card[0], reverse=True)
    for card in board_sorted:
        if card[0] == suit_nuts[card[1]]:
            suit_nuts[card[1]] -= 1    
    
    test_board = board.copy()
    test_board.append(combo.cardA)
    test_board.append(combo.cardB)
    
    suits_list = [[], [], [], []]
    
    for card in test_board:
        suits_list[card[1]].append(card)
        
    for i, suit in enumerate(suits_list):
        if len(suit) == 3:
            if [suit_nuts[i], i] in suit:
                return True
    return False

def bdsd_check(combo, board):
    '''Returns True if if one or both hole cards are used to
    make a backdoor straight draw.'''
    
    if len(board) != 3:
        return False
    
    if straight_check(combo, board):
        return False
    
    if straight_draw_check(combo, board):
        return False
    
    '''At least one hole card rank must differ from board ranks'''
    board_ranks = []
    for card in board:
        board_ranks.append(card[0])
    if combo.cardA[0] in board_ranks and combo.cardB[0] in board_ranks:
        return False
    
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
        
    '''Check every group of three cards'''
    ci = 0
    while len(test_board) - ci >= 3:
        three_card_test = [test_board[ci], test_board[ci + 1], test_board[ci + 2]]
        if 2 <= three_card_test[0][0] - three_card_test[2][0] <= 4:
            for card in test_combo:
                if card in three_card_test:
                    return True
        ci += 1
    return False

def bdsd_open_ended_three_straight_check(combo, board):
    '''Returns True if both hard cards are used to make an
    open ened three straight.'''
    
    if len(board) != 3:
        return False
    
    if straight_check(combo, board):
        return False
    
    if straight_draw_check(combo, board):
        return False
    
    '''Both hole cards must differ from board ranks'''
    board_ranks = []
    for card in board:
        board_ranks.append(card[0])
    if combo.cardA[0] in board_ranks or combo.cardB[0] in board_ranks:
        return False
    
    '''Combine combo cards with board cards and remove duplicate ranks'''
    test_board = removeDuplicateRanks(board, [combo.cardA, combo.cardB])
    test_board = sorted(test_board, key=lambda card: card[0], reverse=True)
     
    
    '''Check every group of three cards'''
    ci = 0
    while len(test_board) - ci >= 3:
        three_card_test = [test_board[ci], test_board[ci + 1], test_board[ci + 2]]
        if three_card_test[0][0] - three_card_test[2][0] == 2:
            if combo.cardA in three_card_test and combo.cardB in three_card_test:
                if three_card_test[0][0] != 12:
                    return True
        ci += 1
    return False

def two_card_bdsd_check(combo, board):
    '''Returns True if both hole cards are used to make a
    back door straight draw.'''
    
    if len(board) != 3:
        return False
    
    if straight_check(combo, board):
        return False
    
    if straight_draw_check(combo, board):
        return False
    
    '''Both hole card ranks must differ from board ranks'''
    board_ranks = []
    for card in board:
        board_ranks.append(card[0])
    if combo.cardA[0] in board_ranks or combo.cardB[0] in board_ranks:
        return False
    
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
        
    '''Check every group of three cards'''
    ci = 0
    card_count = 0
    while len(test_board) - ci >= 3:
        card_count = 0
        three_card_test = [test_board[ci], test_board[ci + 1], test_board[ci + 2]]
        if 2 <= three_card_test[0][0] - three_card_test[2][0] <= 4:
            for card in three_card_test:
                if card in test_combo:
                    card_count += 1
            if card_count == 2:
                return True
        ci += 1
    return False