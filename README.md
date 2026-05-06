# IMC Prosperity 3 (2025) Submission
### Note: This writeup is heavily inspired by the [Alpha Animals](https://github.com/CarterT27/imc-prosperity-3), [CMU Physics](https://github.com/chrispyroberts/imc-prosperity-3), and [Byeongguk Kang, Minwoo Kim, and Uihyung Lee](https://github.com/pe049395/IMC-Prosperity-2024)'s writeups.
---
### Team Name: Salty Seagulls

### Team Members:
1. Tyler Thomas ([LinkedIn](https://www.linkedin.com/in/tyler-b-thomas/), [GitHub](https://github.com/TylerThomas6))
2. Lismarys Cabrales ([LinkedIn](https://www.linkedin.com/in/lismaryscabrales/), [GitHub](https://github.com/ikozmicx))
3. Nicholas Lucky ([LinkedIn](https://www.linkedin.com/in/nicholas-lucky/), [GitHub](https://github.com/Nicholas-Lucky))
---
## Overview
#### [IMC's Prosperity 2025](https://prosperity.imc.com/) is an annual trading challenge that challenges participants to program an algorithm to trade various goods on a virtual trading market — with the goal of gaining as much profit, in the form of SeaShells, as possible. In addition to the algorithm, there are manual trading challenges that allow participants to gain additional seashells. The competition spans five rounds, with each round adding new products for our trading algorithms to consider, and a new manual trading challenge to attempt. This year is the third iteration of the competition (Prosperity 3), and lasted from April 7th, 2025 to April 22nd, 2025. This is our first year in the competition, and we focused on learning and gaining a (at least) general understanding of the competition and the programming and skills required to perform in both the trading algorithm and manual trading challenges.

#### Further details on this year's competition can be found on the [Prosperity 3 Wiki](https://imc-prosperity.notion.site/Prosperity-3-Wiki-19ee8453a09380529731c4e6fb697ea4).
---
<details>
<summary><h2>Round 1 🦑</h2></summary>

### Algorithmic Trading
#### As mentioned in [Round 1 of the wiki](https://imc-prosperity.notion.site/Round-1-19ee8453a09381d18b78cf3c21e5d916), Round 1 introduced us to our first three tradable products: `RAINFOREST_RESIN`, `KELP`, and `SQUID_INK`. These products seem to have varying levels of stability, with `RAINFOREST_RESIN` having relatively stable values, `KELP` having some variation, and `SQUID_INK` having the most volatility of the three products. `RAINFOREST_RESIN` has a position limit of `50`, `KELP` has a position limit of `50`, and `SQUID_INK` has a position limit of `50`.

#### We began with the [IMC_prototype.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/IMC_prototype.py) provided to us by Mark Brezina in the IMC Prosperity Discrod server. After learning the logic of the code, we experimented with different thresholds to buy and sell the tradable products. Realizing that our code needed to be adaptable, we attempted to store and track the sell orders that we encountered in a `sell_order_history` dictionary. We also created a `buy_order_history` dictionary to use alongside `sell_order_history` when calculating buy and sell thresholds for `SQUID_INK`, as suggested by Tyler Thomas. For `sell_order_history`, we would append the lowest sell order of the iteration, while we would append the highest buy order of the iteration to `buy_order_history`. These dictionaries could then be converted into strings to be put in `traderData` and converted back to dictionaries at the start of future iterations.

```python
# In round_1.py

# At the start of the Trader class
sell_order_history = {}
buy_order_history = {}

if state.traderData != "":
    order_histories = string_to_list_of_dictionaries(state.traderData)
    sell_order_history = order_histories[0]
    buy_order_history = order_histories[1]

# ...perform calculations

# At the end of the Trader class
newData = []
newData.append(sell_order_history)
newData.append(buy_order_history)

traderData = str(newData)
```

#### In subsequent iterations, we took the average of the sell orders in `sell_order_history` for each product, and used this average as our threshold for buying and selling. For round 1, we actually ended up not using `buy_order_history` for calculating thresholds for `SQUID_INK`, I think because of time constraints.

```python
# In round_1.py

if product == "KELP":
    #acceptable_buy_price = get_average(sell_order_history[product])
    acceptable_sell_price = get_average(sell_order_history[product]) + 3
```

#### We also attempted to add slight offsets for the buy/sell thresholds for some products, which we hoped would allow us to sell a product at a higher price than what we bought the product for. While most of these offsets were hardcoded based on rough estimates for how volatile each product would be, we added an adaptable offset for `SQUID_INK`, as we felt that such an offset would benefit `SQUID_INK` the most due to the product's high volatility. This adaptable offset was calculated by subtracting the 100th most recent sell order from the most recent sell order, dividing the difference by 6, and taking the absolute value. This result was then added to the threshold to sell, with the idea being that:
1. Quickly rising sell orders should raise our threshold to sell, potentially allowing us to sell `SQUID_INK` at higher prices
2. Stagnating sell orders should maintain our threshold to sell as it is
3. Quickly falling sell orders should also raise our threshold to sell, as we would not want to sell `SQUID_INK` at these prices

```python
# In round_1.py

# In hindsight, index_one and index_two probably should've been switched, but it still be fine given the absolute value 
index_one = 0
index_two = 99
if len(sell_order_history[product]) < 100:
    index_two = len(sell_order_history[product]) - 1

sell_offset = (sell_order_history[product][index_one] - sell_order_history[product][index_two]) / 6
if sell_offset < 0:
    sell_offset *= -1

# ...later in the code...
if product == "SQUID_INK":
    # ...
    acceptable_sell_price = sell_order_ave + sell_offset
```

#### For the first iteration of the `Trader` class, we hardcoded many of the thresholds for all three products. We originally wanted these hardcoded values to only be used in the first iteration, however we found that they provided us with more profit when used in future iterations as well. As a result, assuming that the historical data given would reflect on the final submission data (which we later learned is not the case), we ended up sticking with these hardcoded values for many of our thresholds.

```python
# In round_1.py

# "RAINFOREST_RESIN" price, hardcoded for now
acceptable_buy_price = 9999  # Participant should calculate this value
acceptable_sell_price = 10001  # Participant should calculate this value

if product == "SQUID_INK":
    acceptable_buy_price = 1950
    acceptable_sell_price = 1970

elif product == "KELP":
    acceptable_buy_price = 2030
    acceptable_sell_price = 2032

# ...later in the code; we commented out the lines for calculating thresholds
#if product == "RAINFOREST_RESIN":
#acceptable_buy_price = get_average(sell_order_history[product]) - 2
#acceptable_sell_price = get_average(sell_order_history[product]) + 1
```

#### These are the results of our Round 1 algorithm:

![round_1_algorithm_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_algorithm_results_1.gif)
![round_1_algorithm_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_algorithm_results_2.gif)

#### While we did gain profit from our algorithm, we recognized that some of our buy and sell thresholds were still hardcoded for some of the products. As a result, we attempted to make our thresholds and algorithms more adaptable in future rounds.

### Manual Trading
#### As mentioned in [Round 1 of the wiki](https://imc-prosperity.notion.site/Round-1-19ee8453a09381d18b78cf3c21e5d916), the manual trading challenge for Round 1 was a series of currency trades that we needed to. We began with 500,000 SeaShells, with SeaShells as our starting currency, and we needed to trade this initial amount to different currencies before ending with a trade back to SeaShells. We amount we get from trading to another currency is determined by the multiplier of the trade, as determined by:

| Products/Currencies | Snowballs | Pizzas | Silicon Nuggets | SeaShells |
|:-------------------:|:---------:|:------:|:---------------:|:---------:|
| Snowballs           | 1         | 1.45   | 0.52            | 0.72      |
| Pizzas              | 0.7       | 1      | 0.31            | 0.48      |
| Silicon Nuggets     | 1.95      | 3.1    | 1               | 1.49      |
| SeaShells           | 1.34      | 1.98   | 0.64            | 1         |

#### ^^ For example, if we have 500,000 SeaShells and trade to Pizzas, we will receive 500,000 x 1.98 = 990,000 Pizzas

#### Our goal is to perform 5 trades (with the 5th trade being back to SeaShells) that will ideally net us a profit in SeaShells — the general format is shown below. It is worth noting that we are allowed to trade a currency into the same currency (the resulting multiplier would be 1), and we are allowed to trade into a specific currency more than once.

| Initial Currency | Currency to Trade to |
|:----------------:|:--------------------:|
| SeaShells        | product_1            |
| product_1        | product_2            |
| product_2        | product_3            |
| product_3        | product_4            |
| product_4        | SeaShells            |

#### Our work for this round's manual trading can be viewed in [round_1_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/round_1/round_1_manual_trading.py). Assuming that the 5th trade will always be to SeaShells, we would essentially have 4 trades, each of which has 4 possible currencies to choose from. As a result, we assumed there would be a maximum of 4<sup>4</sup> = 256 possible "paths" for this challenge. Hence, we felt that it was possible to use brute force to determine the optimal series of trades that would yield the highest number of SeaShells. After fixing errors identified by Tyler Thomas, our round_1_manual_trading.py yielded the following path:

![round_1_manual_code_output](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_manual_code_output.jpg)

#### ^^ With a revenue of 544,340.16 SeaShells, and an initial amount of 500,000 SeaShells, our profit from this series of trades would be 544,340.16 - 500,000 = 44,340.16 SeaShells

#### These are the results of our Round 1 manual trading challenge:

![round_1_manual_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_manual_results_1.gif)
![round_1_manual_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_manual_results_2.jpg)
![round_1_manual_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_manual_results_3.jpg)

#### ^^ It seems that the number 1 team in Manual after Round 1, RBQ, also had a profit of 44,340 SeaShells, which supports the claim that we seemed to have submitted the optimal series of trades for Round 1's manual trading challenge.
</details>

---
<details>
<summary><h2>Round 2 🥐</h2></summary>

### Algorithmic Trading
#### As mentioned in [Round 2 of the wiki](https://imc-prosperity.notion.site/Round-2-19ee8453a09381a580cdf9c0468e9bc8), Round 2 introduced us to 5 new tradeable products: `CROISSANTS`, `JAMS`, `DJEMBES`, `PICNIC_BASKET1`, and `PICNIC_BASKET2`. `PICNIC_BASKET1` and `PICNIC_BASKET2` are a little different in that they contain multiple products: `PICNIC_BASKET1` contains 6 `CROISSANTS`, 3 `JAMS`, and 1 `DJEMBES`, while `PICNIC_BASKET2` contains 4 `CROISSANTS` and 2 `JAMS`.

#### `CROISSANTS` has a position limit of `250`, `JAMS` has a position limit of `350`, `DJEMBES` has a position limit of `60`, `PICNIC_BASKET1` has a position limit of `60`, and `PICNIC_BASKET2` has a position limit of `100`.

#### We used a similar strategy for the `CROISSANTS`, `JAMS`, and `DJEMBES`, using the average of the `sell_order_history` for our buy and sell offsets alongside some offsets to ideally allow buying at lower prices and selling at higher prices. For the thresholds to sell, we used the same adaptable offset calculations that were used for `SQUID_INK`.

```python
# In round_2.py

if product == "CROISSANTS":
    acceptable_buy_price = get_average(sell_order_history[product]) - 4
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset

if product == "DJEMBES":
    acceptable_buy_price = get_average(sell_order_history[product]) - 4
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset

if product == "JAMS":
    acceptable_buy_price = get_average(sell_order_history[product]) - 4
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset
```

#### We also used a similar strategy for `PICNIC_BASKET1` and `PICNIC_BASKET2`, however, instead of using the `sell_order_history` of `PICNIC_BASKET1` and `PICNIC_BASKET2`, we broke the baskets down into the individual products they contained. The thresholds for `PICNIC_BASKET1` would be calculated by summing the `sell_order_history` average of `CROISSANTS` multiplied by 6, the `sell_order_history` average of `JAMS` multiplied by 3, and the `sell_order_history` average of `DJEMBES`. The thresholds for `PICNIC_BASKET2` would be calculated by summing the `sell_order_history` average of `CROISSANTS` multiplied by 4 and the `sell_order_history` average of `JAMS` multiplied by 2.

```python
# In round_2.py

if product == "PICNIC_BASKET1":
    croissants = (get_average(sell_order_history["CROISSANTS"])) * 6
    jams = (get_average(sell_order_history["JAMS"])) * 3
    djembe = get_average(sell_order_history["DJEMBES"])

    acceptable_buy_price = croissants + jams + djembe - 5
    acceptable_sell_price = acceptable_buy_price + sell_offset

if product == "PICNIC_BASKET2":
    croissants = (get_average(sell_order_history["CROISSANTS"])) * 4
    jams = (get_average(sell_order_history["JAMS"])) * 2

    acceptable_buy_price = croissants + jams - 5
    acceptable_sell_price = acceptable_buy_price + sell_offset
```

#### We also attempted to add "crash detectors" that can be used to warn the algorithm of an incoming crash. We discussed two possible "crash detectors" to implement:
1. If incoming prices for a product are significantly higher than the historical average, be ready to sell everything we have for that product
2. If incoming prices for a product are significantly lower than prices some number of iterations ago (for example, 5 iterations ago), be ready to sell everything we have for that product

#### We decided that our "crash detectors" should follow the first implementation (point 1), as, while recognizing the possibility of missing the potential upsides of continuously rising trends, it would be ideal for our algorithm to be proactive rather than reactive. As a result, we added four conditions to compare incoming prices and, in the event of one of these conditions being true, signal the algorithm to sell all it currently has for a given product.

```python
# In round_2.py

# Condition 1: Sell order is slightly higher than a recent average (small-dip checker)
# Condition 2: Sell order is too high above the historical average (big-dip checker)
# Condition 3: Sell order of PICNIC_BASKET1 and PICNIC_BASKET2 is slightly higher than a recent average (small-dip checker)
# Condition 4: Sell order of DJEMBES is slightly higher than a recent average (small-dip checker)
# Condition 5 (not used): Sell order is too low vs 5 sell orders ago

# ...later in the code...
if ((condition_one or condition_two or condition_three or condition_four or condition_five) and (sell_order_history.get(product) is not None)):
    # Sell everything for that product
```

#### We also attempted to work with the current positions and position limits of the products, however, due to time constraints, we were not able to implement relevant functionality that we found meaningful. We were able to begin implementation to track current positions for our products, and store these values in `traderData` for future iterations.

```python
# In round_2.py

current_positions = {}

if state.traderData != "":
    order_histories = convert_trading_data(state.traderData)
    # ...
    current_positions = order_histories[2]

# ...

position = 0
    if current_positions.get(product) is not None:
        position = current_positions[product]
    else:
        current_positions[product] = 0

# ...

if int(best_bid) > acceptable_sell_price:
    # Sell some of the product
    # ...
    position -= best_bid_amount

# ...

newData = []
# ...
newData.append(current_positions)

# String value holding Trader state data required. 
# It will be delivered as TradingState.traderData on next execution.
traderData = str(newData)
```

#### Regarding the previous products in Round 1, we attempted to make our algorithm more adaptable by uncommenting our `sell_order_history` averages, allowing the buy and sell thresholds of `RAINFOREST_RESIN`, `KELP`, and `SQUID_INK` to be mainly influenced by previous sell orders; we left hardcoded offsets for some of the thresholds, however. We hope that this change will allow our algorithm to perform in more scenarios than if we solely relied on hardcoded values, despite their performance in Round 1.

```python
# In round_2.py

if product == "RAINFOREST_RESIN":
    acceptable_buy_price = get_average(sell_order_history[product]) - 1   # Influenced by sell_order_history, -1 is still hardcoded
    acceptable_sell_price = get_average(sell_order_history[product]) + 1  # Influenced by sell_order_history, -1 is still hardcoded

if product == "KELP":
    acceptable_buy_price = get_average(sell_order_history[product])       # Influenced by sell_order_history
    acceptable_sell_price = get_average(sell_order_history[product]) + 3  # Influenced by sell_order_history, -3 is still hardcoded
```

#### These are the results of our Round 2 algorithm:

![round_2_algorithm_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_2_algorithm_results_1.gif)
![round_2_algorithm_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_2_algorithm_results_2.gif)

#### ^^ Currently, we suspect a possible reason for this downward trend in profit could be due to faulty "crash detector" logic or implementation or both.

### Manual Trading
#### As mentioned in [Round 2 of the wiki](https://imc-prosperity.notion.site/Round-2-19ee8453a09381a580cdf9c0468e9bc8), the manual trading challenge for Round 2 presented 10 shipping containers, each of which contains a base amount of 10,000 SeaShells, a set multiplier, and some number of inhabitants — all of which will be used to calculate the final amount of SeaShells. The final amount of SeaShells awarded by a crate will also depend on the percentage of participants who choose the crate. The 10 shipping containers are presented below, with each table element (except the empty elements) representing a crate:

| x80 Multiplier, 6 Inhabitants  | x37 Multiplier, 6 Inhabitants |                               |
|:------------------------------:|:-----------------------------:|:-----------------------------:|
| x10 Multiplier, 1 Inhabitant   | x31 Multiplier, 2 Inhabitants | x17 Multiplier, 1 Inhabitant  |
| x90 Multiplier, 10 Inhabitants | x50 Multiplier, 4 Inhabitants |                               |
| x20 Multiplier, 2 Inhabitants  | x73 Multiplier, 4 Inhabitants | x89 Multiplier, 8 Inhabitants |

#### The formula for the final amount of SeaShells awarded by the crate is as follows:
#### $\text{Final Amount}=\frac{10,000 * \text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}$

#### ^^ As an example, if we pick the crate on the top left of the table (x80 Multiplier, 6 Inhabitants). If, at the end of the round, we find that 5% of the participants picked this crate, the amount of SeaShells awarded to us from this crate would be:
#### $\text{Final Amount}=\frac{10,000 * 80}{6 + (0.05 * 100)}=\frac{800,000}{6 + 5}=\frac{800,000}{11}\approx72727.2727\text{ SeaShells}$

#### In this manual trading challenge, we may open up to 2 shipping containers, with the first container being free to pick, and the second container costing an initial fee of 50,000 SeaShells. Our goal is to award ourselves with the most number of SeaShells possible from these crates.

#### Given that the first crate is free to pick, we focused on the possibility of picking a second crate, which is riskier due to its initial 50,000 SeaShell fee. In order for a second crate to be profitable, the final amount of SeaShells it awards to us would need to have at least 50,000 to offset the initial fee. In other words:
#### $\frac{10,000 * \text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}\ge50,000$

#### Rearranging the equation gives us:
#### $10,000 * \frac{\text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}\ge50,000$
#### $\frac{\text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}\ge\frac{50,000}{10,000}$
#### $\frac{\text{Multiplier}}{\text{Inhabitants} + (\text{Participant Pick Percentage} * 100)}\ge5$

#### We interpreted this to mean that the initial multiplier of the crate will be divided by the sum of the number of inhabitants and the participant pick percentage. This quotient will be the "final multiplier" that multiplies with the crate's base amount of 10,000 SeaShells to get the final amount of SeaShells awarded. As a result, we would want the "final multiplier" of the second crate to be greater than or equal to 5 to offset the initial fee of 50,000 SeaShells.

#### With all variables given to us except for the participant pick percentage, we can calculate the maximum participant pick percentage allowed for a crate to have a "final multiplier" of 5. Using [round_2_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/round_2/round_2_manual_trading.py), we found the following maximums for the crates:

![round_2_manual_code_output](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_2_manual_code_output.jpg)
#### ^^ It is worth noting that adding these percentages up yields 58.4%, meaning that it is highly likely that most, if not all, of these crates will not be profitable as a second choice, depending on how the other 41.6% of crate picks are distributed.

#### After some discussion, we eventually decided to pick 2 crates, well aware of the risks of a second crate:
1. x80 Multiplier, 6 Inhabitants
2. x31 Multiplier, 2 Inhabitants

#### We chose the (x80 Multiplier, 6 Inhabitants) crate because we assume more participants would choose the (x90 Multiplier, 10 Inhabitants), (x89 Multiplier, 8 Inhabitants), and (x73 Multiplier, 4 Inhabitants) crates. Hence, we hoped that the maximum participant pick percentage of 10% was feasible. We chose the (x31 Multiplier, 2 Inhabitants) crate because we wanted to pick a crate that had a lower multiplier, and we guessed that the (x10 Multiplier, 1 Inhabitant), (x20 Multiplier, 2 Inhabitants), (x17 Multiplier, 1 Inhabitant), (x37 Multiplier, 3 Inhabitants), and (x50 Multiplier, 4 Inhabitants) crates would have their maximum participant pick percentages exceeded.

#### These are the results of our Round 2 manual trading challenge:

![round_2_manual_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_2_manual_results_1.gif)
![round_2_manual_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_2_manual_results_2.jpg)

#### Both of our crates awarded us with around 33,000 to 34,000 SeaShells each. With an initial fee of 50,000 SeaShells for the second crate, it seems that we would have finished the manual trading challenge with more SeaShells if we had only chosen one crate. It is also worth nothing that the final distribution of crate picks was provided to us in [Round 4 of the wiki](https://imc-prosperity.notion.site/Round-4-19ee8453a0938112aa5fd7f0d060ffe6):

![round_2_manual_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_2_manual_results_3.jpg)

#### ^^ Only the (x10 Multiplier, 1 Inhabitant) and (x20 Multiplier, 2 Inhabitants) crates ended up being profitable as second choices, which we did not expect, as we assumed that they would have had enough picks to have their maximum participant pick percentages exceeded; overall, these crates seemed to risky for us to choose at the time, so a more likely change we could have made to increase our profit is to only choose one crate and forgo the second crate and the 50,000 SeaShell fee.
</details>

---
<details>
<summary><h2>Round 3 🌋</h2></summary>

### Algorithmic Trading
#### As mentioned in [Round 3 of the wiki](https://imc-prosperity.notion.site/Round-3-19ee8453a093811082dbcdd1f6c1cd0f), Round 3 introduced us to the following six tradable products: `VOLCANIC_ROCK_VOUCHER_9500`, `VOLCANIC_ROCK_VOUCHER_9750`, `VOLCANIC_ROCK_VOUCHER_10000`, `VOLCANIC_ROCK_VOUCHER_10250`, `VOLCANIC_ROCK_VOUCHER_10500`, and `VOLCANIC_ROCK`. `VOLCANIC_ROCK_VOUCHER_9500`, `VOLCANIC_ROCK_VOUCHER_9750`, `VOLCANIC_ROCK_VOUCHER_10000`, `VOLCANIC_ROCK_VOUCHER_10250`, and `VOLCANIC_ROCK_VOUCHER_10500` are vouchers that grant us the ability to buy `VOLCANIC_ROCK` at a given price; this price is called the strike price, which we guessed meant that, for example, `VOLCANIC_ROCK_VOUCHER_9500` allows us to buy `VOLCANIC_ROCK` at 9,500 SeaShells. These vouchers also have expiration dates, however it seems that their expiration dates outlast all 5 rounds of the IMC Prosperity 3 competition, meaning that we do not need to worry about expiration dates for this year's competition; expiration dates may ceratinly be a factor in next year's competition, however.

#### The position limit for `VOLCANIC_ROCK` is `400`, the position limit for `VOLCANIC_ROCK_VOUCHER_9500` is `200`, the position limit for `VOLCANIC_ROCK_VOUCHER_9750` is `200`, the position limit for `VOLCANIC_ROCK_VOUCHER_10000` is `200`, the position limit for `VOLCANIC_ROCK_VOUCHER_10250` is `200`, the position limit for `VOLCANIC_ROCK_VOUCHER_10500` is `200`.

#### Tyler Thomas quickly pointed out that the vouchers to buy `VOLCANIC_ROCK` are similar to real-life options in trading. Due to inexperience and time constraints, we were not able to implement a meaningful strategy to trade the vouchers and `VOLCANIC_ROCK` as if they were options, at least to our knowledge. Instead, we traded the vouchers and `VOLCANIC_ROCK` as tradable products:

``` python
# In round_3.py

if product == "VOLCANIC_ROCK":
    acceptable_buy_price = get_average(sell_order_history[product]) - sell_offset
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset

if product == "VOLCANIC_ROCK_VOUCHER_9500":
    acceptable_buy_price = get_average(sell_order_history[product]) - sell_offset
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset

if product == "VOLCANIC_ROCK_VOUCHER_9750":
    acceptable_buy_price = get_average(sell_order_history[product]) - sell_offset
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset

if product == "VOLCANIC_ROCK_VOUCHER_10000":
    acceptable_buy_price = get_average(sell_order_history[product]) - sell_offset
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset

if product == "VOLCANIC_ROCK_VOUCHER_10250":
    acceptable_buy_price = get_average(sell_order_history[product]) - sell_offset
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset

if product == "VOLCANIC_ROCK_VOUCHER_10500":
    acceptable_buy_price = get_average(sell_order_history[product]) - sell_offset
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset
```

#### We also attempted to tweak the "crash detectors" to be less sensitive, as we suspected that the "crash detectors" may have signaled our algorithm to sell everything for a given product too frequently, especially at lower prices. In addition, we changed the `sell_offset` calculations to only include the most recent sell order and the 10th (previously 100th) most recent sell order.

```python
# In round_3.py

index_one = 0
index_two = 10
if len(sell_order_history[product]) < (index_two + 1):
    index_two = len(sell_order_history[product]) - 1

sell_offset = (sell_order_history[product][index_one] - sell_order_history[product][index_two]) / 3
if sell_offset < 0:
    sell_offset *= -1
```

#### These are the results of our Round 3 algorithm:

![round_3_algorithm_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_3_algorithm_results_1.gif)
![round_3_algorithm_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_3_algorithm_results_2.gif)

#### ^^ We suspect that possible reasons for this downward trend could include faulty logic and implementation for trading vouchers and `VOLCANIC_ROCK`, and continued faulty implementation for our "crash detectors".

### Manual Trading
#### As mentioned in [Round 3 of the wiki](https://imc-prosperity.notion.site/Round-3-19ee8453a093811082dbcdd1f6c1cd0f), the manual trading challenge for Round 3 presents us with an opportunity to trade Flippers with a group of Sea Turtles. Our goal is to offer 2 bids for Flippers that are at the best price for the Sea Turtles to accept; we think that it is not required to place 2 bids, however it is encouraged to place 2 bids. For these bids, each of the Sea Turtles will accept the lowest bid that is over their price, which can range from 160 to 200, and from 250 to 320. For our second bid, the Sea Turtles will trade if our bid is higher than the average of all second bids from all participants; if our bid is lower than the average of all second bids from all participants, then the probability of a Sea Turtle trading with us will be decreased. After these trades are made, we are able to sell our Flippers for 320 SeaShells each.

#### This round's manual trading challenge was mostly done by Tyler Thomas, in which he applied a Monte Carlo Simulation to find ideal bid amounts, and adjusted these numbers to be more conservative.

#### These are the results of our Round 3 manual trading challenge:

![round_3_manual_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_3_manual_results_1.gif)
![round_3_manual_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_3_manual_results_2.jpg)
![round_3_manual_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_3_manual_results_3.gif)

#### ^^ It seems that both of our bids were higher than the participant averages, which might have meant that we were more likely to receive trades with the Sea Turtles and hence acquire more Flippers to sell.
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
        <td>1022</td>
        <td>715</td>
        <td>1121</td>
        <td>293</td>
    </tr>
    <tr align="center">
        <td>Round 2</td>
        <td>2971</td>
        <td>1508</td>
        <td>2764</td>
        <td>815</td>
    </tr>
    <tr align="center">
        <td>Round 3</td>
        <td>4036</td>
        <td>1298</td>
        <td>2907</td>
        <td>1013</td>
    </tr>
    <tr align="center">
        <td>Round 4</td>
        <td>3537</td>
        <td>213</td>
        <td> 2900*</td>
        <td> 956*</td>
    </tr>
    <tr align="center">
        <td>Round 5</td>
        <td>1330</td>
        <td>92</td>
        <td>2875</td>
        <td>369</td>
    </tr>
</table>

#### * This ranking was not recorded by us, and is hence estimated
