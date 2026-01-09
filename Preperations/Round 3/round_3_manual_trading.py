# Tyler's ChatGPT code
# Had to install matplotlib via "python3 -m pip install matplotlib" in the terminal/cmd window
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

num_turtles = 10000           # Number of simulated turtles
mean_reserve = 260            # Average reserve price guessed
std_reserve = 20              # Standard deviation (how spread out the reserves are)

reserve_prices = np.random.normal(loc=mean_reserve, scale=std_reserve, size=num_turtles)
reserve_prices = np.clip(reserve_prices, 0, 320)

bid_range = np.arange(200, 320, 5)
results = []

for bid in bid_range:
    fill_rate = np.mean(bid >= reserve_prices)
    profit_per_flipper = 320 - bid
    expected_profit = fill_rate * profit_per_flipper
    results.append((bid, fill_rate, expected_profit))

results = np.array(results)

plt.figure(figsize=(10, 5))
plt.plot(results[:, 0], results[:, 2], color='orange', label='Expected Profit per Turtle')
plt.xlabel("Bid Price")
plt.ylabel("Expected Profit")
plt.title("Monte Carlo Simulation: Expected Profit per Turtle vs Bid Price")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

