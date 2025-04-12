
import json
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем вопросы из JSON
with open("microbiology_tests.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот с тестами по микробиологии. Напиши /test, чтобы начать.")

# Команда /test
async def send_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = random.choice(questions)
    context.user_data["current"] = question
    options = [[opt] for opt in question["options"]]
    await update.message.reply_text(
        question["question"],
        reply_markup=ReplyKeyboardMarkup(options, one_time_keyboard=True, resize_keyboard=True)
    )

# Проверка ответа
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text
    correct_answer = context.user_data.get("current", {}).get("answer")

    if not correct_answer:
        await update.message.reply_text("Начни тест командой /test")
        return

    if user_answer == correct_answer:
        await update.message.reply_text("Правильно! Хочешь ещё? Напиши /test.")
    else:
        await update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}\nНапиши /test для следующего.")

# Основной запуск
def main():
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", send_test))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))
    app.run_polling()

if __name__ == "__main__":
    main()
