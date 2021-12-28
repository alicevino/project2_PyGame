import yfinance as yf
import matplotlib.pyplot as plt


data = yf.download('TSM', '2021-07-10', '2021-12-10')
# data['Adj Close'].plot()

close_price = data['Adj Close']

# print(close_price[0], '\n')
# for cost in close_price:
#     print(int(cost))
# print()
print(len(close_price))
print(max(close_price), min(close_price))
plt.show()

'''

# Define the ticker list
import pandas as pd
tickers_list = ['AAPL', 'WMT', 'IBM', 'MU', 'BA', 'AXP']

# Import pandas
data = pd.DataFrame(columns=tickers_list)

# Fetch the data

for ticker in tickers_list:
    data[ticker] = yf.download(ticker,'2016-01-01','2019-08-01')['Adj Close']

# Print first 5 rows of the data
data.head()

# Plot all the close prices
((data.pct_change()+1).cumprod()).plot(figsize=(10, 7))

# Show the legend
plt.legend()

# Define the label for the title of the figure
plt.title("Adjusted Close Price", fontsize=16)

# Define the labels for x-axis and y-axis
plt.ylabel('Price', fontsize=14)
plt.xlabel('Year', fontsize=14)

# Plot the grid lines
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()
'''