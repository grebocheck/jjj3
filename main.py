import random
import datetime
import time

from data import username, password
from insta import InstagramBot

from loge import log_inf, log_err
from clean import clean


# микронаборы для быстрого создания конфига

# лайки на хештеге
def pod_hashtag(my_bot):
    my_bot.like_photo_by_hashtag("forest", random.randint(7, 24))


# подписки на подпищиков рандомного человека на хештеге
def subscribe(my_bot):
    usr = my_bot.get_donor_followers('forest')
    my_bot.get_followers(usr, random.randint(7, 20))


# отписки от тех кто не подписался в ответ
def unsubscribe(my_bot):
    my_bot.unsubscribe_create_list(username)
    my_bot.unsubscribe_from_list(username, random.randint(7, 22))


# лайки в ленте
def pod_feed(my_bot):
    my_bot.like_photo_by_feed(random.randint(7, 25))


# лайки в ленте + подписки на коментаторов
def pod_feed_and_podes(my_bot):
    my_bot.like_photo_by_feed(random.randint(7, 25))
    my_bot.get_followers_podes(random.randint(7, 15))


def night():
    this_time = datetime.datetime.now()
    night_start = this_time.replace(hour=22, minute=0, second=0, microsecond=0)
    night_end = this_time.replace(hour=8, minute=0, second=0, microsecond=0)

    if this_time > night_start or this_time < night_end:
        return True
    else:
        return False


# рандом де 1 - 100% , 0 - 0% , float -> bool
def bool_random(a):
    if float(random.random()) < a:
        return True
    else:
        return False


func_list = [lambda my_bot: pod_hashtag(my_bot),
             lambda my_bot: subscribe(my_bot),
             lambda my_bot: unsubscribe(my_bot),
             lambda my_bot: pod_feed(my_bot),
             lambda my_bot: pod_feed_and_podes(my_bot)]


def session_bot():
    try:
        my_bot = InstagramBot(username, password)
        my_bot.login(username, password)
        for a in range(random.randrange(1, 3)):
            random.choice(func_list)(my_bot)
        my_bot.close_browser()
        clean()
    except Exception as ex:
        print(ex)
        log_err("Произошла фатальная ошибка сессии")


if __name__ == "__main__":
    log_inf("Старт")
    while True:
        try:
            if night():
                time.sleep(2000)
            else:
                session_bot()
                time_to_sleep = random.randint(7000, 10000)
                log_inf(f'{time_to_sleep} с до новой сессии')
                time.sleep(time_to_sleep)
        except Exception as ex:
            print(ex)
            break
