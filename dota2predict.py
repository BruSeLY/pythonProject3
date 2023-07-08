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
print(r)
matches = {}
t =0
for i in r:
    if len(i) == 19:
        matches_not_final[t] = i[9:]
        t+=1

heroes = requests.get("https://api.opendota.com/api/heroes").json()
print(heroes)
with open ("heroes.txt", "w") as f:
    for i in range(len(heroes)):
        f.write(f'{heroes[i]["localized_name"]} = {heroes[i]["id"]}\n')

response = requests.get('https://api.opendota.com/api/matches/' + matches_not_final[0]).json()
print(response)
print(response["match_id"])
print(response["picks_bans"])
# for j in range(10):
#     if response['picks_bans'][j][
#         matches[response["match_id"]] = f"{response['rad']}radiant_team: {response['picks_bans']"

# print(matches)



bot = telebot.TeleBot("5678522382:AAEtQYOYSChWrI-1mItc0H6_Fq4MsLlgpAM")
gameStarted = False
users = {}
heroesMatch = {}
heroesRadiant = []
heroesDire = []
# mydivsRadiant = soup.find_all("img")
# mydivsDire = soup.find_all("img", {"data-radiant": "false"})
# print(mydivsRadiant)
# print(mydivsDire)

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
