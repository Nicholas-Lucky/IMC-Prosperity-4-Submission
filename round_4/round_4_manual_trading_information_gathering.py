from math import exp, sqrt
from statistics import NormalDist, fmean, median
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

    number_of_runs = 100_000
    for i in range(number_of_runs):
        final_price = run_path(21)[-1]

        if final_price > threshold:
            count += 1
        
        call_payoffs.append(max(final_price - threshold, 0))
        put_payoffs.append(max(threshold - final_price, 0))
    
    probability = count / number_of_runs
    print(f"P(final AC > {threshold}) = {count} / {number_of_runs} ≈ {probability}")
    print(f"Mean Call Payoff = {fmean(call_payoffs)}")
    print(f"Mean Put Payoff = {fmean(put_payoffs)}")

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
    calculate_probability_final_underlying_price_greater_than(35)
    calculate_probability_final_underlying_price_greater_than(44)

main()
