from selenium.webdriver.common import action_chains, keys
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("http://honorcup.ru/quiz/frame/")

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

with open('cookies.pkl', 'rb') as cookie_file: # with auto close file.
    cookies = pickle.load(cookie_file)
    for cookie in cookies:
        driver.add_cookie(cookie)
        print(cookie)

driver.get("http://honorcup.ru/quiz/frame/")

fight_button = driver.find_element_by_xpath("//div[@class=button stretch]")
fight_button = driver.find_element_by_class_name("button stretch")
fight_button = driver.find_element_by_xpath("//div[@class=button stretch]")

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

driver.find_element_by_xpath("//*[@class='button stretch play']").click()

driver.find_element_by_xpath("//*[@class='button play']").click()


driver.find_elements_by_class_name("game__answer")[randint(0,4)].click()

wait = WebDriverWait(driver, 10)

element = wait.until(element_has_css_class((By.ID, 'myNewInput'), "myCSSClass"))
