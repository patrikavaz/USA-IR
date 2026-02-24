import requests
import os
from datetime import datetime
import jdatetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Get data from API
data = requests.get("https://apiv2.nobitex.ir/v3/orderbook/USDTIRT").json()

# Extract price
price = int(data["lastTradePrice"]) // 10

# --- DATE SETUP ---
# 1. Solar Date (Persian) - No time
solar_date = jdatetime.date.today().strftime("%Y/%m/%d")

# 2. Gregorian Date - No time
greg_date = datetime.now().strftime("%Y-%m-%d")

# --- MESSAGE ---
message = f"""💵 قیمت تتر: {price:,} تومان

📅 {solar_date}
📅 {greg_date}"""

# Send to Telegram
requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={"chat_id": CHAT_ID, "text": message}
)
