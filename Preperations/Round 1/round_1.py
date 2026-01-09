from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

def string_to_dictionary(s):
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
        
        for index, value in enumerate(values):
            values[index] = int(value.strip())
        
        d[key] = values
    
    return d

def string_to_list_of_dictionaries(s):
    s = s.strip("[]")
    s = s.split("}")

    dList = []
    for entry in s:
        if entry != "":
            dList.append((entry + "}").strip(", "))
    
    sell_orders = string_to_dictionary(dList[0])
    buy_orders = string_to_dictionary(dList[1])

    dList[0] = sell_orders
    dList[1] = buy_orders
    
    return dList

def get_average(prices):
    return sum(prices) / len(prices)

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

# Kelp sell orders goes from 2029-2034

# Rainforest resin sell orders go from 9998-10005

# Squid Ink sell orders goes from 1942-1987
# ^^ first quarter half was 1970-180
# ^^ last quarter was 1960-1970

class Trader:
    
    def run(self, state: TradingState):
        """
        POSITION_LIMITS = {"RAINFOREST_RESIN": 50,
                           "SQUID_INK": 50,
                           "KELP": 50}        

        current_positions = {"RAINFOREST_RESIN": 0,
                             "SQUID_INK": 0,
                             "KELP": 0}
        
        if state.position.get("RAINFOREST_RESIN") is not None:
            current_positions["RAINFOREST_RESIN"] = state.position["RAINFOREST_RESIN"]
        
        if state.position.get("SQUID_INK") is not None:
            current_positions["SQUID_INK"] = state.position["SQUID_INK"]
        
        if state.position.get("KELP") is not None:
            current_positions["KELP"] = state.position["KELP"]
        """

        # Nothing so far (we need to make this I guess?)
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        print(f"Own trades: {state.own_trades}")

		# Orders to be placed on exchange matching engine
        result = {}

        sell_order_history = {}
        buy_order_history = {}
        if state.traderData != "":
            order_histories = string_to_list_of_dictionaries(state.traderData)
            sell_order_history = order_histories[0]
            buy_order_history = order_histories[1]
        
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

            # Make a list of orders
            orders: List[Order] = []

            """
            # Set to "RAINFOREST_RESIN" price by default
            acceptable_buy_price = 9998.5  # Participant should calculate this value
            acceptable_sell_price = 10002  # Participant should calculate this value

            if product == "SQUID_INK":
                acceptable_buy_price = 1949.5
                acceptable_sell_price = 1970
            
            elif product == "KELP":
                acceptable_buy_price = 2029.5
                acceptable_sell_price = 2032
            """

            # "RAINFOREST_RESIN" price, hardcoded for now
            acceptable_buy_price = 9999  # Participant should calculate this value
            acceptable_sell_price = 10001  # Participant should calculate this value

            if product == "SQUID_INK":
                acceptable_buy_price = 1950
                acceptable_sell_price = 1970
            
            elif product == "KELP":
                acceptable_buy_price = 2030
                acceptable_sell_price = 2032
            
            if sell_order_history.get(product) is not None:
                if product == "KELP":
                    #acceptable_buy_price = get_average(sell_order_history[product])
                    acceptable_sell_price = get_average(sell_order_history[product]) + 3

                if product == "SQUID_INK":
                    sell_order_ave = get_average(sell_order_history[product])
                    buy_order_ave = get_average(buy_order_history[product])

                    index_one = 0
                    index_two = 99
                    if len(sell_order_history[product]) < 100:
                        index_two = len(sell_order_history[product]) - 1
                    
                    sell_offset = (sell_order_history[product][index_one] - sell_order_history[product][index_two]) / 2
                    if sell_offset < 0:
                        sell_offset *= -1

                    #acceptable_buy_price = sell_order_ave
                    acceptable_sell_price = sell_order_ave + 6

            print(f"Acceptable buy price: {acceptable_buy_price}")
            print(f"Acceptable sell price: {acceptable_sell_price}")

            # I guess... how many buy and sell orders?
            print(f"Buy Order depth: {len(order_depth.buy_orders)}, Sell order depth: {len(order_depth.sell_orders)}")

            # If there are sell orders that exist (if bots are selling)
            if len(order_depth.sell_orders) != 0:
                # Get the price and quantity of the first sell?
                # best_ask = price
                # best_ask_amount = quantity
                best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
                print(f"Sell orders: {list(order_depth.sell_orders.items())}")

                if sell_order_history.get(product) is None:
                    sell_order_history[product] = [best_ask]
                else:
                    sell_order_history[product].append(best_ask)
                
                # If the bot is selling for less than we expect (wahoo)
                if int(best_ask) < acceptable_buy_price:
                    # Buy some of that I guess
                    print(f"BUY {(-1 * best_ask_amount)} x {best_ask}")
                    orders.append(Order(product, best_ask, -1 * best_ask_amount))

            # If there are buy orders that exist (if bots are buying)
            if len(order_depth.buy_orders) != 0:
                # Get the price and quantity of the first buy?
                # best_bid = price
                # best_bid_amount = quantity
                best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
                print(f"Buy orders: {list(order_depth.buy_orders.items())}")
                
                if product == "SQUID_INK":
                    if buy_order_history.get(product) is None:
                        buy_order_history[product] = [best_bid]
                    else:
                        buy_order_history[product].append(best_bid)

                # If the bot is buying for more than we expect (wahoo)
                if int(best_bid) > acceptable_sell_price:
                    # Sell some of that I guess
                    print(f"SELL {best_bid_amount} x {best_bid}")
                    orders.append(Order(product, best_bid, -best_bid_amount))
                
            # This is still in the "for product in state.order_depths" for loop
            # After we make our orders, put those orders in result for that respective product
            result[product] = orders

        newData = []
        newData.append(sell_order_history)
        newData.append(buy_order_history)

        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = str(newData)

        # Sample conversion request. Check more details below.
        conversions = 1
        return result, conversions, traderData