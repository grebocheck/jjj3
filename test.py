import random
import datetime
import time

from data import username, password
from insta import InstagramBot


# микронаборы для быстрого создания конфига

# лайки на хештеге
def pod_hashtag():
    my_bot = InstagramBot(username, password)
    my_bot.login(username, password)
    my_bot.like_photo_by_hashtag("forest", random.randint(7, 10))
    my_bot.close_browser()


# подписки на подпищиков рандомного человека на хештеге
def subscribe():
    my_bot = InstagramBot(username, password)
    my_bot.login(username, password)
    usr = my_bot.get_donor_followers('forest')
    my_bot.get_followers(usr, random.randint(7, 10))
    my_bot.close_browser()


# отписки от тех кто не подписался в ответ
def unsubscribe():
    my_bot = InstagramBot(username, password)
    my_bot.login(username, password)
    my_bot.unsubscribe_create_list(username)
    my_bot.unsubscribe_from_list(username, random.randint(7, 10))
    my_bot.close_browser()


if __name__ == "__main__":
    my_bot = InstagramBot(username, password)
    my_bot.login(username, password)
    my_bot.get_followers_podes(25)
    my_bot.close_browser()
