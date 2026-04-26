from math import exp, sqrt
from statistics import NormalDist
from random import gauss

# Provided by IMC
TRADING_DAYS_PER_YEAR = 252
STEPS_PER_DAY = 4
STEPS_PER_YEAR = TRADING_DAYS_PER_YEAR * STEPS_PER_DAY

def weeks_to_years(weeks: float) -> float:
    # 5 business days per week, annualized to 252 trading days
    return (weeks * 5) / TRADING_DAYS_PER_YEAR

def steps_for_weeks(weeks: float) -> int:
    return int(round(weeks * 5 * STEPS_PER_DAY))

# Information about the underlying AETHER_CRYSTAL product
DRIFT = 0
VOLATILITY = 2.51
S_0 = 50  # The bid is 49.975 and the ask is 50.025

class Option:
    def __init__(self, option_name, expiry, bid_size, bid, ask, ask_size, price, option_type, strike_price):
        self.option_name = option_name
        self.expiry = expiry
        self.bid_size = bid_size
        self.bid = bid
        self.ask = ask
        self.ask_size = ask_size
        self.price = price
        self.option_type = option_type
        self.strike_price = strike_price

        self.available_choices = {"buy": "buy", "sell": "sell"}

        # We need to decide this
        self.buy_or_sell_choice = None
        self.volume = None

class All_Available_Options:
    def __init__(self):
        self.available_options = []

        # Initialize all of the options provided
        option_names = ["AC", "AC_50_P", "AC_50_C", "AC_35_P", "AC_40_P", "AC_45_P", "AC_60_C", "AC_50_P_2", "AC_50_C_2", "AC_50_CO", "AC_40_BP", "AC_45_KO"]
        expirys = ["N/A", 21, 21, 21, 21, 21, 21, 14, 14, "14/21", 21, 21]
        bid_sizes = [200, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 500]
        bids = [49.975, 12, 12, 4.33, 6.5, 9.05, 8.8, 9.7, 9.7, 22.2, 5, 0.15]
        asks = [50.025, 12.05, 12.05, 4.35, 6.55, 9.1, 8.85, 9.75, 9.75, 22.3, 5.1, 0.175]
        ask_sizes = [200, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 500]
        prices = [0.71, 2.71, -0.45, 0.42, 0, -0.48, 0.42, 0.71, 0.71, 0.71, 0.71, 0.71]
        option_types = ["N/A", "vanilla", "vanilla", "vanilla", "vanilla", "vanilla", "vanilla", "vanilla", "vanilla", "chooser", "binary", "knock-out"]
        strike_prices = ["N/A", 50, 50, 35, 40, 45, 60, 50, 50, 50, 40, 45]\
        
        for index, option in enumerate(option_names):
            self.available_options.append(Option(option, expirys[index], bid_sizes[index], bids[index], asks[index],
                                                 ask_sizes[index], prices[index], option_types[index], strike_prices[index]))
    
    def run_monte_carlo(self):
        for i in range(50_000):
            fourteen_day_path = self.run_path(14)
            twenty_one_day_path = self.run_path(21)
    
    def run_path(self, expiry_in_days):
        dt = 1 / (TRADING_DAYS_PER_YEAR * STEPS_PER_DAY)
        # Z = NormalDist(mu=0, sigma=1)
        Z = gauss(mu=0, sigma=1)

        # Geometric Brownian Motion (yes)
        # S_t = S_0 * exp((mu - ((VOLATILITY ** 2) / 2)) * t + (VOLATILITY * W_t))
        
        S_t = S_0
        path = [S_0]

        for i in range(expiry_in_days * STEPS_PER_DAY):
            # S_after_dt = S_t * exp(-0.5 * (VOLATILITY ** 2) * dt + VOLATILITY * sqrt(dt) * Z)
            S_t = S_t * exp(-0.5 * (VOLATILITY ** 2) * dt + VOLATILITY * sqrt(dt) * Z)

            path.append(S_t)
        
        return path

    def price_call(path, K):
        pass
    def price_put(path, K):
        pass
    def price_binary_put(path, K, payout=10):
        pass
    def price_knockout_put(path, K, barrier):
        pass
    def price_chooser(path, K):
        pass

def main():
    pass

main()

