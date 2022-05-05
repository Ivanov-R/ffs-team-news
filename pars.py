import os

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

token = os.getenv("TOKEN")
bot = Bot(token=token)
chat_id = 620090788

result_list = []
URL_TEMPLATE = "https://www.fantasyfootballscout.co.uk/team-news/"
FILE_NAME = "test.xlsx"
col_list = ["News"]

old_result = pd.read_excel(FILE_NAME, names=col_list)
old_news_list = old_result.News.to_list()


def parse(url=URL_TEMPLATE):
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    teams = soup.find_all("h2")
    texts = soup.find_all("p")
    for i in range(20):
        result_list.append(f"{teams[i].text}: {texts[i + 6].text[13:]}")
        if result_list[i] != old_news_list[i]:
            bot.send_message(chat_id, result_list[i])
    return result_list


df = pd.DataFrame(parse())
df.to_excel(FILE_NAME)
