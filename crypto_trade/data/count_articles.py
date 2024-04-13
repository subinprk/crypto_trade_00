import sqlite3
import pandas as pd
import requests
import count_articles_data_process as cadp
from bs4 import BeautifulSoup

def putting_data_into_db(data, conn, table_name):
	for i in data:
		print(i)
		df = pd.DataFrame(i, columns=['title', 'writer', 'ip', 'date', 'views', 'recommend'])
		if pd.to_numeric(df['date'], errors='coerce').notna().all():
			# If the date column contains numeric values, cast them to float and convert to datetime
			df['date'] = pd.to_datetime(df['date'].astype(float), unit='ms')
		else:
			# If the date column contains datetime strings, convert to datetime without the unit parameter
			df['date'] = pd.to_datetime(df['date'])
		print("			", df['date'], df['title'], df['ip'])
		df.set_index('date', inplace=True)
		df.to_sql(table_name, conn, if_exists='append', index=True)

def crawl_pages(url, num_pages):
	conn = sqlite3.connect(DB_NAME)
	df = pd.DataFrame()
	for page in range(1, num_pages + 1):
		current_url = f"{url}/?id={params['id']}&page={page}"
		response = requests.get(current_url, headers=headers)
		if response.status_code == 200:
			soup = BeautifulSoup(response.content, 'html.parser')
			contents = soup.find('tbody').find_all('tr')
			#print(contents, "\n")
			data = cadp.process_data(contents)
			putting_data_into_db(data, conn, TABLE_NAME)
		else:
			print(f"Failed to fetch page {page}")
	conn.close()

DB_NAME = 'dcinside.db'
TABLE_NAME = 'dcinside_bitcoin'
BASE_URL = "https://gall.dcinside.com/board/lists"
params={
	'id': 'bitcoins_new1',
}
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
}
NUM_PAGES = 50
crawl_pages(BASE_URL, NUM_PAGES)