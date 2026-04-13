from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
from numpy import mean, std
from math import floor, ceil
import string

class Product:
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit):
        self.product_name = product_name
        self.sell_order_history = sell_order_history
        self.buy_order_history = buy_order_history
        self.current_position = current_position
        self.position_limit = position_limit

        self.sell_order_average = 0
        if len(self.sell_order_history) > 0:
            self.sell_order_average = mean(self.sell_order_history)

        self.buy_order_average = 0
        if len(buy_order_history) > 0:
            self.buy_order_average = mean(buy_order_history)

        # This will be implemented in children classes
        self.acceptable_buy_price = None
        self.acceptable_sell_price = None

class Emerald(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)

        self.average_mid_price = (self.buy_order_average + self.sell_order_average) / 2
        
        # Assuming that the bids are less than the asks most of the time, based on the Tutorial Round's Data in a Bottle
        # This is less "hardcoded", we hope?
        self.acceptable_buy_price = ceil(self.buy_order_average) + 1
        self.acceptable_sell_price = floor(self.sell_order_average) - 1

class Tomatoes(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit, previous_EMA):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)
        
        self.average_mid_price = (self.buy_order_average + self.sell_order_average) / 2

        # TODO: These are VERY experimental
        # TODO: Maybe look into average of the last like 30 prices?
        self.alpha = 0.3
        
        biggest_order_history_size = max(len(sell_order_history), len(buy_order_history))
        if biggest_order_history_size > 0 and False:
            recency_dividor = 30
            recent_past = biggest_order_history_size / recency_dividor

            self.alpha = 2 / (recent_past + 1)
        
        self.previous_EMA = previous_EMA
        if self.previous_EMA == 0 or self.previous_EMA == 0.0:
            self.previous_EMA = self.average_mid_price
        
        check = self.previous_EMA
        if len(sell_order_history) > 30 and len(buy_order_history) > 30:
            # TODO: Fix this and resubmit
            check = mean(mean(sell_order_history[0:25]), mean(buy_order_history[0:25]))

        # self.EMA = (self.alpha * self.average_mid_price) + ((1 - self.alpha) * self.previous_EMA)
        self.EMA = (self.alpha * self.average_mid_price) + ((1 - self.alpha) * check)

        # The idea is that I think there is also a spread between the bid and ask prices in the Tutorial Round Data in a Bottle?
        self.acceptable_buy_price = floor(self.EMA)
        self.acceptable_sell_price = ceil(self.EMA)

class Strategy:
    def __init__(self, sell_order_history, buy_order_history, current_positions, position_limits, previous_EMAs):
        self.product_info = {}

        self.product_info["EMERALDS"] = Emerald("EMERALDS",
                                                sell_order_history["EMERALDS"],
                                                buy_order_history["EMERALDS"],
                                                current_positions["EMERALDS"],
                                                position_limits["EMERALDS"])

        self.product_info["TOMATOES"] = Tomatoes("TOMATOES",
                                                sell_order_history["TOMATOES"],
                                                buy_order_history["TOMATOES"],
                                                current_positions["TOMATOES"],
                                                position_limits["TOMATOES"],
                                                previous_EMAs["TOMATOES"])
    
    def trade_emeralds(self, order_depth):
        emeralds = self.product_info["EMERALDS"]
        product_name = emeralds.product_name
        
        acceptable_buy_price = emeralds.acceptable_buy_price
        acceptable_sell_price = emeralds.acceptable_sell_price

        # Orders to return back
        orders: List[Order] = []

        for i in range(0, len(order_depth.sell_orders)):
            best_ask, best_ask_amount = list(order_depth.sell_orders.items())[i]

            print(f"BUY EMERALDS: {str(-best_ask_amount)} x {acceptable_buy_price}")
            orders.append(Order(product_name, acceptable_buy_price, -best_ask_amount))

        for i in range(0, len(order_depth.buy_orders)):
            best_bid, best_bid_amount = list(order_depth.buy_orders.items())[i]

            print(f"SELL EMERALDS: {str(best_bid_amount)} x {acceptable_sell_price}")
            orders.append(Order(product_name, acceptable_sell_price, -best_bid_amount))
        
        return orders
    
    def trade_tomatoes(self, order_depth, best_bid, best_ask):
        tomatoes = self.product_info["TOMATOES"]
        product_name = tomatoes.product_name
        
        # Handling the spread does help
        spread = best_ask - best_bid

        # TODO: I tried duplicating a code line to sell, and that changed nothing.
        # TODO: Maybe that either means we're selling at a loss or our prices are not favorable instead of a holding issue?
        acceptable_buy_price = floor(tomatoes.acceptable_buy_price - spread)
        acceptable_sell_price = ceil(tomatoes.acceptable_sell_price + spread)

        # Orders to return back
        orders: List[Order] = []

        for i in range(0, len(order_depth.sell_orders)):
            best_ask, best_ask_amount = list(order_depth.sell_orders.items())[i]

            print(f"BUY TOMATOES: {str(-best_ask_amount)} x {acceptable_buy_price}")
            orders.append(Order(product_name, acceptable_buy_price, -best_ask_amount))

        for i in range(0, len(order_depth.buy_orders)):
            best_bid, best_bid_amount = list(order_depth.buy_orders.items())[i]

            print(f"SELL TOMATOES: {str(best_bid_amount)} x {acceptable_sell_price}")
            orders.append(Order(product_name, acceptable_sell_price, -best_bid_amount))
        
        return orders

def make_empty_container(products, make_position_dictionary: bool=False):
    container = {}
    for product in products:
        if make_position_dictionary:
            container[product] = 0

        else:
            container[product] = []
    
    return container

def initialize_product_information(products, sell_order_history, buy_order_history, current_positions, observation_info_history, current_observation_info=None):
    product_info = {}
    for product in products:
        if product == "MAGNIFICENT_MACARONS":
            product_info["MAGNIFICENT_MACARONS"] = Macaron(product, sell_order_history[product], buy_order_history[product], current_positions[product], observation_info_history, current_observation_info)
            continue
        product_info[product] = Product(product, sell_order_history[product], buy_order_history[product], current_positions[product])

    # Manual offset adjustments
    product_info["EMERALDS"].set_buy_price_offset(0)
    product_info["EMERALDS"].set_sell_price_offset(0)
    # product_info["TOMATOES"].set_buy_price_offset(1)
    # product_info["TOMATOES"].set_sell_price_offset(1)

    # Return the products' information
    return product_info

def convert_trading_data(s):
    def get_orders(s):
        s = s.strip("{}")
        s = s.split("]")

        newList = []
        for entry in s:
            if entry != "":
                newList.append((entry + "]").strip(", "))

        d = {}
        for item in newList:
            key_value_pair = item.split(":")
            key = key_value_pair[0].strip(" '")
            
            values = key_value_pair[1].strip(" []").split(",")
            
            if values == ['']:
                d[key] = []
                
            else:
                for index, value in enumerate(values):
                    values[index] = float(value.strip())
                
                d[key] = values
        
        return d

    def get_positions(s):
        s = s.strip("{}")
        s = s.split(",")
        
        newList = []
        for entry in s:
            if entry != "":
                newList.append((entry).strip())

        d = {}
        for item in newList:
            key_value_pair = item.split(":")
            key = key_value_pair[0].strip("'")
            
            value = int(key_value_pair[1].strip())
            d[key] = value
        
        return d
    
    def get_EMAs(s):
        print(f"hello it is i {s}")
        s = s.strip("{}")
        s = s.split(",")
        
        newList = []
        for entry in s:
            if entry != "":
                newList.append((entry).strip())

        d = {}
        for item in newList:
            key_value_pair = item.split(":")
            key = key_value_pair[0].strip("'")
            
            value = float(key_value_pair[1].strip())
            d[key] = value
        
        return d

    # convert_trading_data function code
    s = s.strip("[]")
    s = s.split("}")

    d_list = []
    for entry in s:
        if entry != "":
            d_list.append((entry + "}").strip(", "))
    
    sell_orders = get_orders(d_list[0])
    buy_orders = get_orders(d_list[1])
    positions = get_positions(d_list[2])
    macaron_info = get_orders(d_list[3])
    previous_EMAs = get_EMAs(d_list[4])

    d_list[0] = sell_orders
    d_list[1] = buy_orders
    d_list[2] = positions
    d_list[3] = macaron_info
    d_list[4] = previous_EMAs
    
    return d_list

def voucher_makes_sense(voucher_amount, most_recent_volcanic_rock_sell_order):
    upper_bound = most_recent_volcanic_rock_sell_order * 1.02
    lower_bound = most_recent_volcanic_rock_sell_order * 0.98

    if voucher_amount < upper_bound and voucher_amount > lower_bound:
        print(f"Voucher amount {voucher_amount} DOES (YES) makes sense for most recent volcanic rock sell price {most_recent_volcanic_rock_sell_order}")
        return True
    
    print(f"Voucher amount {voucher_amount} DOES NOT (NO) make sense for most recent volcanic rock sell price {most_recent_volcanic_rock_sell_order}")
    return False

def get_lowest_sell_order(sell_orders):
    lowest_price = 0
    associated_amount = 0

    for index, sell_order in enumerate(sell_orders):
        if index == 0:
            lowest_price = sell_order[0]
            associated_amount = sell_order[1]
            continue
        
        if sell_order[0] < lowest_price:
            lowest_price = sell_order[0]
            associated_amount = sell_order[1]
    
    return (lowest_price, associated_amount)

def get_highest_buy_order(buy_orders):
    highest_price = 0
    associated_amount = 0

    for index, buy_order in enumerate(buy_orders):
        if index == 0:
            highest_price = buy_order[0]
            associated_amount = buy_order[1]
            continue
        
        if buy_order[0] > highest_price:
            highest_price = buy_order[0]
            associated_amount = buy_order[1]
    
    return (highest_price, associated_amount)

def buy_to_bot(orders, current_position, position_limit, product, best_ask, best_ask_amount):
    if current_position - best_ask_amount <= position_limit:
        orders.append(Order(product, best_ask, -1 * best_ask_amount))

def sell_to_bot(orders, current_position, position_limit, product, best_bid, best_bid_amount):
    if current_position - best_bid_amount >= (-1 * position_limit):
        orders.append(Order(product, best_bid, -1 * best_bid_amount))

def big_dip_checker(sell_order_history, buy_order_history, current_mid_price, multiplier):
    sell_average = mean(sell_order_history)
    buy_average = mean(buy_order_history)
    mid_average_value = (sell_average + buy_average) / 2

    return current_mid_price > (mid_average_value * multiplier)

def small_dip_checker(sell_order_history, buy_order_history, recents_length, current_mid_price, multiplier):
    sell_recents = sell_order_history
    if len(sell_recents) > recents_length:
        sell_recents = sell_recents[0:recents_length]
    
    sell_recents_average = mean(sell_recents)
    
    buy_recents = buy_order_history
    if len(buy_recents) > recents_length:
        buy_recents = buy_recents[0:recents_length]
    
    buy_recents_average = mean(buy_recents)

    mid_recents_average = (sell_recents_average + buy_recents_average) / 2

    #print(f"recents_average: {recents_average}")

    return current_mid_price > (mid_recents_average * multiplier)

def update_order_history(history, product, new_addition):
    max_history_length = 150

    if len(history[product]) > max_history_length:
        history[product].pop(0)
    history[product].append(new_addition)

def get_maximum_purchased_order_price(own_trades):
    purchased_prices: list = []

    for product in own_trades:
        for trade_instance in own_trades[product]:
            purchased_prices.append(trade_instance.price)
    
    return max(purchased_prices)

class Trader:
    def bid(self):
        return 15

    def run(self, state: TradingState):
        PRODUCT_NAMES = ["EMERALDS",
                         "TOMATOES"]

        POSITION_LIMITS = {
            "EMERALDS": 80,
            "TOMATOES": 80
        }

        MACARON_INFO = ["askPrice",
                        "bidPrice",
                        "exportTariff",
                        "importTariff",
                        "sugarPrice",
                        "sunlightIndex",
                        "transportFees"]
        


        """ Print state properties """
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        print(f"Own trades: {state.own_trades}")



        """ Make relavant dictionaries (by default) """
        sell_order_history = make_empty_container(products=PRODUCT_NAMES)
        buy_order_history = make_empty_container(products=PRODUCT_NAMES)
        current_positions = make_empty_container(products=PRODUCT_NAMES, make_position_dictionary=True)
        previous_macaron_information = make_empty_container(products=MACARON_INFO)
        previous_EMAs = make_empty_container(products=PRODUCT_NAMES, make_position_dictionary=True)



        """ Update the dictionaries with previous trading data if it exists """
        if state.traderData != "":
            sell_order_history, buy_order_history, current_positions, previous_macaron_information, previous_EMAs = convert_trading_data(state.traderData)

        strategy = Strategy(sell_order_history, buy_order_history, current_positions, POSITION_LIMITS, previous_EMAs)



        """ Orders to be placed on exchange matching engine """
        result = {}



        """ state.order_depths: """
        # keys = products, values = OrderDepth instances



        """ Go through each product, for each product """
        for product in state.order_depths:
            print(f"Current product: {product}")

            """
            OrderDepth contains the collection of all outstanding buy and sell orders
            (or “quotes”) that were sent by the trading bots for a certain symbol

            buy_orders and sell_orders dictionaries:
            Key = price associated with the order
            Value = total volume on that price level
            """
            order_depth: OrderDepth = state.order_depths[product]



            """ Update order histories """
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
                update_order_history(sell_order_history, product, best_ask)
            
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
                update_order_history(buy_order_history, product, best_bid)
            


            """ Update Product EMAs """
            if product == "TOMATOES":
                previous_EMAs[product] = strategy.product_info[product].EMA
            


            """ Skip the first iteration of trading or any products we don't want to trade for now,
                also tariffs are scary (boo) (oh no) (spooky) """
            # products_we_want_to_trade: list[str] = ["EMERALDS"]
            products_we_want_to_trade: list[str] = ["TOMATOES"]

            if state.traderData == "" or (product not in products_we_want_to_trade):
                #print("First iteration, will not do any trading")
                continue
            


            """ Get the current position of the product """
            position = strategy.product_info[product].current_position
            print(f"Current position: {position}")
            


            """ This is still in the for product in state.order_depths for loop """
            # Make our orders, and put those orders in result for that respective product
            if product == "EMERALDS":
                result[product] = strategy.trade_emeralds(order_depth)
            
            elif product == "TOMATOES":
                best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
                best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
                result[product] = strategy.trade_tomatoes(order_depth, best_bid, best_ask)
            
            current_positions[product] = position



        """ Make the new data to append for the next iteration """
        newData = []
        newData.append(sell_order_history)
        newData.append(buy_order_history)
        newData.append(current_positions)
        newData.append(previous_macaron_information)
        newData.append(previous_EMAs)

        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = str(newData)

        # Sample conversion request. Check more details below. 
        conversions = 0
        return result, conversions, traderData
