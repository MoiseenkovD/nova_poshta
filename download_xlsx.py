from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import re


url = 'https://novaposhta.ua/news/rubric/2/id/10171'
r = requests.get(url)
html = bs(r.content, 'html.parser')

select = html.select('.text > p a')

local_file = f'schedule-{datetime.now().strftime("%Y-%m-%d")}.xlsx'

link = select[0]

xlsx_np = link.attrs['href']
data = requests.get(xlsx_np)
res = re.search('\d+', link.text)
if res.group(0) == datetime.now().strftime('%-d'):
    with open(f'data/{local_file}', 'wb') as file:
        file.write(data.content)
