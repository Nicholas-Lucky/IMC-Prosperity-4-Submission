import matplotlib.pyplot as plt
import numpy as np

def plot_round_2_curve():
    round2_xpoints = np.array([10, 17, 20, 31, 37, 50, 73, 80, 89, 90])
    round2_ypoints = np.array([0.998, 7.539, 1.614, 6.987, 5.118, 8.516, 24.060, 18.178, 15.184, 11.807])

    # Attempt to scale the round 2 results to our round 4 curve, as round 2 would understandably have higher values with fewer options
    #scale_round_2_to_round_2(round2_xpoints, round2_ypoints)

    plt.plot(round2_xpoints, round2_ypoints, marker = 'o', label = "Round 2 Crates")

    for index, element in enumerate(round2_xpoints):
        plt.annotate(f"Crate {round2_xpoints[index]}", (round2_xpoints[index], round2_ypoints[index]), fontsize = 7)
    
    round4_idealxpoints = np.array([10, 17, 20, 23, 30, 31, 37, 40, 41, 47, 50, 60, 70, 73, 79, 80, 83, 89, 90, 100])
    round4_idealypoints = np.array([1, 2.4, 2, 2.599, 4, 4.2, 4.4, 5, 5.199, 6.4, 6, 8, 10, 10.6, 10.8, 10, 9.6, 9.8, 8, 5])
    plt.plot(round4_idealxpoints, round4_idealypoints, marker = 'x', label = "Round 4 Suitcases (ideal %)")

    for index, element in enumerate(round4_idealxpoints):
        plt.annotate(f"Suitcase {round4_idealxpoints[index]}", (round4_idealxpoints[index], round4_idealypoints[index]), fontsize = 7)

    plt.title("Round 2 (RAW values) vs Round 4 (IDEAL)", loc='center', fontdict={'fontsize': 16, 'fontweight': 'bold'}, pad = 25)
    #plt.title("Round 2 (SCALED values) vs Round 4 (IDEAL)", loc='center', fontdict={'fontsize': 16, 'fontweight': 'bold'}, pad = 25)

    plt.xlabel("Initial Multiplier")
    plt.ylabel("% picked by players")
    leg = plt.legend(loc='upper left')

    plt.show()

def scale_round_2_to_round_2(x_array, y_array):
    for i, j in enumerate(x_array):
        x_array[i] = (j * 10) / 9

    # Previously y_array[i] = (j * 5) / 11.807
    # Now j / 2 because we're guessing that with 2x more options, a Round 4 suitcase will have half as many picks as a Round 2 crate
    for i, j in enumerate(y_array):
        y_array[i] = (j / 2)

class Suitcase:
    def __init__(self, initial_multiplier, contestants):
        self.initial_multiplier = initial_multiplier
        self.contestants = contestants
    
    def get_max_percentage(self, target_multiplier):
        return (self.initial_multiplier / target_multiplier) - self.contestants
    
    def __repr__(self):
        return f"Suitcase({self.initial_multiplier}, {self.contestants})"

def sort_by_percent(suitcases, max_percent_to_be_profitable):
    for i in range(0, len(suitcases) - 1):
        for j in range(0, len(suitcases) - 1 - i):
            if suitcases[j].get_max_percentage(max_percent_to_be_profitable) > suitcases[j + 1].get_max_percentage(max_percent_to_be_profitable):
                temp = suitcases[j]
                suitcases[j] = suitcases[j + 1]
                suitcases[j + 1] = temp

max_percent_to_be_profitable = 5
suitcases = [Suitcase(80, 6), Suitcase(50, 4), Suitcase(83, 7), Suitcase(31, 2), Suitcase(60, 4),
             Suitcase(89, 8), Suitcase(10, 1), Suitcase(37, 3), Suitcase(70, 4), Suitcase(90, 10),
             Suitcase(17, 1), Suitcase(40, 3), Suitcase(73, 4), Suitcase(100, 15), Suitcase(20, 2),
             Suitcase(41, 3), Suitcase(79, 5), Suitcase(23, 2), Suitcase(47, 3), Suitcase(30, 2)]

sort_by_percent(suitcases, max_percent_to_be_profitable)
percent_sum = 0.0

print(f"MAX % of people needed for suitcase to be profitable (final multiplier of at least {max_percent_to_be_profitable}x):")
print("Note: Order is lowest to highest, and formatting is Suitcase(multiplier, contestants)")
for suitcase in suitcases:
    max_percentage = suitcase.get_max_percentage(max_percent_to_be_profitable)
    print(f"{suitcase}: {max_percentage}%")

    if max_percentage >= 0:
        percent_sum += max_percentage

print(f"Sum of the max percentages (excluding negative percentages) ^^ = {percent_sum}%")

# Plot stuff
plot_round_2_curve()