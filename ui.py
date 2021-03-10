PURPLE = "\033[0;35m"
BOLD = "\033[1m"
END = "\033[0m"


def display_board(board):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    w = len(board[1])
    h = len(board)

    print('='*(w+2))
    for row in range(h):
        print('|',end='')
        print(''.join(board[row]), sep = '', end = '')
        print('|')
    print('='*(w+2))


def print_message(message,data):
    print(message + ": " + str(data))
    
def print_list(message,lista):
    print("\n",message,end="")
    for i in lista:
        if i == lista[-1]:
            print(str(i)+".")
        else:
            print(str(i),end=" ")
    # print()

def print_start_screen():
    print(f"\n{'>'*14}{PURPLE} {'*'*8} {END}{'<'*14}\n")
    print(f"\n{' '*9}{PURPLE} THE TRUE HUNGRY GAMES {END}\n")
    print(f"\n{'>'*14}{PURPLE} {'*'*8} {END}{'<'*14}\n")
    print("\n"*2)
    print(f"{PURPLE}Explore the city, watch your belly  and bucks.{END}")
    print(f"{PURPLE}Food challenges are waiting for you....{END}")
    print(f"\n{PURPLE}Use WASD keys for moving. Q to quit the game. I to display inventory.{END}")
    print()