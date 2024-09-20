import requests
from bs4 import BeautifulSoup
import json
# 节奏榜
url='https://appmedia.jp/fategrandorder/1351236'
# def appemdia_ranking(url='https://appmedia.jp/fategrandorder/1351236'):
response = requests.get(url)
webpage_content = response.content

soup = BeautifulSoup(webpage_content, 'html.parser')


table_id = 'orbit_all'
table_class = 'display_table'

table = soup.find('table', {'id': table_id}) and soup.find('table', {'class': table_class})
table_html = str(table)
rows = soup.select('#orbit_all tr')



SVT_NAME = 'https://raw.githubusercontent.com/chaldea-center/chaldea-data/main/mappings/svt_names.json'
CE_NAME = 'https://raw.githubusercontent.com/chaldea-center/chaldea-data/main/mappings/ce_names.json'

# 翻译工具
def chaldea_translation(urls):
    results = []
    for url in urls:
        file_name = url.split('/')[-1]
        response = requests.get(url)
        webpage_content = response.json()
        with open(f'data/static/{file_name}', 'w', encoding='utf-8') as f:
            json.dump(webpage_content, f, ensure_ascii=False, indent=4)
    

# if __name__ == '__main__':
#     chaldea_translation([SVT_NAME, CE_NAME])