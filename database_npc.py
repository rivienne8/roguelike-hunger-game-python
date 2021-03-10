import random

#non player characters

friends = { "mate" : {'name': 'Seba', 'icon': 'S', 'gifts' : {'bucks': 30, 'belly': -10, 'chunk' : 5},\
                     "position" : [], "occure_on_board" : "", "type" : "enemy"},\
           "uncle" : {'name': 'Zdzislaw', 'icon': 'Z', 'gifts' : {'bucks': 100}, \
                      "position" : [],"occure_on_board" : "" ,"type" : "enemy"},\
            "uncle_3" : {'name': 'Zdzislaw', 'icon': 'Z', 'gifts' : {'bucks': 100}, \
                      "position" : [],"occure_on_board" : "" ,"type" : "enemy"},\
           "snitcher" : {'name': 'snitcher', 'icon': '.','gifts' : { 'bucks': -30}, \
                         "position" : [],"occure_on_board" : "" ,"type" : "enemy"},\
           "mother_in_law" : {'name': 'Evil', 'icon': 'E','gifts' : {'bucks': 100}, \
                              "position" : [],"occure_on_board" : "","type" : "enemy"}
            }

npc_database = {'S': friends["mate"], 'Z': friends["uncle"], 'S': friends["snitcher"], 'E': friends["mother_in_law"]}


FOOD_TRUCKS_X = 17
FOOD_TRUCKS_Y = 27


FULL_SUPPLIES = 0
CURRENT_SUPPLIES = 1
ENEMY_FACTOR = 0.3

food_challenges = { "kebab" : {"type" : "enemy", "move" : True, "icon" : "K" , "position" : [],\
                               "current_index" : 0,"direction" : "forward",\
                                "path" : [(0,0),(1,0),(2,0),(3,0)],"occure_on_board" : "",\
                                "price" : 5, "supplies" : [40,40], "belly" : random.randint(17,25),\
                                 "name" : "Turkish Kebab"},
                    "iskender_kebab" : {"type" : "enemy", "move" : True, "icon" : "K" , "position" : [],\
                               "current_index" : 0,"direction" : "forward",\
                                "path" : [(0,0),(1,0),(2,0),(3,0)],"occure_on_board" : "",\
                                "price" : 5, "supplies" : [40,40], "belly" : random.randint(10,15),\
                                "name" : "Iskender Kebab", "phase":""},          

                    "pizza" : {"type" : "enemy","move" : True,"icon" : "P" , "position" : [],\
                               "current_index" : 0, "direction" : "forward",\
                               "path" :  [(0,0),(0,1),(0,2),(0,3)],"occure_on_board" : "",\
                               "price" : 15,  "supplies" : [40,40], "belly" : random.randint(55,70),
                               "name" : "Pizza Hut", "phase": ""},
                    "cracknel" : {"type" : "enemy","move" : True,"icon" : "O" , "position" : [],\
                               "current_index" : 0, "direction" : "forward","occure_on_board" : "",\
                               "path" : [(0,0),(-1,1),(-2,2),(-3,3)],\
                               "price" : 5,  "supplies" : [40,40], "belly" : random.randint(17,25),\
                                "name" : "Traditional Cracknel", "phase":""},
                    # "uncle" : {"supper"}, # do rozwinięcia
                    "group" : {"type" : "enemy","move" : True,"icon" : "G" , "position" : [],\
                               "current_index" : 0, "direction" : "forward","occure_on_board" : "",\
                               "path" : [(0,0),(-1,1),(-2,2),(-3,1),(-4,0),(-3,-1)],\
                               "price" : 35,  "supplies" : [40,40], "belly" : random.randint(8,20),
                               "name" : "Turkish_Group", "phase": ""},
                    # "company_party" : {},
                    "foodtrucks" : {"type" : "beast","move" : True,"icon_1" : "F" , "icon_2" : "D" ,\
                                    "shape" : [(0,0), (0,1),(1,0),(1,1)], "position" : [] ,\
                                    "path" : [(0,0),(0,1),(0,2),(0,3)], \
                                    "current_index" : 0, "direction" : "forward","occure_on_board" : "",\
                                    "price" : 35,  "supplies" : [40,40], "belly" : random.randint(19,27),
                                    "name" : "Food Trucks", "phase" :""},
                    "chocolate_shop" : {"type" : "beast","move" : True,"icon_1" : "C" , "icon_2" : "C" ,\
                                    "shape" : [(0,0), (0,1),(-1,1),(0,2)], "position" : [] ,\
                                    "path" : [(0,0),(-1,1),(-2,2),(-3,3)], \
                                    "current_index" : 0, "direction" : "forward","occure_on_board" : "",\
                                    "price" : 31,  "supplies" : [70,70], "belly" : random.randint(55,65),
                                    "name" : "Chocolate Shop", "phase": ""},
                    "russian_mother" : {"type" : "beast","move" : True,"icon_1" : "M" , "icon_2" : "R" ,\
                                    "shape" : None, "position" : [] , "size" : 5,\
                                    "path" : [(0,0),(1,0),(2,0),(3,0)], \
                                    "current_index" : 0, "direction" : "forward","occure_on_board" : "",\
                                    "price" : 65,  "supplies" : [140,140], "belly" : random.randint(75,95),
                                    "name" : "Russian Mother in Law", "phase": ""}
                    # "weeding" : { "the biggest challenge or the 3 board"}   # do rozwinięcia
                    }              
            


'''dodać enemy 'speaks': True'''
'''Rozpisanie schematu działań w module sPOTKKANIE i WALKA'''

[(0,0), (0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),()]                   
def create_beast_shape(a):
    shape = []
    for i in range(a):
        for j in range(a):
            shape.append((i,j))

    return shape
    
   
    # if money > price:
    #     while attack: (supplies > 0, belly_void <= 0,):
    #         if money > price/kęs :
    #             if kęs >= supplies:
    #                 money - % price (price/kęs)
    #                 end True
    #                 return has won
    #             else: supplies >  kęs
    #                     money - % price (price/kęs)
    #                     supplies - kęs * factor p * factor_en 
    #                     zmiana factora jesli
    #                     belly_void * factor p * factor_en - fullness
    #                     zmiana factora jesli
                        
    #             if supplies <= 0, belly_void >= 0 :
    #                 end True
    #                 return has won 
    #             elif belly_void <= 0 
    #                 end True 
    #                 return is dead
    #             else:
    #                 enemy changes its factors if can
    #                 display changes of enemy
    #                 ask player would like to use items
    #                 update attributes of player
    #                 display changed attributes
          
    #         else:
    #             enemy reduces a little bit of chunk
    #             return 
        
    # else:
    #     enemy reduces a little bit of chunk
    #     return