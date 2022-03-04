from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime


url = 'https://novaposhta.ua/news/rubric/2/id/10171'
r = requests.get(url)
html = bs(r.content, 'html.parser')

select = html.select('.text > p > a')

local_file = f'schedule-{datetime.now().strftime("%Y-%m-%d")}.xlsx'

for link in select:
    xlsx_np = link.attrs['href']
    data = requests.get(xlsx_np)
    with open(f'data/{local_file}', 'wb') as file:
        file.write(data.content)
