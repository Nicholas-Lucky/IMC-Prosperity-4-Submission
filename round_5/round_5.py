from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
from numpy import mean, std, log, diff
from math import floor, ceil, sqrt, e
from statistics import fmean, NormalDist
from jsonpickle import encode, decode
import string

class New_Data:
    def __init__(self, product_names):
        self.MAX_HISTORY_LENGTH = 150

        self.sell_order_history = self.make_empty_container(products=product_names)
        self.buy_order_history = self.make_empty_container(products=product_names)
        self.mid_order_history = self.make_empty_container(products=product_names)
        self.current_positions = self.make_empty_container(products=product_names, make_position_dictionary=True)
        self.previous_EMAs = self.make_empty_container(products=product_names)

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
        if len(self.previous_EMAs[product]) > self.MAX_HISTORY_LENGTH:
            self.previous_EMAs[product].pop(0)
        self.previous_EMAs[product].append(new_EMA)

class Strategy:
    def __init__(self):
        pass

    def calculate_EMA(self, product_name, new_data, best_bid, best_ask):
        alpha = 0.3

        current_mid_price = (best_bid + best_ask) / 2

        if new_data.previous_EMAs[product_name] == []:
           new_data.previous_EMAs[product_name].append(current_mid_price)

        EMA = (alpha * current_mid_price) + ((1 - alpha) * new_data.previous_EMAs[product_name][-1])
        new_data.update_previous_EMA(product_name, EMA)

        # Currently not really used, but it's good in case maybe
        # self.acceptable_buy_price = ceil(self.EMA)
        # self.acceptable_sell_price = floor(self.EMA)

        return EMA

    def trade_protein_snack_packs(self, product_name, new_data, sorted_buy_orders, best_bid, sorted_sell_orders, best_ask, order_book_imbalance):
        mid_order_history = new_data.mid_order_history[product_name]
        
        recent_mid_prices = mid_order_history[-20:]
        current_mid_price = (best_bid + best_ask) / 2

        fair_value = mean(recent_mid_prices)
        
        mispriced_threshold = fair_value + 0.5 * order_book_imbalance

        current_position_duplicate = new_data.current_positions[product_name]
        position_limit_duplicate = 10

        # Orders to return back
        orders: List[Order] = []
        remaining_buy_capacity = position_limit_duplicate - current_position_duplicate
        remaining_sell_capacity = position_limit_duplicate + current_position_duplicate
        
        # Market making strategy in addition to the mispriced strategy
        ema = self.calculate_EMA(product_name, new_data, best_bid, best_ask)
        spread = abs(best_bid - best_ask)
        position_skew = 0.15

        position_shift = -current_position_duplicate * position_skew

        buy_factor = max(0.0, remaining_buy_capacity / position_limit_duplicate)
        sell_factor = max(0.0, remaining_sell_capacity / position_limit_duplicate)

        buy_size = int(10 * buy_factor)
        sell_size = int(10 * sell_factor)

        # If we're not in a downward trend
        more_recent_average = mean(mid_order_history[-10:])
        less_recent_average = mean(mid_order_history[-20:])
        
        # 30% fair value and 70% ema seems like the sweet spot
        adjusted_fair_value = (0.3 * fair_value) + (0.7 * ema)

        acceptable_buy_price = int(adjusted_fair_value - (spread / 8))
        acceptable_sell_price = int(adjusted_fair_value + (spread / 8))

        if acceptable_sell_price < best_ask and acceptable_sell_price > current_mid_price:  # Selling
            amount_to_sell = min(buy_size, remaining_buy_capacity)
            orders.append(Order(product_name, int(acceptable_sell_price), -amount_to_sell))

        if acceptable_buy_price > best_bid and acceptable_buy_price < current_mid_price and more_recent_average > less_recent_average:  # Buying
            amount_to_buy = min(buy_size, remaining_buy_capacity)
            orders.append(Order(product_name, int(acceptable_buy_price), amount_to_buy))

        return orders

    def trade_pebbles(self, product_name, new_data, sorted_buy_orders, best_bid, sorted_sell_orders, best_ask, order_book_imbalance):
        mid_order_history = new_data.mid_order_history[product_name]
        previous_EMAs = new_data.previous_EMAs[product_name]
        
        recent_mid_prices = mid_order_history[-20:]
        current_mid_price = (best_bid + best_ask) / 2

        fair_value = mean(recent_mid_prices)
        
        mispriced_threshold = fair_value + 0.5 * order_book_imbalance

        current_position_duplicate = new_data.current_positions[product_name]
        position_limit_duplicate = 10

        # Orders to return back
        orders: List[Order] = []
        remaining_buy_capacity = position_limit_duplicate - current_position_duplicate
        remaining_sell_capacity = position_limit_duplicate + current_position_duplicate
        
        # Market making strategy in addition to the mispriced strategy
        ema = self.calculate_EMA(product_name, new_data, best_bid, best_ask)
        spread = abs(best_bid - best_ask)
        position_skew = 0.15

        position_shift = -current_position_duplicate * position_skew

        buy_factor = max(0.0, remaining_buy_capacity / position_limit_duplicate)
        sell_factor = max(0.0, remaining_sell_capacity / position_limit_duplicate)

        buy_size = int(10 * buy_factor)
        sell_size = int(10 * sell_factor)

        # If we're not in a downward trend
        more_recent_average = mean(mid_order_history[-5:])
        less_recent_average = mean(mid_order_history[-10:])
        
        # 30% fair value and 70% ema seems like the sweet spot
        adjusted_fair_value = (0.1 * fair_value) + (0.9 * ema)

        acceptable_buy_price = int(adjusted_fair_value - 1)
        acceptable_sell_price = int(adjusted_fair_value + 1)

        # Only trade when we are in an upward trend
        if more_recent_average > less_recent_average:
            if acceptable_sell_price < best_ask and acceptable_sell_price > current_mid_price:  # Selling
                amount_to_sell = min(buy_size, remaining_buy_capacity)
                orders.append(Order(product_name, int(acceptable_sell_price), -amount_to_sell))

            if acceptable_buy_price > best_bid and acceptable_buy_price < current_mid_price:  # Buying
                amount_to_buy = min(buy_size, remaining_buy_capacity)
                orders.append(Order(product_name, int(acceptable_buy_price), amount_to_buy))
        
        # If we are in a downward trend, get our position to 0 as fast as possible
        elif current_position_duplicate != 0:
            orders.append(Order(product_name, int(current_mid_price), -current_position_duplicate))

        return orders

class Trader:
    def __init__(self):
        self.PRODUCT_NAMES = ["GALAXY_SOUNDS_DARK_MATTER", "GALAXY_SOUNDS_BLACK_HOLES", "GALAXY_SOUNDS_PLANETARY_RINGS", "GALAXY_SOUNDS_SOLAR_WINDS", "GALAXY_SOUNDS_SOLAR_FLAMES",
                              "SLEEP_POD_SUEDE", "SLEEP_POD_LAMB_WOOL", "SLEEP_POD_POLYESTER", "SLEEP_POD_NYLON", "SLEEP_POD_COTTON",
                              "MICROCHIP_CIRCLE", "MICROCHIP_OVAL", "MICROCHIP_SQUARE", "MICROCHIP_RECTANGLE", "MICROCHIP_TRIANGLE",
                              "PEBBLES_XS", "PEBBLES_S", "PEBBLES_M", "PEBBLES_L", "PEBBLES_XL",
                              "ROBOT_VACUUMING", "ROBOT_MOPPING", "ROBOT_DISHES", "ROBOT_LAUNDRY", "ROBOT_IRONING",
                              "UV_VISOR_YELLOW", "UV_VISOR_AMBER", "UV_VISOR_ORANGE", "UV_VISOR_RED", "UV_VISOR_MAGENTA",
                              "TRANSLATOR_SPACE_GRAY", "TRANSLATOR_ASTRO_BLACK", "TRANSLATOR_ECLIPSE_CHARCOAL", "TRANSLATOR_GRAPHITE_MIST", "TRANSLATOR_VOID_BLUE",
                              "PANEL_1X2", "PANEL_2X2", "PANEL_1X4", "PANEL_2X4", "PANEL_4X4",
                              "OXYGEN_SHAKE_MORNING_BREATH", "OXYGEN_SHAKE_EVENING_BREATH", "OXYGEN_SHAKE_MINT", "OXYGEN_SHAKE_CHOCOLATE", "OXYGEN_SHAKE_GARLIC",
                              "SNACKPACK_CHOCOLATE", "SNACKPACK_VANILLA", "SNACKPACK_PISTACHIO", "SNACKPACK_STRAWBERRY", "SNACKPACK_RASPBERRY"]

        self.POSITION_LIMITS = {}

        POSITION_LIMIT_PER_PRODUCT = 10
        for product_name in self.PRODUCT_NAMES:
            self.POSITION_LIMITS[product_name] = POSITION_LIMIT_PER_PRODUCT



        """ Make a New_Data object to update (by default) """
        self.new_data = New_Data(self.PRODUCT_NAMES)

    def bid(self):
        return 2000

    def run(self, state: TradingState):
        """ Print state properties """
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        print(f"Own trades: {state.own_trades}")



        """ Update new_data with previous trading data if it exists """
        # if state.traderData != "":
        #     self.new_data = decode(state.traderData)

        # Update the positions of each product
        for product in state.order_depths:
            current_position = 0
            if state.position:
                current_position = state.position.get(product, 0)

            self.new_data.current_positions[product] = current_position

        strategy = Strategy()



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



            """ If either the buy or sell orders are empty, don't trade anything! """
            if len(order_depth.sell_orders) == 0 or len(order_depth.buy_orders) == 0:
                return []



            """ Update order histories """
            sorted_buy_orders = self.sort_buy_orders_ascended(order_depth.buy_orders)
            sorted_sell_orders = self.sort_sell_orders_absolute_value_and_ascended(order_depth.sell_orders)

            best_bid, best_bid_amount = sorted_buy_orders[0]
            best_ask, best_ask_amount = sorted_sell_orders[0]
            current_mid_price = (best_ask + best_bid) / 2.0

            self.new_data.update_order_history(self.new_data.sell_order_history, product, best_ask)
            self.new_data.update_order_history(self.new_data.buy_order_history, product, best_bid)
            self.new_data.update_order_history(self.new_data.mid_order_history, product, current_mid_price)
            


            """ Calculate the order book imbalance (leftover from the OSMIUM and HYDROGEL_PACK) """
            order_book_imbalance = (best_bid_amount - best_ask_amount) / (best_bid_amount + best_ask_amount + 1e-9)



            """ Skip any products we don't want to trade for now """
            # products_we_want_to_trade: list[str] = ["SNACKPACK_CHOCOLATE", "SNACKPACK_VANILLA", "SNACKPACK_PISTACHIO", "SNACKPACK_STRAWBERRY", "SNACKPACK_RASPBERRY"]
            products_we_want_to_trade: list[str] = ["PEBBLES_XS", "PEBBLES_S", "PEBBLES_M", "PEBBLES_L", "PEBBLES_XL"]

            if product not in products_we_want_to_trade:
                continue
            
            
            
            """
            This is still in the for product in state.order_depths for loop
            Make our orders, and put those orders in result for that respective product
            """
            if product in ["SNACKPACK_CHOCOLATE", "SNACKPACK_VANILLA", "SNACKPACK_PISTACHIO", "SNACKPACK_STRAWBERRY", "SNACKPACK_RASPBERRY"]:
                result[product] = strategy.trade_protein_snack_packs(product, self.new_data, sorted_buy_orders, best_bid, sorted_sell_orders, best_ask, order_book_imbalance)
            
            elif product in ["PEBBLES_XS", "PEBBLES_S", "PEBBLES_M", "PEBBLES_L", "PEBBLES_XL"]:
                result[product] = strategy.trade_pebbles(product, self.new_data, sorted_buy_orders, best_bid, sorted_sell_orders, best_ask, order_book_imbalance)

            else:
                return []



        """ Make the new data to append for the next iteration """
        # Sample conversion request. Check more details below. 
        conversions = 0
        traderData = ""
        return result, conversions, traderData

    def sort_buy_orders_ascended(self, buy_orders):
        return sorted(buy_orders.items(), reverse=True)
    
    def sort_sell_orders_absolute_value_and_ascended(self, sell_orders):
        sell_orders_absolute_value = []
        for price, volume in sell_orders.items():
            sell_orders_absolute_value.append((price, abs(volume)))

        return sorted(sell_orders_absolute_value)

