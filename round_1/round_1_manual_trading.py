from copy import deepcopy

""" Order book dictionaries have the price level as the key and the volume as the value """

dryland_flax_bid_order_book = {
    30: 30000,
    29: 5000,
    28: 12000,
    27: 28000
}

dryland_flax_ask_order_book = {
    28: 40000,
    31: 20000,
    32: 20000,
    33: 33000
}

ember_mushroom_bid_order_book = {
    20: 43000,
    19: 17000,
    18: 6000,
    17: 5000,
    16: 10000,
    15: 5000,
    14: 10000,
    13: 7000
}

ember_mushroom_ask_order_book = {
    12: 20000,
    13: 25000,
    14: 35000,
    15: 6000,
    16: 5000,
    17: 0,
    18: 10000,
    19: 12000
}

def dryland_flax_calculate_best_volume(buy_price, bid_order_book, ask_order_book, buy_back_price, buy_back_fee):
    max_profit = -1
    best_volume = -1
    
    # If we are at the same price level as the clearance price, multiply our profit by 0.9
    # Assume a 10% chance that our stuff doesn't get filled
    same_price_penalty_multiplier = 0.9

    # Go in increments of 1000, so 1000 to 50000 (max volume is 50K)
    for volume in range(9980, 10101, 1):
        # So the original dictionaries don't get messed up
        bid_order_book_copy = deepcopy(bid_order_book)
        ask_order_book_copy = deepcopy(ask_order_book)
        
        bid_order_book_copy[buy_price] += volume

        clearance_price = calculate_clearance_price(bid_order_book_copy, ask_order_book_copy)

        # By default if the clearance price > buy price
        profit = 0

        if clearance_price <= buy_price:
            # Calculate profit
            profit = ((buy_back_price - clearance_price) * volume) - (buy_back_fee * volume)
        
        if clearance_price == buy_price:
            profit *= same_price_penalty_multiplier
        
        if profit > max_profit:
            max_profit = profit
            best_volume = volume
    
    return best_volume

def ember_mushroom_calculate_best_volume(buy_price, bid_order_book, ask_order_book, buy_back_price, buy_back_fee):
    max_profit = -1
    best_volume = -1
    
    # If we are at the same price level as the clearance price, multiply our profit by 0.9
    # Assume a 10% chance that our stuff doesn't get filled
    same_price_penalty_multiplier = 0.9

    # Go in increments of 1000, so 1000 to 50000 (max volume is 50K)
    for volume in range(19500, 20500, 1):
        # So the original dictionaries don't get messed up
        bid_order_book_copy = deepcopy(bid_order_book)
        ask_order_book_copy = deepcopy(ask_order_book)
        
        bid_order_book_copy[buy_price] += volume

        clearance_price = calculate_clearance_price(bid_order_book_copy, ask_order_book_copy)

        # By default if the clearance price > buy price
        profit = 0

        if clearance_price <= buy_price:
            filled_volume = get_filled_volume(buy_price,
                                              bid_order_book_copy,
                                              ask_order_book_copy,
                                              clearance_price,
                                              volume)
            
            # Calculate profit
            profit = ((buy_back_price - clearance_price) * filled_volume) - (((buy_back_fee / 2) * volume) + ((buy_back_fee / 2) * filled_volume))
        
        if clearance_price == buy_price:
            profit *= same_price_penalty_multiplier
        
        if profit > max_profit:
            max_profit = profit
            best_volume = volume
    
    return best_volume

def calculate_clearance_price(bid_order_book, ask_order_book):
    clearance_price = -1
    max_volume = -1
    
    for price_level in range(min(min(bid_order_book), min(ask_order_book)), max(max(bid_order_book), max(ask_order_book)) + 1):
        buy_volume = get_expected_buy_volume(price_level, bid_order_book)
        ask_volume = get_expected_ask_volume(price_level, ask_order_book)

        # >= to CHOOSE THE HIGHER PRICE
        if min(buy_volume, ask_volume) >= max_volume:
            max_volume = min(buy_volume, ask_volume)
            clearance_price = price_level
    
    return clearance_price

def get_expected_buy_volume(clearance_price, bid_order_book):
    total_volume = 0

    for price_level in bid_order_book:
        if price_level >= clearance_price:
            total_volume += bid_order_book[price_level]
    
    return total_volume

def get_expected_ask_volume(clearance_price, ask_order_book):
    total_volume = 0

    for price_level in ask_order_book:
        if price_level <= clearance_price:
            total_volume += ask_order_book[price_level]
    
    return total_volume

def get_filled_volume(buy_price, bid_order_book, ask_order_book, clearance_price, volume):
    # Calculate the volume that will not be filled
    # Assuming that the bid order book is set up that the keys are descending (so we start at the largest prices)
    full_ask_volume = get_expected_ask_volume(clearance_price, ask_order_book)

    excess = 0

    available_volume = full_ask_volume
    for price in bid_order_book:
        if price == buy_price:
            excess = max(bid_order_book[buy_price] - available_volume, 0)
            break

        available_volume -= price

    # Calculate the volume that will be filled
    if excess > 0:
        return volume - excess
    else:
        return volume

def main():
    """ Buyback prices provided by the wiki """
    dryland_flax_buyback_price = 30
    ember_mushroom_buyback_price = 20

    """ Fees per unit when we are buying back """
    dryland_flax_fees_per_unit = 0
    ember_mushroom_fees_per_unit = 0.1

    """ Assume we know the prices we want to buy at """
    dryland_flax_buy_price = 30
    ember_mushroom_buy_price = 17

    dryland_flax_best_volume = dryland_flax_calculate_best_volume(dryland_flax_buy_price, dryland_flax_bid_order_book, dryland_flax_ask_order_book, dryland_flax_buyback_price, dryland_flax_fees_per_unit)
    ember_mushroom_best_volume = ember_mushroom_calculate_best_volume(ember_mushroom_buy_price, ember_mushroom_bid_order_book, ember_mushroom_ask_order_book, ember_mushroom_buyback_price, ember_mushroom_fees_per_unit)

    print(f"@ buy price = {dryland_flax_buy_price}, best volume for Dryland Flax = {dryland_flax_best_volume}")
    print(f"@ buy price = {ember_mushroom_buy_price}, best volume for Ember Mushroom = {ember_mushroom_best_volume}")

main()

