"""

© Copyright 2023 Kalmyk1902
Распространяется по лицензии Apache 2.0


"""
# импортируем нужные библиотеки
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# основная функция программы
def homework(LOGIN: str, PASSWORD: str):
    try: # пробуем выполнить код без ошибок
        url = 'https://schools.by/login' # задаем переменную с ссылкой входа на сайт
        week = datetime.today().strftime('%A') # получаем сегодняшний день недели

        options = Options() # объявляем настройки браузера
        options.add_argument('--headless') # выключаем интерфейс браузера
        options.add_experimental_option("excludeSwitches", ["enable-logging"]) # выключаем логирование
        driver = webdriver.Chrome(options=options) # запускаем браузер (в данном случае Google Chrome)
        wait = WebDriverWait(driver, 10) # задаем таймаут в 10 секунд (позже будет использован)

        driver.get(url) # входим на сайт
        username = driver.find_element(By.ID, 'id_username') # ищем поле ввода логина
        password = driver.find_element(By.ID, 'id_password') # ищем поле ввода пароля
        login = driver.find_element(By.XPATH, "//div[@class='button_wrap']/input[2]") # ищем кнопку входа

        username.send_keys(LOGIN) # вставляем введенный логин
        password.send_keys(PASSWORD) # вставляем введеный пароль
        login.click() # нажимаем кнопку входа
        driver.implicitly_wait(10) # ждем ответа сервера

        if driver.current_url == url: # если мы остались на той же ссылке (не удалось войти)...
            driver.quit() # закрываем браузер
            return 'Не удалось войти :(' # выдаем сообщение об этом

        dnevnik = driver.find_element(By.XPATH, "//ul[contains(@id, 'pupil_tabs_menu')]/li[1]/a") # ищем кнопку для входа в дневник
        dnevnik.click() # нажимаем на нее
        wait.until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, 'td.lesson'))) # ждем загрузки всех уроков в дневнике

        search = 'quarter' if week != 'Saturday' and week != 'Sunday' else 'week' # настройка поиска запросов в зависимости от сегодняшнего дня
        if search == 'week': # если сегодня суббота или воскресенье...
            next = driver.find_element(By.XPATH, "//a[@class='next']") # ищем кнопку перехода на след. страницу
            next.click() # нажимаем на нее
            wait.until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'td.lesson'))) # ждем ее загрузки (исчезновения старых элементов)
        entries = driver.execute_script('return window.performance.getEntries()') # при помощи JavaScript получаем все полученные запросы
        for entry in reversed(entries): # проходимся по всем запросам
            if entry['initiatorType'] == 'xmlhttprequest' and search in entry['name']: # если находим XHR-запрос в котором есть ссылка новой страницы...
                rurl = entry['name'] # сохранаяем ее
                break # выходим из цикла поиска
        driver.get(rurl) # переходим по ссылке (чтобы не видеть лишних элементов с прошлой страницы)
        driver.implicitly_wait(10) # ждем ее загрузки

        with open('days.json', 'r', encoding='utf-8') as f: # открываем JSON-файл с настройками поиска в зависимости от сегодняшнего дня
            weekdays = json.load(f) # загружаем оттуда данные
            weekday = weekdays[week] # задаем переменную для поиска домашки по нужному дню

        tables = driver.find_elements(By.CSS_SELECTOR, 'div.db_day') # ищем все таблицы с уроками
        for t in tables: # проходимся по каждой таблице
            if weekday in t.text: # если находим нужную таблицу
                table = t # объявляем переменную с ней
                break # выходим из цикла поиска

        with open('CACHE.HTML', 'w', encoding='utf-8') as f: # создаем файл с данными с сайта
            f.write(table.get_attribute('innerHTML')) # записываем всю таблицу туда
           
        driver.quit() # закрываем браузер
        final = '' # объявляем финальную строку, присваивая пустое значение
        lessons, works = [], [] # объявляем списки для результатов анализа таблицы

        with open('CACHE.HTML', 'r', encoding='utf-8') as f: # открываем ранее сохраненный файл
            soup = BeautifulSoup(f, 'html.parser') # создаем объект анализа таблицы
            LESSONS = soup.select('td.lesson') # ищем все названия предметов
            for LESSON in LESSONS: # проходимся по каждому элементу
                LESSON = LESSON.text.replace('\n', '').replace('.', '. ', 1) # убираем все переходы строк и добавляем пробел после номера предмета
                lessons.append(LESSON) # добавляем предмет в список

            WORKS = soup.select('td.ht') # ищем все записи домашнего задания
            for WORK in WORKS: # проходимся по каждому элементу
                WORK_SRCH = WORK.find('div', class_='ht-text') # ищем текст в элементе
                works.append(WORK_SRCH.text.strip() if WORK_SRCH is not None else ' ') # добавляем текст Д/З в список если текст есть, иначе добавляем пустую строку

        for lesson, work in zip(lessons, works): # берем 2 списка и берем по одному элементу в них
            final += f'{lesson} – {work}\n' # и добавляем их в финальную строку

        os.remove('CACHE.HTML') # удаляем ранее сохраненный файл
        return final # выдаем Д/З в программу

    except WebDriverException: # при отсутствии интернета...
        return 'НЕТ ИНТЕРНЕТА!' # выдаем сообщение об этом