
import requests
import time
import ta
import pandas as pd
from binance.client import Client

# ---- CONFIG ----
TELEGRAM_TOKEN = '7589492309:AAHdX3scAQyB9Dx3USJ080-L2vbqWoGEYOc'
TELEGRAM_CHAT_ID = '6654971735'
SYMBOL = 'ETHUSDT'
INTERVAL = '1m'
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
# ---- /CONFIG ----

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erreur Telegram:", e)

def get_rsi():
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=100"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=['open_time','open','high','low','close','volume','close_time','qav','num_trades','taker_base_vol','taker_quote_vol','ignore'])
    df['close'] = pd.to_numeric(df['close'])
    rsi = ta.momentum.RSIIndicator(df['close'], RSI_PERIOD).rsi().iloc[-1]
    return rsi

while True:
    try:
        rsi = get_rsi()
        print(f"RSI actuel : {rsi:.2f}")
        if rsi < RSI_OVERSOLD:
            send_telegram(f"🔵 RSI ({SYMBOL}) = {rsi:.2f} → SURVENDU 💎")
        elif rsi > RSI_OVERBOUGHT:
            send_telegram(f"🔴 RSI ({SYMBOL}) = {rsi:.2f} → SURACHETÉ 🚨")
    except Exception as e:
        print("Erreur:", e)
    time.sleep(60)
