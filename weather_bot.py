import os
import requests

def get_max_rain_probability(latitude=25.0330, longitude=121.5654):
    """
    呼叫 Open-Meteo API 查詢當日最高降雨機率
    預設經緯度為台北 (可依需要調整)
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "precipitation_probability_max",
        "timezone": "Asia/Taipei"
    }
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    # 取得當日 (index 0) 最高降雨機率
    max_prob = data["daily"]["precipitation_probability_max"][0]
    return max_prob

def send_telegram_message(token, chat_id, message):
    """透過 Telegram Bot 發送訊息"""
    tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    resp = requests.get(tg_url, params=payload, timeout=10)
    return resp.status_code == 200

def main():
    # 從 GitHub Secrets 注入的環境變數中取得金鑰
    token = os.environ.get("TG_TOKEN")
    chat_id = os.environ.get("TG_CHAT_ID")
    
    if not token or not chat_id:
        print("錯誤：找不到 TG_TOKEN 或 TG_CHAT_ID 環境變數！")
        return

    try:
        max_prob = get_max_rain_probability()
        print(f"今日預報最高降雨機率：{max_prob}%")

        # 題目條件：超過 70% (或 60%) 通知記得帶傘
        # 這裡設定閾值門檻為 60%
        THRESHOLD = 60
        
        if max_prob is not None and max_prob >= THRESHOLD:
            message = f"🌧️【天氣提醒】今天最高降雨機率高達 {max_prob}%，出門記得帶傘喔！🌂"
            success = send_telegram_message(token, chat_id, message)
            if success:
                print("已成功發送提醒至 Telegram！")
            else:
                print("Telegram 訊息發送失敗。")
        else:
            print(f"降雨機率未達 {THRESHOLD}%，無需發送提醒。")

    except Exception as e:
        print(f"執行時發生錯誤: {e}")

if __name__ == "__main__":
    main()
