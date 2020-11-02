# spamma robe a caso su telegram

#import
from selenium import webdriver
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options


#variables
chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
chromedriver_path = '/Users/fornasierarmando/Documents/chromedriver'
telegram_login_page = 'https://web.telegram.org/#/login'

WINDOW_SIZE = "1920,1080"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = chrome_path

browser = webdriver.Chrome(chromedriver_path)    # per debug in caso di errori
#browser = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)


#methods declaration
def login(browser, p_number) :
    browser.get(telegram_login_page)
    time.sleep(3)

    try :
        browser.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/input').send_keys(p_number)
    except NoSuchElementException:
        print('Login failed. unable to locate login element(s)')

    browser.find_element_by_xpath('//*[@id="ng-app"]/body/div[5]/div[2]/div/div/div[2]/button[2]').click()

    # if two-factor authentication is on
    if len(browser.find_elements_by_xpath('//*[@id="ng-app"]/body/div[1]/div/div[2]/div[2]/form/div[4]/input'))!=0 :
        otp = input('Insert opt (sent on Telegram app): ')
        browser.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div/div[2]/div[2]/form/div[4]/input').send_keys(otp)
        # GESTIRE CASO DI ERRORE NEL CODICE


def getNumMessages():
    num = input('How many messages do you want to spam? ')
    if (n>=3600):
        num = 3599
    if (n<0):
        num = 0
    return num


def spammiamo(target, num_msg):
    print('\nOOK!!')
    # TO-DO to be implemented


#MAIN
p_number = input('Insert your phone number to login: ')+'\n'
login(browser, p_number)

target = input('Who is the target? ')
num_msg = getNumMessages()

spammiamo(target, num_msg)

browser.close()
