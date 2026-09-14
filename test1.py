import time
import requests
from bs4 import BeautifulSoup

# 要爬取的股票代號列表
stock = ["1101", "2330", "1102"]

# Telegram Bot 設定 (請將 token 填入你的真實機器人 token)
token = "8967331494:AAEEGNdfSvN3fJeGsnAE7jVEp8gCPqVRnhs"
chat_id = "8525960136"

# 偽裝一般瀏覽器 Header，避免被擋
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for stockid in stock:
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
            price = price_tag.getText().strip()
            message = f"股票 {stockid} 即時股價為：{price}"
        else:
            message = f"股票 {stockid} 抓取失敗：未找到股價元素"

        print(message)

        # 透過 Telegram Bot 回報訊息 (使用 params 自動處理中文字與空格編碼)
        tg_api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        resp = requests.get(tg_api_url, params=payload, timeout=10)
        
        # 若 Telegram 回傳非 200，印出錯誤原因方便排查
        if resp.status_code != 200:
            print(f"Telegram 發送失敗: {resp.text}")

    except Exception as e:
        print(f"處理股票 {stockid} 時發生錯誤: {e}")

    # 每次爬取間隔 3 秒
    time.sleep(3)
