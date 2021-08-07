import os
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from loge import log_inf, log_deb, log_err


class InstagramBot:
    """Instagram Bot на Python by PythonToday Heridium edition"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # options = Options()
        # options.add_argument(f"--window-size={window_size}")                                  -регулировка окна
        # options.add_argument("--headless")                                                    -скрыть
        # self.browser = webdriver.Chrome("../chromedriver/chromedriver.exe", options=options)  -использовать настройки
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=moon_eva")
        chrome_options.add_argument("--remote-debugging-port=49216")
        chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        self.browser = webdriver.Chrome("chromedriver/chromedriver.exe", chrome_options=chrome_options)

    # метод для закрытия браузера
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    # метод логина
    def login(self, username, password):
        """
        Функция авторизации

        :param username: username
        :param password: password
        :return: None
        """
        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(5, 7))

        log_inf("Выполняеться вход")

        if self.xpath_exists("/html/body/div[3]/div/div/button[1]"):
            # Согласиться с куки файлами
            log_inf("Согласились на куки файлы")
            browser.find_element_by_xpath("/html/body/div[3]/div/div/button[1]").click()
            time.sleep(random.randrange(2, 4))

        # Ввод данных для входа
        try:
            username_input = browser.find_element_by_name('username')
            username_input.clear()
            username_input.send_keys(username)

            time.sleep(random.randrange(1, 3))

            password_input = browser.find_element_by_name('password')
            password_input.clear()
            password_input.send_keys(password)

            time.sleep(random.randrange(1, 3))

            password_input.send_keys(Keys.ENTER)
            time.sleep(10)
        except Exception as ex:
            print(ex)
            log_inf("Авторизация не потребувалась")

        log_inf("Данные авторизации введены")

    # метод ставит лайки по hashtag
    def like_photo_by_hashtag(self, hashtag, num):
        """
        Функция установки лайков по хештегам

        :param hashtag: string, хештег
        :param num: количество  требуемых лайков к установке
        :return:
        """

        log_inf("Инициализация функции лайков на хештеге")

        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        scrols = int(num / 12 + 1)

        for i in range(scrols):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in range(num):
            try:
                if bool_random(0.5):
                    browser.get(posts_urls[url])
                    time.sleep(3)
                    browser.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                    log_deb("Нажато на лайк")
                    time.sleep(random.randrange(8, 10))
                else:
                    log_deb("Бот не поставил лайк")
            except Exception as ex:
                print(ex)
                self.close_browser()

        log_inf("Функция завершила свою работу")

    # метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # метод подписки на подписчиков переданного аккаунта
    def get_followers(self, userpage, num):
        """
        Подписка на пользователей определенного аккаунта

        :param userpage: url адрес на страницу пользователя
        :param num: количество подписок которые надо сделать
        :return:
        """

        log_inf("Инициализация функции подписки на пользователей определенного аккаунта")

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            log_deb(f"Папка {file_name} уже существует!")
        else:
            log_deb(f"Создаём папку пользователя {file_name}.")
            os.mkdir(file_name)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            log_deb(f"Пользователя {file_name} не существует, проверьте URL")
            self.close_browser()
        else:
            log_deb(f"Пользователь {file_name} успешно найден, начинаем скачивать ссылки на подписчиков!")
            time.sleep(2)

            followers_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
            followers_count = followers_button.get_attribute('title')
            # followers_count = followers_button.text
            # followers_count = int(''.join(followers_count.split(' ')))

            # если количество подписчиков больше 999, убираем из числа запятые
            if ',' in followers_count:
                followers_count = int(''.join(followers_count.split(',')))
            else:
                followers_count = int(''.join(followers_count.split(' ')))

            log_deb(f"Количество подписчиков: {followers_count}")

            time.sleep(2)

            if num < followers_count:
                count = num
            else:
                count = followers_count

            loops_count = int(count / 12)

            log_deb(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = ''

            if self.xpath_exists("/html/body/div[5]/div/div/div[2]"):
                followers_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
            elif self.xpath_exists("/html/body/div[6]/div/div/div[2]"):
                followers_ul = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]")
            else:
                log_err("followers_ul xpath не найдено")
                exit()

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    log_deb(f"Итерация #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем всех подписчиков пользователя в файл
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls[0:count - 1]:
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        log_deb(f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                log_deb('Файл со ссылками ещё не создан!')
                                print(ex)

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):
                                log_deb("Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span["
                                    "1]/button/div/span"):
                                log_deb(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:
                                time.sleep(random.randrange(4, 8))

                                if self.xpath_exists(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        browser.find_element_by_xpath(
                                            "/html/body/div[1]/section/main/div/header/section/div[1]/div["
                                            "1]/div/div/button").click()
                                        log_deb(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exists(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div["
                                                "1]/div/div/button"):
                                            browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div["
                                                "1]/div/div/button").click()
                                            log_deb(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                        else:
                                            browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div["
                                                "1]/div/div/div/span/span[1]/button").click()
                                            log_deb(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)

                                # записываем данные в файл для ссылок всех подписок, если файла нет, создаём,
                                # если есть - дополняем
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                # time.sleep(random.randrange(70, 150))
                                time.sleep(random.randrange(7, 10))

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

        log_inf("Функция завершила свою работу")

    # получение профиля для сбора подпищиков
    def get_donor_followers(self, hashtag):
        """
        Получение профиля с которого можна собрать подпищиков себе

        :param hashtag: string, хештег
        :return: url на профиль
        """
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        log_inf("Инициализация функции поиска донора подпищиков")

        for i in range(2):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        contin = True

        while contin:
            post_url = random.choice(posts_urls)
            browser.get(post_url)
            time.sleep(random.randrange(3, 6))

            browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div/span/a").click()

            time.sleep(random.randrange(5, 10))

            followers_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
            followers_count = followers_button.get_attribute('title')
            # followers_count = followers_button.text

            # если количество подписчиков больше 999, убираем из числа запятые
            if ',' in followers_count:
                followers_count = int(''.join(followers_count.split(',')))
            else:
                followers_count = int(''.join(followers_count.split(' ')))

            log_deb(f"Количество подписчиков: {followers_count}")

            if followers_count > 500:
                contin = False
                log_inf(f"Этот аккаунт подходит - {post_url}")

        donor_url = browser.current_url
        time.sleep(random.randrange(3, 6))

        return donor_url

    # метод создания листа на отписку
    def unsubscribe_create_list(self, username):

        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        log_inf("Инициализация функции создания листа на отписку")

        followers_button = browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        followers_count = followers_button.get_attribute('title')
        # followers_count = followers_button.text
        # followers_count = int(''.join(followers_count.split(' ')))

        following_button = browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span")
        following_count = following_button.text
        log_deb(following_count)
        # following_count = int(''.join(following_count.split(' ')))

        time.sleep(random.randrange(3, 6))

        # если количество подписчиков больше 999, убираем из числа запятые
        if ',' in followers_count:
            followers_count = int(''.join(followers_count.split(',')))
        else:
            followers_count = int(''.join(followers_count.split(' ')))

        if ',' in following_count:
            following_count = int(''.join(following_count.split(',')))
        else:
            following_count = int(''.join(following_count.split(' ')))

        log_deb(f"Количество подписчиков: {followers_count}")
        followers_loops_count = int(followers_count / 7) + 1
        # followers_loops_count = 3
        log_deb(f"Число итераций для сбора подписчиков: {followers_loops_count}")

        log_deb(f"Количество подписок: {following_count}")
        following_loops_count = int(following_count / 7) + 1
        # following_loops_count = 3
        log_deb(f"Число итераций для сбора подписок: {following_loops_count}")

        # собираем список подписчиков
        followers_button.click()
        time.sleep(4)

        followers_ul = ''

        if self.xpath_exists("/html/body/div[5]/div/div/div[2]"):
            followers_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        elif self.xpath_exists("/html/body/div[6]/div/div/div[2]"):
            followers_ul = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]")
        else:
            log_err("followers_ul xpath не найдено")
            exit()

        try:
            followers_urls = []
            log_deb("Запускаем сбор подписчиков...")
            for i in range(1, followers_loops_count + 1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                time.sleep(random.randrange(3, 5))
                log_deb(f"Итерация #{i}")

            all_urls_div = followers_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                followers_urls.append(url)

            # сохраняем всех подписчиков пользователя в файл
            with open(f"{username}_followers_list.txt", "a") as followers_file:
                for link in followers_urls:
                    followers_file.write(link + "\n")

            time.sleep(random.randrange(4, 6))
            browser.get(f"https://www.instagram.com/{username}/")
            time.sleep(random.randrange(3, 6))

            # собираем список подписок
            following_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
            following_button.click()
            time.sleep(random.randrange(3, 5))

            following_ul = ''

            if self.xpath_exists("/html/body/div[5]/div/div/div[2]"):
                following_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
            elif self.xpath_exists("/html/body/div[6]/div/div/div[2]"):
                following_ul = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]")
            else:
                log_err("following_ul xpath не найдено")
                exit()

            following_urls = []
            log_deb("Запускаем сбор подписок")

            for i in range(1, following_loops_count + 1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
                time.sleep(random.randrange(3, 5))
                log_deb(f"Итерация #{i}")

            all_urls_div = following_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                following_urls.append(url)

            # сохраняем всех подписок пользователя в файл
            with open(f"{username}_following_list.txt", "a") as following_file:
                for link in following_urls:
                    following_file.write(link + "\n")

            """Сравниваем два списка, если пользователь есть в подписках, но его нет в подписчиках,
                заносим его в отдельный список"""

            count = 0
            unfollow_list = []
            for user in following_urls:
                if user not in followers_urls:
                    count += 1
                    unfollow_list.append(user)
            log_deb(f"Нужно отписаться от {count} пользователей")

            # сохраняем всех от кого нужно отписаться в файл
            with open(f"{username}_unfollow_list.txt", "a") as unfollow_file:
                for user in unfollow_list:
                    unfollow_file.write(user + "\n")

        except Exception as ex:
            print(ex)
            self.close_browser()

        log_inf("Функция завершила свою работу")

    # Отписка с использованием листа
    def unsubscribe_from_list(self, username, num):
        """
        Отписка от некоторого количества неподписаных в ответ с использованием листа

        :param username: ваш username
        :param num: количество от которого надо отписаться
        :return:
        """

        browser = self.browser
        print("Запускаем отписку...")
        time.sleep(4)

        log_inf("Инициализация функции отписки с использованием листа")

        # заходим к каждому пользователю на страницу и отписываемся
        with open(f"{username}_unfollow_list.txt") as unfollow_file:
            unfollow_users_list = unfollow_file.readlines()
            unfollow_users_list = [row.strip() for row in unfollow_users_list]

        count_pre = len(unfollow_users_list)
        if count_pre > num:
            count = num
        else:
            count = count_pre

        for user_url in range(count):
            try:
                browser.get(unfollow_users_list[user_url])
                time.sleep(random.randrange(7, 13))

                # кнопка отписки
                try:
                    unfollow_button = browser.find_element_by_xpath(
                        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div["
                        "2]/div/span/span[1]/button")
                    unfollow_button.click()
                except Exception as ex:
                    print(ex)
                    unfollow_button = browser.find_element_by_xpath(
                        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button")
                    unfollow_button.click()

                time.sleep(random.randrange(4, 8))

                # подтверждение отписки
                unfollow_button_confirm = browser.find_element_by_xpath(
                    "/html/body/div[5]/div/div/div/div[3]/button[1]")
                unfollow_button_confirm.click()

                log_deb(f"Отписались от {unfollow_users_list[user_url]}")
                count -= 1
                log_deb(f"Осталось отписаться от: {count} пользователей")

                # time.sleep(random.randrange(120, 130))
                time.sleep(random.randrange(4, 8))

            except Exception as ex:
                print(ex)
                log_deb(f"Не вышло отписаться от {user_url}")

        time.sleep(random.randrange(7, 13))

        log_inf("Функция завершила свою работу")

    def like_photo_by_feed(self, num):
        browser = self.browser
        browser.get("https://www.instagram.com/")
        time.sleep(random.randrange(3, 6))

        log_inf("Инициализация функции лайков в ленте")

        podes = []
        button_like = self.browser.find_elements_by_xpath(
            '/html/body/div[1]/section/main/section/div/div[2]/div/article[1]/div[3]/section[1]/span[1]/button')
        for a in range(num):
            button_like.extend(self.browser.find_elements_by_xpath(
                '/html/body/div[1]/section/main/section/div/div[2]/div/article/div[3]/section[1]/span[1]/button'))
            button_like = grass(button_like)
            time.sleep(random.randrange(3, 25))
            try:
                button_like[a].click()
            except Exception as ex:
                print(ex)
                log_err("Пост №" + str(a) + " не удалось нажать")
            commentator = self.browser.find_elements_by_xpath("//article//a[@class='FPmhX notranslate MBL3Z']")
            for c in commentator:
                pod = c.get_attribute('href')
                podes.append(pod)

            podes = grass(podes)
            with open(f"podes.txt", "a") as followers_file:
                for pod in podes:
                    followers_file.write(pod + "\n")

            if bool_random(0.50):  # 50% шанс снятия лайка ботом
                try:
                    button_like[a].click()
                except Exception as ex:
                    print(ex)
                log_deb("Пост №" + str(a) + " пропущеный")
            else:
                log_deb("Пост №" + str(a) + " получил лайк")
        log_inf("Функция завершила свою работу")

    def get_followers_podes(self, num):
        """
                Подписка на пользователей podes

                :param num: количество подписок которые надо сделать
                :return:
                """

        log_inf("Инициализация функции подписки на пользователей определенного аккаунта")
        with open("podes.txt") as text_file:
            users_urls = text_file.readlines()

            for user in users_urls[0:num - 1]:
                try:
                    browser = self.browser
                    browser.get(user)
                    page_owner = user.split("/")[-2]

                    if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):
                        log_deb("Это наш профиль, уже подписан, пропускаем итерацию!")
                    elif self.xpath_exists(
                            "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span["
                            "1]/button/div/span"):
                        log_deb(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                    else:
                        time.sleep(random.randrange(4, 8))

                        if self.xpath_exists(
                                "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                            try:
                                browser.find_element_by_xpath(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div["
                                    "1]/div/div/button").click()
                                log_deb(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                            except Exception as ex:
                                print(ex)
                        else:
                            try:
                                if self.xpath_exists(
                                        "/html/body/div[1]/section/main/div/header/section/div[1]/div["
                                        "1]/div/div/button"):
                                    browser.find_element_by_xpath(
                                        "/html/body/div[1]/section/main/div/header/section/div[1]/div["
                                        "1]/div/div/button").click()
                                    log_deb(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                else:
                                    browser.find_element_by_xpath(
                                        "/html/body/div[1]/section/main/div/header/section/div[1]/div["
                                        "1]/div/div/div/span/span[1]/button").click()
                                    log_deb(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                            except Exception as ex:
                                print(ex)

                        time.sleep(random.randrange(7, 10))

                except Exception as ex:
                    print(ex)
                    self.close_browser()

        log_inf("Функция завершила свою работу")


def bool_random(a):
    if float(random.random()) < a:
        return True
    else:
        return False


def grass(l):
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n
