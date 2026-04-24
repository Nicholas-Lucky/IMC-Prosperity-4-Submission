from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
from numpy import mean, std, log
from math import floor, ceil, sqrt, e
from statistics import fmean, NormalDist
from jsonpickle import encode, decode
import string

class New_Data:
    def __init__(self, product_names, macaron_info):
        self.MAX_HISTORY_LENGTH = 150

        self.sell_order_history = self.make_empty_container(products=product_names)
        self.buy_order_history = self.make_empty_container(products=product_names)
        self.mid_order_history = self.make_empty_container(products=product_names)
        self.current_positions = self.make_empty_container(products=product_names, make_position_dictionary=True)
        self.previous_macaron_information = self.make_empty_container(products=macaron_info)
        self.previous_EMAs = self.make_empty_container(products=product_names, make_position_dictionary=True)

        # Product-specific information
        self.intarian_pepper_root_intercept = None

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
    def __init__(self, product_name, sell_order_history, buy_order_history, mid_order_history, current_position, position_limit):
        self.product_name = product_name
        self.sell_order_history = sell_order_history
        self.buy_order_history = buy_order_history
        self.mid_order_history = mid_order_history
        self.current_position = current_position
        self.position_limit = position_limit

        self.sell_order_average = 0
        if len(self.sell_order_history) > 0:
            self.sell_order_average = mean(self.sell_order_history)

        self.buy_order_average = 0
        if len(buy_order_history) > 0:
            self.buy_order_average = mean(buy_order_history)

        self.mid_order_average = 0
        if len(mid_order_history) > 0:
            self.mid_order_average = mean(mid_order_history)

        self.historical_average_mid_price = (self.buy_order_average + self.sell_order_average) / 2

        # This will be implemented in children classes
        self.acceptable_buy_price = None
        self.acceptable_sell_price = None

class Intarian_Pepper_Root(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, mid_order_history, current_position, position_limit, intercept):
        super().__init__(product_name, sell_order_history, buy_order_history, mid_order_history, current_position, position_limit)
        
        self.intercept = None
        if intercept is not None:
            self.intercept = intercept

        # The general price increases by 0.001 every timestamp (100 ticks)
        self.drift = 0.001

class Ash_Coated_Osmium(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, mid_order_history, current_position, position_limit, previous_EMA):
        super().__init__(product_name, sell_order_history, buy_order_history, mid_order_history, current_position, position_limit)

class Voucher(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, mid_order_history, current_position, position_limit, previous_EMA):
        super().__init__(product_name, sell_order_history, buy_order_history, mid_order_history, current_position, position_limit)
    
    def calculate_predicted_option_price(best_bid, best_ask):
        # Use the Black Scholes Model
        PLACEHOLDER = 0
        # N = Cumulative distribution function of the standard normal distribution

        underlying_mid_price = (best_bid + best_ask) / 2
        strike_price = PLACEHOLDER
        expiry_time = PLACEHOLDER
        volatility = PLACEHOLDER
        interest_rate = PLACEHOLDER

        d_1 = (log(underlying_mid_price / strike_price) + (((volatility ** 2) / 2) * expiry_time)) / (volatility * sqrt(expiry_time))
        d_2 = d_1 - (volatility * sqrt(expiry_time))

        N_1 = NormalDist.cdf(d_1)
        N_2 = NormalDist.cdf(d_2)

        predicted_option_price = (underlying_mid_price * N_1) - (strike_price * (e ** (-1 * interest_rate * expiry_time)) * N_2)
        return predicted_option_price

class Strategy:
    def __init__(self, sell_order_history, buy_order_history, mid_order_history, current_positions, position_limits, previous_EMAs, intarian_pepper_root_intercept):
        self.product_info = {}

        self.product_info["INTARIAN_PEPPER_ROOT"] = Intarian_Pepper_Root("INTARIAN_PEPPER_ROOT",
                                                                         sell_order_history["INTARIAN_PEPPER_ROOT"],
                                                                         buy_order_history["INTARIAN_PEPPER_ROOT"],
                                                                         mid_order_history["INTARIAN_PEPPER_ROOT"],
                                                                         current_positions["INTARIAN_PEPPER_ROOT"],
                                                                         position_limits["INTARIAN_PEPPER_ROOT"],
                                                                         intarian_pepper_root_intercept)

        self.product_info["ASH_COATED_OSMIUM"] = Ash_Coated_Osmium("ASH_COATED_OSMIUM",
                                                                   sell_order_history["ASH_COATED_OSMIUM"],
                                                                   buy_order_history["ASH_COATED_OSMIUM"],
                                                                   mid_order_history["ASH_COATED_OSMIUM"],
                                                                   current_positions["ASH_COATED_OSMIUM"],
                                                                   position_limits["ASH_COATED_OSMIUM"],
                                                                   previous_EMAs["ASH_COATED_OSMIUM"])
        
        self.product_info["VOUCHER"] = Voucher("VOUCHER",
                                               sell_order_history["VOUCHER"],
                                               buy_order_history["VOUCHER"],
                                               mid_order_history["VOUCHER"],
                                               current_positions["VOUCHER"],
                                               position_limits["VOUCHER"],
                                               previous_EMAs["VOUCHER"])

    def trade_intarian_pepper_root(self, state, buy_orders, highest_buy_order, sell_orders, lowest_sell_order, current_mid_price):
        intarian_pepper_root = self.product_info["INTARIAN_PEPPER_ROOT"]
        product_name = intarian_pepper_root.product_name

        if intarian_pepper_root.intercept is None:
            intarian_pepper_root.intercept = round((current_mid_price - intarian_pepper_root.drift * state.timestamp) / 1000) * 1000

        fair_value = intarian_pepper_root.intercept + intarian_pepper_root.drift * state.timestamp
        remaining_buy_capacity = intarian_pepper_root.position_limit - intarian_pepper_root.current_position
        
        current_position_duplicate = intarian_pepper_root.current_position

        # Orders to return back
        orders: List[Order] = []

        # Buy everything as long as the price is <= fair_value + 7
        for ask, ask_amount in sell_orders:
            if remaining_buy_capacity <= 0:
                break

            if ask <= int(fair_value) + 7:
                amount_to_buy = min(ask_amount, remaining_buy_capacity)

                if amount_to_buy > 0:
                    orders.append(Order(product_name, ask, amount_to_buy))
                    remaining_buy_capacity -= amount_to_buy
        
        # Sell if there is a small dip (highest_buy_order > fair_value - 1) in case of crashes
        if remaining_buy_capacity > 0:
            sell_threshold = int(fair_value) - 1

            if sell_threshold < lowest_sell_order:
                amount_to_sell = min(remaining_buy_capacity, 40)
                orders.append(Order(product_name, sell_threshold, amount_to_sell))
        
        # Also sell if the price is super high (>= fair_value + 8) and if we're at the position limit
        # (we could sell anyway and get more profit than normal)
        if current_position_duplicate >= intarian_pepper_root.position_limit:
            remaining_sell_capacity = intarian_pepper_root.position_limit + current_position_duplicate

            for bid, bid_amount in buy_orders:
                if bid >= int(fair_value) + 8 and current_position_duplicate > 60 and remaining_sell_capacity > 0:
                    amount_to_sell = min(bid_amount, current_position_duplicate - 60, remaining_sell_capacity)

                    if amount_to_sell > 0:
                        orders.append(Order(product_name, bid, -amount_to_sell))
                        remaining_sell_capacity -= amount_to_sell
                        current_position_duplicate -= amount_to_sell
        
        return orders
    
    def trade_ash_coated_osmium(self, buy_orders, highest_buy_order, sell_orders, lowest_sell_order, order_book_imbalance):
        ash_coated_osmium = self.product_info["ASH_COATED_OSMIUM"]
        product_name = ash_coated_osmium.product_name
        
        recent_mid_prices = ash_coated_osmium.mid_order_history[-20:]
        fair_value = mean(recent_mid_prices)
        mispriced_threshold = fair_value + 2.0 * order_book_imbalance

        current_position_duplicate = ash_coated_osmium.current_position

        # Orders to return back
        orders: List[Order] = []
        remaining_buy_capacity = ash_coated_osmium.position_limit - current_position_duplicate
        remaining_sell_capacity = ash_coated_osmium.position_limit + current_position_duplicate

        # Buy mispriced prices
        for ask, ask_amount in sell_orders:
            if remaining_buy_capacity <= 0:
                break

            if mispriced_threshold - ask >= 0.5:
                amount_to_buy = min(ask_amount, remaining_buy_capacity, 30)

                if amount_to_buy > 0:
                    orders.append(Order(product_name, ask, amount_to_buy))
                    remaining_buy_capacity -= amount_to_buy
                    current_position_duplicate += amount_to_buy
        
        # Sell mispriced prices
        for bid, bid_amount in buy_orders:
            if remaining_sell_capacity <= 0:
                break

            if bid - mispriced_threshold >= 0.5:
                amount_to_sell = min(bid_amount, remaining_sell_capacity, 30)

                if amount_to_sell > 0:
                    orders.append(Order(product_name, bid, -amount_to_sell))
                    remaining_sell_capacity -= amount_to_sell
                    current_position_duplicate -= amount_to_sell
        
        # Market making strategy in addition to the mispriced strategy
        spread = 2
        position_skew = 0.10

        position_shift = -current_position_duplicate * position_skew
        acceptable_buy_price = int(fair_value + position_shift - spread)
        acceptable_sell_price = int(fair_value + position_shift + spread) + 1

        if acceptable_buy_price >= lowest_sell_order:
            acceptable_buy_price = lowest_sell_order - 1
        
        if acceptable_sell_price <= highest_buy_order:
            acceptable_sell_price = highest_buy_order + 1

        buy_factor = max(0.0, remaining_buy_capacity / ash_coated_osmium.position_limit)
        sell_factor = max(0.0, remaining_sell_capacity / ash_coated_osmium.position_limit)

        buy_size = int(30 * buy_factor)
        sell_size = int(30 * sell_factor)

        if buy_size > 0 and remaining_buy_capacity > 0 and acceptable_buy_price < fair_value:
            orders.append(Order(product_name, acceptable_buy_price, min(buy_size, remaining_buy_capacity)))
        
        if sell_size > 0 and remaining_sell_capacity > 0 and acceptable_sell_price > fair_value:
            orders.append(Order(product_name, acceptable_sell_price, -min(sell_size, remaining_sell_capacity)))
        
        # Secondary backup layer in case of liquidity
        acceptable_buy_price_secondary = acceptable_buy_price - 3
        acceptable_sell_price_secondary = acceptable_sell_price + 3

        if remaining_buy_capacity > 0 and buy_factor > 0:
            amount_to_buy = min(15, max(0, remaining_buy_capacity - buy_size))
            if amount_to_buy > 0:
                orders.append(Order(product_name, acceptable_buy_price_secondary, amount_to_buy))
        
        if remaining_sell_capacity > 0 and sell_factor > 0:
            amount_to_sell = min(15, max(0, remaining_sell_capacity - sell_size))
            if amount_to_sell > 0:
                orders.append(Order(product_name, acceptable_sell_price_secondary, amount_to_sell))
        
        return orders

    def trade_vouchers(self, state, order_depth):
        voucher = self.product_info["VOUCHER"]
        product_name = voucher.product_name
        
        best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
        best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
        spread = best_ask - best_bid

        predicted_option_price = voucher.calculate_predicted_option_price(best_bid, best_ask)

        acceptable_buy_price = predicted_option_price - (spread / 2)
        acceptable_sell_price = predicted_option_price + (spread / 2)

        # Orders to return back
        orders: List[Order] = []

        for ask, ask_amount in list(order_depth.sell_orders.items()):
            if ask < acceptable_buy_price:
                print(f"BUY voucher: {str(-ask_amount)} x {acceptable_buy_price}")
                orders.append(Order(product_name, ask, -ask_amount))

        for bid, bid_amount in list(order_depth.buy_orders.items()):
            if bid > acceptable_sell_price:
                print(f"SELL voucher: {str(bid_amount)} x {acceptable_sell_price}")
                orders.append(Order(product_name, bid, -bid_amount))
        
        return orders

class Trader:
    def __init__(self):
        self.PRODUCT_NAMES = ["INTARIAN_PEPPER_ROOT",
                              "ASH_COATED_OSMIUM"]

        self.POSITION_LIMITS = {
            "INTARIAN_PEPPER_ROOT": 80,
            "ASH_COATED_OSMIUM": 80
        }

        self.MACARON_INFO = ["askPrice",
                             "bidPrice",
                             "exportTariff",
                             "importTariff",
                             "sugarPrice",
                             "sunlightIndex",
                             "transportFees"]

        """ Make a New_Data object to update (by default) """
        self.new_data = New_Data(self.PRODUCT_NAMES, self.MACARON_INFO)

    def bid(self):
        return 2000

    def run(self, state: TradingState):
        """ Print state properties """
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        print(f"Own trades: {state.own_trades}")



        """ Update new_data with previous trading data if it exists """
        if state.traderData != "":
            self.new_data = decode(state.traderData)

        # Update the positions of each product
        for product in state.order_depths:
            current_position = 0
            if state.position:
                current_position = state.position.get(product, 0)

            self.new_data.current_positions[product] = current_position

        strategy = Strategy(self.new_data.sell_order_history,
                            self.new_data.buy_order_history,
                            self.new_data.mid_order_history,
                            self.new_data.current_positions,
                            self.POSITION_LIMITS,
                            self.new_data.previous_EMAs,
                            self.new_data.intarian_pepper_root_intercept)



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
            


            """ Calculate the order book imbalance (currently for the ASH_COATED_OSMIUM) """
            order_book_imbalance = (best_bid_amount - best_ask_amount) / (best_bid_amount + best_ask_amount + 1e-9)



            """ Skip any products we don't want to trade for now """
            # products_we_want_to_trade: list[str] = ["INTARIAN_PEPPER_ROOT", "ASH_COATED_OSMIUM"]
            products_we_want_to_trade: list[str] = ["INTARIAN_PEPPER_ROOT", "ASH_COATED_OSMIUM"]

            if product not in products_we_want_to_trade:
                continue
            
            
            
            """
            This is still in the for product in state.order_depths for loop
            Make our orders, and put those orders in result for that respective product
            """
            if product == "INTARIAN_PEPPER_ROOT":
                result[product] = strategy.trade_intarian_pepper_root(state, sorted_buy_orders, best_bid, sorted_sell_orders, best_ask, current_mid_price)

                """ Update the intercept for the Intarian Pepper Root """
                self.new_data.intarian_pepper_root_intercept = strategy.product_info[product].intercept
            
            elif product == "ASH_COATED_OSMIUM":
                result[product] = strategy.trade_ash_coated_osmium(sorted_buy_orders, best_bid, sorted_sell_orders, best_ask, order_book_imbalance)

            else:
                return []
            
            self.new_data.current_positions[product] = strategy.product_info[product].current_position



        """ Make the new data to append for the next iteration """
        traderData = encode(self.new_data)

        # Sample conversion request. Check more details below. 
        conversions = 0
        return result, conversions, traderData

    def sort_buy_orders_ascended(self, buy_orders):
        return sorted(buy_orders.items(), reverse=True)
    
    def sort_sell_orders_absolute_value_and_ascended(self, sell_orders):
        sell_orders_absolute_value = []
        for price, volume in sell_orders.items():
            sell_orders_absolute_value.append((price, abs(volume)))

        return sorted(sell_orders_absolute_value)
