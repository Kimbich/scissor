import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set the same random number for energy and price data
re = np.random.RandomState(0)
rp = np.random.RandomState(1)
energy = re.uniform(-10, 10, size=[10, 1])
data = pd.DataFrame(energy, index=["LocalRES_Load03", "LocalRES_Load121", "LocalRES_Load13", "LocalRES_Load15",
                                   "LocalRES_Load16", "LocalRES_Load17", "LocalRES_Load19", "LocalRES_Load23",
                                   "LocalRES_Load31", "LocalRES_Load35"], columns=['Energy'])
price = re.uniform(0, 1, size=[10, 1])
data = pd.concat([data, pd.DataFrame(price, columns=['Price'], index=data.index)], axis="columns")

# Define producers and consumers
Producers = data.loc[data['Energy'] < 0].sort_values('Price', ascending=True)
Producers = abs(Producers)
Consumers = data.loc[data['Energy'] >= 0].sort_values('Price', ascending=False)

# Calculate the widths and positions based on the x-axis values for producers and consumers
widths_producers = Producers.Energy
positions_producers = np.cumsum(widths_producers) - widths_producers/2
widths_consumers = Consumers.Energy
positions_consumers = np.cumsum(widths_consumers) - widths_consumers/2

# Find the overlapping region
min_position = max(positions_producers[0], positions_consumers[0])
max_position = min(positions_producers[-1] + widths_producers[-1], positions_consumers[-1] + widths_consumers[-1])

# Calculate the intersection point
x_intersect = (min_position + max_position) / 2

# Find the price value at the intersection point
idx = np.argmin(np.abs(positions_consumers - x_intersect))
intersection_price = min(Consumers['Price'].iloc[idx], Producers['Price'].iloc[idx])

# Plotting bar figure
fig, ax = plt.subplots()

plt.bar(positions_producers, Producers['Price'], color='g', label='Producers', alpha=0.25, width=widths_producers)
plt.bar(positions_consumers, Consumers['Price'], color='r', label='Consumers', alpha=0.25, width=widths_consumers)

# Add step plots with precise widths
plt.step(np.append(positions_producers - widths_producers / 2, positions_producers[-1] + widths_producers[-1] / 2),
         np.append(Producers['Price'], Producers['Price'].iloc[-1]),
         color='g', label='Producers', alpha=0.25, where='post')
plt.step(np.append(positions_consumers - widths_consumers / 2, positions_consumers[-1] + widths_consumers[-1] / 2),
         np.append(Consumers['Price'], Consumers['Price'].iloc[-1]),
         color='r', label='Consumers', alpha=0.25, where='post')

# Add vertical line to represent the intersection point
plt.axvline(x=x_intersect, color='blue', linestyle='--', label='Intersection')

# Add text for the intersection price
plt.text(x_intersect, intersection_price, f'{intersection_price:.2f}',
         ha='center', va='bottom', color='blue')

# Add x-axis values on top of the bars
for i, val in enumerate(Producers['Energy']):
    ax.text(positions_producers[i], Producers['Price'].iloc[i], f'{val:.2f}', ha='center', va='bottom')
for i, val in enumerate(Consumers['Energy']):
    ax.text(positions_consumers[i], Consumers['Price'].iloc[i], f'{val:.2f}', ha='center', va='bottom')

# Add label to the axis
plt.xticks(np.concatenate((positions_consumers, positions_producers)),
           np.concatenate((Consumers.index, Producers.index)), rotation=90, ha='center', size=8)
for i, val in enumerate(ax.get_xticklabels()):
    household = val.get_text()
    if household in Consumers.index:
        val.set_color('r')  # Set color for consumers
    else:
        val.set_color('g')
ax.set_xlabel('Name of the household')
ax.set_ylabel('Price (€/kWh)')
ax.set_title('Merit Order Effect')
ax.xaxis.set_label_coords(1, -0.03)
ax.grid(linestyle='--')
ax.legend()

# Create a second x-axis
ax1 = ax.twiny()
ax1.set_xlim(ax.get_xlim())
ax1.set_xlabel('Volume (kWh)')
ax1.xaxis.set_label_coords(1, 1.03)
ax1.grid(linestyle=':')

plt.show()

# Show market clearing price from merit order method
print("The Market Clearing Price is at %f kWh with the price at %f €" % (x_intersect, intersection_price))
# Find which producers and customers are able to join the market
Producers_in_P2Ptrading = Producers[Producers['Price'] < intersection_price]
Consumers_in_P2Ptrading = Consumers.loc[Consumers['Price'] > intersection_price]
Household_in_P2Ptrading = pd.concat([Producers_in_P2Ptrading, Consumers_in_P2Ptrading], axis=0)