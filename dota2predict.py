import telebot
from bs4 import BeautifulSoup
import requests

url = "https://stratz.com/matches/"
r = requests.get(url)


bot = telebot.TeleBot("5678522382:AAEtQYOYSChWrI-1mItc0H6_Fq4MsLlgpAM")
gameStarted = False
users = {}
# heroesMatch = set()
# heroesRadiant = []
# heroesDire = []

# soup = BeautifulSoup(r.text, features="html.parser")
# print(soup)
# mydivsRadiant = soup.find_all("div", {"class": "sc-gsDKAQ sc-jRQBWg feaazi bMqZUP"})
# print(mydivsRadiant)


class User:
    def __init__(self, uid, name):
        self.user_id = uid
        self.points = 100
        self.name = name

    def bet(self, msg, put_points):
        if self.points < put_points:
            bot.send_message(msg.chat.id, f"Недостаточно очков. Баланс: {self.points}")
        else:
            self.points -= put_points
            bot.send_message(msg.chat.id, f"Вы поставили {put_points}. Баланс: {self.points}")


@bot.message_handler(content_types=["text"])
def main_text_logic(msg):
    users[msg.from_user.id] = User(msg.from_user.id, msg.from_user.first_name)
    print(users[msg.from_user.id].user_id, users[msg.from_user.id].points, msg.from_user.first_name)
    if "поставить очки" in msg.text.lower():
        print(User.bet(54, 3487234, 43))


bot.polling(none_stop=True, interval=0)
