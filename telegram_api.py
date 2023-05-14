import logging
from telegram import Update
from telegram.ext import filters, ContextTypes, Updater, CommandHandler, MessageHandler, ApplicationBuilder
from chatgpt_api import getModel, getTemp, getTokens, generate_text, setModel, setTemp, setTokens
from dotenv import load_dotenv
import os

load_dotenv()

# Replace YOUR_TOKEN with the token you received from BotFather
TOKEN = os.environ.get("KEY_TELEGRAM")

# Enable basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        set_value = int(context.args[0])
        if set_value not in [8, 32]:
            raise ValueError()
        else:
            setModel(set_value)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Set model to gpt-4-32k\n!!!This model costs 2x!!!" if (
                            context.args[0] == 32) else f"Set model to gpt-4")
    except:
        err_text = f"ERROR\nValue must be 8 or 32"
        print(err_text)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=err_text)


async def set_temp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        set_value = float(context.args[0])
        if set_value > 1.0:
            raise ValueError()
        else:
            setTemp(set_value)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{set_value}")
    except:
        err_text = f"ERROR\nValue must be a float [0.0-1.0]"
        print(err_text)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=err_text)


async def set_tokens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        set_value = int(context.args[0])
        if set_value < 1 or set_value > 32768 or (set_value > 8192 and getModel() == 8):
            raise ValueError()
        else:
            setTokens(set_value)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Set tokens to {set_value} for model {getModel()}")
    except:
        err_text = f"ERROR\nValue not possible."
        print(err_text)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=err_text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
        Send /model to set the model [8,32]. Is {getModel()}.
Send /temp to set the randomness of the answer [0.0-1.0]. Is {getTemp()}.
Send /tokens to set the reply token_no [1-5000]. Is {getTokens()}
""")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("history.txt", "a") as myfile:
        myfile.write(f"\n{update.message.text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=generate_text(update.message.text))


def main():
    """Start the bot."""
    application = ApplicationBuilder().token(TOKEN).build()
    # Get the dispatcher to register handlers
    # dp = application.dispatcher
    dp = application

    # Register command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("model", set_model))
    dp.add_handler(CommandHandler("temp", set_temp))
    dp.add_handler(CommandHandler("tokens", set_tokens))

    dp.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    # Start the bot
    application.run_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # Updater.idle()


if __name__ == "__main__":
    main()
