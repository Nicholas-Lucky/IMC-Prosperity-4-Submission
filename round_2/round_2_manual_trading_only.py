import numpy as np
from math import e

def calculate_research(x):
    return 200_000 * np.log(1 + x) / np.log(1 + 100)

def calculate_scale(x):
    MINIMUM_SCALE = 0
    MAXIMUM_SCALE = 7

    MAXIMUM_PERCENTAGE = 100
    per_percentage = MAXIMUM_SCALE / MAXIMUM_PERCENTAGE

    return x * per_percentage

def calculate_speed_linear(x):
    """ Assuming the player choices for the speed percentages are evenly spread, so the final speed grows linearly from 0.1 to 0.9 """
    MINIMUM_MULTIPLIER = 0.1
    MAXIMUM_MULTIPLIER = 0.9
    mutliplier_range = MAXIMUM_MULTIPLIER - MINIMUM_MULTIPLIER
    
    MAXIMUM_PERCENTAGE = 100
    per_percentage = mutliplier_range / MAXIMUM_PERCENTAGE

    return MINIMUM_MULTIPLIER + (x * per_percentage)

def calculate_speed_exponential_less_steep(x):
    """ Assuming more players pick higher percentages for speed """
    # y = 0.1 + 0.8((e^0.03x - 1) / (e^3 - 1))
    return 0.1 + 0.8 * ((e**(0.03 * x) - 1) / (e**3 - 1))

def calculate_speed_exponential_more_steep(x):
    """ Assuming more players pick higher percentages for speed """
    # Solving for y = ab^x given points (0, 0.1) and (100, 0.9)
    # y = 0.1(1.02221541328^x)

    a = 0.1
    b = 1.02221541328

    return a * (b**x)

def main():
    BUDGET = 50_000

    optimal_profit = -1

    optimal_research_percentage = -1
    optimal_scale_percentage = -1
    optimal_speed_percentage = -1

    optimal_research_value = -1
    optimal_scale_value = -1
    optimal_speed_value = -1

    for research in range(0, 101):
        for scale in range(0, 101 - research):
            for speed in range(0, 101 - research - scale):
                percentage_used = research + scale + speed

                # PnL = (Research × Scale × Speed) − Budget_Used
                research_value = calculate_research(research)
                scale_value = calculate_scale(scale)

                # speed_value = calculate_speed_linear(speed)
                # speed_value = calculate_speed_exponential_less_steep(speed)
                speed_value = calculate_speed_exponential_more_steep(speed)

                PnL = (research_value * scale_value * speed_value) - (BUDGET * (percentage_used / 100))
                print(f"research: {research} scale: {scale} speed: {speed} percentage used: {percentage_used} PnL: {PnL}")

                if PnL > optimal_profit:
                    optimal_profit = PnL

                    optimal_research_percentage = research
                    optimal_scale_percentage = scale
                    optimal_speed_percentage = speed

                    optimal_research_value = research_value
                    optimal_scale_value = scale_value
                    optimal_speed_value = speed_value
    
    print(f"Optimal Profit: {optimal_profit}")
    print(f"\tOptimal Research %: {optimal_research_percentage}\n\t\tResult from this percentage = {optimal_research_value})")
    print(f"\tOptimal Scale %: {optimal_scale_percentage}\n\t\tResult from this percentage = {optimal_scale_value})")
    print(f"\tOptimal Speed %: {optimal_speed_percentage}\n\t\tResult from this percentage = {optimal_speed_value})")

main()