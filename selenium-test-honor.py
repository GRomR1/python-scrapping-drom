from selenium.webdriver.common import action_chains, keys
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

right_answers = dict()

def init_browser():
    driver = webdriver.Chrome()

    driver.get("http://honorcup.ru/quiz/frame/")

    # на случай если нужно сохранить куки
    # pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

    with open('cookies.pkl', 'rb') as cookie_file: # with auto close file.
        cookies = pickle.load(cookie_file)
        for cookie in cookies:
            driver.add_cookie(cookie)
            print(cookie)

    driver.get("http://honorcup.ru/quiz/frame/")
    sleep(3)

    driver.set_window_size(480, 640)
    driver.get_window_size()
    return driver

def start_game(driver):
    # Ищем кнопку Перейти в игру
    enter_the_game = driver.find_element_by_xpath("//*[@class='btn btn_bottom btn_big']")
    enter_the_game.click()
    sleep(2)

    # Ищем кнопку Сражаться за кубок!
    # driver.find_element_by_xpath("//*[@class='button stretch']").get_attribute('innerHTML')
    fight_button = driver.find_element_by_xpath("//*[@class='button stretch']")
    fight_button.click()
    sleep(2)

    # Открываем категорию IoT
    # driver.find_element_by_xpath("//*[@class='theme__layout type-5']").get_attribute('innerHTML')
    iot_category = driver.find_element_by_xpath("//*[@class='theme__layout type-5']")
    iot_category.click()
    sleep(2)

    # Открываем первую тему - Основы IoT
    # driver.find_elements_by_xpath("//*[@class='profile__theme']")[0].get_attribute('innerHTML')
    # driver.find_elements_by_xpath("//*[@class='profile__theme']")[0].text
    iot_base_theme = driver.find_elements_by_xpath("//*[@class='profile__theme']")[0]
    iot_base_theme.click()
    sleep(2)

    # Выбираем Играть
    play = driver.find_element_by_xpath("//*[@class='button play']")
    # play.get_attribute('innerHTML')
    print(play.text)
    play.click()
    sleep(2)

# Отвечаем на вопрос
def answer_to_question(driver, question):
    try:
        answers = driver.find_elements_by_class_name("game__answer")
        answer = answers[randint(0, 4)]
        print(answer.text)
        answer.click()
        sleep(2)
        print(answer.get_attribute("class"))
        if answer.get_attribute("class").find("right") != -1:
            print("!!: {} --- {}".format(question, answer.text))
            right_answers[question] = answer.text
        return True
    except Exception as e:
        print(e)
        return None

# Ждем вопроса
def wait_question(driver):
    try:
        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "game__question-text"))
        )
        print(element.text)
        return element.text
    except Exception as e:
        print(e)
        return None

def check_connection_error(driver):
    try:
        repeat = driver.find_element_by_xpath("//*[@class='problem__icon connection']")
        repeat.click()
        return True
    except Exception as e:
        print("Args: {}\n Type: {}".format(e.args, type(e)))
        print(e)
        return None

# Класс экрана возникающий при ошибке подключения
# problem__icon connection
# При ошибке подключения - Кнопка закрыть - ее класс
# button border red
# После ее нажатия - start_game(driver)

def wait_next_round(driver):
    try:
        element = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "search__round"))
        )
        print(element.text)
        return True
    except NoSuchElementException as e:
        pass
    except Exception as e:
        print("Args: {}\n Type: {}".format(e.args, type(e)))
        print(e)
        return None


# После игры - нажимаем сыграть еще
def repeat_game(driver):
    try:
        repeat = driver.find_element_by_xpath("//*[@class='button stretch play']")
        repeat.click()
        return True
    except Exception as e:
        print("Args: {}\n Type: {}".format(e.args, type(e)))
        print(e)
        return None


driver = init_browser()
start_game(driver)

while True:
    # 5 раундов
    for i in range(5):
        wait_next_round(driver)
        sleep(5)
        question = wait_question(driver)
        if question:
            while not answer_to_question(driver, question):
                sleep(1)
    sleep(50)
    while not repeat_game(driver):
        sleep(1)


repeat_game(driver)

# Класс экрана возникающий при ошибке подключения
# problem__icon connection
# При ошибке подключения - Кнопка закрыть - ее класс
# button border red
# После ее нажатия - start_game(driver)

# Смотрим что за вопрос
question = driver.find_element_by_class_name("game__question-text")
print(question.text)

# Выбираем случайно ответ, выводим его в консоль и отвечаем
answer = driver.find_elements_by_class_name("game__answer")[randint(0,4)]
print(answer.text)
answer.click()




driver.find_element_by_xpath("/html/body").get_attribute('innerHTML')

driver.find_element_by_xpath("/html/body/app/div[1]/about/div/div/div/div[5]").get_attribute('innerHTML')

driver.find_element_by_xpath("/html/body/app/div[1]/about/div/div/div/div[5]/div/span[2]").get_attribute('innerHTML')

driver.find_element_by_xpath("/html/body/app/div[1]/about/div/div/div/div[5]/div/span[2]").click()

driver.find_element_by_xpath("/html/body/app/div[1]/nomination/div/div/div[2]/slider/div/div/div[1]/div/div[3]/div/div").get_attribute('innerHTML')
driver.find_element_by_xpath("/html/body/app/div[1]/nomination/div/div/div[2]/slider/div/div/div[1]/div/div[3]/div/div").click()

driver.find_element_by_class_name("profile__theme").get_attribute('innerHTML')

themes = driver.find_elements_by_class_name("profile__theme")

for x in themes:
  print(x.text)

themes[0].click()

driver.find_element_by_class_name("profile__theme").click()

driver.find_element_by_xpath("//*[@class='button play']").get_attribute('innerHTML')


driver.find_element_by_xpath("//*[@class='button play']").click()


play = driver.find_element_by_xpath("//*[@class='button play']")

wait = WebDriverWait(driver, 10)
element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "game__question-text")))

# page

repeat = driver.find_element_by_xpath("//*[@class='game__answer selected wrong']")
