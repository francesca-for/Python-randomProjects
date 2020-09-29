##!/usr/bin/env python    # per lanciarlo da terminale

from selenium import webdriver
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options

chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
chromedriver_path = '/Users/fornasierarmando/Documents/chromedriver'
page_URL = 'https://www.instagram.com/accounts/login/'
WINDOW_SIZE = "1920,1080"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = chrome_path

# browser = webdriver.Chrome(chromedriver_path)    # per debug in caso di errori
browser = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)     # copiato da fra


# definizione metodi

def login(browser, username, password):
    browser.get(page_URL)
    time.sleep(2)

    try:
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    except NoSuchElementException:
        print("Login failed. Unable to locate Username/Password/LogIn element(s)")

    time.sleep(2)
    if len(browser.find_elements_by_xpath('//*[@id="slfErrorAlert"]'))!=0 :  # if login is unsuccessful
        print("Login failed. Please, double-check your credentials")
    else:
        print("Login successful")
    time.sleep(4)

    # if two-factor authentication is on :
    found = browser.find_elements_by_xpath('//*[@id="verificationCodeDescription"]')
    if len(found)!=0:
        otp = input('Insert security code: ')
        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input').send_keys(otp+'\n')
        time.sleep(3)

        # if security code is not correct -> you can try again
        if len(browser.find_elements_by_xpath('//*[@id="twoFactorErrorAlert"]'))!=0 :
            browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input').clear()
            otpNew = input('Security code is not correct.\nInsert security code again: ')
            browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input').send_keys(otpNew+'\n')
            time.sleep(3)

    browser.get('https://www.instagram.com/francesca_fornasier/')
    time.sleep(5)


def editProfileEveryHour(browser, b1, b2):
    birth = datetime(1999,5,16,15,30)
    iterations = 0

    while True :
        c_time = datetime.now()
        life = c_time - birth
        life_hours = int(int(life.total_seconds())/3600)

        browser.get('https://www.instagram.com/accounts/edit/')
        time.sleep(4)

        newBioWithName = updateName(iterations%3) + '\n' + bio1 + "21  ≈  " + str(life_hours) + " ± 1 ore      :)" + bio2

        editBio(browser, newBioWithName)

        time.sleep(4)
        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/form/div[10]/div/div/button').click()   # save

        print('Descrizione aggiornata:  '+ str(c_time)+'   |   '+updateName(iterations%3)+'    |    '+str(life_hours))

        iterations+=1
        time.sleep(890)   # update every 15 minutes


def editBio(browser, new):
    browser.find_element_by_xpath('//*[@id="pepBio"]').clear()
    browser.find_element_by_xpath('//*[@id="pepBio"]').send_keys(new)


def updateName(numL):
    name = ['f', 'r', 'a']
    name[numL] = name[numL].upper()
    newName = str(name[0])+name[1]+name[2]
    return newName



# MAIN

username = input('Insert username:' )
password = input('Insert password:' )

login(browser, username, password)
time.sleep(2)

bio1 = "• Torino\n• PoliTo\n• "
bio2 = "\n________________________________________"

editProfileEveryHour(browser, bio1, bio2)

browser.close()
