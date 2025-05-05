import requests
import telebot

# === Configuration ===
BOT_TOKEN = "7678722383:AAFW5zg_kbRcyO2ug6SwkQV3G671WnWyFz8"
API_KEY = "AIzaSyDA1mlDKRTzZBRFF3_LkvSwo3wS4KH7ZW4"
CX = "c307367182cd945b4"
lang = "en"

bot = telebot.TeleBot(BOT_TOKEN)

# === Google Custom Search API ===
def google_search(query, search_type=""):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}&lr=lang_{lang}"
    if search_type == "image":
        url += "&searchType=image"
    response = requests.get(url)
    return response.json()

# === /start Command ===
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hey there, future cyber defender! 🛡 What would you like to search or learn about in cybersecurity?"
    )

# === Text Message Handler ===
@bot.message_handler(func=lambda m: True)
def text_handler(message):
    query = message.text.strip().lower()
    is_image_search = any(word in query for word in ["photo", "image", "picture"])

    results = google_search(query, search_type="image" if is_image_search else "")

    if "items" not in results:
        bot.reply_to(message, "Sorry, no results found.")
        return

    if is_image_search:
        for item in results["items"][:3]:  # Limit to 3 images
            image_url = item.get("link")
            bot.send_photo(message.chat.id, photo=image_url)
    else:
        response_text = ""
        for i, item in enumerate(results["items"][:5], 1):
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No description available.")
            link = item.get("link", "No link available.")
            response_text += f"{i}. <b>{title}</b>\n{snippet}\n<a href='{link}'>🔗 Read more</a>\n\n"
        bot.send_message(message.chat.id, response_text.strip(), parse_mode="HTML")

# === Run Bot ===
print("🤖 Bot is running...")
bot.infinity_polling()
