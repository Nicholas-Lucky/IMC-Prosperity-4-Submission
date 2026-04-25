import numpy as np
from math import e

# Each team may submit two price offers (between 670 and 920 XIRECs)
MINIMUM_BID = 670
MAXIMUM_BID = 920

# The distribution of the bids is uniformly distributed at increments of 5 between 670 and 920 (inclusive on both ends).
MINIMUM_RESERVE_PRICE = 670
MAXIMUM_RESERVE_PRICE = 920
RESERVE_PRICE_INCREMENT = 5

# On the next trading day, you’re able to sell all the product for a fair price, 920
SELL_AMOUNT = 920

def calculate_optimal_first_bid():
    optimal_b1_profit = -1
    optimal_b1 = -1
    
    for b1 in range(MINIMUM_BID, MAXIMUM_BID + 1, 1):
        # print(b1)

        current_b1_profit = 0

        for reserve_price in range(MINIMUM_RESERVE_PRICE, MAXIMUM_RESERVE_PRICE + 1, RESERVE_PRICE_INCREMENT):
            # print(reserve_price)

            # If the first bid is higher than the reserve price, they trade with you at your first bid
            if b1 > reserve_price:
                current_b1_profit += (SELL_AMOUNT - b1)
        
        if current_b1_profit > optimal_b1_profit:
            optimal_b1_profit = current_b1_profit
            optimal_b1 = b1
    
    return (optimal_b1, optimal_b1_profit)

def calculate_optimal_second_bid(avg_b2):
    optimal_b2_profit = -1
    optimal_b2 = -1
    
    for b2 in range(MINIMUM_BID, MAXIMUM_BID + 1, 1):
        current_b2_profit = 0

        for reserve_price in range(MINIMUM_RESERVE_PRICE, MAXIMUM_RESERVE_PRICE + 1, RESERVE_PRICE_INCREMENT):
            # If the first bid is higher than the reserve price, they trade with you at your first bid
            if b2 > reserve_price:
                penalty_multiplier = 1

                if b2 <= avg_b2:
                    penalty_multiplier = ((SELL_AMOUNT - avg_b2) / (SELL_AMOUNT - b2)) ** 3

                current_b2_profit += ((SELL_AMOUNT - b2) * penalty_multiplier)
        
        if current_b2_profit > optimal_b2_profit:
            optimal_b2_profit = current_b2_profit
            optimal_b2 = b2
    
    return (optimal_b2, optimal_b2_profit)

def get_average_bid(bids, associated_percentages):
    avg_b2 = 0

    for index, bid in enumerate(bids):
        avg_b2 += (bid * associated_percentages[index])

    return avg_b2

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

    bids = [791, 820, 830, 840, 850, 860, 870, 880, 890, 900, 920]
    associated_percentages = [0.05, 0.10, 0.10, 0.10, 0.15, 0.10, 0.10, 0.10, 0.08, 0.07, 0.05]

    return get_average_bid(bids, associated_percentages)

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

    bids = [791, 840, 850, 860, 870, 880, 890, 900, 920]
    associated_percentages = [0.03, 0.05, 0.15, 0.15, 0.15, 0.17, 0.18, 0.07, 0.05]

    return get_average_bid(bids, associated_percentages)

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

    bids = [791, 850, 860, 870, 880, 890, 900, 920]
    associated_percentages = [0.01, 0.15, 0.16, 0.17, 0.19, 0.18, 0.11, 0.03]

    return get_average_bid(bids, associated_percentages)

def main():
    optimal_b1, optimal_b1_profit = calculate_optimal_first_bid()
    print(f"Optimal b1: {optimal_b1}\n\tProfit from b1 = {optimal_b1} : {optimal_b1_profit}")

    print("\n--------- OPTIMAL b2 SCENARIOS: ---------\n")

    print("SCENARIO 1: Relatively evenly distributed from 791 to 920")
    optimal_b2, optimal_b2_profit = calculate_optimal_second_bid(second_bid_scenario_1())
    print(f"Optimal b2: {optimal_b2}\n\tProfit from b2 = {optimal_b2} : {optimal_b2_profit}")

    print("\nSCENARIO 2: More concentrated from 840 to 920")
    optimal_b2, optimal_b2_profit = calculate_optimal_second_bid(second_bid_scenario_2())
    print(f"Optimal b2: {optimal_b2}\n\tProfit from b2 = {optimal_b2} : {optimal_b2_profit}")

    print("\nSCENARIO 3: Even more concentrated from 850 to 900")
    optimal_b2, optimal_b2_profit = calculate_optimal_second_bid(second_bid_scenario_3())
    print(f"Optimal b2: {optimal_b2}\n\tProfit from b2 = {optimal_b2} : {optimal_b2_profit}")

main()

