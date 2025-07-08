        import requests
	import pandas as pd
	import time
	import telegram
	from datetime import datetime

	# --- CONFIGURATION ---
	TOKEN = "7589492309:AAHdX3scAQyB9Dx3USJ080-L2vbqWoGEYOc"  # Ton bot Telegram
	CHAT_ID = "6654971735"  # Ton ID Telegram perso
	COIN_ID = "bitcoin"  # À changer si tu veux ("ethereum", etc.)

	bot = telegram.Bot(token=TOKEN)

	# --- RÉCUPÉRER LES PRIX ---
	def get_prices():
        url=
      f"https://api.coingecko.com/api/v3/coins/{COIN_ID}/market_chart"		
    params = {"vs_currency": "usd", "days": "1", "interval": "minute"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "prices" in data:
            prices = [price[1] for price in data["prices"]]                                                             
            return prices
    except:
        return None

	# --- CALCUL RSI ---   
	def calculate_rsi(prices, period=14):
        df = pd.DataFrame(prices, columns=["price"])
    delta = df["price"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

	# --- SAUVEGARDE HISTORIQUE CSV ---
	def save_signal(rsi, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("historique_signaux.csv", "a") as f:
        f.write(f"{now},{rsi:.2f},{message}\n")

	# --- BOUCLE PRINCIPALE ---
	while True:
    prices = get_prices()
    if prices:
        rsi = calculate_rsi(prices)
        print(f"RSI actuel : {rsi:.2f}")

        # --- CHOIX DU MESSAGE SELON RSI ---
        if rsi > 70:
            message = f"🔴 RSI = {rsi:.2f} ➤ Zone de surachat ➤ POSSIBLE VENTE"
        elif rsi < 30:
            message = f"🟢 RSI = {rsi:.2f} ➤ Zone de survente ➤ POSSIBLE ACHAT"
        else:
            message = f"⚪ RSI = {rsi:.2f} ➤ Zone neutre"

        # --- ENVOI DU MESSAGE À TOI ---
        bot.send_message(chat_id=CHAT_ID, text=message)

        # --- ENVOI AUTOMATIQUE À UNIBOT (si RSI < 30) ---                          
        if rsi < 30:
            bot.send_message(chat_id="@Unibot", text="Buy 0.05 ETH")

        # --- SAUVEGARDE DU SIGNAL ---
        save_signal(rsi, message)

    print("⏳ PAUSE 5 MINUTES...")
    time.sleep(300)