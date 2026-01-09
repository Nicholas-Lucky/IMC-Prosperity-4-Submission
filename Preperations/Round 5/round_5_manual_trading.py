# This code is heavily inspired by Round5.ipynb in gabsens's IMC-Prosperity-2-Manual GitHub repository
# Link: https://github.com/gabsens/IMC-Prosperity-2-Manual/blob/master/Round5.ipynb

# https://www.google.com/search?q=numpy+t+%40&rlz=1C1VDKB_enUS970US970&oq=numpy+t+%40&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDE2ODNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
# import numpy as np

def get_historical_user_picked_sentiments_info():
    sentiments = {
        'Haystacks': '+',
        'Ranch sauce': '++',
        'Cacti Needle': '----',
        'Solar panels': '--',
        'Red Flags': '+',
        'VR Monocle': '+++',
        'Quantum Coffee': '---',
        'Moonshine': '-',
        'Striped shirts': '+'
    }

    sentiment_multipliers = {
        '+++': 0.25,
        '++': 0.15,
        '+': 0.05,
        '-': -0.05,
        '--': -0.11,
        '---': -0.43,
        '----': -0.6
    }

    return sentiments, sentiment_multipliers

def get_historical_optimal_sentiments_info():
    # Historical data for reference
    historical_optimal_product_sentiment_multipliers = {
        'Refrigerators': 0.020713448079427082,
        'Earrings': 0.12367402886284722,
        'Blankets': -0.32888405330882353,
        'Sleds': -0.2829537109375,
        'Sculptures': 0.19637428385416666,
        'PS6': 0.3095545703125,
        'Serum': -0.8157531666666666,
        'Lamps': 6.103515625e-05,
        'Chocolate': -0.000404595947265625
    }

    # Haystacks similar to Refrigerators
    # Ranch sauce similar to Earrings
    # Cacti Needle similar to Blankets (similar blaming tone)
    # Solar panels similar to Sleds
    # Red Flags similar to Sculptures
    # VR Monocle similar to PS6
    # Quantum Coffee similar to Serum

    # Moonshine similar to Chocolate??? (not sure)
    # Striped shirts similar to Lamps??? (Striped shirts will probably have little effect like the lamps?) (not sure)

    sentiments = {
        'Haystacks': '++',
        'Ranch sauce': '+++',
        'Cacti Needle': '---',
        'Solar panels': '--',
        'Red Flags': '++++',
        'VR Monocle': '+++++',
        'Quantum Coffee': '----',
        'Moonshine': '-',
        'Striped shirts': '+'
    }

    sentiment_multipliers = {
        '+++++': 0.3095545703125,
        '++++': 0.19637428385416666,
        '+++': 0.12367402886284722,
        '++': 0.020713448079427082,
        '+': 6.103515625e-05,
        '-': -0.000404595947265625,
        '--': -0.2829537109375,
        '---': -0.32888405330882353,
        '----': -0.8157531666666666
    }

    return sentiments, sentiment_multipliers

def make_product_multipliers(sentiments, sentiment_multipliers):
    d = {}
    for product, sentiment in sentiments.items():
        d[product] = sentiment_multipliers[sentiment]

    return d

def print_format_one(products, optimal_profits, initial_capital):
    total_expected_profit = 0
    total_percent = 0

    print("------- OPTIMAL %'S TO ALLOCATE PER PRODUCT (POSITIVE = BUY, NEGATIVE = SELL) -------\n")
    for product in products:
        optimal_pi_i = round(optimal_profits[product][0], 2)
        expected_profit = round(optimal_profits[product][1], 2)

        print(f"{product}: {optimal_pi_i}%")
        print(f"    Expected profit: {expected_profit}\n")

        total_percent += abs(optimal_pi_i)
        total_expected_profit += expected_profit
    
    print(f"Total expected profit: {round(total_expected_profit, 2)}")
    print(f"Total %/capital used: {total_percent}% = {initial_capital * (total_percent / 100)} seashells")

def print_format_two(products, optimal_profits, initial_capital):
    total_expected_profit = 0
    total_percent = 0

    print("------- OPTIMAL %'S TO ALLOCATE PER PRODUCT -------\n")
    for product in products:
        optimal_pi_i = round(optimal_profits[product][0], 2)
        expected_profit = round(optimal_profits[product][1], 2)

        if optimal_pi_i > 0:
            print(f"{product}: {optimal_pi_i}% BUY")
        else:
            print(f"{product}: {-1 * optimal_pi_i}% SELL")

        print(f"    Expected profit: {expected_profit}\n")

        total_percent += abs(optimal_pi_i)
        total_expected_profit += expected_profit
    
    print(f"Total expected profit: {round(total_expected_profit, 2)}")
    print(f"Total %/capital used: {total_percent}% = {initial_capital * (total_percent / 100)} seashells")

#sentiments, sentiment_multipliers = get_historical_user_picked_sentiments_info()
sentiments, sentiment_multipliers = get_historical_optimal_sentiments_info()

products = list(sentiments.keys())
product_multipliers = make_product_multipliers(sentiments, sentiment_multipliers)

#print(products)
#print(product_multipliers)

# pi_i = % allocated (optimize this)
# r_i = anticipated return multiplier I guess? (product_multipliers)
# Fee = 120 * pi_i^2
initial_capital = 1_000_000

# profit_dictionary = {product: [pi_i, associated profit]}
optimal_profits = {}

for product in products:
    r_i = product_multipliers[product]
    pi_i = -100

    while True:
        # Stop at 100% (include 100% in the calculations though)
        if pi_i > 100:
            break
        
        # In the GitHub: profit = 7500 * r_i * pi_i - 90 * pi_i^2
        profit = (initial_capital * r_i * (pi_i / 100)) - (120 * pi_i * pi_i)

        if optimal_profits.get(product) is None:
            optimal_profits[product] = [pi_i, profit]
        
        else:
            if profit > optimal_profits[product][1]:
                optimal_profits[product] = [pi_i, profit]

        # Test all percentages from -100% to 100% with up to 2 decimal places 
        pi_i += 0.01

#print_format_one(products, optimal_profits, initial_capital)
print()
print_format_two(products, optimal_profits, initial_capital)
print()
