import requests
import os
from datetime import datetime

# Telegram Config
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_usdt_price():
    """Fetch USDT price from Nobitex API"""
    try:
        url = "https://apiv2.nobitex.ir/v3/orderbook/USDTIRT"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("status") == "ok":
            # Get lastTradePrice (in Rial)
            last_price_rial = int(data["lastTradePrice"])
            
            # Convert to Toman (divide by 10)
            last_price_toman = last_price_rial // 10
            
            # Get lastUpdate (Unix timestamp in milliseconds)
            last_update_ms = data["lastUpdate"]
            
            # Convert to seconds and then to datetime
            last_update_dt = datetime.fromtimestamp(last_update_ms / 1000)
            
            # Format the date
            last_update_str = last_update_dt.strftime("%Y-%m-%d %H:%M:%S")
            
            return last_price_toman, last_update_str
        else:
            print("API status not ok")
            return None, None
            
    except Exception as e:
        print(f"Error fetching rate: {e}")
        return None, None

def send_telegram_message(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=payload)
    return response.json()

def main():
    # Fetch USDT price and last update time
    price, last_update = get_usdt_price()
    
    if price and last_update:
        message = f"""
💵 <b>قیمت تتر (USDT)</b>

📅 آخرین بروزرسانی: {last_update}
💰 قیمت: <b>{price:,}</b> تومان

📊 منبع: نوبیتکس
        """
    else:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"⚠️ خطا در دریافت قیمت از نوبیتکس\n📅 {now}"
    
    # Send to Telegram
    result = send_telegram_message(message)
    
    if result.get("ok"):
        print("✅ Message sent successfully!")
    else:
        print(f"❌ Failed to send: {result}")

if __name__ == "__main__":
    main()
