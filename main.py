import engine
import util
import ui
import database_boards
import database_player
import database_items
import database_npc
import extras
import os
import random
class ExitException(Exception):
    pass

    # laying items on the board 1: 
def lying_items_on_board():
    # board_to_put_on = database_boards.board_list["1"]
    engine.initialize_item(database_boards.board_1, database_npc.food_challenges["foodtrucks"], 15, 12,True)
    engine.initialize_item(database_boards.board_1, database_npc.food_challenges["russian_mother"], 8, 80,True)
    engine.initialize_item(database_boards.board_1, database_npc.food_challenges["chocolate_shop"], 8, 62,True)
    engine.initialize_item(database_boards.board_1, database_npc.friends["mate"], 3, 50,True)
    engine.initialize_item(database_boards.board_1, database_items.beer, 6, 26)
    engine.initialize_item(database_boards.board_1, database_items.district_pass, 13, 95)
    engine.initialize_item(database_boards.board_1, database_items.gravy, 4, 16)
    engine.initialize_item(database_boards.board_1, database_items.atm, 2, 89)
    engine.initialize_item(database_boards.board_1, database_items.euronet, 6, 56)
    engine.initialize_item(database_boards.board_1, database_items.planetCash, 14, 16)
    engine.initialize_item(database_boards.board_1, database_npc.friends["snitcher"], 6, 86,True)
    engine.initialize_item(database_boards.board_1, database_npc.friends["uncle"], 17, 78,True)
    engine.initialize_item(database_boards.board_1, database_items.ranigast, 13, 44)
    engine.initialize_item(database_boards.board_1, database_items.jeezy, 4, 37)
    engine.initialize_item(database_boards.board_1, database_items.toi_toi, 1, 61)
    engine.initialize_item(database_boards.board_1, database_items.golden_credit_card, 13, 59)
    engine.initialize_item(database_boards.board_1, database_npc.food_challenges["kebab"], 10, 47,True)
    engine.initialize_item(database_boards.board_1, database_npc.food_challenges["pizza"], 5, 48,True)
    # engine.initialize_item(database_boards.board_1, database_npc.food_challenges["cracknel"], 18, 47,True)
    engine.initialize_item(database_boards.board_1, database_npc.food_challenges["group"], 7, 55,True)

 

    # laying items on the board 2: 
def laying_items_on_board_2():
    engine.initialize_item(database_boards.board_2, database_items.beer, 12, 4)
    engine.initialize_item(database_boards.board_2, database_npc.friends["snitcher"], 7, 36,True)
    engine.initialize_item(database_boards.board_2, database_items.gravy, 8, 74)
    engine.initialize_item(database_boards.board_2, database_items.herbs, 5, 33)
    engine.initialize_item(database_boards.board_2, database_npc.friends["uncle"], 19, 63,True)
    engine.initialize_item(database_boards.board_2, database_npc.food_challenges["iskender_kebab"], 18, 3,True)

    # laying items on the board 3: 
def laying_items_on_board_3():
    engine.initialize_item(database_boards.board_3, database_items.beer, 14, 16)
    engine.initialize_item(database_boards.board_3, database_items.herbs, 3, 82)
    engine.initialize_item(database_boards.board_3, database_items.golden_credit_card, 8, 33)
    engine.initialize_item(database_boards.board_3, database_items.ranigast, 10, 71)
    engine.initialize_item(database_boards.board_3, database_npc.friends["uncle_3"], 9, 50,True)
    engine.initialize_item(database_boards.board_3, database_npc.food_challenges["cracknel"], 18, 47,True)

def prepare_game_environment():
    lying_items_on_board()
    laying_items_on_board_2()
    laying_items_on_board_3()
    
def start(current_board,player):
    print('Current City District Visited: ', extras.board_level_info(current_board))
    extras.how_occupied_belly(player)
    database_player.put_player_on_board(current_board, player)
    ui.display_board(current_board)



def player_action(current_board,player):
    # change_board = False
    player_turn = True
    while  player_turn:
        key = engine.get_key()
        if key == 'q':
            player_turn = False
            raise ExitException
        elif key == 'i':
            print(player['inventory'])
            engine.use_inventory(player)
            util.press_any_key()
            util.clear_screen()
            start(current_board,player)
            continue
        else:
            future_x,future_y = engine.get_move_coords(player,key)
        
        engine.remove_player_from_board(current_board, player)
        if engine.can_move_player_to(current_board, player, future_x, future_y):
            # moves the player to the next / previous board(s) / if has the district_pass
            if database_boards.is_cell_exit(current_board, future_x, future_y):
                if engine.player_has_item(player, database_items.district_pass):
                    current_board = engine.go_to_next_board(current_board,player,future_x,future_y,database_boards.board_list)
                    player_turn = False
                    # change_board = True
                    
                    
                else:
                    print('You need to find a district pass first... (#)')
                    util.press_any_key()
            else:
                enemies_coords = engine.get_coords(current_board,database_npc.food_challenges)
                friends_coords = engine.get_coords(current_board, database_npc.friends,True)
                if engine.is_meet(future_x,future_y,enemies_coords,friends_coords):
                    engine.player_meets(current_board,player,future_x,future_y,enemies_coords,friends_coords,database_npc.food_challenges,database_npc.friends)
                    if current_board[future_x][future_y] == database_boards.BOARD_FIELD_SIGN:
                        engine.move_player_to(player, future_x, future_y)
                        player_turn = False
                    else:
                        player_turn = True
                        
                else:
                    engine.move_player_to(player, future_x, future_y)
                    if current_board[future_x][future_y] in database_items.item_database:
                        engine.put_item_into_the_inv(player, database_items.item_database[current_board[future_x][future_y]])
                        print(f"You have added sth special to your backpack.\n")
                        util.press_any_key()
                    
                    player_turn = False
    return current_board 
                    

def game_action(current_board,enemies,player):
    engine.enemies_move_on_current_board(current_board,enemies,player)


def main():
    player = database_player.create_player()
    prepare_game_environment()
    util.clear_screen()
    ui.print_start_screen()
    util.press_any_key()
    # setting which board is the 1st to start the gameplay    
    current_board = database_boards.board_list['1']
    
    util.clear_screen()
    is_running = True
    while is_running:
        start(current_board,player)
        current_board = player_action(current_board,player)
        game_action(current_board,database_npc.food_challenges,player)

        util.clear_screen()


if __name__ == '__main__':
    # main()
    try:
        main()
    except (ExitException,SystemExit):
        print("You quit the game")
