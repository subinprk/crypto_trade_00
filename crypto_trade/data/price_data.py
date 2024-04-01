
import	pandas as pd
import	sqlite3
import	ccxt

def price_database(_symbol, _db_name, _table_name):
	binance = ccxt.binance()
	timeframe = '15m'
	timestart = binance.parse8601('2024-03-18 00:00:00')
	symbol = _symbol
	db_name = _db_name
	table_name = _table_name
	conn = sqlite3.connect(db_name)

	eth_ohlcv = binance.fetch_ohlcv(symbol, timeframe, since=timestart, limit=1000)
	df = pd.DataFrame(eth_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
	df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
	df.set_index('timestamp', inplace=True)
	df.to_sql(table_name, conn, if_exists='replace', index=True)
	while True:
		timestart = eth_ohlcv[-1][0]
		eth_ohlcv = binance.fetch_ohlcv(symbol, timeframe, since=timestart, limit=1000)
		df = pd.DataFrame(eth_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
		df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
		df.set_index('timestamp', inplace=True)
		df.to_sql(table_name, conn, if_exists='append', index=True)
		if len(eth_ohlcv) != 1000 :
			break

	cursor = conn.cursor()
	cursor.execute('SELECT * FROM ' + table_name)
	#rows = cursor.fetchall()
	#print(rows[0:5])

	conn.close()


price_database('ETH/USD', 'eth.db', 'eth_usd_15m')
price_database('BTC/USD', 'btc.db', 'btc_usd_15m')
price_database('DOG/USD', 'dog.db', 'dog_usd_15m')