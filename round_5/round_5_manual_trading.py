# This code is heavily inspired by Round5.ipynb in gabsens's IMC-Prosperity-2-Manual GitHub repository
# Link: https://github.com/gabsens/IMC-Prosperity-2-Manual/blob/master/Round5.ipynb

# https://www.google.com/search?q=numpy+t+%40&rlz=1C1VDKB_enUS970US970&oq=numpy+t+%40&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDE2ODNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
# import numpy as np

predicted_sentiments = {
    'Obsidian cutlery': '----',
    'Pyroflex cells': '--',
    'Thermalite core': '++++',
    'Lava cake': '-----',
    'Magma ink': '++',
    'Scoria paste': '+',
    'Ashes of the Phoenix': '---',
    'Volcanic incense': '---',
    'Sulfur reactor': '+'
}

def get_historical_gabsens_picked_sentiments_info():
    sentiment_multipliers = {
        '+++': 0.25,
        '++': 0.15,
        '+': 0.05,
        '-': -0.05,
        '--': -0.11,
        '---': -0.43,
        '----': -0.6
    }

    return predicted_sentiments, sentiment_multipliers

def get_historical_optimal_sentiments_info():
    # Historical data for reference
    prosperity_2_historical_optimal_product_sentiment_multipliers = {
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

    prosperity_3_historical_optimal_product_sentiment_multipliers = {
        'Haystacks': -0.0048,
        'Ranch sauce': -0.0072,
        'Cacti Needle': -0.412,
        'Solar panels': -0.089,
        'Red Flags': 0.509,
        'VR Monocle': 0.224,
        'Quantum Coffee': -0.6679,
        'Moonshine': 0.03,
        'Striped shirts': 0.0021
    }

    # Current multiplier predictions
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

    return predicted_sentiments, sentiment_multipliers

def get_scenario_1_sentiments_info():
    """
    Lava cake is similar to quantum coffee
    Volcanic incense sounds like a pump and dump no?
    Sulfur reactor sounds like a rly small buy, the news is positive but like it seems minimal???
    Scoria paste was advocated for by a livestreamer, similar to striped shirts maybe
    Ashes of the Phoenix has 'public outcry' which is a key word, not sure if this takes place during or way after the outcry, maybe small-large sell?
    Obsidian cutlery sounds similar to cactus needle
    Pyroflex cell... idk if there's a similarity look into this as well
    Thermalite core is similar to VR monocle
    Magma ink is similar to ranch sauce, but magma ink had a crowd show up while that was not mentioned in the ranch sauce story
    """
    sentiment_multipliers = {
        '+++++': 0.5,
        '++++': 0.22,
        '+++': 0.15,
        '++': 0.03,
        '+': 0.002,
        '-': -0.005,
        '--': -0.08,
        '---': -0.22,
        '----': -0.4,
        '-----': -0.65
    }

    return predicted_sentiments, sentiment_multipliers

def get_scenario_2_sentiments_info():
    sentiment_multipliers = {
        '+++++': 0.5,
        '++++': 0.22,
        '+++': 0.15,
        '++': 0.03,
        '+': 0.002,
        '-': -0.005,
        '--': -0.08,
        '---': -0.22,
        '----': -0.4,
        '-----': -0.65
    }

    return predicted_sentiments, sentiment_multipliers

def get_scenario_3_sentiments_info():
    sentiment_multipliers = {
        '+++++': 0.4,
        '++++': 0.18,
        '+++': 0.14,
        '++': 0.025,
        '+': 0.002,
        '-': -0.005,
        '--': -0.07,
        '---': -0.18,
        '----': -0.35,
        '-----': -0.55
    }

    return predicted_sentiments, sentiment_multipliers

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
    print(f"Total %/capital used: {total_percent}% = {initial_capital * (total_percent / 100)} XIRENs")

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
    print(f"Total %/capital used: {total_percent}% = {initial_capital * (total_percent / 100)} XIRENs")

#sentiments, sentiment_multipliers = get_historical_user_picked_sentiments_info()
# sentiments, sentiment_multipliers = get_historical_optimal_sentiments_info()
# sentiments, sentiment_multipliers = get_scenario_1_sentiments_info()
sentiments, sentiment_multipliers = get_scenario_3_sentiments_info()

products = list(sentiments.keys())
# product_multipliers = make_product_multipliers(sentiments, sentiment_multipliers)

# Override the multipliers with this for faster testing
# product_multipliers = {
#     'Obsidian cutlery': -0.20,
#     'Pyroflex cells': -0.10,
#     'Thermalite core': 0.15,
#     'Lava cake': -0.28,
#     'Magma ink': 0.04,
#     'Scoria paste': 0.01,
#     'Ashes of the Phoenix': -0.22,
#     'Volcanic incense': -0.005,
#     'Sulfur reactor': 0.1
# }

#print(products)
#print(product_multipliers)

# pi_i = % allocated (optimize this)
# r_i = anticipated return multiplier I guess? (product_multipliers)
# fee = (volume_for_specific_product / 100) * (volume_for_specific_product / 100) * budget
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
        
        # In the GitHub: profit = 7500 * r_i * pi_i - fee
        fee = (pi_i / 100) * (pi_i / 100) * initial_capital
        profit = (initial_capital * r_i * (pi_i / 100)) - fee

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
