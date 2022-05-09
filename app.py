from flask import Flask, render_template, url_for, redirect, request
import csv
import requests
import yfinance as yf
from stock import Stock


app = Flask(__name__)


# 全部的 個股列表
stock_list_all = []
# 首頁要顯示的、客製化的 個股字典
stock_dict_customized = {}


# 打開stock_tw.csv
with open('stock_tw.csv', newline='', encoding='utf-8') as stock_tw_csv:
    # 把csv檔案格式轉換為list
    stock_list_tw = list(csv.reader(stock_tw_csv))
    # print(stock_list_tw)
    # print(type(stock_list_tw)) # list
    for stock_tw in stock_list_tw:
        # 建立一個股物件
        s_tw = Stock(stock_tw[0], stock_tw[1], True)
        # 將個股物件新增到個股清單內
        stock_list_all.append(s_tw)
        # print(s_tw)


# 打開stock_two.csv
with open('stock_two.csv', newline='', encoding='utf-8') as stock_two_csv:
    # 把csv檔案格式轉換為list
    stock_list_two = list(csv.reader(stock_two_csv))
    # print(stock_list_two)
    # print(type(stock_list_two)) # list
    for stock_two in stock_list_two:
        # 建立一個股物件
        s_two = Stock(stock_two[0], stock_two[1], False)
        # 將個股物件新增到個股清單內
        stock_list_all.append(s_two)
        # print(s_two)


def build_stock_dict_customized():
    # 打開stock_dict_customized.csv
    with open('stock_dict_customized.csv', newline='', encoding='utf-8') as stock_customized_csv:
        # 讀取 CSV 檔內容，將每一列轉成一個 dictionary
        rows = csv.DictReader(stock_customized_csv)
        # 以迴圈輸出指定欄位
        for row in rows:
            # 將個股新增到個股字典內
            stock_dict_customized.update({row['Code']: row['Name']})
            # print(row['Code'], row['Name'])


build_stock_dict_customized()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404


@app.route('/')
# 首頁路由
def index_page():
    stock_dict_customized.clear()
    build_stock_dict_customized()
    return render_template('index.html',
                           stock_dict_customized=stock_dict_customized)


@app.route('/stock/<code>')
# 個股詳情頁路由
def stock_page(code):
    stock = None
    for s in stock_list_all:
        # 如果真有<code>此一股票代號
        if s.code == code:
            stock = s
            # print(stock)

    if stock == None:
        return render_template('stock_not_found.html', code=code)

    if stock.is_tw:
        yahoo_finance_object = yf.Ticker(code + '.TW')
    else:
        yahoo_finance_object = yf.Ticker(code + '.TWO')
    # print(yahoo_finance_object)

    # df: dataframe
    yahoo_finance_df = yahoo_finance_object.history()
    yahoo_finance_table = yahoo_finance_df.to_html(
        classes=['table-bordered', 'table-hover', 'table-sm', 'text-right'], header=True)
    return render_template('stock.html',
                           stock=stock,
                           yahoo_finance_table=yahoo_finance_table)


@app.route('/setting')
def setting_page():
    # 客製化的 個股列表
    stock_list_customized = stock_dict_customized.keys()
    # print(stock_dict_customized)
    # print(stock_list_customized)
    stock_str_customized = ' '.join(stock_list_customized)
    # print(stock_str_customized)
    return render_template('setting.html',
                           stock_str_customized=stock_str_customized)


@app.route('/setting_save', methods=['GET', 'POST'])
def setting_save():
    if request.method == 'POST':
        stock_customized_input = request.form['stockCustomizedInput']
        # print(stock_customized_input)
        # print(type(stock_customized_input)) # str
        stock_customized_input_list = stock_customized_input.split()
        # print(stock_customized_input_list)
        # print(type(stock_customized_input_list)) # list

        # 開啟輸出的 CSV 檔案
        with open('stock_dict_customized.csv', 'w', newline='') as stock_customized_csv:
            # 建立 CSV 檔寫入器
            writer = csv.writer(stock_customized_csv)
            # 寫入一列資料
            writer.writerow(['Code', 'Name'])
            for stock in stock_list_all:
                if stock.code in stock_customized_input_list:
                    # 寫入一列資料
                    writer.writerow([stock.code, stock.name])

        return redirect(url_for('index_page'))
    else:
        return redirect(url_for('setting_page'))


if __name__ == '__main__':
    app.run(debug=True)
