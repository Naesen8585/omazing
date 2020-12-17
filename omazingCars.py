import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from dbmanager import *

DBNAME="omaze.sqlite"

def getCarList():
    url="https://www.omaze.com/collections/omaze-cars"
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--ignore_certificate_errors")
    #options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    #scroll down and ensure it's all loaded
    for i in range(5000):
        time.sleep(.01)
        driver.execute_script("window.scrollTo(0,"+str(i)+")")
    #time.sleep(5)
    #driver.find_element(By.ID, "ozEmailOptinCustomerEmail").click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    url_list=[]
    for rawlink in soup.find_all('a'):
        try:
            if rawlink.attrs['href'].startswith("/products"):
                strippedlink = rawlink.attrs['href'].split("https://")[-1]
                url_list.append("https://www.omaze.com" + strippedlink)
        except:
            continue
    driver.close()
    return url_list

def enterCarContest(url,firstname,lastname,email,address,zip,city,state):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--ignore_certificate_errors")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    time.sleep(random.random()*random.randint(3,5))
    driver.find_element(By.LINK_TEXT, "Enter without contributing").click()
    time.sleep(random.random() * random.randint(3, 5))
    driver.find_element(By.ID, "country-select").click()
    dropdown = driver.find_element(By.ID, "country-select")
    dropdown.find_element(By.XPATH, "//option[. = 'United States']").click()
    realkeystrokes(driver.find_element(By.NAME, "first_name"),firstname)
    realkeystrokes(driver.find_element(By.NAME, "last_name"),lastname)
    realkeystrokes(driver.find_element(By.NAME, "email"),email)
    realkeystrokes(driver.find_element(By.NAME, "address1"),address)
    realkeystrokes(driver.find_element(By.NAME, "city"),city)
    driver.find_element(By.ID, "province-select").click()
    dropdown = driver.find_element(By.ID, "province-select")
    dropdown.find_element(By.XPATH, "//option[. = '"+state+"']").click()
    realkeystrokes(driver.find_element(By.ID, "zip-input"),zip)
    driver.execute_script("document.getElementById('payment-form').submit()")
    driver.close()
    print("Sleeping for the cooldown period...")
    time.sleep(60+(random.random()*random.randint(15,120)))

def realkeystrokes(element,text):
    time.sleep(random.random()*random.randint(2,4))
    element.click()
    for c in text:
        time.sleep(random.random()/random.randint(3,5))
        element.send_keys(c)



def mainfunction():
    tableGenerator(DBNAME)
    firstname=input("First name >")
    lastname=input("Last name >")
    email=input("Email address >")
    address=input("Street address >")
    city=input("City >")
    state=input("State (full, no abbreviations)>")
    zip=input("Zip code >")
    carurls=getCarList()
    for url in carurls:
        while geturlvalue(DBNAME,url) < 3:
            enterCarContest(url=url,firstname=firstname,lastname=lastname,email=email,address=address,city=city,state=state,zip=zip)
            updatedb(DBNAME,url)
        print("Max submissions for "+url+" completed!")

mainfunction()
