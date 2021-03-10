PLAYER_ICON = '\u001b[45m\u001b[30m@\u001b[0m'
PLAYER_START_X = 13
PLAYER_START_Y = 84


def create_player():
    return {
        'icon': PLAYER_ICON, 
        'position': (PLAYER_START_X, PLAYER_START_Y), 
        'inventory': {
            'ranigast' : 1,
            'small_beer': 2,
            'bucks': 150
        },
        'belly': 1,
        'age' : 40,
        'charisma': 18,
        'chunk': 10
    }

def put_player_on_board(board, player):
    x, y = player['position']
    board[x][y] = player['icon']