import requests
import os
from datetime import datetime

# Telegram Config
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_exchange_rate():
    """Fetch USD to Toman rate from API"""
    try:
        # Option 1: Using a free API (example)
        url = "https://api.navasan.tech/latest/?api_key=freeNkhYuE8MhPpRyQVZsHGJkqLDwe0z"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Extract USD rate (in Rial, divide by 10 for Toman)
        usd_rate = int(data['usd_sell']['value']) // 10
        return usd_rate
        
    except Exception as e:
        print(f"Error fetching rate: {e}")
        return None

def get_exchange_rate_alternative():
    """Alternative: Using bonbast (unofficial)"""
    try:
        url = "https://bonbast.com/json"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        usd_rate = int(data['usd1'])  # Already in Toman
        return usd_rate
        
    except Exception as e:
        print(f"Error: {e}")
        return None

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
    # Get current date/time
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Fetch exchange rate
    rate = get_exchange_rate()
    
    if rate:
        message = f"""
💵 <b>نرخ دلار به تومان</b>

📅 تاریخ: {now}
💰 قیمت: {rate:,} تومان

🔄 بروزرسانی هر ۲۴ ساعت
        """
    else:
        message = f"⚠️ خطا در دریافت نرخ ارز\n📅 {now}"
    
    # Send to Telegram
    result = send_telegram_message(message)
    print(f"Message sent: {result}")

if __name__ == "__main__":
    main()
