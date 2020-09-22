# ig bot 1
# modifica automaticamente la bio di instagram ogni giorno

from selenium import webdriver
import time
from datetime import datetime

chromedriverPath = '/Users/fornasierarmando/Documents/chromedriver'
page_URL = 'https://www.instagram.com'
browser = webdriver.Chrome(chromedriverPath)
browser.get(page_URL)   #apre URLq


# definizione metodi

def login(browser, username, password):
    #browser.get("https://www.instagram.com/accounts/login/")
    time.sleep(2)

    try:
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    except NoSuchElementException:
        print("Login failed. Unable to locate Username/Password/LogIn element(s)")

    ok = browser.find_elements_by_xpath('//*[@id="slfErrorAlert"]')
    if len(ok)!=0:
        print("Login failed. Please, double-check your credentials")
        login(browser, username, password)
    else:
        print("Login successful")
    time.sleep(5)

    # in caso di autenticazione a due fattori
    found = browser.find_elements_by_xpath('//*[@id="verificationCodeDescription"]')
    if len(found)!=0:
        otp = input('Insert security code: ')
        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input').send_keys(otp)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/button').click()
        time.sleep(3)

        ok = browser.find_elements_by_xpath('//*[@id="twoFactorErrorAlert"]') :   # if security code is not correct
        if len(ok)!=0 :
            browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input').clear()
            otpNew = input('Security code is not correct.\nInsert security code again: ')
            browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input').send_keys(otpNew)
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/button').click()
            time.sleep(3)

def editProfileEveryHour(action, bio1, bio2):
    birth = datetime(1999,5,16,15,30)
    iterations = 0

    while True:
        c_time = datetime.now()
        life = c_time - birth
        life_hours = int(int(life.total_seconds()/3600))

        browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').click()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div/div[2]/div[2]/a[3]/div').click()
        time.sleep(5)

        #newBio = bio1 + "21 ≈ " + str(int(life_hours/24)) + " ± 1 giorni" + bio2  # ~
        newBio = bio1 + "21 ≈ " + str(life_hours) + " ± 1 ora" + bio2

##        if action == "bio":
##            updateBio(newBio)
##        else if action == "name":
##            updateName(iterations%3)

        updateBio(newBio)
        updateName(iterations%3)
##      if (life_hours%24) == 0 :
##          updateBio(newBio)

        time.sleep(2)

        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/form/div[10]/div/div/button').click()

        print('Descrizione aggiornata: '+ str(c_time)+'    ||    '+str(int(life_hours/24)))

        iterations+=1
        time.sleep(50+60*59)


def updateBio(new):
    browser.find_element_by_xpath('//*[@id="pepBio"]').clear()
    browser.find_element_by_xpath('//*[@id="pepBio"]').send_keys(new)


def updateName(numL):
    name = ['f', 'r', 'a']
    name[numL] = name[numL].upper()
    newName = str(name[0])+name[1]+name[2]
    browser.find_element_by_xpath('//*[@id="pepName"]').clear()
    browser.find_element_by_xpath('//*[@id="pepName"]').send_keys(newName)



# MAIN

username = input('Insert username:' )
password = input('Insert password:' )
bio1 = "• Torino\n• PoliTo\n• "
bio2 = "\n________________________________________"

login(browser, username, password)

action = input('What do you want to edit? (choose bw name - bio) ')
editProfileEveryHour(action, bio1, bio2)

time.sleep(2)

browser.close()
