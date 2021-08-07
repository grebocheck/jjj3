import logging
import random
import datetime
# import time

from data import username, password
from insta import InstagramBot


# микронаборы для быстрого создания конфига

# лайки на хештеге
def pod_hashtag():
    my_bot = InstagramBot(username, password)
    my_bot.login(username, password)
    my_bot.like_photo_by_hashtag("forest", random.randint(75, 100))
    my_bot.close_browser()


# подписки на подпищиков рандомного человека на хештеге
def subscribe():
    my_bot = InstagramBot(username, password)
    my_bot.login(username, password)
    usr = my_bot.get_donor_followers('forest')
    my_bot.get_followers(usr, random.randint(75, 100))
    my_bot.close_browser()


# отписки от тех кто не подписался в ответ
def unsubscribe():
    my_bot = InstagramBot(username, password)
    my_bot.login(username, password)
    my_bot.unsubscribe_create_list(username)
    my_bot.unsubscribe_from_list(username, random.randint(75, 100))
    my_bot.close_browser()


logging.basicConfig(level=logging.DEBUG)


def today10():
    this_time = datetime.datetime.now()
    return this_time.replace(hour=random.randint(9, 10),
                             minute=random.randint(0, 59),
                             second=random.randint(0, 59),
                             microsecond=0)


def today15():
    this_time = datetime.datetime.now()
    return this_time.replace(hour=random.randint(14, 15),
                             minute=random.randint(0, 59),
                             second=random.randint(0, 59),
                             microsecond=0)


def today20():
    this_time = datetime.datetime.now()
    return this_time.replace(hour=random.randint(19, 20),
                             minute=random.randint(0, 59),
                             second=random.randint(0, 59),
                             microsecond=0)


func = {1: pod_hashtag(),
        2: subscribe(),
        3: unsubscribe()}

if __name__ == "__main__":
    now_time = datetime.datetime.now()
    difference = int((today10() - now_time + datetime.timedelta(days=1)).total_seconds())
    print(f"старт начнеться через {difference} с")
