
import requests
from bs4 import BeautifulSoup

#resp = requests.get(BASE_URL, params=params, headers=headers)
# resp.content
# soup = BeautifulSoup(resp.content, 'html.parser')
# contents = soup.find('tbody').find_all('tr')
# print(contents)


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
			

def process_data(contents):
	for i in contents:
		print('-'*15)
		
		# 제목 추출
		title_tag = i.find('a')
		title = title_tag.text
		print("제목: ", title)
		
		# 글쓴이 추출
		writer_tag = i.find('td', class_='gall_writer ub-writer').find('span', class_='nickname')
		if writer_tag is not None: # None 값이 있으므로 조건문을 통해 회피 
			writer = writer_tag.text
			print("글쓴이: ", writer)
			
		else:
			print("글쓴이: ", "없음")
		
		# 유동이나 고닉이 아닌 글쓴이 옆에 있는 ip 추출
		ip_tag = i.find('td', class_='gall_writer ub-writer').find('span', class_='ip')
		if ip_tag is not None:  # None 값이 있으므로 조건문을 통해 회피 
			ip = ip_tag.text
			print("ip: ", ip)
		
		# 날짜 추출 
		date_tag = i.find('td', class_='gall_date')
		date_dict = date_tag.attrs

		if len(date_dict) == 2:
			print("날짜: ", date_dict['title'])
		
		else:
			print("날짜: ", date_tag.text)
			pass
		
		# 조회 수 추출
		views_tag = i.find('td', class_='gall_count')
		views = views_tag.text
		print("조회수: ", views)
		
		# 추천 수 추출
		recommend_tag = i.find('td', class_='gall_recommend')
		recommend = recommend_tag.text
		print("추천수: ", recommend)
		
BASE_URL = "https://gall.dcinside.com/board/lists"
params={
	'id': 'bitcoins_new1',
}
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
}
num_pages = 15
crawl_pages(BASE_URL, num_pages)