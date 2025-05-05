import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Assuming the data is loaded as a pandas DataFrame named 'data'
# The 'Date' column needs to be converted to datetime type, and the data needs to be sorted by date.

# Load your data (ensure 'Date' is in datetime format)
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Calculate the Triple EMA (10, 50, 100)
data['EMA_10'] = data['Close'].ewm(span=10, adjust=False).mean()
data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
data['EMA_100'] = data['Close'].ewm(span=100, adjust=False).mean()

# Initialize columns to hold Buy and Sell signals
data['Buy_Signal'] = 0
data['Sell_Signal'] = 0

# Create Buy Signal: when 10-period EMA crosses above 50-period EMA and both are above 100-period EMA
data['Buy_Signal'][((data['EMA_10'] > data['EMA_50']) & (data['EMA_50'] > data['EMA_100']))] = 1

# Create Sell Signal: when 10-period EMA crosses below 50-period EMA and both are below 100-period EMA
data['Sell_Signal'][((data['EMA_10'] < data['EMA_50']) & (data['EMA_50'] < data['EMA_100']))] = 1

# Backtest the strategy
capital = 100000  # starting capital
position = 0
buy_price = 0
sell_price = 0
trade_log = []

# Loop through the data and track buy/sell positions
for i in range(1, len(data)):
    if data['Buy_Signal'][i] == 1 and position == 0:
        # Buy Signal
        position = capital / data['Close'][i]  # Number of shares to buy
        buy_price = data['Close'][i]
        trade_log.append(('Buy', data.index[i], buy_price))
    
    elif data['Sell_Signal'][i] == 1 and position > 0:
        # Sell Signal
        capital = position * data['Close'][i]  # Value of position when sold
        sell_price = data['Close'][i]
        trade_log.append(('Sell', data.index[i], sell_price))
        position = 0  # Reset position

# If position is still open, sell at the last price
if position > 0:
    capital = position * data['Close'].iloc[-1]
    trade_log.append(('Sell', data.index[-1], data['Close'].iloc[-1]))

# Final capital after backtest
final_capital = capital

# Calculate profit/loss
profit_loss = final_capital - 100000  # Assuming the starting capital was $100,000

# Print results
print(f"Final Capital: {final_capital}")
print(f"Profit/Loss: {profit_loss}")
print(f"Number of Trades: {len(trade_log)//2}")
print(f"Trade Log: {trade_log}")

# Plotting the strategy
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['EMA_10'], label='EMA 10', alpha=0.7)
plt.plot(data['EMA_50'], label='EMA 50', alpha=0.7)
plt.plot(data['EMA_100'], label='EMA 100', alpha=0.7)

buy_signals = [trade[1] for trade in trade_log if trade[0] == 'Buy']
buy_prices = [trade[2] for trade in trade_log if trade[0] == 'Buy']
sell_signals = [trade[1] for trade in trade_log if trade[0] == 'Sell']
sell_prices = [trade[2] for trade in trade_log if trade[0] == 'Sell']

plt.scatter(buy_signals, buy_prices, marker='^', color='g', label='Buy Signal', alpha=1)
plt.scatter(sell_signals, sell_prices, marker='v', color='r', label='Sell Signal', alpha=1)

plt.legend()
plt.title('Triple EMA Crossover Strategy (10/50/100)')
plt.show()