#import stdiomask
''' a cross-platform Python module for entering passwords to a stdio
    terminal and displaying a **** mask, which getpass cannot do
    -> To be istalled with pip    '''
from selenium import webdriver
import time
from datetime import datetime
from selenium.webdriver.firefox.options import Options

firefox_path = '/Applications/Firefox.app/Contents/MacOS/Firefox'
geckodriver_path = '/Users/fornasierarmando/Documents/geckodriver'
page_URL = 'https://www.instagram.com/accounts/login/'
WINDOW_SIZE = "1920,1080"

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("--headless")
firefox_options.add_argument("--window-size=%s" % WINDOW_SIZE)
firefox_options.binary_location = firefox_path

#browser = webdriver.Firefox(executable_path=geckodriver_path)    # per debug in caso di errori
browser = webdriver.Firefox(executable_path=geckodriver_path, options=firefox_options)



# definizione metodi


def login(browser):
    username = input('Username: ')
    password = input('Password: ')
    #password = stdiomask.getpass(prompt = 'Insert password: ', mask = '*')    # idk if it's correct

    browser.get(page_URL)
    time.sleep(2)

    try:
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
        if len(browser.find_elements_by_xpath('/html/body/div[2]/div/div/div/div[1]/h3'))!=0 :
            browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]').click()   # accept cookies
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    except NoSuchElementException:
        print("Login failed. Unable to locate login element(s)")

    time.sleep(2)
    if len(browser.find_elements_by_xpath('//*[@id="slfErrorAlert"]'))!=0 :  # if login is unsuccessful
        print("Login failed. Please, double-check your credentials")
        login(browser)
    else:
        print("Login successful")
    time.sleep(4)


def editProfileEveryNhours(browser, b1, b2):
    birth = datetime(1999,5,16,17,30)
    iterations = 0

    while True :
        c_time = datetime.now()
        life = c_time - birth
        life_hours = int(int(life.total_seconds())/3600)

        browser.get('https://www.instagram.com/accounts/edit/')
        time.sleep(4)

        new_bio = updateName(iterations%3) + '\n' + bio1 + str(getAge(c_time, birth)) + "\t≈\t" + str(life_hours) + " ± 1 ore      :)\n" + bio2

        editBio(browser, new_bio)

        time.sleep(4)
        browser.find_element_by_xpath('/html/body/div[1]/section/main/div/article/form/div[10]/div/div/button').click() # save

        print('Last update:   '+ str(c_time)+'   |   '+updateName(iterations%3)+'    |    '+str(life_hours))

        iterations+=1
        time.sleep(1790)   # update every 30 minutes


def getAge(c_time, birth) :
    age = int(c_time.year) - int(birth.year)
    if c_time.month<birth.month or (c_time.month==birth.month and c_time.day<birth.day) :
        age-=1
    return age


def editBio(browser, new_bio):
    browser.find_element_by_xpath('//*[@id="pepBio"]').clear()
    browser.find_element_by_xpath('//*[@id="pepBio"]').send_keys(new_bio)


def updateName(numL):
    name = ['f', 'r', 'a']
    name[numL] = name[numL].upper()
    newName = str(name[0])+name[1]+name[2]
    return newName



#*******   MAIN   *******

login(browser)
twoFactorAuthentication(browser)
time.sleep(2)

bio1 = "📍 Torino\n📚 PoliTo\n🔸 "
bio2 = "\n________________________________________"

editProfileEveryNhours(browser, bio1, bio2)

browser.close()
