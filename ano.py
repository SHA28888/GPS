import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# API-nøkkel fra BotFather
API_KEY = '7674556511:AAE_JRtnN1_wMdt4c4DZ0LYTsE0GayUmlDU'
bot = telebot.TeleBot(API_KEY)

# Priser per dose
prices = {
    'amfetamin': 100,
    'kokain': 200,
    'benzo': 50,
    'xanax': 30,
    'vodka': 20,
    '2cb': 150
}

# Funksjon for å lage produktmeny
def product_menu():
    markup = InlineKeyboardMarkup()
    for product in prices.keys():
        markup.add(InlineKeyboardButton(f"💊 {product}", callback_data=f"price_{product}"))
    return markup

# Håndterer /start-kommandoen
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Velg et produkt for å se prisen per dose:", reply_markup=product_menu())

# Håndterer /info-kommandoen
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, "ℹ️ Dette er en prisbot! Velg et produkt med /start for å se prisen per dose og beregne totalpris for flere doser.")

# Håndterer callback-knapper
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data
    try:
        if data.startswith("price_"):
            product = data.split("_")[1]
            price = prices.get(product, "Ukjent")
            bot.answer_callback_query(call.id, f"Prisen for én dose {product} er {price} kr.")
            # Knapper for antall doser
            markup = InlineKeyboardMarkup()
            for quantity in [1, 2, 3, 5, 10]:
                markup.add(InlineKeyboardButton(f"{quantity}", callback_data=f"quantity_{product}_{quantity}"))
            markup.add(InlineKeyboardButton("🔙 Tilbake", callback_data="back"))
            bot.send_message(call.message.chat.id, f"💰 Hvor mange doser av {product} vil du kjøpe?", reply_markup=markup)

        elif data.startswith("quantity_"):
            _, product, quantity = data.split("_")
            quantity = int(quantity)
            price_per_dose = prices.get(product, 0)
            total_price = price_per_dose * quantity
            bot.answer_callback_query(call.id)
            # Bekreftelsesmelding
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("✅ Start på nytt", callback_data="restart"))
            bot.send_message(call.message.chat.id, f"💸 Totalprisen for {quantity} doser {product} er {total_price} kr.", reply_markup=markup)

        elif data == "back":
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "👋 Velg et produkt for å se prisen per dose:", reply_markup=product_menu())

        elif data == "restart":
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "👋 Velg et produkt for å se prisen per dose:", reply_markup=product_menu())

    except Exception as e:
        bot.answer_callback_query(call.id, "❌ Noe gikk galt, prøv igjen!")
        bot.send_message(call.message.chat.id, "⚠️ En feil oppstod. Bruk /start for å prøve igjen.")

# Starter boten
bot.polling()
