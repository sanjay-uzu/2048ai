import numpy as np
import matplotlib.pyplot as plt

NUMBER_OF_MOVES = 4
SAMPLE_COUNT = 50

SPM_SCALE_PARAM = 10
SL_SCALE_PARAM = 4
SEARCH_PARAM = 200

from game_functions import initialize_game, random_move,\
                            move_down, move_left,\
                            move_right, move_up,\
                            check_for_win, add_new_tile



def get_search_params(move_number):
    searches_per_move = SPM_SCALE_PARAM * (1+(move_number // SEARCH_PARAM))
    search_length = SL_SCALE_PARAM * (1+(move_number // SEARCH_PARAM))
    return searches_per_move, search_length

def ai_move(board, searches_per_move, search_length):
    dic = {0: 0, 2: 0, 4: 4, 8: 16, 16: 48, 32: 128, 64: 320, 128: 768, 256: 1792, 512: 4096, 1024: 9216, 2048: 20480}
    possible_first_moves = [move_left, move_up, move_down, move_right]
    first_move_scores = np.zeros(NUMBER_OF_MOVES)
    for first_move_index in range(NUMBER_OF_MOVES):
        first_move_function = possible_first_moves[first_move_index]
        board_with_first_move, first_move_made, first_move_score = first_move_function(board)
        if first_move_made:
            board_with_first_move = add_new_tile(board_with_first_move)
            first_move_scores[first_move_index] += first_move_score
        else:
            continue
        for _ in range(searches_per_move):
            move_number = 1
            search_board = np.copy(board_with_first_move)
            game_valid = True
            while game_valid and move_number < search_length:
                search_board, game_valid, score = random_move(search_board)
                if game_valid:
                    search_board = add_new_tile(search_board)
                    first_move_scores[first_move_index] += score
                    move_number += 1
    best_move_index = np.argmax(first_move_scores)
    best_move = possible_first_moves[best_move_index]
    search_board, game_valid, score = best_move(board)
    for elem in search_board:
        for ele in elem:
            score+=dic[ele]
    print(score)
    return search_board, game_valid,score

def ai_move3(board, searches_per_move, search_length):
    dic={0:0,2:0,4:4,8:16,16:48,32:128,64:320,128:768,256:1792,512:4096,1024:9216,2048:20480}
    len=0
    possible_first_moves = [move_left, move_up, move_down, move_right]
    available=[]
    for ele in possible_first_moves:
        x,y,z=ele(board)
        if y:
            available.append(ele)

    if (available)==None:
        return board,False
    max_score=float('-inf')
    alpha=float('-inf')
    beta=float('-inf')
    depth=1
    max_depth=8
    for ele in available:
        board1,y,z=ele(board)
        score=search2(board1,alpha,beta,depth,max_depth)
        if score>max_score:
            score=max_score
            max_move=ele
    x, y, z = max_move(board)
    score=0
    for elem in x:
        for ele in elem:
            score+=dic[ele]
    print(score)
    return x,True,score
def ai_move2(board, searches_per_move, search_length):
    len=0
    dic = {0: 0, 2: 0, 4: 4, 8: 16, 16: 48, 32: 128, 64: 320, 128: 768, 256: 1792, 512: 4096, 1024: 9216, 2048: 20480}
    possible_first_moves = [move_left, move_up, move_down, move_right]
    available=[]
    for ele in possible_first_moves:
        x,y,z=ele(board)
        if y:
            available.append(ele)

    if (available)==None:
        return board,False
    max_score=float('-inf')
    alpha=float('-inf')
    beta=float('-inf')
    depth=1
    max_depth=5
    for ele in available:
        board1,y,z=ele(board)
        score=search2(board1,alpha,beta,depth,max_depth)
        if score>max_score:
            score=max_score
            max_move=ele
    x, y, z = max_move(board)
    score = 0
    for elem in x:
        for ele in elem:
            score += dic[ele]
    print(score)
    return x, True, score
    return x,True


def search(board,alpha,beta,depth,max_depth):

    if depth>max_depth:
        return evaluate(board)
    v=float('-inf')
    possible_first_moves = [move_left, move_up, move_down, move_right]
    available = []
    tot=0
    lenth=0
    for ele in possible_first_moves:
        x,y,z=ele(board)
        if y:
            available.append(ele)
    if len(available)==0:
        return evaluate(board)
    for i in range(len(available)):
        board1, y, z = available[i](board)

        tot+=search(board1,alpha,beta,depth+1,max_depth)
        lenth+=1
        i=i+1

    return tot/lenth
def search2(board,alpha,beta,depth,max_depth):

    if depth>max_depth:
        return evaluate(board)
    v=float('-inf')
    possible_first_moves = [move_left, move_up, move_down, move_right]
    available = []
    for ele in possible_first_moves:
        x,y,z=ele(board)
        if y:
            available.append(ele)
    if len(available)==0:
        return evaluate(board)
    for i in range(len(available)):
        board1, y, z = available[i](board)
        prev_v=v
        v=max(v,search(board1,alpha,beta,depth+1,max_depth))
        if v>=beta:
            return v
        alpha=max(alpha,v)
        i=i+1
    return v

def evaluate(board):
    empty=0
    max_score=0
    result = 0
    WEIGHT_MATRIX = [
        [2048, 1024, 64, 32],
        [512, 128, 16, 2],
        [256, 8, 2, 1],
        [4, 2, 1, 1]
    ]
    mono = 0

    row, col = len(board), len(board[0]) if len(board) > 0 else 0
    for r in board:
        diff = r[0] - r[1]
        for i in range(col - 1):
            if (r[i] - r[i + 1]) * diff <= 0:
                mono += 1
            diff = r[i] - r[i + 1]

    for j in range(row):
        diff = board[0][j] - board[1][j]
        for k in range(col - 1):
            if (board[k][j] - board[k + 1][j]) * diff <= 0:
                mono += 1
            diff = board[k][j] - board[k + 1][j]
    smoothness = 0

    row, col = len(board), len(board[0]) if len(board) > 0 else 0
    for r in board:
        for i in range(col - 1):
            smoothness += abs(r[i] - r[i + 1])
            pass
    for j in range(row):
        for k in range(col - 1):
            smoothness += abs(board[k][j] - board[k + 1][j])
    for i in range(len(board)):
        for j in range(len(board)):
            result += board[i][j] * WEIGHT_MATRIX[i][j]
    for ele in board:
        for elem in ele:
            if elem==0:
                empty+=1
    return smoothness+mono+result+empty





def ai_play(board):
    move_number = 0
    valid_game = True
    while valid_game:
        move_number += 1
        number_of_simulations, search_length = get_search_params(move_number)
        board, valid_game = ai_move(board, number_of_simulations, search_length)
        if valid_game:
            board = add_two(board)
        if check_for_win(board):
            valid_game = False
        print(board)
        print(move_number)
    print(board)
    return np.amax(board)

def ai_plot(move_func):
    tick_locations = np.arange(1, 12)
    final_scores = []
    for _ in range(SAMPLE_COUNT):
        print('thing is ', _)
        board = initialize_game()
        game_is_win = ai(board)
        final_scores.append(game_is_win)
    all_counts = np.zeros(11)
    unique, counts = np.unique(np.array(final_scores), return_counts=True)
    unique = np.log2(unique).astype(int)
    index = 0

    for tick in tick_locations:
        if tick in unique:
            all_counts[tick-1] = counts[index]
            index += 1

    plt.bar(tick_locations, all_counts)
    plt.xticks(tick_locations, np.power(2, tick_locations))
    plt.xlabel("Score of Game", fontsize = 24)
    plt.ylabel(f"Frequency per {SAMPLE_COUNT} runs", fontsize = 24)
    plt.show()