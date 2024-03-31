
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://gall.dcinside.com/board/lists"
params={
	'id': 'bitcoins_new1',
}
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
}
resp = requests.get(BASE_URL, params=params, headers=headers)
resp.content
soup = BeautifulSoup(resp.content, 'html.parser')
contents = soup.find_all('tbody').find_all('tr')
# print(soup.prettify())

for i in contents:
	print()