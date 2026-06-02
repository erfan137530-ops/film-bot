import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# توکن رباتت رو اینجا بذار
TOKEN = "TOKEN_ETUN"

# لینک کانال‌های تبلیغاتی
CHANNELS = ["@channel1", "@channel2", "@channel3"]

# لینک فیلم‌ها
MOVIES = {
    "فیلم ۱": "https://example.com/film1.mp4",
    "فیلم ۲": "https://example.com/film2.mp4",
    "فیلم ۳": "https://example.com/film3.mp4",
}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    
    not_joined = []
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                not_joined.append(channel)
        except:
            not_joined.append(channel)
    
    if not_joined:
        keyboard = []
        for channel in not_joined:
            keyboard.append([InlineKeyboardButton(f"عضویت در {channel}", url=f"https://t.me/{channel.replace('@', '')}")])
        keyboard.append([InlineKeyboardButton("بررسی مجدد ✅", callback_data="check")])
        
        await update.message.reply_text(
            "برای دیدن فیلم‌ها باید در کانال‌های تبلیغاتی عضو شوید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await show_movies(update, context)

async def show_movies(update: Update, context: CallbackContext):
    keyboard = []
    for name, link in MOVIES.items():
        keyboard.append([InlineKeyboardButton(name, url=link)])
    
    await update.message.reply_text(
        "فیلم‌های موجود:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def check_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await start(update, context)

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_callback))
    
    application.run_polling()

if __name__ == "__main__":
    main()
