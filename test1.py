import time
import requests
from bs4 import BeautifulSoup

# 要爬取的股票代號列表
stock = ["1101", "2330","1102"]

# Telegram Bot 設定 (請替換為你的實際資料)
token = "8967331494:AAEEGNdfSvN3fJeGsnAE7jVEp8gCPqVRnhs"
chat_id = "8525960136"

# 偽裝一般瀏覽器 Header，避免被 Yahoo 擋掉
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for i in range(len(stock)):
    stockid = stock[i]
    url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # 定位股價元素
        target_classes = [
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)",
        ]

        price_tag = soup.find("span", class_=target_classes)

        if price_tag:
            price = price_tag.getText()
            message = f"股票 {stockid} 即時股價為 {price}"
        else:
            message = f"股票 {stockid} 抓取失敗：未找到股價元素"

        # 透過 Telegram Bot 回報訊息
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(tg_url)

    except Exception as e:
        print(f"處理股票 {stockid} 時發生錯誤: {e}")

    # 每次爬取間隔 3 秒
    time.sleep(3)
