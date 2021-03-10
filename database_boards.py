import random
import database_player as pl

GREEN= '\u001b[48;5;28m'
YELLOW = '\u001b[48;5;130m'
BLUE= '\u001b[48;5;4m'
END = '\u001b[0m'

BOARD_WIDTH = 100
BOARD_HEIGHT = 20
BOARD_FIELD_SIGN = '.'
BLOCKED_COORDS_1 = [(pl.PLAYER_START_X, pl.PLAYER_START_Y)]
BLOCKED_COORDS_2 = []
BLOCKED_COORDS_3 = []

def create_board(width, height): 
    return [['.']*width for x in range(height)]

def open_file(filename):
    with open(filename,"r") as afile:
        lines = afile.readlines()

    new_lines = []
    for line in lines:
        line = line.rstrip('\n')
        new_lines.append(line)
    
    return new_lines

def put_fixed_elements_on_board(filename,board,blocked_list):
    picture_lines = open_file(filename)
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            # print(i,j)
            if picture_lines[i][j] == "X":
                board[i][j] = f'{YELLOW}{picture_lines[i][j]}{END}'
                blocked_list.append((i,j))
            elif picture_lines[i][j] == "T":
                board[i][j] = f'{GREEN}{picture_lines[i][j]}{END}'
                blocked_list.append((i,j))
            elif picture_lines[i][j] == "V":
                board[i][j] = f'{BLUE}{picture_lines[i][j]}{END}'
                blocked_list.append((i,j))
                # print(board[i][j])

def prepare_board(filename,blocked_list):
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    put_fixed_elements_on_board(filename,board,blocked_list)
    return board


def add_exit_to_board(board, icon, x, y):
    board[x][y] = icon

def is_cell_exit(board, x, y):
    try: 
        int(board[x][y])
        return True
    except ValueError:
        return False

board_1 = prepare_board("board_1.txt",BLOCKED_COORDS_1)        
# board_1 = create_board(BOARD_WIDTH, BOARD_HEIGHT)
board_2 = create_board(BOARD_WIDTH, BOARD_HEIGHT)
board_3 = create_board(BOARD_WIDTH, BOARD_HEIGHT)

board_list = {'1': board_1, '2': board_2, '3': board_3}

# ==================== SET EXITS AND ENTRIES ====================
# set exit from board 1 to 2                                   
exit_1_to_2_x = random.randrange(0, len(board_list['1']))
exit_1_to_2_y = BOARD_WIDTH-1
add_exit_to_board(board_list['1'], '2', exit_1_to_2_x, exit_1_to_2_y)

# set entry to board 2 from 1                                  
add_exit_to_board(board_list['2'], '1', exit_1_to_2_x, 0)
    
# set exit from board 2 to 3                                   
exit_2_to_3_x = random.randrange(0, len(board_list['2']))
exit_2_to_3_y = BOARD_WIDTH-1
add_exit_to_board(board_list['2'], '3', exit_2_to_3_x, exit_2_to_3_y)
    
# set entry to board 3 from 2                                  
add_exit_to_board(board_list['3'], '2', exit_2_to_3_x, 0)
# ===============================================================