
def get_writer_and_ip(content):
	writer_tag = content.find('td', class_='gall_writer ub-writer').find('span', class_='nickname')
	if writer_tag is not None: # None 값이 있으므로 조건문을 통해 회피 
		writer = writer_tag.text
	else:
		writer = "Nan"
	ip_tag = content.find('td', class_='gall_writer ub-writer').find('span', class_='ip')
	if ip_tag is not None:  # None 값이 있으므로 조건문을 통해 회피 
		ip = ip_tag.text
	else:
		ip = "Nan"
	return writer, ip

def get_date_views_recommend(content):
	date_tag = content.find('td', class_='gall_date')
	date_dict = date_tag.attrs
	if len(date_dict) == 2:
		date = date_dict['title']
	else:
		date = date_tag.text
	views_tag = content.find('td', class_='gall_count')
	views = views_tag.text
	recommend_tag = content.find('td', class_='gall_recommend')
	recommend = recommend_tag.text
	return date, views, recommend

def process_data(contents):
	data = []
	for index, i in enumerate(contents):
		if index < 5: # 0, 1번째 글은 공지사항이므로 제외
			continue
		title_tag = i.find('a')
		title = title_tag.text[1:]
		writer, ip = get_writer_and_ip(i)
		date, views, recommend = get_date_views_recommend(i)
		data.append([title, writer, ip, date, views, recommend])
	for item in data:
		print(item)
	return data
