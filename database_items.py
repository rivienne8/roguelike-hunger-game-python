#belly - belly capacity
#board_occurencies
district_pass = {'name': 'district_pass', 'icon': '#', "position_1" : [],"position_2" : [],"position_3" : []}
small_beer = {'name': 'small_beer', 'icon': 'b', 'belly': -10,"position_1" : [],"position_2" : [],"position_3" : []}
beer = {'name': 'beer', 'icon': 'B', 'belly': -20,"position_1" : [],"position_2" : [],"position_3" : []}
herbs = {'name': 'herbs', 'icon': 'H', 'belly': -15,"position_1" : [],"position_2" : [],"position_3" : []}
ranigast = {'name': 'ranigast', 'icon': 'R', 'belly': -40,"position_1" : [],"position_2" : [],"position_3" : []}
atm = {'name': 'atm', 'icon': '$', 'bucks': 90,"position_1" : [],"position_2" : [],"position_3" : []}
planetCash = {'name': 'planetCash', 'icon': 'P', 'bucks': 120,"position_1" : [],"position_2" : [],"position_3" : []}
euronet = {'name': 'euronet', 'icon': 'E', 'bucks': 100,"position_1" : [],"position_2" : [],"position_3" : []}
jeezy = {'name': 'jeezy', 'icon': 'J', 'belly': -12,"position_1" : [],"position_2" : [],"position_3" : []}
toi_toi = {'name': 'toi_toi', 'icon': 'U', 'belly': -18,"position_1" : [],"position_2" : [],"position_3" : []}
gravy = {'name': 'gravy', 'icon': 'g', 'belly': -12,"position_1" : [],"position_2" : [],"position_3" : []}
golden_credit_card = {'name': 'golden_credit_card', 'icon': 'D', 'bucks': 500,"position_1" : [],"position_2" : [],"position_3" : []}

item_database = {'#': district_pass, 'B': beer, 'b' : small_beer, 'H': herbs, 'R': ranigast,\
                 '$': atm, 'P' : planetCash, 'E' : euronet, 'J': jeezy, 'U': toi_toi, 'g': gravy, 'D': golden_credit_card}

def get_item_by_name(name):
    for key,value in item_database.items():
        if value['name'] == name:
            return value

def get_item_by_icon(icon):
    for key in item_database:
        if key == icon:
            return item_database[key]
        
    return {}
        
