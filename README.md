# IMC Prosperity 4 (2026) Submission
### Note: This writeup is heavily inspired by the [Alpha Animals](https://github.com/CarterT27/imc-prosperity-3), [CMU Physics](https://github.com/chrispyroberts/imc-prosperity-3), and [Byeongguk Kang, Minwoo Kim, and Uihyung Lee](https://github.com/pe049395/IMC-Prosperity-2024)'s writeups.
---
### Team Name: QuantCrow

### Team Members:
1. Tyler Thomas ([LinkedIn](https://www.linkedin.com/in/tyler-b-thomas/), [GitHub](https://github.com/TylerThomas6))
2. Nicholas Lucky ([LinkedIn](https://www.linkedin.com/in/nicholas-lucky/), [GitHub](https://github.com/Nicholas-Lucky))
---
## Overview
#### [IMC's Prosperity 2026](https://prosperity.imc.com/) is an annual trading challenge that challenges participants to program an algorithm to trade various goods on a virtual trading market with the goal of gaining as much profit, in the form of the XIREN currency, as possible. In addition to the algorithm, there are manual trading challenges that allow participants to gain additional seashells. The competition spans five rounds, with each round adding new products for our trading algorithms to consider, and a new manual trading challenge to attempt. This year, there is also an added "qualifier challenge" where teams need to make total profit of 200 thousand XIRENs in the first two rounds in order to continue competing in the third, forth, and fifth rounds. This year is the fourth iteration of the competition (Prosperity 4), and lasted from April 14th, 2026 to April 28nd, 2026. This is our second year in the competition, and we focused on continuing to learn and improve our skills in programming both an effective main trading algorithm and helpful manual trading-related code to aid us in our decision-making in the manual trading challenges.

#### Further details on this year's competition can be found on the [Prosperity 4 Wiki](https://imc-prosperity.notion.site/prosperity-4-wiki).
---
<details>
<summary><h2>Tutorial Round 🍅</h2></summary>

### Algorithmic Trading
#### As mentioned in [the Tutorial Round of the wiki](https://imc-prosperity.notion.site/tutorial-round-simulator-practice), the Tutorial Round introduced us to two products: `EMERALDS` and `TOMATOES`. `EMERALDS` is said to be relatively stable product, while `TOMATOES` is said to be less stable and fluctuates over time. `EMERALDS` has a position limit of `80`, and `TOMATOES` has a position limit of `80`.

#### Using the provided Data Capsule that allowed us to view historical prices of both `EMERALDS` and `TOMATOES`, we constructed the following price graphs of the two products:

![emeralds_historical_prices_day_minus_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/emeralds_historical_prices_day_minus_2.png)

#### From the above price graph of the `EMERALDS` product, we confirmed that `EMERALDS` does seem to be quite stable over time. Interestingly, the bid prices are generally lower than the ask prices.

![tomatoes_historical_prices](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/tomatoes_historical_prices.png)

#### From the above price graph of the `TOMATOES` product, we confirmed that `TOMATOES` does seem to be less stable than `EMERALDS` over time. Interestingly, the bid prices are also generally lower than the ask prices, and the fluctuations of the above `TOMATOES` price graph might resemble a random walk.

#### We began with the [round_5.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/Preperations/Round%205/round_5.py), which was our submitted code for the last round (Round 5) of last year's Prosperity 3 competition. We figured that this file would have a lot of existing infrastructure and logic that we could potentially use to save implementation time in this year's competition. After relearning the algorithm, we decided to simplify the algorithm by removing/storing existing functions and logic, and adding more infrastructure to potentially give the algorithm more abstraction and modularity.

#### We decided to store functionality that we thought might be useful later in the competition, but did not plan to use at the moment, in a `Functions_Storage` class. That way, the unused functions could be hidden through a dropdown menu in our IDEs without needing to delete them entirely:

```python
# In tutorial_round.py

class Functions_Storage:
    # A function we are not currently using but might consider in the future
    def voucher_makes_sense(voucher_amount, most_recent_volcanic_rock_sell_order):
        upper_bound = most_recent_volcanic_rock_sell_order * 1.02
        lower_bound = most_recent_volcanic_rock_sell_order * 0.98

        if voucher_amount < upper_bound and voucher_amount > lower_bound:
            print(f"Voucher amount {voucher_amount} DOES (YES) makes sense for most recent volcanic rock sell price {most_recent_volcanic_rock_sell_order}")
            return True
        
        print(f"Voucher amount {voucher_amount} DOES NOT (NO) make sense for most recent volcanic rock sell price {most_recent_volcanic_rock_sell_order}")
        return False
    
    # ...more functions we are not currently using but might consider in the future
```

#### In addition, we tried building off of the existing `Product` class infrastructure to make a structure where the `Product` class will be the parent class that houses attributes shared across multiple products, and individual children classes that inherit the `Product` class and can have extra attributes and functions that are more specific to a particular product:

```python
# In tutorial_round.py

# Parent class
class Product:
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit):
        self.product_name = product_name
        self.sell_order_history = sell_order_history
        self.buy_order_history = buy_order_history

        # ...other attributes that are shared across multiple products

# Child class of the Product class (in this case, the Emerald class as an example)
class Emerald(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)
        
        # These calculations for the acceptable buy and sell prices are specific to the Emerald product
        self.acceptable_buy_price = ceil(self.buy_order_average) + 1
        self.acceptable_sell_price = floor(self.sell_order_average) - 1
```

#### We wanted to simplify the `Trader` class implementation, mainly the `run()` method in the `Trader` class, so we also made a seperate `Strategy` class that the `run()` method can call to create and return back our orders we make for a given product:

```python
# In tutorial_round.py

# Strategy class
class Strategy:
    def __init__(self, sell_order_history, buy_order_history, current_positions, position_limits, previous_EMAs):
        self.product_info = {}

        # Initialize the product information (in this example, the EMERALDS product)
        self.product_info["EMERALDS"] = Emerald("EMERALDS",
                                                sell_order_history["EMERALDS"],
                                                buy_order_history["EMERALDS"],
                                                current_positions["EMERALDS"],
                                                position_limits["EMERALDS"])
    
    # This function can be called elsewhere
    def trade_emeralds(self, order_depth):
        # Trading logic

        # Orders to return back
        orders: List[Order] = []

        # More trading logic
        
        return orders

# ...later in the Trader class's run() method:
class Trader:
    def run(self, state: TradingState):
        # Trading logic

        """ Go through each product, for each product """
        for product in state.order_depths:
            
            # More trading logic

            if product == "EMERALDS":
                # Call the trade_emeralds() function we have in the Strategy class (in this example)
                result[product] = strategy.trade_emeralds(order_depth)
```

#### We also used the `traderData` variable to store product information (buy order histories, sell order histories, etc.) across different trading iterations; we also did this last year! The main change for this year's competition is that we used `jsonpickle` to more easily encode and decode information into and out of the `traderData` variable, as opposed to making customized parsing functions for the `traderData` string that might need to be updated each time we add additional types of information to `traderData`. With this functionality, we could construct a `New_Data` class that initializes and updates the current product information, which can then be encoded into `traderData`:

``` python
# In tutorial_round.py

# New_Data class to house our product information
class New_Data:
    def __init__(self, product_names, macaron_info):
        self.MAX_HISTORY_LENGTH = 150

        # Product information
        self.sell_order_history = self.make_empty_container(products=product_names)

        # More product information
    
    def make_empty_container(self, products, make_position_dictionary: bool=False):
        # Method implementation

# ...later in the Trader class's run() method:
class Trader:
    def run(self, state: TradingState):
        # Make a New_Data object to update (by default)
        new_data = New_Data(PRODUCT_NAMES, MACARON_INFO)

        # Update new_data with previous trading data if it exists
        if state.traderData != "":
            new_data = decode(state.traderData)

        # Trading logic (could include calls to update the current information in new_data)

        # Make the new data to append for the next iteration
        traderData = encode(new_data)
```

#### Our trading strategy for the `EMERALDS` product mainly involves market-making. Because the product's price is said, and was confirmed to be, relatively stable (between around 9990 and 10010), and the ask prices are generally higher than the bid prices, there seemed to be a spread that we could work with to gain profit. By buying at a price slightly higher than the average bid price, our price could be seen as more favorable relative to other bid prices, which would make us more likely to continuously be able to successfully buy `EMERALDS`. By selling at a price slightly lower than the average ask price, our price could be seen as more favorable relative to other ask prices, which would make us more likely to continuously be able to successfully sell the `EMERALDS` we previously bought. As a result of the product's spread and the ask prices generally being higher than the bid prices, this means that even though we are buying at a slightly higher price and selling at a slightly lower price, we would still be making a profit each time we buy and subsequently sell `EMERALDS`. As a result, for `EMERALDS`, we mainly calculated our acceptable buy and sell prices through the current buy and sell order averages (to potentially reduce hardcoding), and continuously buy and sell `EMERALDS` at our acceptable buy and sell prices respectively:

``` python
# In tutorial_round.py

class Emerald(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)
        
        # This is less "hardcoded", we hope?
        self.acceptable_buy_price = ceil(self.buy_order_average) + 1
        self.acceptable_sell_price = floor(self.sell_order_average) - 1

# In the Strategy class's trade_emeralds() method
class Strategy:
    # Strategy implementation

    # Method to trade the EMERALDS product
    def trade_emeralds(self, order_depth):
        # Try to buy each sell order with our acceptable buy price
        for best_ask, best_ask_amount in list(order_depth.sell_orders.items()):
            orders.append(Order(product_name, acceptable_buy_price, -best_ask_amount))

        # Try to sell to each buy order with our acceptable sell price
        for best_bid, best_bid_amount in list(order_depth.buy_orders.items()):
            orders.append(Order(product_name, acceptable_sell_price, -best_bid_amount))
```

#### Our trading strategy for the `TOMATOES` product also involves market-making, as I think the historical price graph of `TOMATOES` does also show the ask prices generally being greater than the bid prices. The difference with the `TOMATOES` product, however, is that the price of `TOMATOES` tends to fluctuate a lot, with the IMC Prosperity Discord describing it as a random walk. In order to calculate a threshold that continuously keeps up with the price fluctuations, we used exponential moving average (EMA) as our main value. The formula for exponential moving average (EMA) we used is the following:

$\text{EMA} = α * \text{Current Mid Price} + (1 - α) * \text{Previous EMA}$

#### We set alpha (α) (seemingly a value between 0 and 1 that determines how strongly more recent prices will affect the EMA) to be 0.3 to make our EMA moderately affected by more recent prices, given the random walk nature of `TOMATOES`. We calculated the current mid price during each iteration by taking the average of the highest bid price and the lowest ask price. Finally, on the first iteration, if the previous EMA has not yet been defined, we would set the previous EMA to the current mid price. After calculating the EMA, the previous EMA would be updated to the current EMA for the next iteration of the algorithm:

``` python
# In tutorial_round.py

class Tomatoes(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit, previous_EMA):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)

        self.alpha = 0.3

        self.previous_EMA = previous_EMA
        self.EMA = self.previous_EMA

# In the Strategy class's trade_tomatoes() method
class Strategy:
    # Strategy implementation

    # Method to trade the TOMATOES product
    def trade_tomatoes(self, order_depth):
        def calculate_EMA(tomatoes, best_bid, best_ask):
            # EMA calculation logic

            tomatoes.EMA = (tomatoes.alpha * current_mid_price) + ((1 - tomatoes.alpha) * tomatoes.previous_EMA)

            # EMA calculation logic

            return tomatoes.EMA
        
        # Start of the tomatoes trading strategy
        
        # ...
        
        # Calculate the EMA
        calculate_EMA(tomatoes, best_bid, best_ask)
```

#### We then used the spread between the highest bid price and the lowest ask price alongside the current EMA to help stabilize our acceptable buy and sell thresholds and better calculate our favorable buy and sell prices:

``` python
# In tutorial_round.py

class Strategy:
    # Strategy implementation

    # Method to trade the TOMATOES product
    def trade_tomatoes(self, order_depth):
        # ...

        best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
        best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
        spread = best_ask - best_bid

        # Calculate the EMA
        calculate_EMA(tomatoes, best_bid, best_ask)

        acceptable_buy_price = ceil(tomatoes.EMA - (spread / 2) + 1)
        acceptable_sell_price = floor(tomatoes.EMA + (spread / 2) - 1)
```

#### With our acceptable buy and sell prices calculated, we bought and sold `TOMATOES` similarly to how we bought and sold `EMERALDS` by trying to buy each existing sell order at our acceptable buy price, and sell to each existing buy order at our acceptable sell price:

``` python
# In tutorial_round.py

class Strategy:
    # Strategy implementation

    # Method to trade the TOMATOES product
    def trade_tomatoes(self, order_depth):
        # ...

        # Orders to return back
        orders: List[Order] = []

        # Try to buy each sell order with our acceptable buy price
        for ask, ask_amount in list(order_depth.sell_orders.items()):
            orders.append(Order(product_name, acceptable_buy_price, -ask_amount))

        # Try to sell to each buy order with our acceptable sell price
        for bid, bid_amount in list(order_depth.buy_orders.items()):
            orders.append(Order(product_name, acceptable_sell_price, -bid_amount))
        
        return orders
```

#### This is the result of our Tutorial Round algorithm only trading `EMERALDS`:

![tutorial_round_emeralds_results](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/tutorial_round_emeralds_results.png)

#### This is the result of our Tutorial Round algorithm only trading `TOMATOES`:

![tutorial_round_tomatoes_results](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/tutorial_round_tomatoes_results.png)

#### Overall, it seems that our trading strategies for `EMERALDS` and `TOMATOES` are relatively successful, at least in the sense that they are both generating steady profit! Together, if I'm remembering correctly, the entire algorithm trading both `EMERALDS` and `TOMATOES` resulted in a final total profit of around 2.1 thousand XIRENs, which we were satisfied with. We are sure there is definitely some room for improvement, however, which we are curious to identify and learn.
</details>

---
<details>
<summary><h2>Round 1 🍄</h2></summary>

### Algorithmic Trading
#### As mentioned in [Round 1 of the wiki](https://imc-prosperity.notion.site/round-1-trading-groundwork), Round 1 introduced us to our first two official tradable products: `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`. The price of `INTARIAN_PEPPER_ROOT` seems to be increasing steadilya nd linearly, while the price of `ASH_COATED_OSMIUM` seems to fluctuate in value and is more volatile. `ASH_COATED_OSMIUM` has a position limit of `80`, and `INTARIAN_PEPPER_ROOT` has a position limit of `80`.

#### Using the provided Data Capsule that allowed us to view historical prices of both `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`, we constructed the following price graphs of the two products:

![ash_coated_osmium_historical_prices_day_minus_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/ash_coated_osmium_historical_prices_day_minus_2.png)

#### From the above price graph of the `ASH_COATED_OSMIUM` product, we confirmed that `ASH_COATED_OSMIUM` seems quite volatile, and might potentially involve either a random walk or mean-reversion? 

![intarian_pepper_root_historical_prices_day_minus_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/intarian_pepper_root_historical_prices_day_minus_2.png)

#### From the above price graph of the `INTARIAN_PEPPER_ROOT` product, we confirmed that `INTARIAN_PEPPER_ROOT` does seem to be more stable than `ASH_COATED_OSMIUM`, and generally increases in price at a linear rate.

#### We began with the [tutorial_round.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/tutorial_round/tutorial_round.py) we used in the Tutorial Round, and added an `Intarian_Pepper_Root` and `Ash_Coated_Osmium` class to use in our algorithm:

```python
# In round_1.py

class Intarian_Pepper_Root(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)

        # Specific attributes go here...

class Ash_Coated_Osmium(Product):
    def __init__(self, product_name, sell_order_history, buy_order_history, current_position, position_limit, previous_EMA):
        super().__init__(product_name, sell_order_history, buy_order_history, current_position, position_limit)

        # Specific attributes go here...

# Strategy class used to trade our products
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
        # Trading logic goes here...

    def trade_ash_coated_osmium(self, order_depth):
        # Trading logic goes here...
```

#### Generally in this round, due to time contraints and limited time availability, we chose to focus on trading the `INTARIAN_PEPPER_ROOT`, as we felt that the price behavior of this product was simpler to work with. Given that the price of the `INTARIAN_PEPPER_ROOT` was continuously rising in the historical price, we could theoretically buy as much `INTARIAN_PEPPER_ROOT` as we can at the beginning, and hold it until the end of the trading window. However, such a strategy depends on the `INTARIAN_PEPPER_ROOT`'s price always increasing. If the price of `INTARIAN_PEPPER_ROOT` "crashes" at the end of the trading window, our holding of `INTARIAN_PEPPER_ROOT` might end up resulting in us losing a lot of our profit, or all of our profit in general. As a result, we wanted to create a safer algorithm that still buys and holds `INTARIAN_PEPPER_ROOT`, however also sells some `INTARIAN_PEPPER_ROOT` in case of a price drop in order to confirm at least some profit. Unfortunately, we were not able to fully create an algorithm that noticeably performed this "safety sell" in our test submissions, and we hence decided to submit a zero-profit algorithm to at least eliminate the possibility of a crash leaving us with negative profit. The zero-profit algorithm essentially skips all trading algorithms for all products, meaning the no trades should ever occur in the algorithm:

```python
# In sleepy_trader.py

class Trader:
    def run(self, state: TradingState):
        # Previous data setup lines...

        for product in state.order_depths:
            # Don't trade any products ever to guarantee zero profit
            break
```

#### These are the results of our Round 1 algorithm:

![round_1_algorithm_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_algorithm_results_1.png)
![round_1_algorithm_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_algorithm_results_2.png)

#### As expected, our algorithm resulted in zero profit, which we were fine with, as we decided to be safer this round until we can be more confident in our algorithm.

### Manual Trading
#### As mentioned in [Round 1 of the wiki](https://imc-prosperity.notion.site/round-1-trading-groundwork), the manual trading challenge for Round 1 involved two call auctions. each of which is for two separate products: `DRYLAND_FLAX` and `EMBER_MUSHROOM`. In each of the call auctions, our goal is to submit a bid price and associated quantity, and enter the auction. After entering the auction with our bid price, the auction is assumed to "end", and a clearing price will then be calculated to maximize the total volume that is traded. Any bids that are greater than or equal to the clearance price, and any asks that are less than or equal to the clearance price, can potentially be traded with. However, an important note is that the allocation for these trades are price priority, and then time priority (for trades in the same price level). In the case of our bids, this means that bids at a higher price level than our bid will be allocated first. In the same bid price level, we are assumed to be the last bids time-wise, meaning the rest of the bids from other parties at our bid price level will be allocated before our bid and quantity is allocated.

#### After the auction ends and the trades have been allocated, if our bid price and quantity allows us to have some/all of our quantity allocated, we will essentially have bought some of the associated product. At the end, we will sell this product back to the Merchant Guild at a flat rate. The rates for the two products are:
1. `DRYLAND_FLAX`: 30 XIRENs per unit (no fees)
2. `EMBER_MUSHROOM`: 20 XIRENs per unit (fee: 0.10 per unit traded)

#### The main IMC game website also provided us with the following order books for the `DRYLAND_FLAX` and `EMBER_MUSHROOM` call auctions:

![round_1_manual_trading_dyland_flax_order_book](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_manual_trading_dyland_flax_order_book.png)
![round_1_manual_trading_ember_mushroom_order_book](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_manual_trading_ember_mushroom_order_book.png)

#### Our goal is to place a bid price and bid quantity for the `DRYLAND_FLAX` and `EMBER_MUSHROOM` that nets us as much profit as we can gain at the end of the separate call auctions. It is also worth noting that the maximum bid quantity we can place for a product is `50,000`.

#### Tyler Thomas identified that a bid price level of `30` and a quantity of `9999` would be optimal for the `DRYLAND_FLAX`, and a bid price level of `17` and a quantity of `19999` would be optimal for the `EMBER_MUSHROOM`. To double-check his initial answer, we coded a [round_1_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/round_1/round_1_manual_trading.py) field that uses brute force to simulate placing different potential quantities at a certain price level, and comparing the resulting profits to find the optimal quantity to place for a given price level. Tyler Thomas was completely sure that the bid price level of `30` and `17` are optimal for the `DRYLAND_FLAX` and `EMBER_MUSHROOM` respectively (we mainly wanted to double-check the associated bid quantities), so we were able to restrict the brute force algorithm to only simulating trading with these bid prices, which simplified the time complexity of our algorithm:

```python
# In round_1_manual_trading.py

def main():
    # Setup information...

    """ Assume we know the prices we want to buy at """
    dryland_flax_buy_price = 30
    ember_mushroom_buy_price = 17
```

#### We also added the bid and ask order books of both the `DRYLAND_FLAX` and `EMBER_MUSHROOM` as dictionaries which we can use to "insert" our bid quantity to:
```python
# In round_1_manual_trading.py

dryland_flax_bid_order_book = {
    30: 30000,
    29: 5000,
    28: 12000,
    27: 28000
}

dryland_flax_ask_order_book = {
    28: 40000,
    31: 20000,
    32: 20000,
    33: 33000
}

ember_mushroom_bid_order_book = {
    20: 43000,
    19: 17000,
    18: 6000,
    17: 5000,
    16: 10000,
    15: 5000,
    14: 10000,
    13: 7000
}

ember_mushroom_ask_order_book = {
    12: 20000,
    13: 25000,
    14: 35000,
    15: 6000,
    16: 5000,
    17: 0,
    18: 10000,
    19: 12000
}
```

#### Using this, the general process of our `round_1_manual_trading.py` code is generally the following for each of the two products:
1. With our specified bid price, loop through different bid quantities to place into the associated product order book at that bid price
2. Calculate the clearance price of this modified order book
3. Calculate the subsequent quantity of our bid that will be filled (we mainly did this for the `EMBER_MUSHROOM` product)
4. Calculate the resulting profit, which we generally had as `profit = ((buy_back_price - clearance_price) * volume) - (buy_back_fee * filled_volume)`
5. Of the profits we get from the different bid quantities we tested, find the highest profit, and return the associated bid quantity


#### After fixing errors identified by Tyler Thomas, our `round_1_manual_trading.py` yielded the following:

![round_1_manual_trading_code_output](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_manual_trading_code_output.png)

#### ^^ This output confirmed Tyler Thomas's initial answer, so we decided to use these bid prices and quantities as our answer. Intuitively, we also thought that the bid quantities being `9999` and `19999` made sense, in that increasing the quantities to `10000` and `20000` might have resulted in the clearance price becoming one price level higher, which would cause us to lose more profit in total than we would gain from the extra quantity.

#### These are the results of our Round 1 manual trading challenge:

![round_1_manual_trading_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_manual_trading_results_1.png)
![round_1_manual_trading_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_manual_trading_results_2.png)
![round_1_manual_trading_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_manual_trading_results_3.png)
![round_1_manual_trading_results_4](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_manual_trading_results_4.png)

#### ^^ It seems that our total profit from our manual trading is ranked 1st, meaning we were able to provide the optimal bid prices and quantities for the Round 1's manual trading challenge.

### Overall Round Result

![round_1_overall_result](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_1_overall_result.png)

#### ^^ In total, we made around 87,995 XIRENs in Round 1, all of which came from our manual trading performance. This total puts us at around 44% of our goal to reach 200,000 XIRENs by the end of Round 2.

</details>

---
<details>
<summary><h2>Round 2 🌶️</h2></summary>

### Algorithmic Trading
#### As mentioned in [Round 2 of the wiki](https://imc-prosperity.notion.site/Round-2-Growing-Your-Outpost-345e8453a09380b29132fdf4de9174d4), no new tradeable products are added to be traded for the algorithm. Instead, Round 2 provides us with the opportunity to gain access to 25% more trade offers, provided that we place a bid in a `bid()` function that is in the top 50% of other bidders. If our bid is in the top 50% of other bidders, it seems we will then need to pay whatever we bid as a fee to access the full market.

#### We ended up not focusing too much on the bid for the extra trade offers, and instead just returned `2000` in our `bid()` function:

```python
# In round_2.py

class Trader:
    # ...

    def bid(self):
        return 2000
```

#### <b>It is important to note that we received help for our changes in our `INTARIAN_PEPPER_ROOT` and `ASH_COATED_OSMIUM` algorithms.</b>

#### For trading `INTARIAN_PEPPER_ROOT`, the algorithm begins by calculating the expected fair value of the `INTARIAN_PEPPER_ROOT` at this current moment in time. Since the price of `INTARIAN_PEPPER_ROOT` is historically a steady linear time, we can calculate the fair value through a linear equation: y = mx + b. In this case, y = the fair value, m = the slope/drift by which the `INTARIAN_PEPPER_ROOT` is increasing by after each timestamp difference, x = the current timestamp, and b = the initial price of `INTARIAN_PEPPER_ROOT` at the start of the algorithm.

```python
# In round_2.py

# In the Strategy class
    
    # In the trade_intarian_pepper_root() function

        fair_value = intarian_pepper_root.intercept + intarian_pepper_root.drift * state.timestamp
        remaining_buy_capacity = intarian_pepper_root.position_limit - intarian_pepper_root.current_position
```

#### We can now use this `fair_value` as a threshold to buy and sell our `INTARIAN_PEPPER_ROOT`. For one, we can buy `INTARIAN_PEPPER_ROOT` if a sell order has a price that is at most `7` more than the fair value. In such a case, we can buy some `INTARIAN_PEPPER_ROOT` as that sell order's price, and the amount we will buy is the minimum of the sell order's ask amount and our `remaining_buy_capacity`:

```python
# In round_2.py

# In the Strategy class
    
    # In the trade_intarian_pepper_root() function

        # Buy everything as long as the price is <= fair_value + 7
        for ask, ask_amount in sell_orders:
            if remaining_buy_capacity <= 0:
                break

            if ask <= int(fair_value) + 7:
                amount_to_buy = min(ask_amount, remaining_buy_capacity)

                if amount_to_buy > 0:
                    orders.append(Order(product_name, ask, amount_to_buy))
                    remaining_buy_capacity -= amount_to_buy
```

#### We can also sell some `INTARIAN_PEPPER_ROOT` if we notice that the lowest sell order is greater than 1 + the fair value. As mentioned in the Round 1 algorithm, if the price of the `INTARIAN_PEPPER_ROOT` remained stable and continously rose, we could technically buy as much `INTARIAN_PEPPER_ROOT` as we can at the start of the trading window and hold it until the end without needing to sell it. However, as we were worried about potential crashes, we wanted a way to safely sell and buy back `INTARIAN_PEPPER_ROOT` to keep holding `INTARIAN_PEPPER_ROOT` while also securing profit in case of a crash:

```python
# In round_2.py

# In the Strategy class
    
    # In the trade_intarian_pepper_root() function

        # Sell if there is a small dip (lowest_sell_order > fair_value - 1) in case of crashes
        if remaining_buy_capacity > 0:
            sell_threshold = int(fair_value) - 1

            if sell_threshold < lowest_sell_order:
                amount_to_sell = min(remaining_buy_capacity, 40)
                orders.append(Order(product_name, sell_threshold, amount_to_sell))
```

#### The algorithm also has a second condition to sell, if a buy order's price is more than 8 + the fair value. In this case, the current price of the `INTARIAN_PEPPER_ROOT` would be higher than normal (our expected linear pattern and slope/drift of the `INTARIAN_PEPPER_ROOT` price), so we would have the opportunity to make slightly more profit than normal in this timestamp, and we can always buy back `INTARIAN_PEPPER_ROOT` in a later timestamp:

```python
# In round_2.py

# In the Strategy class
    
    # In the trade_intarian_pepper_root() function

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
```

#### For trading `ASH_COATED_OSMIUM`, since (as seen in the Round 1 algorithm) the historical price of the `ASH_COATED_OSMIUM` is a lot more volatile, the algorithm bases its thresholds based on mid prices. The mid price made sense, as the `ASH_COATED_OSMIUM` does have a slight spread between the buy and sell order prices. As a result, the algorithm starts by getting the past 20 mid prices, and uses the average of these 20 prices as the fair value. The algorithm also calculates the mispriced threshold, and the remaining buy and sell capacities to make sure we are not buying or selling more than our current position and the `ASH_COATED_OSMIUM` position limit allows us to:

```python
# In round_2.py

# In the Strategy class
    
    # In the trade_ash_coated_osmium() function

        recent_mid_prices = ash_coated_osmium.mid_order_history[-20:]
        fair_value = mean(recent_mid_prices)
        mispriced_threshold = fair_value + 2.0 * order_book_imbalance

        # ...
        
        remaining_buy_capacity = ash_coated_osmium.position_limit - current_position_duplicate
        remaining_sell_capacity = ash_coated_osmium.position_limit + current_position_duplicate
```

#### The algorithm then tries to buy mispriced prices, which is checked by seeing if the `mispriced_threshold` is greater than or equal to 0.5 + the price of the current sell order:

```python
# In round_2.py

# In the Strategy class
    
    # In the trade_ash_coated_osmium() function

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
```

#### The algorithm also uses a similar condition for selling mispriced prices, and checks if the `mispriced_threshold` is less than or equal to the price of the current buy order - 0.5:

```python
# In round_2.py

# In the Strategy class
    
    # In the trade_ash_coated_osmium() function

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
```

#### We can also do some market making with `ASH_COATED_OSMIUM`, as there is a small spread between the buy and sell orders, with the sell orders generally being slightly higher than that of the buy orders. In this case, the algorithm assumes that the spread is a rigid `2`. The algorithm then calculates the position shift based on the algorithm's current position in `ASH_COATED_OSMIUM` and a rigid position skew. With this, we can then calculate the acceptable buy and sell prices based on the fair value, spread, and the position shift (as an offset). As this is a market making strategy, however, we also need to make sure that the acceptable buy price is lower than the rest of the sell order prices, and that the acceptable sell price is higher than the rest of the buy order prices.

#### We can then use this `acceptable_buy_price` and `acceptable_sell_price` as thresholds for buying and selling `ASH_COATED_OSMIUM`. If the acceptable buy price is less than the fair value, we will buy `ASH_COATED_OSMIUM`, and if the acceptable sell price is greater than the fair value, we will sell `ASH_COATED_OSMIUM`.

```python
# In round_2.py

# In the Strategy class
    
    # In the trade_ash_coated_osmium() function

        """ Market making strategy """
        spread = 2
        position_skew = 0.10

        # Calculate the acceptable buy and sell prices
        position_shift = -current_position_duplicate * position_skew
        acceptable_buy_price = int(fair_value + position_shift - spread)
        acceptable_sell_price = int(fair_value + position_shift + spread) + 1

        if acceptable_buy_price >= lowest_sell_order:
            acceptable_buy_price = lowest_sell_order - 1
        
        if acceptable_sell_price <= highest_buy_order:
            acceptable_sell_price = highest_buy_order + 1

        # Calculate how much to buy or sell
        buy_factor = max(0.0, remaining_buy_capacity / ash_coated_osmium.position_limit)
        sell_factor = max(0.0, remaining_sell_capacity / ash_coated_osmium.position_limit)

        buy_size = int(30 * buy_factor)
        sell_size = int(30 * sell_factor)

        # Conditions to buy or sell
        if buy_size > 0 and remaining_buy_capacity > 0 and acceptable_buy_price < fair_value:
            orders.append(Order(product_name, acceptable_buy_price, min(buy_size, remaining_buy_capacity)))
        
        if sell_size > 0 and remaining_sell_capacity > 0 and acceptable_sell_price > fair_value:
            orders.append(Order(product_name, acceptable_sell_price, -min(sell_size, remaining_sell_capacity)))
```

#### The algorithm also has secondary buying and selling prices which is more selective than the `acceptable_buy_price` and `acceptable_sell_price`. The secondary buy price is 3 less than the `acceptable_buy_price`, and the secondary sell price is 3 more than the `acceptable_sell_price`. We then try to place a buy order at the secondary buying price if we still have some buying capacity and `buy_factor > 0`, and we try to place a sell order at the secondary selling price if we still have some selling capacity and `sell_factor > 0`:

```python
# In round_2.py

# In the Strategy class
    
    # In the trade_ash_coated_osmium() function

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
```

#### In addition, in the `Trader` class itself, we also made a small change to initialize our `New_Data` object in a separate `__init__(self)` constructor function, as we learned that, in the submission, the `Trader` class itself might only be initialized once, rather that it's the `run()` function that is being called multiple times across the timestamps. As a result, we can set attributes and our `New_Data` object in the constructor without worrying that such data will not exist in subsequent timestamps. Which this might not affect our profits too much, this change may result in better code quality and a performance imrpvoement to an extent, as we wouldn't be constantly creating and deleting `New_Data` objects.

```python
# In round_2.py

# In the Trader class

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
```

#### These are the results of our Round 2 algorithm:

![round_2_algorithm_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_algorithm_results_1.png)
![round_2_algorithm_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_algorithm_results_2.png)

#### ^^ It is very clear that the algorithm we submitted for this round worked really well.

### Manual Trading
#### As mentioned in [Round 2 of the wiki](https://imc-prosperity.notion.site/Round-2-Growing-Your-Outpost-345e8453a09380b29132fdf4de9174d4), the manual trading challenge for Round 2 gives us a budget of `50000` to invest in three areas: Research, Scale, and Speed. Each area has its own mechanic for gaining profit.

#### Research determines the strength of our trading edge. The profit formula for this area is a logarithmic function: `research(x) = 200_000 * np.log(1 + x) / np.log(1 + 100)`. It is worth noting that `np.log` is the `log` function from the Python NumPy package.

#### Scale determines our broadly we deploy our strategy. The profit from this area is more of a multiplier that is used to multiply the current Profit and Loss (PnL). The scale multiplier we can get ranges from `0` to `7`, and grows linearly based on our allocation percentage. While not stated in the wiki, we used the following formula to calculate the scale multiplier we would receive based on our allocation: `scale(x) = x * (7 / 100)`.

#### Speed determines how often we win our trades. The profit from this area is also more of a multiplier that is multiplied onto the current PnL. Unlike the Research and Scale areas, however, the Speed area always results in the loss of PnL, as the range of the Speed multiplier is from `0.1` to `0.9`. In addition, the way the Speed multiplier is calculated depends on both our allocation and the allocations of other teams. The Speed multiplier is ranked based, meaning that the team with the highest speed allocation will get `0.9`, the team with the lowest speed allocation will get `0.1`, and the Speed multiplier will be spread linearly among the rest of the teams (if multiple teams have the same Speed allocation, the multiple teams will receive the same Speed multiplier).

#### Altogether, the total PnL we will get from our investment is `(Research * Scale * Speed) - Budget_Used`. Our goal is to determine what percentage of our `50000` budget to allocate to each area, and maximize our profit.

#### Our work for the Round 2 Manual Trading round can be found in our [round_2_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/round_2/round_2_manual_trading.py). Going into this round, we thought that figuring out an optimal combination of Research and Scale was doable; we can use mathematical equations and derivatives to maximize the gains of Research and Scale, while accounting for the diminishing gains from the logarithmically growing Research, or code a brute force algorithm to confirm the optimal combination of allocations by testing all combinations possible. However, we realized that the main "mystery" in this round involves the Speed allocation, as this is the only area that depends on the choices of other teams.

#### Tyler Thomas mentioned that, technically, a fully optimal Speed allocation would be 0 or 1, provided that every team in the competition chose the same Speed allocation. Given that we kind of assumed that this possibility would be very unlikely, our initial guess was a Speed allocation of 2, as it would be just above the perceived nash equilibrium of Speed = 0 or 1 (in reality, I don't know if, if every team picked the same Speed allocation, every team would have been awarded a Speed multiplier of `0.9` or `0.1`). As we continued to discuss how other teams would allocate their Speed, we developed some scenarios in [round_2_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/round_2/round_2_manual_trading.py) on how the Speed allocations would be distributed, and, using this distribution, used a brute force algorithm to find the optimal combination of Research, Scale, and Speed that would reward the highest PnL.

#### The first scenario we tried for the Speed allocations is a linear distribution from `0.1` to `0.9`. This means that, in this scenario, the teams are evenly distributed across all possible Speed allocations. This scenario gave the following result:

![round_2_manual_trading_code_output_linear_speed](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_code_output_linear_speed.png)

#### ^^ The optimal Speed allocation in this scenario, `35` is noticeably larger than our initial guess of `2`, which is understandable, as this assumes that every team would be evenly distributed on all potential Speed allocations (low, middle, and high), which could be unlikely.

#### The second scenario we tried is a "less steep" exponential curve, which would mean that teams are generally picking higher Speed allocations than otherwise, meaning we would need a higher Speed allocation to secure a good Speed multiplier. This scenario gave the following result:

![round_2_manual_trading_code_output_exponential_less_steep_speed](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_code_output_exponential_less_steep_speed.png)

#### ^^ The optimal Speed allocation in this scenario is `32`, which is surpsingly lower than the optimal Speed allocation from the linear Speed distribution. Right now, we think that this might either be because of the specific equation that we used for this secnario, or maybe because the exponential distribution means that the Speed multiplier will not change as much in lower Speed allocations (we might be wrong on this).

#### The third scenario we tried is a "more steep" exponential curve, which would mean that even more teams in general would pick higher Speed allocations, which would hence incentivize an even higher Speed allocation to maintain a good Speed multiplier. This scenario gave the following result:

![round_2_manual_trading_code_output_exponential_more_steep_speed](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_code_output_exponential_more_steep_speed.png)

#### ^^ As expected, this optimal Speed allocation of `39` is higher than the optimal Speed allocation of `32` from the "less steep" exponential curve.

#### The fourth scenario we tried is a quaratic curve, which would mean that teams would generally pick lower Speed allocations, meaning that, as we increase our Speed allocation, we would immediately start surpassing the Speed allocations of many teams, however the number of teams we surpass as we increase our Speed allocation would diminish. We thought that this distribution might be a little more reasonable, given that we thought that it is likely that teams will generally pick lower Speed allocations. This scenario gave the following result:

![round_2_manual_trading_code_output_quadratic_speed](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_code_output_quadratic_speed.png)

#### ^^ The optimal Speed allocation for this scenario is `33`, which is similar to the linear Speed distribution scenario. This was a little surprising, as I initially thought that the optimal Speed allocation for this scenario would have been lower than the linear Speed scenario, however I think that a possible reason might be that the main change in this scenario from the linear Speed scenario is more so the optimal Speed multiplier we can achieve (meaning that, using this quadratic curve, we could allocate the same amount of percentage for Speed, and achieve a higher Speed multiplier by default from the graph).

#### The fifth scenario we tried involves manually creating a list of Speed allocations that will be picked. The idea of this scenario is that, at some point during our discussion, we also considered the possibility that another way to view the Speed allocations from the other team is simply what Speed allocations will at least one team pick. In other words, this view asks "what Speed allocation numbers will be picked?", instead of "how many teams will pick a particular Speed allocation number?". In this scenario, we assumed that the Speed allocations of 0-11, 19-21, 24-26, 29-41, 49-52, 55, 60-61, and 89-100 will be picked by at least one team. With this list, as we loop through potential Speed allocations in our brute force algorithm, we can insert our Speed allocation into this list, and calculate our Speed multiplier we would subsequently receive. This scenario gave the following result:

![round_2_manual_trading_code_output_tylers_version_1_speed](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_code_output_tylers_version_1_speed.png)

#### ^^ The optimal Speed allocation for this scenario is `41`, which is currently our highest optimal Speed allocation scenario.

#### The sixth scenario we tried is similar to the fifth scenario, in which we created a list of Speed allocations that will be picked. The difference in this scenario is we just assumed that all Speed allocations (0-100) will be picked. The idea of this is that, if only one team is required to pick a certain Speed allocation for that Speed allocation to be accounted for in the Speed multiplier calculations, with a large enough number of competing teams, it might make sense to think that it's possible for all Speed allocations to be picked at least once. This scecnario gave the following result:

![round_2_manual_trading_code_output_tylers_version_2_speed](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_code_output_tylers_version_2_speed.png)

#### ^^ The optimal Speed allocation for this scenario is `35`, which is interestingly the same as the linear Speed distribution scenario, which probably makes sense, as the premises of the two scenarios do seem similar.

#### Overall, what we found notable in these results is that the optimal Speed allocation was around the 30-41 range, which is more than our initial guess of `2`. After some discussion, we eventually agreed that our hesitancy for picking Speed allocations as high as 30-42 was because we weren't sure if such a Speed allocation was optimal; if such a Speed allocation was too high, a lower Speed allocation would have allowed us to gain more profit from investing in more Research and Scale. On the other hand, a higher Speed allocation would be much safer, meaning we would not need to worry as much about picking a Speed allocation that is too low, as we both agreed that a Speed allocation of 30-41 is likely to be around or above the majority of allocation picks from other teams.

#### After more discussion, we agreed that, given our time and current expertise, it is unlikely that doing more research would provide us with the optimal answer, at least one that we would be confident in. Despite this, our main priority during this time is to meet the 200,000 XIRENs threshold in order to advance past Round 2. After Round 1, we needed to make at least 112,005 XIRENs in Round 2 in order to meet this threshold.

#### This consideration of meeting the 200,000 XIREN threshold was where the suggestion of picking a higher Speed allocation began to make more sense. Particularly, we felt quite comfortable with the optimal Speed allocation from the fifth scenario: `41`. In the fifth scenario, the optimal Speed allocation of `41`, along with the associated optimal Research and Scale allocations, gave an optimal profit of around `148912` XIRENs, which, if true, would be more than enough for us to meet the 200,000 XIREN requirement. In addition, we found comfort in our assumption that a Speed allocation of `41` would be quite high, high enough that it is potentially likely for it to surpass the allocations of the majority of other teams, and give us an even higher Speed multiplier, and hence PnL, than the code output. As a result, while we didn't think that a Speed allocation of `41` was optimal, we thought that the allocation was a comfortable choice that could safely guarantee enough profit to advance past Round 2.

#### After we made our submission, Tyler Thomas decided to change our Speed allocation to `42`, after seeing some teams communicate their preference for the Speed allocation of `41` in the IMC Prosperity Discord server. As a result, our final submission for this manual trading round is the following:

![round_2_manual_trading_submission](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_submission.png)

#### These are the results of our Round 2 manual trading challenge:

![round_2_manual_trading_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_results_1.png)
![round_2_manual_trading_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_results_2.png)

#### We were pleasantly surprised to find that our allocations were actually optimal! Our manual trading result of `217869` XIRENs is also nearly 80,000 XIRENs above the fifth scenario's estimated profit, which meant that it does seem that our Speed allocation of `42` was more than the majority of other Speed allocations, and ended up giving us a higher than expected Speed multiplier. The IMC game website also provided the following insights regarding the submitted Speed allocation distribution:

![round_2_manual_trading_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_manual_trading_results_3.png)

#### ^^ It seems that we currently assumed that teams would generally pick lower Speed allocations, however it seems that we were also correct to consider that the main factor in the Speed multiplier is the Speed allocations that at least one team picked at all, rather than the number of teams that picked a certain Speed allocation.

### Overall Round Result

![round_2_overall_result](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_2_overall_result.png)

#### ^^ In total, we made around 301,972 XIRENs in Round 2, with a good amount of which coming from our manual trading performance. This thankfully allowed us to reach our goal of at least 200,000 XIRENs by the end of Round 2!

</details>

---
<details>
<summary><h2>Round 3 🥭</h2></summary>

### Algorithmic Trading
#### As mentioned in [Round 3 of the wiki](https://imc-prosperity.notion.site/Round-3-Gloves-Off-34ce8453a0938072a58cc7de372ff551), Round 3 removed all of the previous tradable products from rounds 1 and 2, and introduced us to 12 new tradeable products. The first two products are `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`, both of which are said to be "delta 1" products that behave similarly to previous products in rounds 1 and 2. The other ten products, however, are option vouchers that are involved with the `VELVETFRUIT_EXTRACT` product: `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`, `VEV_5400`, `VEV_5500`, `VEV_6000`, and `VEV_6500`. Each voucher has a respective strike price that is indicated in their names and a 7-day expiration deadline starting from round 1 (each round represents 1 day).

#### The position limit for `HYDROGEL_PACK` is `200`, the position limit for `VELVETFRUIT_EXTRACT` is `200`, and the position limit for each of the ten vouchers is `300` each.

#### Using the provided Data Capsule that allowed us to view historical prices of `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and the ten vouchers. Using the historical prices, we constructed the following price graphs of the products:

#### Hydrogel Packs:
![hydrogel_packs_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/hydrogel_packs_historical_prices_day_0.png)

#### Velvetfruit Extract:
![velvetfruit_extract_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/velvetfruit_extract_historical_prices_day_0.png)

#### VEV_4000:
![vev_4000_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_4000_historical_prices_day_0.png)

#### VEV_4500:
![vev_4500_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_4500_historical_prices_day_0.png)

#### VEV_5000:
![vev_5000_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_5000_historical_prices_day_0.png)

#### VEV_5100:
![vev_5100_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_5100_historical_prices_day_0.png)

#### VEV_5200:
![vev_5200_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_5200_historical_prices_day_0.png)

#### VEV_5300:
![vev_5300_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_5300_historical_prices_day_0.png)

#### VEV_5400:
![vev_5400_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_5400_historical_prices_day_0.png)

#### VEV_5500:
![vev_5500_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_5500_historical_prices_day_0.png)

#### VEV_6000:
![vev_6000_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_6000_historical_prices_day_0.png)

#### VEV_6500:
![vev_6500_historical_prices_day_0](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/vev_6500_historical_prices_day_0.png)

#### Due to time constraints, we ended up trying to only trade the `HYDROGEL_PACK`. We began with the general strategy we used for the `ASH_COATED_OSMIUM` in Round 2, and tried different variations and thresholds of the strategy in our test submissions to see if a particular variation worked for the `HYDROGEL_PACK`. Our thought process for this is that the historical price graph for the `HYDROGEL_PACK` did seem similar to the `ASH_COATED_OSMIUM` in that they both do seem to be "delta-1" products.

#### For `HYDROGEL_PACK`, the strategy we ended up submitting in our [round_3.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/round_3/round_3.py) involved EMA (which in hindsight doesn't seem to be the most robust, especially as it was used solely and without previous metrics like the historical mid prices). Essentially, we would calculate the current EMA for the `HYDROGEL_PACK` product, and use it in our market-making thresholds to buy and sell:

```python
# In round_3.py

# In the Strategy class
    
    # In the trade_hydrogel_pack() function

        # ...
        
        current_position_duplicate = hydrogel_pack.current_position

        # ...

        ema = hydrogel_pack.calculate_EMA(highest_buy_order, lowest_sell_order)
        spread = abs(lowest_sell_order - highest_buy_order)
        position_skew = 0.15

        position_shift = -current_position_duplicate * position_skew

        acceptable_buy_price = int(ema + position_shift - (spread / 2))
        acceptable_sell_price = int(ema + position_shift + (spread / 2)) + 1

        # Emphasize the market-making strategy by making our buy and sell orders more favorable than the rest of the buy and sell orders
        if acceptable_buy_price >= lowest_sell_order:
            acceptable_buy_price = lowest_sell_order - 1
        
        if acceptable_sell_price <= highest_buy_order:
            acceptable_sell_price = highest_buy_order + 1
```

#### We also added a small check to only do market-making with the `HYDROGEL_PACK` if the current price is not in a downward trend. Otherwise, we will sell a little bit of our `HYDROGEL_PACK` inventory to ideally add a bit more safety and confirmation in our algorithm in case of a crash or downward trend that does not resolve to what the prices previously were:

```python
# In round_3.py

# In the Strategy class
    
    # In the trade_hydrogel_pack() function

        # ...
        
        current_position_duplicate = hydrogel_pack.current_position

        # ...

        # If we're not in a downward trend
        if hydrogel_pack.mid_order_history[-2] <= hydrogel_pack.mid_order_history[-1] and hydrogel_pack.mid_order_history[-3] <= hydrogel_pack.mid_order_history[-1]:
            orders.append(Order(product_name, highest_buy_order + 1, min(buy_size, remaining_buy_capacity)))
            orders.append(Order(product_name, lowest_sell_order - 1, -min(buy_size, remaining_buy_capacity)))
        
        else:
            # Sell some to be safe so we're not holding things too much
            orders.append(Order(product_name, lowest_sell_order - 3, -5))
```

#### These are the results of our Round 3 algorithm:

![round_3_algorithm_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_algorithm_results_1.png)
![round_3_algorithm_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_algorithm_results_2.png)

#### ^^ Given the complexity of the `HYDROGEL_PACK` product, we were definitely happy to have gained profit at all. However, it is curious to note that we had a PnL of around 22,000 at one point, however we ended up losing a lot of this PnL towards the end of the trading window. As a result, in the future, finding ways to confirm PnL and overall make a safer approach to our algorithm could benefit our profit even more. It is unclear if our downward trend check was fully useful in this case (it might have been, however we currently are unsure) 

### Manual Trading
#### As mentioned in [Round 3 of the wiki](https://imc-prosperity.notion.site/Round-3-Gloves-Off-34ce8453a0938072a58cc7de372ff551), the manual trading challenge for Round 3 presents us with an opportunity to trade with a number of counterparties, each of whom have a reserve price ranging between `670` and `920` XIRENs. Our goal is to offer 2 bids for the counterparties that are at the best price for them to accept; we think that it is not required to place 2 bids, however it is encouraged to place 2 bids. For these bids, each of the counterparties will accept the lowest bid that is over their reserve price. For our second bid, in addition to the reserve price requirement, the counterparties will trade if our bid is higher than the average of all second bids from all participants; if our second bid is lower than the average of all second bids from all participants, then the probability of our second bid trading will be decreased. After these trades are made, we are able to sell the product we are trading for `920` XIRENs each.

#### Our work for this round's manual trading challenge can be found in our [round_3_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/round_3/round_3_manual_trading.py). Generally, our process for calculating potential optimal first and second bid pairs involves what we assume the second bid average from all participants would be (which we will discuss later). For now, assuming that we have provided an assumed second bid average, `avg_b2`:

1. We start by looping through all potential first bid options (as the bid options range from `670` to `920`).
2. For each first bid option, we see how many counterparties would trade with the first bid, and add their trades to our current profit.
3. The remaining counterparties that did not trade with the first bid could potentially trade with out second bid, so we loop through all potential second bid options (assuming that the second bid needs to be higher than the first bid).
4. We then find the counterparties that would be willing to trade with the second bid, taking into account their reserve prices and our assumed `avg_b2`, add their trades to a separate running profit for the second bids, and find the optimal second bid to associate alongside the first bid.
5. Using this, we can find the optimal pair of a first and second bid that will yield the highest profit.

#### Our process is essentially a brute force algorithm, however, as mentioned before, the main assumption we need to have for the algorithm is the second bid average of all participants. Similar to the Manual Challenge in Round 2, this second bid average is a complex and consequential aspect of trying to find the optimal bids for this round. As a result, we decided to create five potential scenarios on how the rest of the teams will choose their second bid.

#### The first scenario involves a relatively even distribution of second bid picks, with the picks mostly being above 800. The main idea with this distribution was to provide a baseline of what a potentially optimal second bid would look like.

```python
# In round_3_manual_trading.py

def second_bid_scenario_1():
    """
    Current assumptions on the player b2 (second bid) distribution:
         5% pick 791
        10% pick 820
        10% pick 830
        10% pick 840
        15% pick 850
        10% pick 860
        10% pick 870
        10% pick 880
         8% pick 890
         7% pick 900
         5% pick 920
    """
```

#### Using this distribution, the code outputted the following optimal pair of first and second bids:

![round_3_manual_trading_code_output_scenario_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_manual_trading_code_output_scenario_1.png)

#### The second scenario is more narrow than the first scenario, and had a distribution of second bids that was more concentrated between 840 and 920. The main idea with this distribution, and a few other subsequent scenarios, is that Tyler Thomas rightfully mentioned that it is likely that teams might choose higher second bids this round as opposed to what we were expecting in Round 2. This will be discussed later.

```python
# In round_3_manual_trading.py

def second_bid_scenario_2():
    """
    Current assumptions on the player b2 (second bid) distribution:
         3% pick 791
         5% pick 840
        15% pick 850
        15% pick 860
        15% pick 870
        17% pick 880
        18% pick 890
         7% pick 900
         5% pick 920
    """
```

#### Using this distribution, the code outputted the following optimal pair of first and second bids:

![round_3_manual_trading_code_output_scenario_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_manual_trading_code_output_scenario_2.png)

#### The third scenario is even more narrow than the second scenario, and had a distribution of second bids that was more concentrated between 850 and 900:

```python
# In round_3_manual_trading.py

def second_bid_scenario_3():
    """
    Current assumptions on the player b2 (second bid) distribution:
         1% pick 791
        15% pick 850
        16% pick 860
        17% pick 870
        19% pick 880
        19% pick 890
        12% pick 900
         1% pick 920
    """
```

#### Using this distribution, the code outputted the following optimal pair of first and second bids:

![round_3_manual_trading_code_output_scenario_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_manual_trading_code_output_scenario_3.png)

#### The fourth scenario is similar to the third scenario, with the main change being that the distribution of second bids that was more concentrated around 860 and 900:

```python
# In round_3_manual_trading.py

def second_bid_scenario_4():
    """
    Current assumptions on the player b2 (second bid) distribution:
         1% pick 820
         5% pick 850
        16% pick 860
        19% pick 870
        22% pick 880
        22% pick 890
        14% pick 900
         1% pick 910
    """
```

#### Using this distribution, the code outputted the following optimal pair of first and second bids:

![round_3_manual_trading_code_output_scenario_4](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_manual_trading_code_output_scenario_4.png)

#### The fifth scenario goes the other way and tries to be more broad than the first scenario, increasing the concentration of second bids to between 761 and 920:

```python
# In round_3_manual_trading.py

def second_bid_scenario_5():
    """
    Current assumptions on the player b2 (second bid) distribution:
         5% pick 761
         5% pick 781
         5% pick 820
        10% pick 830
        10% pick 840
        15% pick 850
        10% pick 860
        10% pick 870
        10% pick 880
         8% pick 890
         7% pick 900
         5% pick 920
    """
```

#### Using this distribution, the code outputted the following optimal pair of first and second bids:

![round_3_manual_trading_code_output_scenario_5](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_manual_trading_code_output_scenario_5.png)

#### From these scenarios, the code's optimal second bids were `857`, `872`, `876`, `878`, and `856` respectively. Generally, this does indicate that, assuming the accuracy and reliability of the code, a potentialy optimal second bid could be somewhere between 855 to 880, maybe around `860` or `870`. After some discussion, however, we decided to choose a higher second bid of `902`, for the reason mentioned earlier by Tyler Thomas. We knew that, when the results for the Manual Challenge of Round 2 were released, many teams ended up picking lower Speed allocations, and the general distribution of Speed allocations (or at least the allocations that were picked) were relatively similar to what we expected in our [round_2_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/round_2/round_2_manual_trading.py) code. However, it is also worth considering the possibility that many teams would have chosen to adapt as a result of this information, and would hence pick a higher second bid in this round to adjust from Round 2. This would shift the distribution of second bids up, and might end up causing our chosen second bid scenarios to be inaccurate. Another reason that potentially supported this change was that a similar change happened in last year's Prosperity 3 competition, in which many teams picked higher-numbed crates in the Round 2 Manual Challenge, and then proceeded to pick lower-numbered crates in the Round 4 Manual Challenge (I think). In addition, while we knew that the optimal second bid needs to be just above the average of the second bids of all participants, we also acknowledged that it is probably better to be way above the second bid average than being under it, as being under the average might mean our second bid will not trade at all, while we might still be able to gain some profit (albiet not the optimal amount of profit) from a second bid that is higher than the average.

#### As a result, we decided to enter `902` as our second bid, and we were then able to reconfigure our brute force algorithm to find the optimal first bid to pair with a second bid of `902`. At some point, the night before the end of Round 3, we did end up deciding to lower our second bid to around `895`, however we both ended up forgetting to make the actual change on the IMC website, so our submission remained as follows:

![round_3_manual_trading_submission](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_3_manual_trading_submission.png)

#### These are the results of our Round 3 manual trading challenge:

![round_3_manual_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_manual_results_1.png)
![round_3_manual_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_manual_results_2.png)
![round_3_manual_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_manual_results_3.png)

#### ^^ Overall, we did pretty well in the Round 3 Manual Challenge. However, as the average second bid ended up actually being `859`, it was very clear that we had overestimated the increase in magnitude other teams would place in their second bids. In hindsight, our code scenarios did seem to have more "optimal" answers (although we're not sure if the second bids of `856` and `857` from Scenarios 1 and 5 would have been better, as they were under the actual second bid average), which we found very interesting. Perhaps some of the scenarios like Scenarios 2, 3, and 4 did end up taking into account concerns of higher second bids from other teams enough such that it was reliable enough to follow. Either way, we found our second bid of `902` to be reasonable in the moment, and we plan to reflect on how we can improve our predictions in future scenarios.

### Overall Round Result

![round_3_overall_result](https://github.com/Nicholas-Lucky/IMC-Prosperity-4-Submission/blob/main/readme_embeds/round_3_overall_result.png)

#### ^^ In total, we made around 76,536 XIRENs in Round 3, with a good amount of which coming from our manual trading performance.
</details>

---
<details>
<summary><h2>Round 4 🍪</h2></summary>

### Algorithmic Trading
#### As mentioned in [Round 4 of the wiki](https://imc-prosperity.notion.site/Round-4-19ee8453a0938112aa5fd7f0d060ffe6), Round 4 introduced us to the `MAGNIFICENT_MACARONS`, a tradable product whose value is dependent on multiple factors such as `transportFees`, `exportTariff`, `importTariff`, `sugarPrice`, and `sunlightIndex` — at least we assumed that these are factors that can influence the value of `MAGNIFICENT_MACARONS`. The wiki provided us with a hint that, if `sunlightIndex` went and remained below a threshold called the CriticalSunlightIndex (CSI), then `sugarPrice` and `MAGNIFICENT_MACARONS` prices would increase; otherwise, `sugarPrice` and `MAGNIFICENT_MACARONS` prices would maintain their respective fair values.

#### It is worth noting that it seems that `MAGNIFICENT_MACARONS` is the only newly-introduced tradable product this round; `transportFees`, `exportTariff`, `importTariff`, `sugarPrice`, and `sunlightIndex` are not tradable. In addition, we found that information regarding the `transportFees`, `exportTariff`, `importTariff`, `sugarPrice`, and `sunlightIndex` for a specific iteration was found in `state.observations.conversionObservations`; it seems that `state.observations.conversionObservations` contains the conversion observations for all products, including the `MAGNIFICENT_MACARONS`, so we would need to access the item in `state.observations.conversionObservations` with `"MAGNIFICENT_MACARONS"` as the key. Finally, it seems that it is possible to perform conversions with the `MAGNIFICENT_MACARONS`, with `MAGNIFICENT_MACARONS` having a conversion limit of `10`. Due to inexperience and time constraints, we decided not to attempt to interact with conversions for `MAGNIFICENT_MACARONS`.

#### `MAGNIFICENT_MACARONS` has a position limit of `75`.

#### At the end of Round 3 and the start of Round 4, we decided to refactor our code to make our `Trader` class easier to read and implement. We created a `Product` class to house the relevant information for each of our tradable products. We hope that this form of abstraction would allow for our `Trader` class to be more understandable and concise, especially if we needed to scroll through the class for a specific code snippet.

```python
# In round_4_experimental.py

class Product:
    def __init__(self, name, sell_order_history, buy_order_history, current_position):
        # Name
        self.name = name

        # Sell order history
        self.sell_order_history = sell_order_history
        self.sell_order_average = get_average(self.sell_order_history)

        # Buy order history
        self.buy_order_history = buy_order_history
        self.buy_order_average = get_average(self.buy_order_history)

        # Mid Price
        self.average_mid_price = (self.sell_order_average + self.sell_order_average) / 2

        # Position information
        self.position = current_position
        self.position_limit = get_position_limits()[name]

        # Default buy and sell thresholds
        self.default_offset = self.calculate_offset(10, 3)
        self.current_offset = self.default_offset
        self.acceptable_buy_price = self.average_mid_price - self.default_offset
        self.acceptable_sell_price = self.average_mid_price + self.default_offset

    # Other functionality and methods for the Product class...
```

#### We also created a `Macaron` child class that inherits the general setup of the `Product` class and houses additional information and calculations specific to the `MAGNIFICENT_MACARONS` product. In hindsight, it does seem that we ended up not using any of the `Product` class functionality in the `Macaron` child class, so it may have been optional for the `Macaron` class to be a child class.

```python
# In round_4_experimental.py

class Macaron(Product):
    def __init__(self, name, sell_order_history, buy_order_history, current_position, observation_info_history, current_observation_info):
        #super().__init__(name, sell_order_history, buy_order_history, current_position)  # Commented out

        # Add the initializer logic...
```

#### To further support the abstraction of our products' information in the `Trader` class, we created a function called `initialize_product_information()` to return a dictionary that houses the product names as keys and a respective `Product` or `Macaron` (for `MAGNIFICENT_MACARONS`) class as values. We were also able to use `initialize_product_information()` to set the buy and sell thresholds for `PICNIC_BASKET1` and `PICNIC_BASKET2` based on our previous calculations with the products contained in these baskets, and manually set offsets for the thresholds.

```python
# In round_4_experimental.py

def initialize_product_information(products, sell_order_history, buy_order_history, current_positions, observation_info_history, current_observation_info):
    product_info = {}
    for product in products:
        if product == "MAGNIFICENT_MACARONS":
            product_info["MAGNIFICENT_MACARONS"] = Macaron(product, sell_order_history[product], buy_order_history[product], current_positions[product], observation_info_history, current_observation_info)
            continue
        product_info[product] = Product(product, sell_order_history[product], buy_order_history[product], current_positions[product])
    
    # Set picnic basket buy and sell thresholds
    # ...

    # Manual offset adjustments
    # ...

    # Return the products' information
    return product_info
```

#### For calculating the buy and sell thresholds for the `MAGNIFICENT_MACARONS` in particular, we began by keeping track of both the product's `sell_order_history` and `buy_order_history`, which we used to calculate the averages of the histories, and these average of the 2 averages, which we called the `historical_average_mid_price`. From there, we also kept track of the possible factors influencing the value of `MAGNIFICENT_MACARONS` (`transportFees`, `exportTariff`, `importTariff`, `sugarPrice`, and `sunlightIndex`) through `state.observations.conversionObservations`. From this, we were able to build an `observation_info_history`, similar to how we built `sell_order_history` and `buy_order_history`, to compare with the current values of the factors during an iteration.

```python
# In round_4_experimental.py
# In the Trader class

macaron_state = state.observations.conversionObservations["MAGNIFICENT_MACARONS"]

# Initialize product information
products = initialize_product_information(PRODUCT_NAMES, sell_order_history, buy_order_history, current_positions, previous_macaron_information, macaron_state)

previous_macaron_information["askPrice"].append(macaron_state.askPrice)
previous_macaron_information["bidPrice"].append(macaron_state.bidPrice)
previous_macaron_information["exportTariff"].append(macaron_state.exportTariff)
previous_macaron_information["importTariff"].append(macaron_state.importTariff)
previous_macaron_information["sugarPrice"].append(macaron_state.sugarPrice)
previous_macaron_information["sunlightIndex"].append(macaron_state.sunlightIndex)
previous_macaron_information["transportFees"].append(macaron_state.transportFees)
```

#### Given the historical values of `transportFees`, `exportTariff`, `importTariff`, `sugarPrice`, and `sunlightIndex`, we calculated the values' mean and standard deviations. We then used the current values (of a current iteration) of `transportFees`, `exportTariff`, `importTariff`, `sugarPrice`, and `sunlightIndex` to calculate the normalized values of these current values using the following formula:

#### $x_{normalized}=\frac{x-\text{Mean}}{\text{Standard Deviation}}$

```python
# In round_4_experimental.py
# In the Macaron class

self.export_tariff = current_observation_info.exportTariff
self.import_tariff = current_observation_info.importTariff
self.sugar_price = current_observation_info.sugarPrice
self.sunlight = current_observation_info.sunlightIndex
self.transport_fees = current_observation_info.transportFees

# ...

self.normalized_export_tariff = 0
if self.historical_export_tariff_std != 0:
    self.normalized_export_tariff = (self.export_tariff - self.historical_export_tariff_mean) / self.historical_export_tariff_std

# ^^ similar normalization calculations done for the rest of the factors
```

#### We then took a weighted sum of these normalized values, which we used as both our buy and sell thresholds for `MAGNIFICENT_MACARONS`.

```python
# In round_4_experimental.py
# In the Macaron class

self.MVI_multiplier = (self.normalized_export_tariff * self.export_tariff_weight) + \
                      (self.normalized_import_tariff * self.import_tariff_weight) + \
                      (self.normalized_sugar_price * self.sugar_price_weight) + \
                      (self.normalized_sunlight * self.sunlight_weight) + \
                      (self.normalized_transport_fees * self.transport_fees_weight)

self.hybrid_average_mid_price = (0.3 * self.historical_average_mid_price) + (0.7 * self.current_average_mid_price)
self.acceptable_buy_price = self.hybrid_average_mid_price * self.MVI_multiplier
self.acceptable_sell_price = self.acceptable_buy_price
```

#### The weights for the factors are as follows:

```python
# In round_4_experimental.py
# In the Macaron class

self.export_tariff_weight = 0.1
self.import_tariff_weight = 0.1
self.sugar_price_weight = 0.1
self.sunlight_weight = -0.4
self.transport_fees_weight = 0.1
```

#### ^^ These weights are currently hardcoded, and were chosen so that `sunlightIndex` would have a greater impact on the value of `MAGNIFICENT_MACARONS` than the rest of the factors, given the hint provided by the competition; `self.sunlight_weight` was set to `-0.4` instead of `0.4` because, if the hint is accurate, a low enough `sunlightIndex` could cause higher `MAGNIFICENT_MACARONS` prices — implying a negative relationship between `sunlightIndex` and `MAGNIFICENT_MACARONS`.

#### Regarding our past products, we found through [round_4_resin_only.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/round_4/round_4_resin_only.py) that using both a `sell_order_history` and `buy_order_history` to calculate the buy and sell thresholds allowed us to achieve noticeably more profits from `RAINFOREST_RESIN` than with just `sell_order_history`. As a result, we decided to add this change to all the past products. We would track previous buy orders in `buy_order_history`, similarly to how we tracked previous sell orders in `sell_order_history`. In calculating the buy and sell thresholds of a product, we would then take the averages of `sell_order_history` and `buy_order_history`, and find the average of these two averages.

```python
# In round_4_resin_only.py

class Product:
    def __init__(self, name, sell_order_history, buy_order_history, current_position):
        # ...
        
        self.acceptable_buy_price = (self.sell_order_average + self.buy_order_average) / 2 - self.default_offset
        self.acceptable_sell_price = (self.sell_order_average + self.buy_order_average) / 2 + self.default_offset

# ...

def initialize_product_information(products, sell_order_history, buy_order_history, current_positions):
    # ...
    
    product_info["RAINFOREST_RESIN"].set_buy_price_offset(0)
    product_info["RAINFOREST_RESIN"].set_sell_price_offset(0)

# ...

# In the Trader class
best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
update_buy_order_history(buy_order_history, product, best_bid)

# ...

newData = []
newData.append(sell_order_history)
newData.append(buy_order_history)  # buy_order_history is included in traderData
newData.append(current_positions)

# String value holding Trader state data required. 
# It will be delivered as TradingState.traderData on next execution.
traderData = str(newData)
```

#### These are the results of our Round 4 algorithm:

![round_4_algorithm_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_algorithm_results_1.gif)
![round_4_algorithm_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_algorithm_results_2.jpg)

#### This was a very unexpected result on our end. Looking at the submission logs, we found the following warning:

![round_4_algorithm_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_algorithm_results_3.jpg)

#### We assumed that this warning was the main issue preventing our code from running in the final submission. Hence, we made an effort to fix this error in the next round. We were not aware, however, of another error that took place in our submission, which occurred later in the submission logs:

![round_4_algorithm_results_4](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_algorithm_results_4.jpg)

### Manual Trading
#### As mentioned in [Round 4 of the wiki](https://imc-prosperity.notion.site/Round-4-19ee8453a0938112aa5fd7f0d060ffe6), the manual trading challenge for Round 4 was a game of "Seal or No Seal", which was similar to the manual trading challenge for Round 2. In the challenge, a grid of suitcases was presented, with each suitcase containing a base amount of 10,000 SeaShells, a multiplier, and a predefined number of contestants we will need to share the SeaShells of the suitcase with. The final amount of SeaShells that will be awarded from a suitcase will also be influenced by the percentage of participants who pick that particular suitcase. We are able to choose up to 3 suitcases, with the first suitcase being free to pick, the second suitcase requiring an initial 50,000 SeaShell fee, and the third suitcase requiring an initial 100,000 SeaShell fee (if we remember correctly).

![round_4_manual](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_manual.png)

#### The formula for calculating the final amount of SeaShells awarded from a suitcase remains identical to the formula used in the manual trading challenge of Round 2:
#### $\text{Final Amount}=\frac{10,000 * \text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}$

#### Our work for this round's manual trading challenge can be found in [round_4_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/round_4/round_4_manual_trading.py). Given that this manual trading challenge had more options to choose than the manual trading challenge of Round 2, we felt a lot more comfortable with picking a second suitcase, as we hoped that the participants' picks will be distributed enough across all the suitcases to leave many of the suitcases profitable as a second choice. Identical to the manual trading challenge of Round 2, the "final multiplier" needed for a suitcase to be profitable as a second choice needs to be greater than or equal to 5:
#### $\frac{\text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}\ge5$

#### Calculating the `max_percentage` of participants who can pick a suitcase for the suitcase to be profitable has a second choice, for all suitcases, yielded the following output:

![round_4_manual_code_output_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_manual_code_output_1.jpg)

#### ^^ The maximum percentages for the suitcases sum up to around 125%, which we interpret as a certainty that there will exist at least one suitcase that is profitable as a second choice.

#### In attempting to narrow down the safest and most profitable suitcases, we graphed line graphs of the suitcases and their respective `max_percentage` of participants alongside the final distribution of crate picks from Round 2's manual trading challenge (given to us in [Round 4 of the wiki](https://imc-prosperity.notion.site/Round-4-19ee8453a0938112aa5fd7f0d060ffe6)). The x-axis of the graph is the displayed multiplier of the suitcases/crates, and the y-axis of the graph is the percentage of participants that are expected to/actually pick a particular suitcase/crate. We also attempted to account for the differences in scenarios between the two manual trading challenges by scaling the distribution of Round 2 crate picks to better fit the condition of the Round 4 suitcases.

```python
# In round_4_manual_trading.py

def scale_round_2_to_round_2(x_array, y_array):
    for i, j in enumerate(x_array):
        x_array[i] = (j * 10) / 9

    # Previously y_array[i] = (j * 5) / 11.807
    # Now j / 2 because we're guessing that with 2x more options, a Round 4 suitcase will have half as many picks as a Round 2 crate
    for i, j in enumerate(y_array):
        y_array[i] = (j / 2)
```

#### The unmodified line graphs are displayed in the graph titled _**Round 2 (RAW values) vs Round 4 (IDEAL)**_, while the modified line graphs are displayed in the graph titled _**Round 2 (SCALED values) vs Round 4 (IDEAL)**_.

![round_4_manual_code_output_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_manual_code_output_2.jpg)
![round_4_manual_code_output_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_manual_code_output_3.jpg)

#### ^^ We interpreted _**Round 2 (SCALED values) vs Round 4 (IDEAL)**_ to mean that, if participants picked suitcases the same way they picked the crates in Round 2's manual trading challenge, the following suitcases would be profitable as a second choice:
1. x10 Multiplier, 1 Contestant
2. x23 Multiplier, 2 Contestants
3. x30 Multiplier, 2 Contestants
4. x31 Multiplier, 2 Contestants
5. x37 Multiplier, 3 Contestants
6. x40 Multiplier, 3 Contestants
7. x41 Multiplier, 3 Contestants (optimal)
8. x47 Multiplier, 3 Contestants (optimal)
9. x50 Multiplier, 4 Contestants
10. x60 Multiplier, 4 Contestants
11. x70 Multiplier, 4 Contestants
12. x73 Multiplier, 4 Contestants
13. x89 Multiplier, 8 Contestants

#### From _**Round 2 (SCALED values) vs Round 4 (IDEAL)**_, it would seem that the suitcases with (x41 Multiplier, 3 Contestants) and (x47 Multiplier, 3 Contestants) are the safest and most profitable to pick. Tyler Thomas, however, pointed out that it is unlikely that the participants' picks will be identical to Round 2's manual trading challenge, and considered the possibility of participants now being less likely to pick suitcases with higher multipliers: in Round 2's manual trading challenge, the crates with the highest multipliers were the most frequently picked; with these crates turning out to not be profitable, participants may be less inclined to pick suitcases with higher multipliers in this round's manual trading challenge; if this is the case, suitcases with higher multipliers would be picked less frequently, while the rest of the suitcases would be picked more frequently; consequently, suitcases with higher multipliers would be the most profitable, while the suitcases with multipliers between 30-50, while still safe, would be less profitable than what our line graphs imply. After some discussion and consideration of both the line graphs and Tyler's remarks, we ended up choosing the following suitcases:
1. x89 Multiplier, 8 Contestants
2. x90 Multiplier, 10 Contestants

#### We also considered the possibility of choosing a third suitcase, however we quickly decided against such a choice, as we felt that it was very unlikely, even more so than the possibility of a second crate pick in Round 2's manual trading challenge, that any of the suitcases would be profitable as a third choice. This is supported by a slightly modified version of round_4_manual_trading.py, in which we changed `max_percent_to_be_profitable` from `5` to `10`; in hindsight, it seems that `max_percent_to_be_profitable` should have been renamed to `max_multiplier_to_be_profitable`.

#### $10,000 * \frac{\text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}\ge100,000$
#### $\frac{\text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}\ge\frac{100,000}{10,000}$
#### $\frac{\text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}\ge10$

![round_4_manual_code_output_4](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_manual_code_output_4.jpg)

#### ^^ It is worth noting that, as supported by the code, the suitcases with (x100 Multiplier, 15 Contestants) and (x90 Multiplier, 10 Contestants) would not be profitable as a third choice regardless of how frequently they are picked, as their predefined number of contestants would be enough to reduce the multiplier below 10. As an example, if 0% of participants picked suitcase (x90 Multiplier, 10 Contestants), suitcase (x90 Multiplier, 10 Contestants) would have awarded 90,000 SeaShells, which is not enough to cover the initial 100,000 SeaShell fee of a third choice.
#### $\text{Final Amount}=\frac{10,000 * 90}{10 + (0 * 100)}$
#### $\text{Final Amount}=\frac{900,000}{10}$
#### $\text{Final Amount}=90,000\text{ SeaShells}<100,000\text{ SeaShells (Initial Fee)}$

#### These are the results of our Round 4 manual trading challenge:

![round_4_manual_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_manual_results_1.gif)
![round_4_manual_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_4_manual_results_2.jpg)

#### It is very clear that Tyler Thomas's predictions were correct.
</details>

---
<details>
<summary><h2>Round 5 🕵️‍♀️</h2></summary>

### Algorithmic Trading
#### As mentioned in [Round 5 of the wiki](https://imc-prosperity.notion.site/Round-5-19ee8453a0938154bd42d50839bbccee), Round 5 did not introduce any new tradable products. Instead, Round 5 introduced information on the counterparties we traded against, which the wiki mentioned can be found in the `OwnTrade` class.

#### Due to time constraints, we did not develop a meaningful strategy that used the counterparty information. Instead, we attempted to refine our existing algorithm and fix the errors that prevented our code from running in the final submission. As mentioned in Round 4, an error that we encountered in our final submission log involved a `RuntimeWarning`, in which it seemed that NumPy's `mean()` function was being called on empty lists, presumably on the first iteration of the `Trader` class when our product and `observation_info_history` histories are initially empty. Hence, we decided to set variables that used NumPy's `mean()` function to `0` when the relevant lists are empty.

```python
# In round_5.py
# In the Macaron class

self.historical_ask_price_mean = 0
if len(observation_info_history["askPrice"]) > 0:
    self.historical_ask_price_mean = mean(observation_info_history["askPrice"])

# ...

self.historical_ask_price_std = 0
if len(observation_info_history["askPrice"]) > 0:
    self.historical_ask_price_std = std(observation_info_history["askPrice"])
```

#### In addition, we adjusted our "crash detectors" to include both the `sell_order_history` and `buy_order_history` in their calculations, as opposed to only the `sell_order_history` previously, and slightly tweaked their thresholds. We hope that these changes could help make our "crash detectors" more stable and reasonable, especially as this change seems to have increased our overall profits in our submissions.

```python
# In round_5.py

def big_dip_checker(sell_order_history, buy_order_history, current_mid_price, multiplier):
    sell_average = get_average(sell_order_history)
    buy_average = get_average(buy_order_history)
    mid_average_value = (sell_average + buy_average) / 2

    return current_mid_price > (mid_average_value * multiplier)

def small_dip_checker(sell_order_history, buy_order_history, recents_length, current_mid_price, multiplier):
    # ...

    mid_recents_average = (sell_recents_average + buy_recents_average) / 2

    #print(f"recents_average: {recents_average}")

    return current_mid_price > (mid_recents_average * multiplier)
```

#### These are the results of our Round 5 algorithm:

![round_5_algorithm_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_5_algorithm_results_1.gif)
![round_5_algorithm_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_5_algorithm_results_2.jpg)

#### ^^ This, once again, was surprising to us, as we thought that the `RuntimeWarning` error was the sole reason for our algorithm previously not running. In hindsight, while the `RuntimeWarning` error no longer seems to be an issue in our algorithm, we did not end up fixing, or catching, another error in our algorithm, in which it seems that our algorithm would "time out". We currently have not implemented and tested possible fixes for this error, however, we suspect that this error might involve `observation_info_history` — as we may not have set a size limit for the history, causing the history to continuously append thousands of elements; this could explain why the algorithm did not seem to encounter errors during the first 4,000 iterations or so, as `observation_info_history` would have been smaller and easier to handle during these iterations.

![round_5_algorithm_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_5_algorithm_results_3.jpg)

### Manual Trading
#### As mentioned in [Round 5 of the wiki](https://imc-prosperity.notion.site/Round-5-19ee8453a0938154bd42d50839bbccee), the manual trading challenge for Round 5 involves us trading in the West Archipelago exchange. Using an initial capital of 1,000,000 SeaShells, and information from the [Goldberg news source](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/round_5/goldberg_news_source.png), we needed to perform trades for an array of products: for each product, we needed to decide whether to buy or sell the product, and for what percentage of our initial capital. There is also a fee associated with each product we trade, which we found can be calculated using the following formula:
#### $\text{Fee}=120*\text{Percentage of our Initial Capital Used}*100$

#### ^^ For example, if we decided to buy Haystacks for 1% of our initial capital, the associated fee for such a trade would be:
#### $\text{Fee}=120*(0.01*100)$
#### $\text{Fee}=120\text{ SeaShells}$

#### The goal of this manual trading challenge is to perform the correct trades (buys and sells) with the optimal percentages for these products, and secure as much profit from these trades as we can. The products we will be trading are provided as follows. It is worth noting that it seems that the Goldberg news source has a news section for each of the products to be traded.
1. Haystacks
2. Ranch sauce
3. Cacti Needle
4. Solar panels
5. Red Flags
6. VR Monocle
7. Quantum Coffee
8. Moonshine
9. Striped Shirts

#### We began this manual trading challenge by noting our reactions on how the events in the Goldberg news source will affect the listed products. We concluded that a train derailment will negatively affect Cacti Needle, discovered issues will significantly hurt Quantum Coffee, an acquisition could mean that we should buy Ranch sauce, increased costs might negatively affect Solar panels, it is unclear how a trip to space and scientific opinions will affect Moonshine, it is unlikely that rumors will affect Haystacks, there might be reason to buy Red Flags, changes in Striped Shirts will depend on the popularity and reputation of the Dalton Brothers, and growing popularity could indicate a need to buy VR Monocle unless the growth is too unsustainable. We then refined our trades with [round_5_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/round_5/round_5_manual_trading.py), which was heavily inspired by [Round5.ipynb](https://github.com/gabsens/IMC-Prosperity-2-Manual/blob/master/Round5.ipynb) in gabsens's IMC-Prosperity-2-Manual GitHub repository. In this file, we ended up using the optimal sentiments and sentiment multipliers from a similar manual trading challenge in last year's IMC Prosperity 2 competition, as we noticed that many of last year's products had similar associated stories as our products this year. From this assumption, our code yielded the following:

![round_5_manual_code_output](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_5_manual_code_output.jpg)

#### These are the results of our Round 5 manual trading challenge:

![round_5_manual_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_5_manual_results_1.gif)
![round_5_manual_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_5_manual_results_2.jpg)

#### ^^ Overall, it seems that we performed well on some products (e.g., Cacti Needle, Red Flags, Quantum Coffee) and had room to improve on other products (e.g, Haystacks, Ranch sauce, Solar panels). This is supported by the optimal trades for the challenge provided by K_Tesla in the IMC Prosperity Discord server. It is worth noting that a positive percentage indicates that a buy is suggested, while a negative percentage indicates that a sell is suggested.

![round_5_manual_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_5_manual_results_3.png)

#### ^^ Comparing our profits to the optimal profits, it is clear that we have room for improvement.

</details>

---
## Results and Rankings
<table>
    <tr align="center">
        <th></th>
        <th colspan="4">Rank</th>
    </tr>
    <tr align="center">
        <th>Round</th>
        <th>Overall</th>
        <th>Manual</th>
        <th>Algorithmic</th>
        <th>Country</th>
    </tr>
    <tr align="center">
        <td>Round 1</td>
        <td>3932</td>
        <td>1</td>
        <td>5323</td>
        <td>1027</td>
    </tr>
    <tr align="center">
        <td>Round 2</td>
        <td>1849</td>
        <td>1</td>
        <td>4221</td>
        <td>456</td>
    </tr>
    <tr align="center">
        <th colspan="5">Rankings Resetted At This Point</th>
    </tr>
    <tr align="center">
        <td>Round 3</td>
        <td>2052</td>
        <td>498</td>
        <td>1958</td>
        <td>528</td>
    </tr>
    <tr align="center">
        <td>Round 4</td>
        <td>1170</td>
        <td>282</td>
        <td>2204</td>
        <td>303</td>
    </tr>
    <tr align="center">
        <td>Round 5</td>
        <td>855</td>
        <td>244</td>
        <td>1763</td>
        <td>229</td>
    </tr>
</table>
