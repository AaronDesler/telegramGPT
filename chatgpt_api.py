import openai
from dotenv import load_dotenv
import os

load_dotenv()

model_gpt = "gpt-3.5-turbo"
temp_gpt = 0.8
tokens_gpt = 150
openai.api_key = os.environ.get("KEY_OPENAI")


def setModel(_):
    global model_gpt
    if _ == 8:
        model_gpt = "gpt-4"
    elif _ == 32:
        model_gpt = "gpt-4-32k"


def setTemp(_):
    global temp_gpt
    temp_gpt = _


def setTokens(_):
    global tokens_gpt
    tokens_gpt = _


def getModel():
    return model_gpt


def getTemp():
    return temp_gpt


def getTokens():
    return tokens_gpt


def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model=model_gpt,
        messages=[{"role": "user", "content": str(prompt)}],
        max_tokens=tokens_gpt,
        n=1,
        temperature=temp_gpt,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response['choices'][0]['message']['content'].strip()
