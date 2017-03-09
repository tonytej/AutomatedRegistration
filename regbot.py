from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchFrameException

def login(SID, password):
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'user')))
    userid = browser.find_element_by_id('user')
    userid.send_keys(SID)
    pwd = browser.find_element_by_id('pass')
    pwd.send_keys(password)
    pwd.submit()

def goToReg():
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Registration')))
    reg = browser.find_element_by_link_text('Registration')
    browser.execute_script('arguments[0].click();', reg)
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'Chnl_OpenCourses_TermCode')))
    select = Select(browser.find_element_by_id('Chnl_OpenCourses_TermCode'))
    select.select_by_visible_text('2017 Spring De Anza')
    button = browser.find_element_by_xpath('//button[text()="Browse Course Listings"]')
    browser.execute_script('arguments[0].click();', button)

def add_class(crnnum):
    browser.execute_script('window.history.go(-1)')
    browser.switch_to.default_content()
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Registration')))
    reg = browser.find_element_by_link_text('Registration')
    browser.execute_script('arguments[0].click();', reg)

    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Add or Drop Classes')))
    add = browser.find_element_by_link_text('Add or Drop Classes')
    browser.execute_script('arguments[0].click();', add)

    browser.switch_to.default_content()
    browser.switch_to.frame('content')
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'dataentrytable')))
    submit = browser.find_element_by_class_name('dataentrytable')
    submit.submit()

    browser.switch_to.default_content()
    browser.switch_to.frame('content')
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'crn_id1')))
    crn = browser.find_element_by_id('crn_id1')
    crn.send_keys('00436')
    submit = browser.find_element_by_xpath('//input[@value="Submit Changes"]')
    browser.execute_script('arguments[0].click()', submit)

def isAvailable(coursename):
    browser.switch_to.default_content()
    while True:
        try:
            browser.switch_to.frame('content')
        except NoSuchFrameException:
            browser.refresh()
            continue
        break
    while True:
        try:
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, '//table[@dept="ACCT"]')))
        except TimeoutException:
            browser.refresh()
            continue
        break
    try:
        course = browser.find_element_by_xpath('//td[text()="' + coursename + '"]')
    except NoSuchElementException:
        return False
    if course.is_displayed():
        return True
    return False

def getcrn(coursename):
    table = browser.find_element_by_xpath('//table[@dept="MATH"]')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        coursecol = row.find_elements(By.TAG_NAME, 'td')
        if len(coursecol) > 1 and coursecol[3].text == coursename:
                return coursecol[2].text

#sid = input('Student ID: ')
#pwd = input('Password: ')
#course = input('Course to be found (CAPITAL LETTERS): ')

sid = '20241842'
pwd = 'Jetynot1997'
course = 'LINEAR ALGEBRA'

print('Opening browser...')
browser = webdriver.Firefox()
browser.get('http://myportal.fhda.edu')
print('Logging in...')
login(sid, pwd)
goToReg()

while True:
    try:
        print('Checking...')
        while not isAvailable(course):
            browser.refresh();
        print('Adding...')
        add_class(getcrn(course))
        print('Course added succesfully')
    except:
        browser.get('http://myportal.fhda.edu')
        goToReg()
        continue
    break


