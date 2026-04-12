from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
from numpy import mean, std
import string

def get_position_limits():
    POSITION_LIMITS = {
        "EMERALDS": 80,
        "TOMATOES": 80
    }
    
    return POSITION_LIMITS

class Product:
    def __init__(self, name, sell_order_history, buy_order_history, current_position):
        # Name
        self.name = name

        # Sell order history
        self.sell_order_history = sell_order_history
        self.sell_order_average = 0
        if len(self.sell_order_history) > 0:
            self.sell_order_average = mean(self.sell_order_history)

        # Buy order history
        self.buy_order_history = buy_order_history
        self.buy_order_average = 0
        if len(self.buy_order_history) > 0:
            self.buy_order_average = mean(self.buy_order_history)

        # Mid Price
        self.average_mid_price = (self.buy_order_average + self.sell_order_average) / 2

        # 1.002 -> 0.8
        # 1 -> 0.5
        # 0.002 -> 0.3
        # 0.000 to 0.002 -> 0.0 -> 0.3
        # 0.002 * x = 0.3
        # x = 0.3 / 0.002 = 150
        # if self.sell_order_average > 1.002 * self.buy_order_average:
        #     buy_order_weight = ((self.sell_order_average / self.buy_order_average) - 1) * 150
        #     self.average_mid_price = (buy_order_weight * self.buy_order_average) + ((1 - buy_order_weight) * self.sell_order_average)
        # self.average_mid_price = 0.8 * self.buy_order_average + 0.2 * self.sell_order_average

        # Position information
        self.position = current_position
        self.position_limit = get_position_limits()[name]

        # Default buy and sell thresholds
        self.default_offset = self.calculate_offset(10, 3)
        self.current_offset = self.default_offset
        self.acceptable_buy_price = self.average_mid_price - self.current_offset
        self.acceptable_sell_price = self.average_mid_price + self.current_offset
    
    def calculate_offset(self, range, divisor=3):
        if len(self.sell_order_history) == 0:
            return 0
    
        if len(self.buy_order_history) == 0:
            return 0

        index_one = 0
        index_two = range
        if len(self.sell_order_history) < (range + 1):
            index_two = len(self.sell_order_history) - 1
        if len(self.buy_order_history) < (range + 1):
            index_two = len(self.buy_order_history) - 1

        if index_two == len(self.buy_order_history) - 1:
            if len(self.sell_order_history) - 1 < index_two:
                index_two = len(self.sell_order_history) - 1

        most_recent = (self.sell_order_history[index_one] + self.buy_order_history[index_one]) / 2
        less_recent = (self.sell_order_history[-index_two] + self.buy_order_history[-index_two]) / 2
        sell_offset = (most_recent - less_recent) / divisor
        if sell_offset < 0:
            sell_offset *= -1
        
        return sell_offset

    def set_buy_price_offset(self, new_offset):
        self.acceptable_buy_price += self.current_offset
        self.acceptable_buy_price -= new_offset

        self.current_offset = new_offset

    def set_sell_price_offset(self, new_offset):
        self.acceptable_sell_price -= self.current_offset
        self.acceptable_sell_price += new_offset

        self.current_offset = new_offset

    def set_acceptable_buy_price(self, new_price):
        self.acceptable_buy_price = new_price - self.current_offset
    
    def set_acceptable_sell_price(self, new_price):
        self.acceptable_sell_price = new_price + self.current_offset
    
    def get_recent_mid_price(self, recent):
        recent_sell_order_average = self.sell_order_average
        recent_buy_order_average = self.buy_order_average

        if len(self.sell_order_history) > recent:
            recent_sell_order_average = mean(self.buy_order_history[-recent:])
        if len(self.buy_order_history) > recent:
            recent_buy_order_average = mean(self.buy_order_history[-recent:])
        
        return (recent_sell_order_average + recent_buy_order_average) / 2

class Macaron(Product):
    def __init__(self, name, sell_order_history, buy_order_history, current_position, observation_info_history, current_observation_info):
        #super().__init__(name, sell_order_history, buy_order_history, current_position)
        self.name = name

        self.sell_order_history = sell_order_history
        self.buy_order_history = buy_order_history

        self.sell_order_average = 0
        if len(sell_order_history) > 0:
            self.sell_order_average = mean(sell_order_history)
        
        self.buy_order_average = 0
        if len(buy_order_history) > 0:
            self.buy_order_average = mean(buy_order_history)

        self.historical_average_mid_price = (self.sell_order_average + self.sell_order_average) / 2

        self.position = current_position

        self.observation_info_history = observation_info_history
        
        self.historical_ask_price_mean = 0
        if len(observation_info_history["askPrice"]) > 0:
            self.historical_ask_price_mean = mean(observation_info_history["askPrice"])

        self.historical_bid_price_mean = 0
        if len(observation_info_history["bidPrice"]) > 0:
            self.historical_bid_price_mean = mean(observation_info_history["bidPrice"])

        self.historical_export_tariff_mean = 0
        if len(observation_info_history["exportTariff"]) > 0:
            self.historical_export_tariff_mean = mean(observation_info_history["exportTariff"])

        self.historical_import_tariff_mean = 0
        if len(observation_info_history["importTariff"]) > 0:
            self.historical_import_tariff_mean = mean(observation_info_history["importTariff"])

        self.historical_sugar_price_mean = 0
        if len(observation_info_history["sugarPrice"]) > 0:
            self.historical_sugar_price_mean = mean(observation_info_history["sugarPrice"])

        self.historical_sunlight_mean = 0
        if len(observation_info_history["sunlightIndex"]) > 0:
            self.historical_sunlight_mean = mean(observation_info_history["sunlightIndex"])

        self.historical_transport_fees_mean = 0
        if len(observation_info_history["transportFees"]) > 0:
            self.historical_transport_fees_mean = mean(observation_info_history["transportFees"])

        self.historical_ask_price_std = 0
        if len(observation_info_history["askPrice"]) > 0:
            self.historical_ask_price_std = std(observation_info_history["askPrice"])
        
        self.historical_bid_price_std = 0
        if len(observation_info_history["bidPrice"]) > 0:
            self.historical_bid_price_std = std(observation_info_history["bidPrice"])
        
        self.historical_export_tariff_std = 0
        if len(observation_info_history["exportTariff"]) > 0:
            self.historical_export_tariff_std = std(observation_info_history["exportTariff"])
        
        self.historical_import_tariff_std = 0
        if len(observation_info_history["importTariff"]) > 0:
            self.historical_import_tariff_std = std(observation_info_history["importTariff"])
        
        self.historical_sugar_price_std = 0
        if len(observation_info_history["sugarPrice"]) > 0:
            self.historical_sugar_price_std = std(observation_info_history["sugarPrice"])
        
        self.historical_sunlight_std = 0
        if len(observation_info_history["sunlightIndex"]) > 0:
            self.historical_sunlight_std = std(observation_info_history["sunlightIndex"])
        
        self.historical_transport_fees_std = 0
        if len(observation_info_history["transportFees"]) > 0:
            self.historical_transport_fees_std = std(observation_info_history["transportFees"])
        
        self.current_average_mid_price = (self.historical_ask_price_mean + self.historical_bid_price_mean) / 2

        self.current_observation_info = current_observation_info

        self.ask_price = current_observation_info.askPrice
        self.bid_price = current_observation_info.bidPrice
        self.export_tariff = current_observation_info.exportTariff
        self.import_tariff = current_observation_info.importTariff
        self.sugar_price = current_observation_info.sugarPrice
        self.sunlight = current_observation_info.sunlightIndex
        self.transport_fees = current_observation_info.transportFees

        # maybe comment out
        """ self.normalized_ask_price = 0
        if self.historical_ask_price_std != 0:
            self.normalized_ask_price = (self.ask_price - self.historical_ask_price_mean) / self.historical_ask_price_std
        
        self.normalized_bid_price = 0
        if self.historical_bid_price_std != 0:
            self.normalized_bid_price = (self.bid_price - self.historical_bid_price_mean) / self.historical_bid_price_std """

        self.normalized_export_tariff = 0
        if self.historical_export_tariff_std != 0:
            self.normalized_export_tariff = (self.export_tariff - self.historical_export_tariff_mean) / self.historical_export_tariff_std
        
        self.normalized_import_tariff = 0
        if self.historical_import_tariff_std != 0:
            self.normalized_import_tariff = (self.import_tariff - self.historical_import_tariff_mean) / self.historical_import_tariff_std
        
        self.normalized_sugar_price = 0
        if self.historical_sugar_price_std != 0:
            self.normalized_sugar_price = (self.sugar_price - self.historical_sugar_price_mean) / self.historical_sugar_price_std
        
        self.normalized_sunlight = 0
        if self.historical_sunlight_std != 0:
            self.normalized_sunlight = (self.sunlight - self.historical_sunlight_mean) / self.historical_sunlight_std
        
        self.normalized_transport_fees = 0
        if self.historical_transport_fees_std != 0:
            self.normalized_transport_fees = (self.transport_fees - self.historical_transport_fees_mean) / self.historical_transport_fees_std

        #self.MVI_multiplier = (self.normalized_ask_price * 0.1) + (self.normalized_bid_price * 0.1) + (self.normalized_export_tariff * 0.1) + (self.normalized_import_tariff * 0.1) + (self.normalized_sugar_price * 0.1) + (self.normalized_sunlight * -0.4) + (self.normalized_transport_fees * 0.1)
        #self.acceptable_buy_price = current_average_mid_price * self.MVI_multiplier
        #self.acceptable_buy_price = self.historical_average_mid_price * self.MVI_multiplier

        self.export_tariff_weight = 0.1
        self.import_tariff_weight = 0.1
        self.sugar_price_weight = 0.1
        self.sunlight_weight = -0.4
        self.transport_fees_weight = 0.1

        self.MVI_multiplier = (self.normalized_export_tariff * self.export_tariff_weight) + \
                              (self.normalized_import_tariff * self.import_tariff_weight) + \
                              (self.normalized_sugar_price * self.sugar_price_weight) + \
                              (self.normalized_sunlight * self.sunlight_weight) + \
                              (self.normalized_transport_fees * self.transport_fees_weight)
        
        self.hybrid_average_mid_price = (0.3 * self.historical_average_mid_price) + (0.7 * self.current_average_mid_price)
        self.acceptable_buy_price = self.hybrid_average_mid_price * self.MVI_multiplier
        self.acceptable_sell_price = self.acceptable_buy_price

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

    d_list[0] = sell_orders
    d_list[1] = buy_orders
    d_list[2] = positions
    d_list[3] = macaron_info
    
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
        
        # Print state properties
        #print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        print(f"Own trades: {state.own_trades}")

        # testing
        print("testing")
        if state.own_trades != {}:
            for key in state.own_trades:
                print(f"PRODUCT: {key} ", end="")
                
                for item in state.own_trades[key]:
                    print(f"{item.price}, ", end="")

        # Make relavant dictionaries (by default)
        sell_order_history = make_empty_container(products=PRODUCT_NAMES, make_position_dictionary=False)
        buy_order_history = make_empty_container(products=PRODUCT_NAMES, make_position_dictionary=False)
        current_positions = make_empty_container(products=PRODUCT_NAMES, make_position_dictionary=True)
        previous_macaron_information = make_empty_container(products=MACARON_INFO, make_position_dictionary=False)

        # Update the dictionaries with previous trading data if it exists
        if state.traderData != "":
            sell_order_history, buy_order_history, current_positions, previous_macaron_information = convert_trading_data(state.traderData)

        products = initialize_product_information(PRODUCT_NAMES, sell_order_history, buy_order_history, current_positions, previous_macaron_information, None)

        # Orders to be placed on exchange matching engine
        result = {}

        # state.order_depths:
        # keys = products, values = OrderDepth instances

        # Go through each product, for each product
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

            # Skip the first iteration of trading, also tariffs are scary (boo) (oh no) (spooky)
            #if state.traderData == "" or product == "MAGNIFICENT_MACARONS":
            if state.traderData == "" or product != "TOMATOES":
                #print("First iteration, will not do any trading")
                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
                    update_order_history(sell_order_history, product, best_ask)

                    best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
                    update_order_history(buy_order_history, product, best_bid)
                continue
            
            # Get the current position of the product
            position = products[product].position
            print(f"Current position: {position}")

            # Make a list of orders
            orders: List[Order] = []
            
            # Get the thresholds to buy and sell for this specific product
            acceptable_buy_price = products[product].acceptable_buy_price
            acceptable_sell_price = products[product].acceptable_sell_price

            print(f"Acceptable buy price: {acceptable_buy_price}")
            print(f"Acceptable sell price: {acceptable_sell_price}")
            print(f"Buy Order depth: {len(order_depth.buy_orders)}, Sell order depth: {len(order_depth.sell_orders)}")

            # Make conditions (for a crash or not) in which we would want to sell everything
            best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
            best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
            mid_price = (best_ask + best_bid) / 2

            # If there are sell orders that exist (if bots are selling)
            if len(order_depth.sell_orders) != 0:
                # Get the price and quantity of the first sell?
                # best_ask = price
                # best_ask_amount = quantity
                best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
                #print(f"Sell orders: {list(order_depth.sell_orders.items())}")

                # Add the lowest sell order to sell_order_history
                update_order_history(sell_order_history, product, best_ask)

                sell_order_history[product].append(best_ask)
                
                # If the bot is selling for less than we expect (wahoo)
                if int(best_ask) < acceptable_buy_price:
                    # Buy some of that I guess
                    print(f"BUY {(-1 * best_ask_amount)} x {best_ask}")
                    buy_to_bot(orders, position, POSITION_LIMITS[product], product, best_ask, best_ask_amount)
                    #orders.append(Order(product, best_ask, -1 * best_ask_amount))
                    position += best_ask_amount

            # If there are buy orders that exist (if bots are buying)
            # if len(order_depth.buy_orders) != 0:
            for buy_order in list(order_depth.buy_orders.items()):
                # Get the price and quantity of the first buy?
                # best_bid = price
                # best_bid_amount = quantity
                best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
                print(f"Buy orders: {list(order_depth.buy_orders.items())}")
                
                update_order_history(buy_order_history, product, best_bid)

                higher_than_our_own_purchase = True
                if state.own_trades != {}:
                    maximum_purchased_price = get_maximum_purchased_order_price(state.own_trades)
                    if int(best_bid) < maximum_purchased_price:
                        higher_than_our_own_purchase = False

                # If the bot is buying for more than we expect (wahoo)
                if int(best_bid) > acceptable_sell_price and higher_than_our_own_purchase:
                # if int(best_bid) > acceptable_sell_price:
                    # Sell some of that I guess
                    print(f"SELL {best_bid_amount} x {best_bid}")
                    #sell_to_bot(orders, position, POSITION_LIMITS[product], product, best_bid, best_bid_amount)
                    orders.append(Order(product, best_bid, -1 * best_bid_amount))
                    position -= best_bid_amount
                
            # This is still in the "for product in state.order_depths" for loop
            # After we make our orders, put those orders in result for that respective product
            result[product] = orders
            current_positions[product] = position

        #print(f"WHAT IS SELL: {sell_order_history}")

        newData = []
        newData.append(sell_order_history)
        newData.append(buy_order_history)
        newData.append(current_positions)
        newData.append(previous_macaron_information)

        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = str(newData)

        # Sample conversion request. Check more details below. 
        conversions = 0
        return result, conversions, traderData
