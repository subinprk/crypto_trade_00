
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

conn = sqlite3.connect('eth.db')
cursor = conn.cursor()

cursor.execute('SELECT timestamp, open FROM eth_usd_15m')
rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=['timestamp', 'open'])
plt.figure(figsize=(14, 7))
plt.title('ETH/USD 15m')
plt.xlabel('Time')
plt.ylabel('Open Price')

plt.plot_date(df['timestamp'], df['open'], '-')
plt.show()

conn.close()
