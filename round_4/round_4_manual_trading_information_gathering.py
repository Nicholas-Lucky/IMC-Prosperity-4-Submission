from math import exp, sqrt
from statistics import NormalDist, fmean, median
from random import gauss
from numpy import percentile

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

def run_path(expiry_in_days):
    dt = 1 / (TRADING_DAYS_PER_YEAR * STEPS_PER_DAY)

    # Geometric Brownian Motion (yes)
    # S_t = S_0 * exp((mu - ((VOLATILITY ** 2) / 2)) * t + (VOLATILITY * W_t))
    
    S_t = S_0
    path = [S_0]

    for i in range(expiry_in_days * STEPS_PER_DAY):
        # Z = NormalDist(mu=0, sigma=1)
        Z = gauss(mu=0, sigma=1)

        # S_after_dt = S_t * exp(-0.5 * (VOLATILITY ** 2) * dt + VOLATILITY * sqrt(dt) * Z)
        S_t = S_t * exp(-0.5 * (VOLATILITY ** 2) * dt + VOLATILITY * sqrt(dt) * Z)

        path.append(S_t)
    
    return path

def simulate_final_underlying_price_one():
    final_prices = []
    number_of_runs = 100

    for i in range(number_of_runs):
        final_prices.append(run_path(21)[-1])

    return fmean(final_prices)

def calculate_probability_final_underlying_price_greater_than(threshold):
    count = 0
    call_payoffs = []
    put_payoffs = []
    knockout_payoffs = []
    final_prices = []
    knockout_barrier_broken_count = 0

    number_of_runs = 100_000
    for i in range(number_of_runs):
        path = run_path(21)
        final_price = path[-1]
        final_prices.append(final_price)

        for price in path:
            if price < 30:
                knockout_barrier_broken_count += 1
                break

        if final_price > threshold:
            count += 1
        
        call_payoffs.append(max(final_price - threshold, 0))
        put_payoffs.append(max(threshold - final_price, 0))
        
        knockout_payoff = max(45 - final_price, 0) - 0.175
        if min(path) < 30:
            knockout_payoff = -0.175
        
        knockout_payoffs.append(knockout_payoff)
    
    probability = count / number_of_runs
    print(f"P(final AC > {threshold}) = {count} / {number_of_runs} ≈ {probability}")
    print(f"Mean Call Payoff = {fmean(call_payoffs)}")
    print(f"Mean Put Payoff = {fmean(put_payoffs)}")
    print(f"OVER {number_of_runs} RUNS:")
    print(f"AC Range: {min(final_prices)} to {max(final_prices)} | range = {max(final_prices) - min(final_prices)}")
    print(f"AC Mean: {fmean(final_prices)}")
    print(f"AC Median: {median(final_prices)}")
    print(f"AC 25th Percentile: {percentile(final_prices, 25)}")
    print(f"AC 75th Percentile: {percentile(final_prices, 75)}")
    print(f"P(Knockout barrier = 30 broken) = {knockout_barrier_broken_count / number_of_runs}")
    print(f"Mean Knockout Payoff = {fmean(knockout_payoffs)}")

def calculate_probabilities_and_mean_payoffs():
    options = {"AC_50_P": {"strike_price": 50, "ask": 12.05, "type": "vanilla_put", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_50_C": {"strike_price": 50, "ask": 12.05, "type": "vanilla_call", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_35_P": {"strike_price": 35, "ask": 4.35, "type": "vanilla_put", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_40_P": {"strike_price": 40, "ask": 6.55, "type": "vanilla_put", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_45_P": {"strike_price": 45, "ask": 9.1, "type": "vanilla_put", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_60_C": {"strike_price": 60, "ask": 8.85, "type": "vanilla_call", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_50_P_2": {"strike_price": 50, "ask": 9.75, "type": "vanilla_put", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_50_C_2": {"strike_price": 50, "ask": 9.75, "type": "vanilla_call", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_50_CO": {"strike_price": 50, "ask": 22.3, "type": "chooser", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_40_BP": {"strike_price": 40, "ask": 5.1, "type": "binary_put", "total_payoff": 0, "profitable_final_underlying_price_count": 0},
               "AC_45_KO": {"strike_price": 45, "ask": 0.175, "type": "knock-out_put", "total_payoff": 0, "profitable_final_underlying_price_count": 0}}
    
    count = 0
    final_prices = []
    knockout_barrier_broken_count = 0

    number_of_runs = 100_000
    for i in range(number_of_runs):
        path = run_path(21)
        path_14 = path[:(14 * STEPS_PER_DAY) + 1]
        final_price = path[-1]
        final_prices.append(final_price)

        for price in path:
            if price < 30:
                knockout_barrier_broken_count += 1
                break

        for option in options:
            threshold = options[option]["strike_price"] + options[option]["ask"]
        
            if final_price > threshold:
                options[option]["profitable_final_underlying_price_count"] += 1
            
            # Calculate the payoffs
            if options[option]["type"] == "knock-out_put":
                knockout_payoff = max(options[option]["strike_price"] - final_price, 0) - options[option]["ask"]
                if min(path) < 30:
                    knockout_payoff = -options[option]["ask"]
                
                options[option]["total_payoff"] += knockout_payoff

            elif options[option]["type"] == "binary_put":
                if final_price < options[option]["strike_price"]:
                    options[option]["total_payoff"] += (10 - options[option]["ask"])
                else:
                    options[option]["total_payoff"] += (-options[option]["ask"])
                
            elif options[option]["type"] == "chooser":
                decider_price = path_14[-1]

                if decider_price >= threshold:
                    options[option]["total_payoff"] += (max(final_price - options[option]["strike_price"], 0) - options[option]["ask"])
                else:
                    options[option]["total_payoff"] += (max(options[option]["strike_price"] - final_price, 0) - options[option]["ask"])

            elif options[option]["type"] == "vanilla_put":
                options[option]["total_payoff"] += (max(options[option]["strike_price"] - final_price, 0) - options[option]["ask"])
            
            elif options[option]["type"] == "vanilla_call":
                options[option]["total_payoff"] += (max(final_price - options[option]["strike_price"], 0) - options[option]["ask"])
    
    print(f"OVER {number_of_runs} RUNS:")
    print(f"AC Range: {min(final_prices)} to {max(final_prices)} | range = {max(final_prices) - min(final_prices)}")
    print(f"AC Mean: {fmean(final_prices)}")
    print(f"AC Median: {median(final_prices)}")
    print(f"AC 25th Percentile: {percentile(final_prices, 25)}")
    print(f"AC 75th Percentile: {percentile(final_prices, 75)}")
    print(f"P(Knockout barrier = 30 broken) = {knockout_barrier_broken_count / number_of_runs}")

    for option in options:
        current_option = options[option]

        if options[option]["type"] in ["vanilla_call", "chooser"]:
            print(f"{option} : P(final AC > {current_option['strike_price']} + {current_option['ask']}) = {current_option['profitable_final_underlying_price_count'] / number_of_runs}")
        else:
            print(f"{option} : P(final AC < {current_option['strike_price']} - {current_option['ask']}) = {current_option['profitable_final_underlying_price_count'] / number_of_runs}")
        
        print(f"{option} : Mean Payoff = {current_option['total_payoff'] / number_of_runs}")

def main():
    # print(f"Running {number_of_simulations} simulations, this might take a few minutes...")

    # final_underlying_price_means = []
    # number_of_simulations = 10_000
    
    # for i in range(number_of_simulations):
    #     final_underlying_price_means.append(simulate_final_underlying_price_one())
    
    # print(f"OVER {number_of_simulations} SIMULATIONS:")
    # print(f"AC Mean Range: {min(final_underlying_price_means)} to {max(final_underlying_price_means)} | range = {max(final_underlying_price_means) - min(final_underlying_price_means)}")
    # print(f"AC Mean Mean: {fmean(final_underlying_price_means)}")
    # print(f"AC Mean Median: {median(final_underlying_price_means)}")

    # calculate_probability_final_underlying_price_greater_than(35 - 4.35)
    # calculate_probability_final_underlying_price_greater_than(62.05)
    calculate_probabilities_and_mean_payoffs()

main()
