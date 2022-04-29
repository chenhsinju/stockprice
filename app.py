from flask import Flask, render_template, url_for, redirect
from flask import jsonify
from flask import request
import csv
import requests
from stock import Stock


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# 上市個股日收盤價及月平均價 API url
url = 'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_AVG_ALL'
# 透過requests模組取得url來源的回應
res = requests.get(url)
# print(res)
stock_day_avg_all_list = res.json()
# print(type(stock_day_avg_all_list))


# 全部的 個股列表
stock_list_all = []
# 客製化的、在首頁顯示的 個股列表
stock_list_customized = []


for t in stock_day_avg_all_list:
    # 建立一個股物件
    s = Stock(t['Code'], t['Name'], t['MonthlyAveragePrice'])
    # 將個股物件新增到個股清單內
    stock_list_all.append(s)


def reload_csv():
    # 打開stock_list_customized.csv
    with open('stock_list_customized.csv', newline='', encoding='utf-8') as stock_csv:
        stock_list_customized.clear()
        # 把csv檔案格式轉換為list
        table = list(csv.reader(stock_csv))
        # print(table)
        # # print(type(table))
        for t in table:
            # 建立一個股物件
            s = Stock(t[0], t[1], t[2])
            # 將個股物件新增到個股清單內
            stock_list_customized.append(s)
            # print(s)


@app.route('/')
# 首頁路由
def index_page():
    reload_csv()
    return render_template('index.html',
                           stock_list_customized=stock_list_customized)


@app.route('/setting')
def setting_page():
    return render_template('setting.html',
                           stock_list_all=stock_list_all,
                           stock_list_customized=stock_list_customized)


@app.route('/setting_save', methods=['GET', 'POST'])
def setting_save():
    if request.method == 'POST':
        select_list = request.form.getlist('mySelect2')
        # print(select_list)
        # print(type(select_list))

        # 打開stock_list_customized.csv
        with open('stock_list_customized.csv', 'w', newline='') as stock_csv:
            # 建立 CSV 檔寫入器
            writer = csv.writer(stock_csv)
            for stock in stock_list_all:
                if stock.code in select_list:
                    writer.writerow([stock.code, stock.name,
                                    stock.monthly_average_price])
        return redirect(url_for('index_page'))
    else:
        return redirect(url_for('setting_page'))


@app.route('/stock/<code>')
# 個股詳情頁路由
def stock_detail_page(code):
    stock = None
    for s in stock_list_all:
        if s.code == code:
            stock = s
            # print(stock)
            break
    # 爬取個股詳細資料
    stock.get_data()
    return render_template('stock-detail.html',
                           stock=stock)


if __name__ == '__main__':
    app.run(debug=True)
