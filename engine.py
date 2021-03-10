import os
import random
import ui
import util
import extras as ext
import database_npc as npcs
import database_boards as boards
import database_player as pl
import database_items as it



def get_key():
    key = util.key_pressed()    
    while not key.lower() in ["w","s","a","d","i","q"]:
        key = util.key_pressed()
    return key


def remove_player_from_board(board, player):
    x, y = player['position']
    board[x][y] = '.'

def move_player_to(player, future_x, future_y):
    player['position'] = (future_x, future_y)

def can_move_player_to(board, player, future_x, future_y):
    x, y = player['position']
    current_board = board
    if future_x not in range(len(current_board)) or\
       future_y not in range(len(current_board[x]))\
       or current_board[future_x][future_y] in [f"{boards.GREEN}T{boards.END}",f"{boards.BLUE}V{boards.END}",f"{boards.YELLOW}X{boards.END}"]:
        return False
    return True

def create_item_on_board(board, item, x, y):
    board[x][y] = item['icon']
    
def put_item_into_the_inv(player, item):
    if 'value' in item:
        value = item['value']
    else:
        value = 1
    
    if item['name'] not in player['inventory']: 
        player['inventory'][item['name']] = value
    else:
        player['inventory'][item['name']] += value
    
def player_has_item(player, item):
    return item['name'] in player['inventory']

# function that specifies is the key for moving
def is_move_key(key):  
    if key in ["w", "a","s","d"]:
        return True
    else:
        return False

# functions that precizes next coords according to key that has been pressed
def get_move_coords(player,key):
    x, y = player['position']
    if key == 'w':
        return x - 1, y
    elif key == 's':
        return  x + 1,y
    elif key == 'a':
        return  x,y - 1
    elif key == 'd':
        return  x, y + 1


def go_to_next_board(current_board,player,future_x,future_y,boards_list):
    for key in boards_list:                                          
        if current_board[future_x][future_y] == key:                
            result = boards_list[key]                         
    if future_y == 0:
        player['position'] = future_x, future_y + boards.BOARD_WIDTH - 2
    else:
        player['position'] = future_x, future_y - boards.BOARD_WIDTH + 2
    pl.put_player_on_board(result,player)
    return result


# function that puts a npc on board
def put_enemy_on_board(board,enemy):
    if enemy['type'] == 'beast':
        for i in range(len(enemy['position'])):
            (x,y) = enemy['position'][i]
            if y % 2 == 0:
                board[x][y] = enemy['icon_1']
            else:
                board[x][y] = enemy['icon_2']
    elif enemy['type'] == "enemy":
        (x,y) = enemy['position'][0]
        board[x][y] = enemy['icon']
    
    else:
        (x,y) = enemy['position'][0]
        board[x][y] = enemy['icon']

# function that provides an information on which board the item occures
# and which BLOCKED_COORDS_LIST includes its coords
def specify_position_and_coords_list_and_boardkey(board):
    for key,value in boards.board_list.items():
        if value == board:
            board_key = key

    if board_key == "2":
        position = "position_2"
        coords_list = boards.BLOCKED_COORDS_2
    elif board_key == "3":
        position = "position_3"
        coords_list = boards.BLOCKED_COORDS_3
    else:
        position = "position_1"
        coords_list = boards.BLOCKED_COORDS_1
    
    return [position,coords_list,board_key]

# function that creates npc if shape is not specified in npc's dictionary, 
# initializes npc on board and provides its position's coords to its dictionary
def create_enemy_on_board(board,enemy,x,y,coords_list):
    if "size" in enemy:
        shape = npcs.create_beast_shape(enemy["size"])
        enemy["shape"] = shape
    if enemy["type"] == "beast":
        test_coords = get_shape_coords(enemy,x,y)
        if is_space(test_coords,coords_list):
            for coords in test_coords:
                enemy['position'].append(coords)
                put_enemy_on_board(board,enemy)
                coords_list.append(coords)
                enemy["occure_on_board"] = board
    else:
        enemy["position"].append((x,y))
        put_enemy_on_board(board,enemy)
        coords_list.append((x,y))
        enemy["occure_on_board"] = board

# function that initializes item / npc on board and provides its position's coords to its dictionary
def initialize_item(board,item,x,y,enemies=None):
    position = specify_position_and_coords_list_and_boardkey(board)[0]
    coords_list = specify_position_and_coords_list_and_boardkey(board)[1]
    # board_key = specify_position_and_coords_list_and_boardkey(board)[2]    

    while (x,y) in coords_list:
        x = random.randint(0,boards.BOARD_HEIGHT-1)
        y = random.randint(0,boards.BOARD_WIDTH-1)

    if enemies:
        try:
            create_enemy_on_board(board,item,x,y,coords_list) 
        except :
            print(f"There is no space for beast")

    else:
        create_item_on_board(board,item,x,y)
        item[position].append((x,y))
        item["occure_on_board"] = board
        coords_list.append((x,y))
    
# function that gets coords of future position of an enemy
def get_shape_coords(enemy,x,y):
    test_coords = []
    for coords in enemy["shape"]:
        shape_x = coords[0]
        shape_y = coords[1]
        test_x = x + shape_x 
        test_y = y + shape_y
        test_coords.append((test_x,test_y))
    return test_coords

# function that shows if there is space for an enemy on board
def is_space(potential_coords,blocked_coords):
    if all( (x,y) not in blocked_coords for (x,y) in potential_coords ):
        return True
    else:
        raise ValueError


# function that changes the direction of moving of a character
def change_direction(direction,enemy):
    if direction == "forward":
        enemy['direction'] = "backward"
    else:
        enemy['direction'] = "forward"
        
# function that changes index in [path] 
# (coords in [path] indicates how far is the character from start position)
def change_current_index(enemy):
    if enemy['direction'] == 'forward':    
        enemy['current_index'] += 1
    else:
        enemy['current_index'] -= 1
    


# function that indicates what is the distance between start coords and the coords of next move
def count_delta_coords(enemy):
    if enemy['direction'] == 'forward':
        (delta_x,delta_y) = enemy['path'][enemy['current_index']+1]       
    else:
        (delta_x,delta_y) = enemy['path'][enemy['current_index']-1]
   

    return delta_x,delta_y


# function that moves characters on boards  - spróbuje ją zrefaktorować jak będę miała czas
def get_enemy_signs_move(board,enemy,player):
    # current distance from start position
    (n,m) = enemy['path'][enemy['current_index']]
    #conditions for changing direction
    if enemy['current_index'] == len(enemy['path'])-1 or\
       (enemy['current_index'] == 0 and enemy['direction'] == 'backward') :
        change_direction(enemy['direction'],enemy)

    should_stay = False
    while not should_stay:
        coords = [(enemy['position'][i][0] + n, enemy['position'][i][1] + m) for i in range(len(enemy["position"]))]
        #distance between start position and next position
        delta_x,delta_y = count_delta_coords(enemy)
        next_coords = [(enemy['position'][i][0]+ delta_x, enemy['position'][i][1]+ delta_y) for i in range(len(enemy["position"]))]

        icons = prepare_for_checking_space(enemy)
        #check if there is space for move
        if all(next_x not in [-1, boards.BOARD_HEIGHT ] for (next_x,next_y) in next_coords ) and \
           all(next_y not in [-1,boards.BOARD_WIDTH] for (next_x,next_y) in next_coords ) and\
           all(board[next_x][next_y] in icons for (next_x,next_y) in next_coords ) and \
           player["position"] not in next_coords:
            swap_signs(board,enemy,coords,next_coords)
            should_stay = True          
        else:
            if player["position"] in next_coords:
                enemy['phase'] = 'fight'
            # if is_player(board,next_coords,player):
                should_stay = True
            #check is the start or end position
            elif enemy['current_index'] == len(enemy['path'])-1 or\
                enemy['current_index'] == 0:
                    should_stay = True
                    readjust_enemy_supplies(player,enemy)
                    change_direction(enemy['direction'],enemy)
            #if character may return,than returns
            else:
                change_direction(enemy['direction'],enemy)

# function that provides a list of available fields
def prepare_for_checking_space(enemy):
    if enemy['type'] == 'beast':
        icons = [boards.BOARD_FIELD_SIGN,enemy['icon_1'], enemy['icon_2']]
    else:
        icons = [boards.BOARD_FIELD_SIGN, enemy['icon']]
    return icons

# function that swap the enemy signs on board when enemy moves
def swap_signs(board,enemy,coords,next_coords):
    # next_x not in [-1, boards.BOARD_HEIGHT+1] and next_y not in [-1,boards.BOARD_WIDTH+1]:
    if enemy['direction'] == 'forward':
        #moving all positions of character to the next position and clean previous position
        for i in range(len(next_coords)-1,-1,-1):
            (next_x,next_y) = next_coords[i]
            x,y = coords[i]
            board[next_x][next_y] = board[x][y]
            board [x][y] = boards.BOARD_FIELD_SIGN
        change_current_index(enemy)

    else:
        #moving all positions of character to the next position and clean previous position
        for i in range(len(next_coords)):
            (next_x,next_y) = next_coords[i]
            x,y = coords[i]
            board[next_x][next_y] = board[x][y]
            board [x][y] = boards.BOARD_FIELD_SIGN
        change_current_index(enemy)


# function that checks if player has met npc
def is_meet(future_x,future_y,enemies_coords,friends_coords):
    # enemies_coords = get_coords(enemies)
    # friends_coords = get_coords(friends)
    if (future_x,future_y) in enemies_coords or (future_x,future_y) in friends_coords:
        return True
    else:
        return False

# function that gets current coords of enemy
def get_current_enemy_coords(enemies,enemy):
    current_coords = []
    position = "position"
    for i in range(len(enemies[enemy][position])):
        if "move" in enemies[enemy]:
            (n,m) = enemies[enemy]['path'][enemies[enemy]['current_index']]
            (x,y) = (enemies[enemy][position][i][0] + n, enemies[enemy][position][i][1] + m)
            current_coords.append((x,y))
        else:
            (x,y) = (enemies[enemy][position][i][0], enemies[enemy][position][i][1])
            current_coords.append((x,y))
    return current_coords


# function that gets current coords of npcs
def get_coords(board,enemies,friends =None):
    enemies_coords = []
    position = "position"
    for enemy in enemies:
        for i in range(len(enemies[enemy][position])):
            if friends:
                enemies_coords.append(enemies[enemy][position][i])
            else:
                (n,m) = enemies[enemy]['path'][enemies[enemy]['current_index']]
                (x,y) = (enemies[enemy][position][i][0] + n, enemies[enemy][position][i][1] + m)
                enemies_coords.append((x,y))
    return enemies_coords

# function that readjusts player attributes
def check_player_attributes_values(player):
    if player["belly"] < 0:
        player["belly"] = 0
    if player["belly"] > 1000:
        player["belly"] = 1000
    if player["inventory"]["bucks"] < 0:
        player["inventory"]["bucks"] = 0

# function that pricises if the npc is an enemy
def find_npc(future_x,future_y,enemies,enemies_coords):
    if (future_x,future_y) in enemies_coords:
        for enemy in enemies:
            current_enemy_position = get_current_enemy_coords(enemies,enemy)
            if (future_x,future_y) in current_enemy_position:
                npc = enemy
    else:
        npc = ""
    return npc

# function that checks if player has beaten the enemy
def has_won(player,enemies,npc):
    if enemies[npc]["supplies"][npcs.CURRENT_SUPPLIES]<= 0 and player["belly"] <1000:
        return True
    else:
        return False

# function that checks if player has died
def has_died(player):
    if player["belly"] >= 1000:
        return True
    else:
        return False


# function that indicates string-type name of npc dictionary
def indicate_npc(future_x,future_y,enemies_coords,friends_coords,enemies,friends):
    # enemies_coords = get_coords(enemies)
    # friends_coords = get_coords(friends)
    if find_npc(future_x,future_y,enemies,enemies_coords) == "":
        npc = find_npc(future_x,future_y,friends,friends_coords)
    else:
        npc = find_npc(future_x,future_y,enemies,enemies_coords)
    return npc

# function that adds gift from a friend to attributes of player or makes the bucks smaller if npc == snitcher
def receive_gift(player,friends,npc):
    for gift in friends[npc]["gifts"]:
        if gift in ["belly","charisma", "chunk"]:
            player[gift] += friends[npc]["gifts"][gift]
        else:
            if gift in player["inventory"]:
                player["inventory"][gift] += friends[npc]["gifts"][gift]
            else:
                player["inventory"][gift] = friends[npc]["gifts"][gift]
        check_player_attributes_values(player)
        if npc == "snitcher":
            print(f"You have been robbed by a snitcher. You have now only {player['inventory'][gift]} bucks.\n")
        else:    
            print(f"You have received from {npc} {friends[npc]['gifts'][gift]} of {gift}.\n" )

# function that removes signs of npc from board
def remove_enemy_from_board(board,enemy,enemies, foes=None):
    if foes:
        current_enemy_position = get_current_enemy_coords(enemies,enemy)
    else:
        current_enemy_position = enemy["position"]
    for (x,y) in current_enemy_position:
        board[x][y] = '.'

# function that removes coords of npc from BLOCKED_COORDS_LIST
def remove_coords_defeated_enemy(enemy,coords_list,enemies, foes = None):
    if foes:
        current_enemy_position = get_current_enemy_coords(enemies,enemy)
    else:
        current_enemy_position = enemies[enemy]["position"]

    for (x,y) in current_enemy_position:
        coords_list.remove((x,y))

# function that specify BLOCKED_COORDS_LIST for current board
def specify_blocked_coords_list(board):
    if board == boards.board_list["1"]:
        blocked_coords = boards.BLOCKED_COORDS_1
    elif board == boards.board_list["2"]:
        blocked_coords = boards.BLOCKED_COORDS_2
    elif board == boards.board_list["3"]:
        blocked_coords = boards.BLOCKED_COORDS_3
    return blocked_coords

# function that gives information is player on given coords
def is_player(board, next_coords, player):
    if  player["position"] in next_coords:
        return True
    else:
        return False

# function that describe how enemy attacks player while his movement
def enemy_begins_fight(board,player,enemies,enemy):
    # pl.put_player_on_board(board, player)
    if player["inventory"]["bucks"] >= enemies[enemy]["price"]:
        player["inventory"]["bucks"] -= round(enemies[enemy]["price"],2)
    else:
        player["inventory"]["bucks"] =  0 
    print(f"\nYou have already paid for entrace to '{enemies[enemy]['name']}'.")
    print(f"Now you have only: {player['inventory']['bucks']} bucks.")

    printing(player,enemies,enemy)
    # user_choice = input("Do you wat to order something? y/n\n")
    user_choice = ""
    while user_choice not in ["y", "n"]:
        user_choice = input("Would you like to order something? y/n\n")
        if user_choice.lower().strip() == "y":
            print(f"To make an order,try to get position of {enemies[enemy]['name']}")
            util.press_any_key()
            return
        elif user_choice.lower().strip() == "n":
            # enemies[enemy]['phase'] = ""
            return
        

    # util.press_any_key()



# function that precises what is going on after meeting a friend
def player_meets_friend(board,player,future_x, future_y, friends,npc):
    receive_gift(player,friends,npc)
    check_player_attributes_values(player)
    remove_enemy_from_board(board,friends[npc],friends)
    friends[npc]["position"] = []
    blocked_coords = specify_blocked_coords_list(board)
    blocked_coords.remove((future_x,future_y))

# function that precises what is going on after meeting an enemy
def player_meets_enemy(board,player,enemies,npc):    
    # util.clear_screen
    # pl.put_player_on_board(board, player)
    # ui.display_board(board)
    printing(player,enemies,npc)
    if player["inventory"]["bucks"] > enemies[npc]["price"]:
        if player["chunk"] >= enemies[npc]["supplies"][npcs.CURRENT_SUPPLIES]:
            when_chunk_bigger_than_supplies(player,enemies,npc)                 
        # if player["chunk"] < npc["supplies"]    
        else:
            when_chunk_smaller_than_supplies(player,enemies,npc)
        check_player_attributes_values(player)

        if has_won(player,enemies,npc):
            printing(player,enemies,npc)
            after_defeating_enemy(board,player,enemies,npc)
        elif has_died(player):
            printing(player,enemies,npc)
            ui.print_message("You have died... Your belly: ",player["belly"])
            util.press_any_key()
            raise SystemExit
            

        elif not has_won(player,enemies,npc):
            decide_next_move(player,enemies,npc)
    #if player["bucks"] < npc["price"]
    else:
        ui.print_message("You have not money enough. The price is",enemies[npc]["price"])
        util.press_any_key()

# function that increases enemy's supplieses after player quit fight
def readjust_enemy_supplies(player,enemy):
    if enemy["supplies"][npcs.CURRENT_SUPPLIES] != 0:
        enemy["supplies"][npcs.CURRENT_SUPPLIES] += player["chunk"] / 4
        if enemy["supplies"][npcs.CURRENT_SUPPLIES] > enemy["supplies"][npcs.FULL_SUPPLIES]:
            enemy["supplies"][npcs.CURRENT_SUPPLIES] = enemy["supplies"][npcs.FULL_SUPPLIES]


# function that precises the steps in fight when chunk > supplieses
def when_chunk_bigger_than_supplies(player,enemies,npc):
    ratio = enemies[npc]["supplies"][npcs.CURRENT_SUPPLIES]/player["chunk"]
    if player["inventory"]["bucks"] >= enemies[npc]["price"] * ratio:
        player["inventory"]["bucks"] -= round(enemies[npc]["price"] * ratio,2)
        enemies[npc]["supplies"][npcs.CURRENT_SUPPLIES] -= player["chunk"]
        player["belly"] += round(enemies[npc]["belly"] * ratio,2)
        # printing(player,enemies,npc)
        # stop_attacking = True
    #if player["inventory"]["bucks"] < enemies[npc]["price"] * ratio    
    else:
        player["belly"] += round(0.2 * player["chunk"],2)  # stres ścisnął żołądek
        # print("")
        # printing(player,enemies,npc)
        ui.print_message("Go away. You have not money enough. The price is",enemies[npc]["price"])
        util.press_any_key()
        # stop_attacking = True  

# function that precises the steps in fight when chunk < supplieses
def when_chunk_smaller_than_supplies(player,enemies,npc):
    if player["inventory"]["bucks"] >= enemies[npc]["price"]:  
        player["inventory"]["bucks"] -= round(enemies[npc]["price"],2)
        enemies[npc]["supplies"][npcs.CURRENT_SUPPLIES] -= player["chunk"]
        if enemies[npc]["type"] == "beast" and (15 < enemies[npc]["supplies"][npcs.CURRENT_SUPPLIES] < 31):
            ui.print_message("Enemy has got angry. It has served you a spoilt ingridient. Your belly feels a chunk havier by", npcs.ENEMY_FACTOR )
            player["belly"] += round(enemies[npc]["belly"] * npcs.ENEMY_FACTOR,2) # * player[factor obniżajacy] 
        else:                 
            player["belly"] += round(enemies[npc]["belly"],2) # * player[factor obniżajacy] 
            return False
    else:
        ui.print_message("Go away. You have not money enough. The price is",enemies[npc]["price"])
        util.press_any_key()
        # stop_attacking = True
        return True

# function that precises the steps after player has beaten an enemy
def after_defeating_enemy(board,player,enemies,npc):
    print(f"{ui.PURPLE}You have won the fight!{ui.END} Your belly: ",player["belly"])
    remove_enemy_from_board(board,npc,enemies,True) # rozszerzone dla beasta
    enemies[npc]["position"] = []
    blocked_coords = specify_blocked_coords_list(board)
    remove_coords_defeated_enemy(npc,blocked_coords,enemies,True) # rozszerzone dla beasta
    util.press_any_key()

# function that precises the steps if player has not beaten an enemy yet
def decide_next_move(player,enemies,npc):
    # ui.print_list("Your status: ", ["chunk: ",player["chunk"], "belly: ", player["belly"], "inventory: ",player["inventory"]])
    # ui.print_message("Your status",player["inventory"])
    # ui.print_list("Status of ", [npc, "price: ", enemies[npc]["price"], "supplies: ", enemies[npc]["supplies"][npcs.CURRENT_SUPPLIES],"belly_factor: ",enemies[npc]["belly"]])
    
    ui.print_message("To make an order,try to get position of", npc)
    ui.print_message("Or You can just move away from...", npc)


# function that precises next steps after player has met npc
def player_meets(board,player,future_x,future_y,enemies_coords,friends_coords,enemies,friends):
    npc = indicate_npc(future_x,future_y,enemies_coords,friends_coords,enemies,friends)
    if  npc in friends:
        player_meets_friend(board,player,future_x, future_y, friends,npc)
        util.press_any_key()      

    if npc in enemies:
        player_meets_enemy(board,player,enemies,npc)


# function that moves enemies on current board
def enemies_move_on_current_board(current_board,enemies,player):
    for enemy in enemies:
        if enemies[enemy]["occure_on_board"] == current_board:
            get_enemy_signs_move(current_board,enemies[enemy],player)
            readjust_enemy_supplies(player,enemies[enemy])
        if 'phase' in enemies[enemy] and enemies[enemy]['phase'] == "fight":
            enemy_begins_fight(current_board,player,enemies,enemy)
            enemies[enemy]['phase'] = ""

# function that prepares data for printing current fight status
def prepare_data_for_printing(player,enemies,npc):
    bucks = "BUCKS: " +  str(round(player['inventory']['bucks'],2))
    price = "PRICE: " + str(round(enemies[npc]['price'],2))
    chunk = "CHUNK: " + str(player['chunk'])
    supplies = "SUPPLIES: " + str(enemies[npc]['supplies'][npcs.CURRENT_SUPPLIES])
    belly = "BELLY: " + str(round(player['belly'],2))
    belly_npc = "BELLY FILL FACTOR: " + str(round(enemies[npc]['belly'],2))

    return [(bucks,price),(chunk,supplies),(belly,belly_npc)]

# function that display current status of the fight
def printing(player,enemies,npc):
    # util.clear_screen()
    tuples = prepare_data_for_printing(player,enemies,npc)
    
    print("\n"*2)
    # print(f"{'FOOD'.rjust(24)}")
    print(f"{'PLAYER'.rjust(15)} | {enemies[npc]['name'].upper().ljust(15)}")
    print(("="*40).center(36))
    
    for (i,j) in tuples:
        print(f"{i.rjust(15)} | {j.ljust(15)}")
    print("\n", "belly status:")
    ext.how_occupied_belly(player)
    print("\n")



# function that allows player to choose an item from backpack
def choose_from_inventory(player):  
    for name in player['inventory']:
        if name == 'bucks':
            continue
        item = it.get_item_by_name(name)
        print()
        print(f"{item['icon']} for {item['name']}")
        

    # choice = False
    # while not choice:
    choice = input("\nTo use an item enter a  letter .\nOr 'n' to back to the game..\n")
    if choice.lower().strip() == "n":
        raise ValueError  
    # if str(choice) not in player['inventory']:
    #     choice = True
    # else:
    item = it.get_item_by_icon(choice)
    # print(item)
    if item == {}:
        raise ValueError    
    return item

# function that update inventory and player's attributes after using an item
def take_benefit_from_item(player,item):
    # print(item)
    if 'belly' in item:
        player['belly'] += item['belly']
        print(f"Thanks to {item['name']} your belly status is lower by {item['belly']}")
    if 'bucks' in item:
        player['inventory']['bucks'] += item['bucks']
        print(f"In your wallet is additional {item['bucks']} bucks.")
    player['inventory'][item['name']] -= 1
    if player['inventory'][item['name']] == 0:
        player['inventory'].pop(item['name'])
    check_player_attributes_values(player)

# function that allows player to use an item
def use_inventory(player):
    try:
        item = choose_from_inventory(player)
        take_benefit_from_item(player,item)
    except ValueError:
        return
    # else:
    #     take_benefit_from_item(player,item)



        


        

    


















        
        