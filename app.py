from flask import Flask
from telegram_api import main as start_telegram

app = Flask(__name__)


@app.route("/")
def hello_world():
    # start_telegram()
    return "<p>Telegram started!</p>"
