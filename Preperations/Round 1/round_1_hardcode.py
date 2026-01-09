from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

def getLowestSellOrder(sell_orders):
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

def getHighestBuyOrder(buy_orders):
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

            # Make a list of orders
            orders: List[Order] = []

            # Set to "RAINFOREST_RESIN" price by default
            acceptable_buy_price = 9999  # Participant should calculate this value
            acceptable_sell_price = 10001  # Participant should calculate this value

            if product == "SQUID_INK":
                acceptable_buy_price = 1950
                acceptable_sell_price = 1970
            
            elif product == "KELP":
                acceptable_buy_price = 2030
                acceptable_sell_price = 2032

            print(f"Acceptable buy price: {acceptable_sell_price}")
            print(f"Acceptable sell price: {acceptable_sell_price}")

            # I guess... how many buy and sell orders?
            print(f"Buy Order depth: {len(order_depth.buy_orders)}, Sell order depth: {len(order_depth.sell_orders)}")

            # If there are sell orders that exist (if bots are selling)
            if len(order_depth.sell_orders) != 0:
                # Get the price and quantity of the first sell?
                # best_ask = price
                # best_ask_amount = quantity
                best_ask, best_ask_amount = getLowestSellOrder(list(order_depth.sell_orders.items()))
                print(f"Sell orders: {list(order_depth.sell_orders.items())}")

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
                best_bid, best_bid_amount = getHighestBuyOrder(list(order_depth.buy_orders.items()))
                print(f"Buy orders: {list(order_depth.buy_orders.items())}")

                # If the bot is buying for more than we expect (wahoo)
                if int(best_bid) > acceptable_sell_price:
                    # Sell some of that I guess
                    print(f"SELL {best_bid_amount} x {best_bid}")
                    orders.append(Order(product, best_bid, -best_bid_amount))
                
            # This is still in the "for product in state.order_depths" for loop
            # After we make our orders, put those orders in result for that respective product
            result[product] = orders

        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE"
        
        # Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData
