from imdbinfo import search_title
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# استخدم التوكن الذي حصلت عليه من BotFather
import os
TOKEN = os.getenv("TOKEN")

# تابع البحث عن الفيلم
async def handle_message(update: Update, context: CallbackContext):
    name = update.message.text  # الحصول على النص الذي أرسله المستخدم
    
    # إذا لم يدخل اسم الفيلم
    if not name:
        await update.message.reply_text("just send me the name of the movie you want to search for!\nارسل لي اسم الفيلم الذي تريد البحث عنه!")
        return
    
    try:
        # البحث عن الفيلم باستخدام imdbinfo
        results = search_title(name)
        if not results.titles:
            await update.message.reply_text("no results found for that title. make sure you spelled it correctly!\nلم يتم العثور على نتائج لهذا العنوان. تأكد من تهجئته بشكل صحيح!")
            return
        
        # استخراج الـ IMDb ID
        movie_id = results.titles[0].imdbId
        imdb_url = f"https://www.playimdb.com/title/{movie_id}/?ref_=fn_t_1"
        
        # إنشاء زر يحتوي على اسم الفيلم مع الرابط
        keyboard = [[InlineKeyboardButton(results.titles[0].title, url=imdb_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # إرسال الرسالة مع الزر
        await update.message.reply_text(f"{results.titles[0].title} ({results.titles[0].year}) - Rating: {results.titles[0].rating}", reply_markup=reply_markup)
    except Exception as e:
        await update.message.reply_text(f"error occurred: {str(e)}")

# إضافة أوامر البوت
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("just send me the name of the movie you want to search for!\nارسل لي اسم الفيلم الذي تريد البحث عنه!")

def main():
    application = Application.builder().token(TOKEN).build()

    # بدء أوامر البوت
    application.add_handler(CommandHandler('start', start))
    
    # التعامل مع الرسائل النصية مباشرة
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # تشغيل البوت
    application.run_polling()

if __name__ == '__main__':
    main()
