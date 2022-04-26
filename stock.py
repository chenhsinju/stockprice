import requests
from bs4 import BeautifulSoup


class Stock():
    # 個股包含以下屬性
    # 個股代號、名稱、成交價
    def __init__(self, sid, name):
        self.id = sid
        self.name = name
        self.price = None

    # 定義爬取個股資訊的函式
    def get_data(self):
        url = 'https://tw.stock.yahoo.com/q/q?s=' + self.id
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'lxml')
        # 找到你要的那個div 其下的span標籤, 並擷取標籤裡的文字
        price = soup.find('div', 'D(f) Ai(fe) Mb(4px)').span.text.strip()
        self.price = price
