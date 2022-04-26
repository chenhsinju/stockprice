from flask import Flask, render_template
import csv
import requests
from stock import Stock


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# 站內要顯示的個股列表
stock_list = []


# 打開stock_list.csv
with open('stock_list.csv', newline='', encoding='utf-8') as stock_csv:
    # 把csv檔案格式轉換為list
    table = list(csv.reader(stock_csv))
    # print(table)
    for t in table:
        # 建立一個股物件
        s = Stock(t[0], t[1])
        # 將個股物件新增到個股清單內
        stock_list.append(s)
        # print(s)


@app.route('/')
# 首頁路由
def index_page():
    return render_template('index.html',
                           stock_list=stock_list)


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/stock/<sid>')
# 個股詳情頁路由
def stock_detail_page(sid):
    stock = None
    for s in stock_list:
        if s.id == sid:
            stock = s
            # print(stock)
    # 爬取個股詳細資料
    stock.get_data()

    # 個股股價
    stock_price = []
    # 打開stock_price.csv
    with open('stock_price.csv', newline='', encoding='utf-8') as stock_price_csv_open:
        table_price = list(csv.reader(stock_price_csv_open))
        for tp in table_price:
            p = tp[0]
            stock_price.append(p)
            # print(stock_price[0])
    return render_template('stock-detail.html',
                           stock=stock,
                           stock_price=stock_price[0])


if __name__ == '__main__':
    app.run(debug=True)
