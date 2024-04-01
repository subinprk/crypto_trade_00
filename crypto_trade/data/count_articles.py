import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup

def putting_data_into_db(data, conn, table_name):
	df = pd.DataFrame(list(zip(*data)), columns=['title', 'writer', 'ip', 'date', 'views', 'recommend'])
	if pd.to_numeric(df['date'], errors='coerce').notna().all():
		# If the date column contains numeric values, cast them to float and convert to datetime
		df['date'] = pd.to_datetime(df['date'].astype(float), unit='ms')
	else:
		# If the date column contains datetime strings, convert to datetime without the unit parameter
		df['date'] = pd.to_datetime(df['date'])
	
	df.set_index('date', inplace=True)
	df.to_sql(table_name, conn, if_exists='append', index=True)


def process_data(contents):
	for i in contents:
		if i == 0 or i == 1: # 0, 1번째 글은 공지사항이므로 제외
			continue
		title_tag = i.find('a')
		title = title_tag.text
		writer_tag = i.find('td', class_='gall_writer ub-writer').find('span', class_='nickname')
		if writer_tag is not None: # None 값이 있으므로 조건문을 통해 회피 
			writer = writer_tag.text
		else:
			writer = "Nan"
		ip_tag = i.find('td', class_='gall_writer ub-writer').find('span', class_='ip')
		if ip_tag is not None:  # None 값이 있으므로 조건문을 통해 회피 
			ip = ip_tag.text
		else:
			ip = "Nan"
		date_tag = i.find('td', class_='gall_date')
		date_dict = date_tag.attrs
		if len(date_dict) == 2:
			date = date_dict['title']
		else:
			date = date_tag.text
		views_tag = i.find('td', class_='gall_count')
		views = views_tag.text
		recommend_tag = i.find('td', class_='gall_recommend')
		recommend = recommend_tag.text
		return title, writer, ip, date, views, recommend



def crawl_pages(url, num_pages):
	conn = sqlite3.connect(DB_NAME)
	df = pd.DataFrame()
	for page in range(1, num_pages + 1):
		current_url = f"{url}/?id={params['id']}&page={page}"
		response = requests.get(current_url, headers=headers)
		if response.status_code == 200:
			soup = BeautifulSoup(response.content, 'html.parser')
			contents = soup.find('tbody').find_all('tr')
			data = process_data(contents)
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