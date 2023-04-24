import json
import multiprocessing as mp
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def homework(LOGIN: str, PASSWORD: str):
    try:
        url = 'https://schools.by/login'
        week = datetime.today().strftime('%A')

        options = Options()
        options.add_argument('--headless')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        driver.get(url)
        username = driver.find_element(By.ID, 'id_username')
        password = driver.find_element(By.ID, 'id_password')
        login = driver.find_element(By.XPATH, "//div[@class='button_wrap']/input[2]")

        username.send_keys(LOGIN)
        password.send_keys(PASSWORD)
        login.click()
        driver.implicitly_wait(10)

        if driver.current_url == url:
            driver.quit()
            return 'Не удалось войти :('

        dnevnik = driver.find_element(By.XPATH, "//ul[contains(@id, 'pupil_tabs_menu')]/li[1]/a")
        dnevnik.click()
        wait.until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, 'td.lesson')))

        search = 'quarter' if week != 'Saturday' and week != 'Sunday' else 'week'
        if search == 'week':
            next = driver.find_element(By.XPATH, "//a[@class='next']")
            next.click()
            wait.until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'td.lesson')))
        entries = driver.execute_script('return window.performance.getEntries()')
        for entry in reversed(entries):
            if entry['initiatorType'] == 'xmlhttprequest' and search in entry['name']:
                rurl = entry['name']
                break
        driver.get(rurl)
        driver.implicitly_wait(10)

        with open('days.json', 'r', encoding='utf-8') as f:
            weekdays = json.load(f)
            weekday = weekdays[week]

        final = ''
        tables = driver.find_elements(By.CSS_SELECTOR, 'div.db_day')
        for table in tables:
            if weekday in table.text:
                lessons = table.find_elements(By.CSS_SELECTOR, 'td.lesson')
                infos = table.find_elements(By.CSS_SELECTOR, 'td.ht')
                works = []
                for info in infos:
                    try:
                        works.append(info.find_element(By.CSS_SELECTOR, 'div.ht-text').text)
                    except NoSuchElementException:
                        works.append(' ')
                for lesson, work in zip(lessons, works):
                    final += f'{lesson.text} {work}\n'
                final = final[:-2]
                break

        driver.quit()
        return final

    except WebDriverException:
        return 'НЕТ ИНТЕРНЕТА!'
    