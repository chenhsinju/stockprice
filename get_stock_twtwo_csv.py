import csv
import requests


# 盤後資訊 > 個股日成交資訊 API url
URL_TW = 'https://quality.data.gov.tw/dq_download_json.php?nid=11549&md5_url=da96048521360db9f23a2b47c9c31155'
# 上櫃股票收盤行情 API url
URL_TWO = 'https://quality.data.gov.tw/dq_download_json.php?nid=11371&md5_url=60b0c520b3da145594cdc100ed6833c5'

# 透過requests模組取得url來源的回應
res_tw = requests.get(URL_TW)
res_two = requests.get(URL_TWO)
# print(res)

stock_api_list_tw = res_tw.json()
stock_api_list_two = res_two.json()
# print(type(stock_api_list_two)) # list
# print(stock_api_list_two)
# {'證券代號': '9958', '證券名稱': '世紀鋼', '成交股數': '12458269', '成交金額': '1635999119', '開盤價': '130.00', '最高價': '134.00', '最低價': '128.00', '收盤價': '134.00', '漲跌價差': '0.5000', '成交筆數': '7704'}
# 證券代號、證券名稱、成交股數、成交金額、開盤價、最高價、最低價、收盤價、漲跌價差、成交筆數
# {'資料日期': '1110414', '代號': '020027', '名稱': '元大上櫃ESG成長N', '收盤': '4.45', '漲跌': '-0.01', '開盤': '4.43', '最高': '4.45', '最低': '4.43', '成交股數': '139000', '成交金額': '617070', '成交筆數': '18', '最後買價': '4.45', '最後賣價': '4.46', '發行股數': '400000000', '次日漲停價': '4.89', '次日跌停價': '4.01'}
# 資料日期、代號、名稱、收盤、漲跌、開盤、最高、最低、成交股數、成交金額、成交筆數、最後買價、最後賣價、發行股數、次日漲停價、次日跌停價


# 開啟輸出的 CSV 檔案
with open('stock_tw.csv', 'w', newline='') as stock_tw_csv:
    # 建立 CSV 檔寫入器
    writer_tw = csv.writer(stock_tw_csv)
    for stock_tw in stock_api_list_tw:
        writer_tw.writerow([stock_tw['證券代號'], stock_tw['證券名稱']])


# 開啟輸出的 CSV 檔案
with open('stock_two.csv', 'w', newline='') as stock_two_csv:
    # 建立 CSV 檔寫入器
    writer_two = csv.writer(stock_two_csv)
    for stock_two in stock_api_list_two:
        writer_two.writerow([stock_two['代號'], stock_two['名稱']])
