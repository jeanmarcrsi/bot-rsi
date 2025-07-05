import requests
import pandas as pd
import time
import telegram

def get_prices():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "1", "interval": "minute"}
    response = requests.get(url, params=params)
    data = response.json()

    if "prices" in data:
        prices = [price[1] for price in data["prices"]]
        return prices
    else:
        return None

def calculate_rsi(prices, period=14):
    df = pd.DataFrame(prices, columns=["price"])
    delta = df["price"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]  # dernière valeur du RSI

while True:
    prices = get_prices()
    if prices:
        rsi = calculate_rsi(prices)
        print(f"RSI actuel : {rsi:.2f}")

        if rsi > 70:
            print("🔻 RSI > 70 → Zone de surachat → POSSIBLE VENTE")
        elif rsi < 30:
            print("🔺 RSI < 30 → Zone de survente → POSSIBLE ACHAT")
        else:
            print("📉 RSI neutre, on attend...")

    print("⏸️ PAUSE 5 MINUTES...")
    time.sleep(300)
    
# ENVOI DU RSI SUR TELEGRAM
bot = telegram.Bot(token='7589492309:AAHdX3scAQyB9Dx3USJ080-L2vbqWoGEYOc')

message = f"RSI actuel : {rsi:.2f}"
bot.send_message(chat_id=6654971735, text=message)