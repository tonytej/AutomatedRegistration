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

def add_class(crnnum):
    print('Checking...')
    done = False
    while not done:
        for e in crnnum:
            try:
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
                    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'term_id')))
                    select = Select(browser.find_element_by_id('term_id'))
                    select.select_by_visible_text('2017 Spring Foothill')
                    submit = browser.find_element_by_class_name('dataentrytable')
                    submit.submit()

                    browser.switch_to.default_content()
                    browser.switch_to.frame('content')
                    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'crn_id1')))
                    crn = browser.find_element_by_id('crn_id1')
                    crn.send_keys(e)
                     
                    submit = browser.find_element_by_xpath('//input[@value="Submit Changes"]')
                    browser.execute_script('arguments[0].click()', submit)
                    WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'waitaction_id1')))
                    print('Slot available on ' + e + '. Waitlisting...')
                    select1 = Select(browser.find_element_by_id('waitaction_id1'))
                    select1.select_by_visible_text('Waitlisted')
                    submit = browser.find_element_by_xpath('//input[@value="Submit Changes"]')
                    browser.execute_script('arguments[0].click()', submit)
                    print('Waitlisted on ' + e)
                    done = True
            except:
                print(e + ' full.')
                browser.get('https://myportal.fhda.edu')
                login(sid, pwd)
                continue
            break

sid = input('Student ID: ')
pwd = input('Password: ')

print('Opening browser...')
browser = webdriver.Firefox()
browser.get('https://myportal.fhda.edu')
print('Logging in...')
login(sid, pwd)
add_class(['40419', '40169', '41460'])


