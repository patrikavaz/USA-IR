import requests
import os
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Get data from API
data = requests.get("https://apiv2.nobitex.ir/v3/orderbook/USDTIRT").json()

# Extract price and lastUpdate
price = int(data["lastTradePrice"]) // 10
last_update = datetime.fromtimestamp(data["lastUpdate"] / 1000).strftime("%Y-%m-%d %H:%M:%S")

# Send to Telegram
message = f"💵 قیمت تتر: {price:,} تومان\n📅 آخرین بروزرسانی: {last_update}"
requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={"chat_id": CHAT_ID, "text": message}
)
