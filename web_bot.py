from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime



# modificare la path di Chrome e di chromedriver (da scaricare da internet)
CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
CHROMEDRIVER_PATH = 'C:/Users/Francesco/Documents/GitHub/test_bot/chromedriver.exe'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                            options=chrome_options
                            )

def login(browser, username, password):
    """ Methods that log in to Instagram by taking user's credentials as parameters"""
    browser.get("https://www.instagram.com/accounts/login/")
    time.sleep(2)
    try:
        browser.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username) # filling username
        browser.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password) # filling password
        browser.find_element_by_xpath("//button[@type=\"submit\"]").click()              # submit form
    except NoSuchElementException:
        print("Failed to log in: Unable to locate Username/Password/LogIn element(s)")

    # If login is unsuccessful, Instagram will show a message "Sorry, your password was incorrect. Please double-check your password."
    success = browser.find_elements_by_xpath("//p[@id = \"slfErrorAlert\"]")
    if len(success) == 0:
        print("Login successful!")
    else:
        print("Sorry, sign in unsuccessful. Please double-check your credentials.")

    time.sleep(5)
    browser.get_screenshot_as_file("capture1.png")
    otp= input("inserisci qui l'otp: ")
    browser.find_element_by_xpath("//input[@name=\"verificationCode\"]").send_keys(otp+'\n')
    time.sleep(5)
    browser.get("https://www.instagram.com/mazza._.francesco/")
    time.sleep(5)
    browser.get_screenshot_as_file("capture2.png")



username= input('Inserisci il tuo username: ')
password = input('Inserisci la tua Password: ')

# per il login suppongo ci sia l'autenticazione a due fattori altrimenti cancellare la parte finale della funzione login()
login(browser,username,password)
time.sleep(3)


while 1:
    browser.get("https://www.instagram.com/accounts/edit/")
    time.sleep(5)
    now = datetime.now()
    birth = datetime(2001,1,31,20,35)
    life = now - birth
    life_in_seconds=str(int(life.total_seconds()))
    browser.find_element_by_id('pepBio').clear()
    browser.find_element_by_id('pepBio').send_keys('SNS | Chemistry\nBeach Tennis\nAl mondo da circa %s ± 60 secondi' % life_in_seconds)
    time.sleep(2)
    browser.find_element_by_xpath('//button[normalize-space()="Invia"]').click()
    print('Descrizione aggiornata: '+str(now)+'    ||    '+str(life_in_seconds))
    time.sleep(52)

browser.close()
