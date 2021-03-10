def how_occupied_belly(player):
    s = '[    |    |    |    |     ]'
    if player['belly'] <= 400: 
        colour = '\u001b[42m'
    elif player['belly'] <= 800:
        colour = '\u001b[43m'
    elif player['belly'] <= 999:
        colour = '\u001b[41m'
    else:
        colour = '\u001b[45m'
    reset_index = int(player['belly']/40)+1
    s = s[:reset_index] + '\u001b[0m' + s[reset_index:]
    s = s[:1] + colour + s[1:]
    print(s, round(player['belly']/10,2),'%')

def board_level_info(current_board):
    for x in current_board:
        if '2' in x[-1]:
            return '1'
        elif '1' in x:
            return '2'
        elif '2' in x[0]:
            return '3'
