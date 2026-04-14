from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    def bid(self):
        return 15
    
    def run(self, state: TradingState):
        """Only method required. It takes all buy and sell orders for all
        symbols as an input, and outputs a list of orders to be sent."""

        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        # Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            if product != "EMERALDS":
                continue

            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            # Current Emerald bid prices from data in a bottle tutorial round: 9990, 9992, 10000
            # Current Emerald ask prices from data in a bottle tutorial round: 10000, 10008, 10010

            acceptable_buy_price = 9995 # Participant should calculate this value
            acceptable_sell_price = 10005 # Participant should calculate this value

            print("Acceptable buy price : " + str(acceptable_buy_price))
            print("Acceptable sell price : " + str(acceptable_sell_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            for i in range(0, len(order_depth.sell_orders)):
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[i]

                # if int(best_ask) < acceptable_buy_price:
                #     print("BUY", str(-best_ask_amount) + "x", best_ask)
                #     orders.append(Order(product, best_ask, -best_ask_amount))

                print("BUY", str(-best_ask_amount) + "x", acceptable_buy_price)
                orders.append(Order(product, acceptable_buy_price, -best_ask_amount))

            for i in range(0, len(order_depth.buy_orders)):
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[i]
                
                # if int(best_bid) > acceptable_sell_price:
                #     print("SELL", str(best_bid_amount) + "x", best_bid)
                #     orders.append(Order(product, best_bid, -best_bid_amount))

                print("SELL", str(best_bid_amount) + "x", acceptable_sell_price)
                orders.append(Order(product, acceptable_sell_price, -best_bid_amount))
            
            result[product] = orders
    
        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
        # Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData