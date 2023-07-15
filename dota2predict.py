import requests
import telebot
from bs4 import BeautifulSoup
import time
from requests_html import HTMLSession

session = HTMLSession()
url = "https://www.opendota.com/matches/highMmr"
r = session.get(url)
r.html.render(sleep=1, keep_page=True, scrolldown=1)
matches_not_final = {}
r = r.html.links

matches = {}
t = 0
for i in r:
    if len(i) == 19:
        matches_not_final[t] = i[9:]
        t += 1

heroes = requests.get("https://api.opendota.com/api/heroes").json()

with open ("heroes.txt", "w") as f:
    for i in range(len(heroes)):
        if i != len(heroes) - 1:
            f.write(f'{heroes[i]["id"]};{heroes[i]["localized_name"]}\n')
        else:
            f.write(f'{(heroes[i]["id"])};{heroes[i]["localized_name"]}')

print(matches_not_final)
for i in range(len(matches_not_final)):
    response = requests.get('https://api.opendota.com/api/matches/' + matches_not_final[i]).json()

    radiant = []
    dire = []
    if "picks_bans" in response:
        for j in range(10):
            if response['picks_bans'][j]["team"] == 0:
                radiant.append(str(response["picks_bans"][j]["hero_id"]))
            else:
                dire.append(str(response["picks_bans"][j]["hero_id"]))
    sl = dict()
    with open ("heroes.txt", "r") as f:
        s = f.read().split("\n")
        for row in s:
            row = row.split(";")
            sl[row[0]] = row[1]
    if "radiant_win" in response:
        radiantWin = response["radiant_win"]
    if len(radiant) == 5 and len(dire) == 5:
        for j in range(5):
            radiant[j] = sl[radiant[j]]
        for j in range(5):
            dire[j] = sl[dire[j]]
        # print(radiantWin)
        # print(radiant, "vs", dire)
        with open("matches.txt", "a") as f:
            f.write(f"{response['match_id']};{radiant};{dire};{radiantWin};0;0;0,5\n")

bot = telebot.TeleBot("5678522382:AAEtQYOYSChWrI-1mItc0H6_Fq4MsLlgpAM")
gameStarted = False
users = {}
print("END")


class User:
    def __init__(self, uid, name):
        global users
        self.user_id = uid
        self.status = "menu"
        self.points = 100
        self.name = name

    def bet(self, msg, put_points):
        if users[msg.from_user.id].points < put_points:
            bot.send_message(msg.chat.id, f"Недостаточно очков. Баланс: {users[msg.from_user.id].points}")
        else:
            users[msg.from_user.id].points -= put_points
            bot.send_message(msg.chat.id, f"Вы поставили {put_points}. Баланс: {users[msg.from_user.id].points}")

    def get_status(self):
        return self.status


@bot.message_handler(content_types=["text"])
def main_text_logic(msg):
    global users
    if msg.from_user.id not in users:
        users[msg.from_user.id] = User(msg.from_user.id, msg.from_user.first_name)
    print(users[msg.from_user.id].user_id, users[msg.from_user.id].points, users[msg.from_user.id].status)
    usr = User(msg.from_user.id, msg.from_user.first_name)
    if "поставить очки" in msg.text.lower():
        with open ("matches.txt", "r") as f:
            bot.send_message(msg.chat.id, f"")
            bot.send_message(msg.chat.id, f"Введите колличество очков через <bet колличество очков> без ковычек")
            users[msg.from_user.id].status = "bet"
    if users[msg.from_user.id].status == "bet":
        play(msg, usr)


def play(msg, usr):
    print(msg.text.lower)
    if "bet" in msg.text.lower():
        bet = int(msg.text.split()[1])
        print(usr.bet(msg, bet))
        users[msg.from_user.id].status = "menu"


bot.polling(none_stop=True, interval=0)
