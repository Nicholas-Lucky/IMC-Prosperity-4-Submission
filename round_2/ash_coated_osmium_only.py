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

class Intarian_Pepper_Root(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)
        
        # Assuming that the bids are less than the asks most of the time, based on the Tutorial Round's Data in a Bottle
        # Also assuming that the prices will remain stable the whole way through
        # This is less "hardcoded", we hope?
        self.acceptable_buy_price = ceil(self.buy_order_average) + 1
        self.acceptable_sell_price = floor(self.sell_order_average) - 1

class Ash_Coated_Osmium(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit, previous_EMA):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)

        # TODO: These are VERY experimental
        # TODO: This is hardcoded, maybe look into calculating this in some way?
        self.alpha = 0.5

        self.previous_EMA = previous_EMA
        self.EMA = self.previous_EMA

class Strategy:
    def __init__(self, sell_order_history, buy_order_history, current_positions, position_limits, previous_EMAs):
        self.product_info = {}

        self.product_info["INTARIAN_PEPPER_ROOT"] = Intarian_Pepper_Root("INTARIAN_PEPPER_ROOT",
                                                                         sell_order_history["INTARIAN_PEPPER_ROOT"],
                                                                         buy_order_history["INTARIAN_PEPPER_ROOT"],
                                                                         current_positions["INTARIAN_PEPPER_ROOT"],
                                                                         position_limits["INTARIAN_PEPPER_ROOT"])

        self.product_info["ASH_COATED_OSMIUM"] = Ash_Coated_Osmium("ASH_COATED_OSMIUM",
                                                                   sell_order_history["ASH_COATED_OSMIUM"],
                                                                   buy_order_history["ASH_COATED_OSMIUM"],
                                                                   current_positions["ASH_COATED_OSMIUM"],
                                                                   position_limits["ASH_COATED_OSMIUM"],
                                                                   previous_EMAs["ASH_COATED_OSMIUM"])
    
    def trade_intarian_pepper_root(self, order_depth):
        intarian_pepper_root = self.product_info["INTARIAN_PEPPER_ROOT"]
        product_name = intarian_pepper_root.product_name
        
        acceptable_buy_price = intarian_pepper_root.acceptable_buy_price
        acceptable_sell_price = intarian_pepper_root.acceptable_sell_price

        # Orders to return back
        orders: List[Order] = []

        for best_ask, best_ask_amount in list(order_depth.sell_orders.items()):
            print(f"BUY INTARIAN_PEPPER_ROOT: {str(-best_ask_amount)} x {acceptable_buy_price}")
            orders.append(Order(product_name, acceptable_buy_price, -best_ask_amount))

        for best_bid, best_bid_amount in list(order_depth.buy_orders.items()):
            print(f"SELL INTARIAN_PEPPER_ROOT: {str(best_bid_amount)} x {acceptable_sell_price}")
            orders.append(Order(product_name, acceptable_sell_price, -best_bid_amount))
        
        return orders
    
    def trade_ash_coated_osmium(self, state, order_depth):
        def calculate_EMA(ash_coated_osmium, best_bid, best_ask):
            current_mid_price = (best_bid + best_ask) / 2

            if ash_coated_osmium.previous_EMA == 0 or ash_coated_osmium.previous_EMA == 0.0:
                ash_coated_osmium.previous_EMA = current_mid_price

            ash_coated_osmium.EMA = (ash_coated_osmium.alpha * current_mid_price) + ((1 - ash_coated_osmium.alpha) * ash_coated_osmium.previous_EMA)

            # Currently not really used, but it's good in case maybe
            ash_coated_osmium.acceptable_buy_price = ceil(ash_coated_osmium.EMA)
            ash_coated_osmium.acceptable_sell_price = floor(ash_coated_osmium.EMA)

            return ash_coated_osmium.EMA
        
        # Start of the Ash Coated Osmium trading strategy
        print(f"Good morning the position IS: {state.position}")

        ash_coated_osmium = self.product_info["ASH_COATED_OSMIUM"]
        product_name = ash_coated_osmium.product_name
        
        # Handling the spread did help before with a different strategy to make the algorithm more stable
        # In this current strategy, it is used to offset the EMA to get our favorable buy and sell prices
        best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
        best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
        spread = best_ask - best_bid
        mid_price = ((best_bid + best_ask) / 2)
        
        # Weighted mid: weight by available volume at each level
        # weighted_bid = sum(p * v for p, v in order_depth.buy_orders.items()) / sum(order_depth.buy_orders.values())
        # weighted_ask = sum(p * abs(v) for p, v in order_depth.sell_orders.items()) / sum(abs(v) for v in order_depth.sell_orders.values())
        # weighted_mid = (weighted_bid + weighted_ask) / 2

        # Calculate the EMA
        calculate_EMA(ash_coated_osmium, best_bid, best_ask)
        
        historical_mid_price = (ash_coated_osmium.sell_order_average + ash_coated_osmium.buy_order_average) / 2

        # mean_average_fair_value = (ash_coated_osmium.EMA + weighted_mid + mid_price) / 3
        # mean_average_fair_value = (ash_coated_osmium.EMA + mid_price) / 2
        # mean_average_fair_value = (ash_coated_osmium.EMA + mid_price) / 3
        # mean_average_fair_value = mid_price
        mean_average_fair_value = ash_coated_osmium.EMA

        # acceptable_buy_price = int(ash_coated_osmium.EMA) - 1
        # acceptable_sell_price = int(ash_coated_osmium.EMA) + 1

        acceptable_buy_price = int(mean_average_fair_value - 1)
        acceptable_sell_price = int(mean_average_fair_value + 1)

        # Orders to return back
        orders: List[Order] = []

        # Assuming that the prices will always be greater than 0
        max_own_trade_test = -1
        
        if state.own_trades != {} and (state.own_trades.get("ASH_COATED_OSMIUM") is not None):
            for trade in state.own_trades["ASH_COATED_OSMIUM"]:
                if trade.price > max_own_trade_test and trade.buyer == "SUBMISSION":
                    max_own_trade_test = trade.price

        # TODO: Maybe check if we're in a rising trend and if so buy and sell??? Or going down trend too maybe :0
        for ask, ask_amount in list(order_depth.sell_orders.items()):
            # if ask < acceptable_buy_price:
            test_amount_limit = min(ask_amount, 5)

            print(f"BUY ASH_COATED_OSMIUM: {str(-ask_amount)} x {acceptable_buy_price}")
            # orders.append(Order(product_name, ask, -ask_amount))
            orders.append(Order(product_name, ask, -test_amount_limit))

        for bid, bid_amount in list(order_depth.buy_orders.items()):
            if bid > acceptable_sell_price:
                test = 0
                if state.position.get("ASH_COATED_OSMIUM") is not None:
                    test = state.position["ASH_COATED_OSMIUM"]
                
                if test - bid_amount >= 0:
                    print(f"SELL ASH_COATED_OSMIUM: {str(bid_amount)} x {acceptable_sell_price}")
                    orders.append(Order(product_name, bid, -bid_amount))
                else:
                    print(f"Look at this: {test} - {bid_amount} = {test - bid_amount}")
        
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
        PRODUCT_NAMES = ["INTARIAN_PEPPER_ROOT",
                         "ASH_COATED_OSMIUM"]

        POSITION_LIMITS = {
            "INTARIAN_PEPPER_ROOT": 80,
            "ASH_COATED_OSMIUM": 80
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
            if product == "ASH_COATED_OSMIUM":
                new_data.update_previous_EMA(product, strategy.product_info[product].EMA)
            


            """
            Skip the first iteration of trading or any products we don't want to trade for now,
            also tariffs are scary (boo) (oh no) (spooky)
            """
            # products_we_want_to_trade: list[str] = ["INTARIAN_PEPPER_ROOT", "ASH_COATED_OSMIUM"]
            products_we_want_to_trade: list[str] = ["ASH_COATED_OSMIUM"]

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
            if product == "INTARIAN_PEPPER_ROOT":
                result[product] = strategy.trade_intarian_pepper_root(order_depth)
            
            elif product == "ASH_COATED_OSMIUM":
                result[product] = strategy.trade_ash_coated_osmium(state, order_depth)
            
            new_data.current_positions[product] = position



        """ Make the new data to append for the next iteration """
        traderData = encode(new_data)

        # Sample conversion request. Check more details below. 
        conversions = 0
        return result, conversions, traderData

