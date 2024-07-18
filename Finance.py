
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Configure Seaborn style
sns.set(style='whitegrid')

# Extract historical data for RY (Royal Bank of Canada) for the last year
ticker = yf.Ticker("RY") #If you want to see another ticket, just change it here. An example is Tellus; you just need to replace RY with T.
data = ticker.history(period="1y")

# Plot a line chart for closing prices
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Close'], label='Close Price')
plt.title('RY Closing Prices (Last Year)')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.legend()
plt.show()

# Additional analysis: Calculate the 50-day moving average
data['50_MA'] = data['Close'].rolling(window=50).mean()

# Plot a line chart for closing prices and the 50-day moving average
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Close'], label='Close Price')
plt.plot(data.index, data['50_MA'], label='50-Day MA', color='orange')
plt.title('RY Closing Prices and 50-Day Moving Average (Last Year)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Additional analysis: Plot trading volume
plt.figure(figsize=(14, 7))
plt.bar(data.index, data['Volume'], label='Volume', color='skyblue')
plt.title('RY Trading Volume (Last Year)')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.legend()
plt.show()

# Additional analysis: Calculate daily returns
data['Daily_Return'] = data['Close'].pct_change()

# Plot a line chart for daily returns
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Daily_Return'], label='Daily Return', color='purple')
plt.title('RY Daily Returns (Last Year)')
plt.xlabel('Date')
plt.ylabel('Daily Return')
plt.legend()
plt.show()

# Print some descriptive statistics
print("Descriptive Statistics of Daily Returns:")
print(data['Daily_Return'].describe())
