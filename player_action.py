a =

def inventory_command():
    while:
        display_inventory()
        choice = input("want to use sth? "):
        if "q":
            raise SystemExit
        elif yes:
            print menu
            choice = input("what item? "):
            found = False
            for item in items:
                if choice == item:
                    use_item()
                    found = True
                    # break
                "try again"
                continue
        else:
            break


def player_action():
    if empty_field:
        player_move()
    elif door:
        change_board()
                        # zmiana boarda w jaki sposób? current_board = boards[]/ 
                        #put player on board
                        # jak stąd wrocic na poczatek while'a   / raise Exception?
    elif item_in_field:
        take_item()
        player_move()
    elif friend_in_field:
        take_gifts()
        player_move()  
                        
    elif enemy_in_field:
        player_meets_enemy()


def player_meets_enemy(enemy_first=None):
    
    is_fight = True
    while is_fight:
        cls()
        display_fight_status_screen()
        
        if won():
            print(status)
            press_any_key()s
            is_fight = False
        elif died():
            print(status)
            press_any_key()
            raise SystemExit
        else:
            
            key = input("fight or run away")
            if "q":
                raise SystemExit
            elif "r":
                return
            elif "i":
                inventory_command()
            elif "f":
                is_fight = fight()
                # if not is_fight:
                #     break
            else:
                continue

def fight():
    if bucks < price:
        print(info) # tutaj?
        press_any_key()
        return False
    if bucks > price:
        if enemy_first:
            enemy_attacks()
            player_attacks()
        else:
            player_attaks()
            enemy_attacks()
        return True

           
def enemy_action():
    for enemy in {enemies}:
        check_coordinates()
        if player[position]:
            player_meets_enemy()
        else:                                  
            enemy_move()





