import os
import shutil

from loge import log_inf, log_deb, log_err

whitelist = [".idea",
             "log",
             "chromedriver",
             "clean.py",
             "data.py",
             "insta.py",
             "loge.py",
             "main.py",
             "main2.py",
             "moon_eva",
             "old",
             "prod",
             "requirements.txt",
             "test.py",
             "test2.py",
             "venv",
             "__pycache__"]


def clean():
    folder = os.listdir()

    log_inf("Инициализация функции очистки")

    for a in folder:
        if a not in whitelist:
            try:
                if os.path.isfile(a):
                    os.remove(a)
                    log_deb(f"Файл {a} успешно удален")
                elif os.path.isdir(a):
                    shutil.rmtree(a)
                    log_deb(f"Папка {a} успешно удалена")
                else:
                    log_err(f"{a} не файл и не папка")
            except Exception as ex:
                print(ex)
                log_err(f"{a} не вышло удалить")

    log_inf("Функция завершила свою работу")
