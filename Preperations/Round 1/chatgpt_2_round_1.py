from datamodel import OrderDepth, TradingState, Order
import json
from typing import List
import statistics

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

def get_average(prices):
    return sum(prices) / len(prices)

def get_lowest_sell_order(sell_orders):
    return min(sell_orders, key=lambda x: x[0])

def get_highest_buy_order(buy_orders):
    return max(buy_orders, key=lambda x: x[0])

class Trader:
    def run(self, state: TradingState):
        result = {}
        conversions = 0
        sell_order_history = {}
        buy_order_history = {}

        if state.traderData != "":
            try:
                saved = json.loads(state.traderData)
                sell_order_history = saved.get("sell", {})
                buy_order_history = saved.get("buy", {})
            except Exception:
                pass

        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            sell_orders = list(order_depth.sell_orders.items())
            buy_orders = list(order_depth.buy_orders.items())

            # Initialize history lists
            if product not in sell_order_history:
                sell_order_history[product] = []
            if product not in buy_order_history:
                buy_order_history[product] = []

            # Record new prices
            if sell_orders:
                best_ask, _ = get_lowest_sell_order(sell_orders)
                sell_order_history[product].append(best_ask)
                if len(sell_order_history[product]) > 100:
                    sell_order_history[product].pop(0)

            if buy_orders:
                best_bid, _ = get_highest_buy_order(buy_orders)
                buy_order_history[product].append(best_bid)
                if len(buy_order_history[product]) > 100:
                    buy_order_history[product].pop(0)

            # Use midprice and volatility for adaptive fair value
            recent_asks = sell_order_history[product]
            recent_bids = buy_order_history[product]
            if recent_asks and recent_bids:
                mid_prices = [(a + b) / 2 for a, b in zip(recent_asks, recent_bids)]
                fair_price = get_average(mid_prices)
                volatility = statistics.stdev(mid_prices) if len(mid_prices) >= 2 else 1
            elif recent_asks:
                fair_price = get_average(recent_asks)
                volatility = statistics.stdev(recent_asks) if len(recent_asks) >= 2 else 1
            elif recent_bids:
                fair_price = get_average(recent_bids)
                volatility = statistics.stdev(recent_bids) if len(recent_bids) >= 2 else 1
            else:
                fair_price = 1000  # Fallback
                volatility = 1

            spread_buffer = max(2, 2.5 * volatility)
            acceptable_buy_price = fair_price - spread_buffer
            acceptable_sell_price = fair_price + spread_buffer

            pos = state.position.get(product, 0)
            position_limit = 50

            if sell_orders:
                best_ask, best_ask_amount = get_lowest_sell_order(sell_orders)
                if best_ask < acceptable_buy_price and pos < position_limit:
                    buy_qty = min(best_ask_amount, position_limit - pos)
                    orders.append(Order(product, best_ask, buy_qty))
                    pos += buy_qty

            if buy_orders:
                best_bid, best_bid_amount = get_highest_buy_order(buy_orders)
                if best_bid > acceptable_sell_price and pos > -position_limit:
                    sell_qty = min(best_bid_amount, pos + position_limit)
                    orders.append(Order(product, best_bid, -sell_qty))
                    pos -= sell_qty

            result[product] = orders

        traderData = json.dumps({"sell": sell_order_history, "buy": buy_order_history})
        return result, conversions, traderData