import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup

def putting_data_into_db():
	conn = sqlite3.connect('dcinside.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS dcinside (title TEXT, writer TEXT, ip TEXT, date TEXT, views TEXT, recommend TEXT)')
	conn.commit()
	conn.close()

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
		#print("추천수: ", recommend)



def crawl_pages(url, num_pages):
	for page in range(1, num_pages + 1):
		current_url = f"{url}/?id={params['id']}&page={page}"
		response = requests.get(current_url, headers=headers)
		if response.status_code == 200:
			soup = BeautifulSoup(response.content, 'html.parser')
			contents = soup.find('tbody').find_all('tr')
			process_data(contents)
		else:
			print(f"Failed to fetch page {page}")


BASE_URL = "https://gall.dcinside.com/board/lists"
params={
	'id': 'bitcoins_new1',
}
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
}
num_pages = 50
crawl_pages(BASE_URL, num_pages)