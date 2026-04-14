from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
from numpy import mean, std
from math import floor, ceil
from statistics import fmean
from jsonpickle import encode, decode
import string

# This is a class to house currently-unused functions that we might consider looking into in the future
class Functions_Storage:
    def voucher_makes_sense(voucher_amount, most_recent_volcanic_rock_sell_order):
        upper_bound = most_recent_volcanic_rock_sell_order * 1.02
        lower_bound = most_recent_volcanic_rock_sell_order * 0.98

        if voucher_amount < upper_bound and voucher_amount > lower_bound:
            print(f"Voucher amount {voucher_amount} DOES (YES) makes sense for most recent volcanic rock sell price {most_recent_volcanic_rock_sell_order}")
            return True
        
        print(f"Voucher amount {voucher_amount} DOES NOT (NO) make sense for most recent volcanic rock sell price {most_recent_volcanic_rock_sell_order}")
        return False
    
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
    
    def get_maximum_purchased_order_price(own_trades):
        purchased_prices: list = []

        for product in own_trades:
            for trade_instance in own_trades[product]:
                purchased_prices.append(trade_instance.price)
        
        return max(purchased_prices)

class New_Data:
    def __init__(self, product_names, macaron_info):
        self.MAX_HISTORY_LENGTH = 150

        self.sell_order_history = self.make_empty_container(products=product_names)
        self.buy_order_history = self.make_empty_container(products=product_names)
        self.current_positions = self.make_empty_container(products=product_names, make_position_dictionary=True)
        self.previous_macaron_information = self.make_empty_container(products=macaron_info)
        self.previous_EMAs = self.make_empty_container(products=product_names, make_position_dictionary=True)

    def make_empty_container(self, products, make_position_dictionary: bool=False):
        container = {}
        for product in products:
            if make_position_dictionary:
                container[product] = 0

            else:
                container[product] = []
        
        return container
    
    def update_order_history(self, history, product, new_addition):
        if len(history[product]) > self.MAX_HISTORY_LENGTH:
            history[product].pop(0)
        history[product].append(new_addition)
    
    def update_previous_EMA(self, product, new_EMA):
        self.previous_EMAs[product] = new_EMA

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

        self.historical_average_mid_price = (self.buy_order_average + self.sell_order_average) / 2

        # This will be implemented in children classes
        self.acceptable_buy_price = None
        self.acceptable_sell_price = None

class Emerald(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)
        
        # Assuming that the bids are less than the asks most of the time, based on the Tutorial Round's Data in a Bottle
        # Also assuming that the prices will remain stable the whole way through
        # This is less "hardcoded", we hope?
        self.acceptable_buy_price = ceil(self.buy_order_average) + 1
        self.acceptable_sell_price = floor(self.sell_order_average) - 1

class Tomatoes(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit, previous_EMA):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)

        # TODO: These are VERY experimental
        # TODO: This is hardcoded, maybe look into calculating this in some way?
        self.alpha = 0.3

        self.previous_EMA = previous_EMA
        self.EMA = self.previous_EMA

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

        for best_ask, best_ask_amount in list(order_depth.sell_orders.items()):
            print(f"BUY EMERALDS: {str(-best_ask_amount)} x {acceptable_buy_price}")
            orders.append(Order(product_name, acceptable_buy_price, -best_ask_amount))

        for best_bid, best_bid_amount in list(order_depth.buy_orders.items()):
            print(f"SELL EMERALDS: {str(best_bid_amount)} x {acceptable_sell_price}")
            orders.append(Order(product_name, acceptable_sell_price, -best_bid_amount))
        
        return orders
    
    def trade_tomatoes(self, order_depth):
        def calculate_EMA(tomatoes, best_bid, best_ask):
            current_mid_price = (best_bid + best_ask) / 2

            if tomatoes.previous_EMA == 0 or tomatoes.previous_EMA == 0.0:
                tomatoes.previous_EMA = current_mid_price

            tomatoes.EMA = (tomatoes.alpha * current_mid_price) + ((1 - tomatoes.alpha) * tomatoes.previous_EMA)

            # Currently not really used, but it's good in case maybe
            tomatoes.acceptable_buy_price = ceil(tomatoes.EMA)
            tomatoes.acceptable_sell_price = floor(tomatoes.EMA)

            return tomatoes.EMA
        
        # Start of the tomatoes trading strategy
        tomatoes = self.product_info["TOMATOES"]
        product_name = tomatoes.product_name
        
        # Handling the spread did help before with a different strategy to make the algorithm more stable
        # In this current strategy, it is used to offset the EMA to get our favorable buy and sell prices
        best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
        best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
        spread = best_ask - best_bid
        
        # Calculate the EMA
        calculate_EMA(tomatoes, best_bid, best_ask)

        """ The idea is that I think there is also a spread between the bid and ask prices in the Tutorial Round Data in a Bottle?
            So we can do a similar strategy to emeralds where we sell 1 below the ask and sell 1 above the bid
            Refer to Tomatoes Current Strategy in the IMC 4 Product Info & Strategy Notes """
        acceptable_buy_price = ceil(tomatoes.EMA - (spread / 2) + 1)
        acceptable_sell_price = floor(tomatoes.EMA + (spread / 2) - 1)

        # Orders to return back
        orders: List[Order] = []

        # TODO: Maybe check if we're in a rising trend and if so buy and sell??? Or going down trend too maybe :0
        for ask, ask_amount in list(order_depth.sell_orders.items()):
            print(f"BUY TOMATOES: {str(-ask_amount)} x {acceptable_buy_price}")
            orders.append(Order(product_name, acceptable_buy_price, -ask_amount))

        for bid, bid_amount in list(order_depth.buy_orders.items()):
            print(f"SELL TOMATOES: {str(bid_amount)} x {acceptable_sell_price}")
            orders.append(Order(product_name, acceptable_sell_price, -bid_amount))
        
        return orders

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



        """ Make a New_Data object to update (by default) """
        new_data = New_Data(PRODUCT_NAMES, MACARON_INFO)



        """ Update new_data with previous trading data if it exists """
        if state.traderData != "":
            new_data = decode(state.traderData)

        strategy = Strategy(new_data.sell_order_history, new_data.buy_order_history, new_data.current_positions, POSITION_LIMITS, new_data.previous_EMAs)



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
                new_data.update_order_history(new_data.sell_order_history, product, best_ask)
            
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
                new_data.update_order_history(new_data.buy_order_history, product, best_bid)
            


            """ Update Product EMAs """
            if product == "TOMATOES":
                new_data.update_previous_EMA(product, strategy.product_info[product].EMA)
            


            """
            Skip the first iteration of trading or any products we don't want to trade for now,
            also tariffs are scary (boo) (oh no) (spooky)
            """
            # products_we_want_to_trade: list[str] = ["EMERALDS", "TOMATOES"]
            products_we_want_to_trade: list[str] = ["EMERALDS", "TOMATOES"]

            if state.traderData == "" or (product not in products_we_want_to_trade):
                #print("First iteration, will not do any trading")
                continue
            


            """ Get the current position of the product """
            position = strategy.product_info[product].current_position
            print(f"Current position: {position}")
            


            """
            This is still in the for product in state.order_depths for loop
            Make our orders, and put those orders in result for that respective product
            """
            if product == "EMERALDS":
                result[product] = strategy.trade_emeralds(order_depth)
            
            elif product == "TOMATOES":
                result[product] = strategy.trade_tomatoes(order_depth)
            
            new_data.current_positions[product] = position



        """ Make the new data to append for the next iteration """
        traderData = encode(new_data)

        # Sample conversion request. Check more details below. 
        conversions = 0
        return result, conversions, traderData

