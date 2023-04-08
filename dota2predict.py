import telebot
from bs4 import BeautifulSoup
from requests_html import HTMLSession


session = HTMLSession()

r = session.get('http://www.yourjspage.com')

r.html.render()  # this call executes the js in the page



bot = telebot.TeleBot("5678522382:AAEtQYOYSChWrI-1mItc0H6_Fq4MsLlgpAM")
gameStarted = False
users = {}
heroesMatch = {}
heroesRadiant = []
heroesDire = []

soup = BeautifulSoup(r.text, features="html5lib")
print(soup)
mydivsRadiant = soup.find_all("div", {"class": "sc-gsDKAQ jVYsTL"})



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
