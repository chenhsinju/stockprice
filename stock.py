import requests
from bs4 import BeautifulSoup


class Stock():
    # 個股包含以下屬性
    # 個股代號、名稱、月平均價、是否被選取、成交價
    def __init__(self, code, name, monthly_average_price, is_selected):
        self.code = code
        self.name = name
        self.monthly_average_price = monthly_average_price
        self.is_selected = is_selected
        self.price = None

    # 定義爬取個股資訊的函式
    def get_data(self):
        url = 'https://tw.stock.yahoo.com/q/q?s=' + self.code
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'lxml')
        # 找到你要的那個div 其下的span標籤, 並擷取標籤裡的文字
        price = soup.find('div', 'D(f) Ai(fe) Mb(4px)').span.text.strip()
        self.price = price

    def set_is_selected_true(self):
        self.is_selected = True

    def set_is_selected_false(self):
        self.is_selected = False
