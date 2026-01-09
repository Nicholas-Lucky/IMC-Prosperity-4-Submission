# Snowballs = 0
# Pizzas = 1
# Silicon Nuggets = 2
# SeaShells = 3

table = [[1, 1.45, 0.52, 0.72],
         [0.7, 1, 0.31, 0.48],
         [1.95, 3.1, 1, 1.49],
         [1.34, 1.98, 0.64, 1]]

class ManualTrade:
    def __init__(self, prev_history=[], prev_revenue=500000):
        self.history = []
        for item in prev_history:
            self.history.append(item)
        
        self.revenue = prev_revenue
    
    def __repr__(self):
        return f"ManualTrade({self.history})"

    def add_to_history(self, item_index):
        self.revenue *= table[self.history[-1]][item_index]
        self.history.append(item_index)
    
    def getHistory(self):
        return self.history

    def printHistory(self):
        for i, itemIndex in enumerate(self.history):
            itemName = "Snowballs"

            if itemIndex == 1:
                itemName = "Pizzas"
            elif itemIndex == 2:
                itemName = "Silicon Nuggets"
            elif itemIndex == 3:
                itemName = "SeaShells"
            
            if i != 0:
                print(f"{itemName}", end="\n")

                if i != len(self.history) - 1:
                    print(f"{itemName} -> ", end="")
            
            else:
                print(f"{itemName} -> ", end="")
        print()
        print(f"Total Revenue: {self.revenue}")

def getMaxTrade(trades):
    currentMax = 0
    maxIndex = -1

    for i, trade in enumerate(trades):
        if trade.revenue > currentMax:
            currentMax = trade.revenue
            maxIndex = i
    
    return trades[maxIndex]

starting_amount = 500000
starting_index = 3
ending_index = 3
num_trades = 5
num_item_choices = 4

trades = [ManualTrade([starting_index], starting_amount)]

for i in range(num_trades):
    this_levels_trades = []

    for trade in trades:
        for j in range(num_item_choices):
            newTrade = ManualTrade(trade.getHistory(), trade.revenue)

            if i == (num_trades - 1):
                newTrade.add_to_history(ending_index)

            else:
                newTrade.add_to_history(j)
            
            this_levels_trades.append(newTrade)
    
    trades = this_levels_trades

maxTrade = getMaxTrade(trades)
print()
maxTrade.printHistory()
print()
print(maxTrade.getHistory())