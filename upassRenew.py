from selenium import webdriver
from typing import Dict, List
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import os
import json


#Load configuration:
with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json') as config:
        config_data: Dict[str, str] = json.load(config)
        j_username = config_data['username']
        j_password = config_data['password']


#Select the upass student in UBC.
browser = webdriver.Chrome(executable_path= '/Users/karry/chromedriver')
browser.get("https://upassbc.translink.ca/")

selectschool = Select(browser.find_element_by_id("PsiId"))
selectschool.select_by_visible_text("University of British Columbia")

gobtn = browser.find_element_by_id("goButton")
gobtn.click()

# Terminate when wrong user/password combination.
if "Login Failed" in browser.page_source:
	browser.quit()
	input("Login Failed: press any key to close")
	exit()

#Login in the UBC CWL
#username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "username")))

username = browser.find_element_by_id("username")
password = browser.find_element_by_id("password")

username.send_keys(j_username)
password.send_keys(j_password)

loginbtn = browser.find_element_by_name("_eventId_proceed")
loginbtn.click()


#Continue to the translink
print(browser.page_source)
upasstoload = browser.find_elements_by_css_selector("form#form-request table [type=checkbox]")

if len(upasstoload) <= 0:
	print("No new upass to request!")
else:
	for toload in upasstoload:
		if not toload.is_selected():
			toload.click()
	upasstoload[0].submit()

## logout
logoutBtn = browser.find_element_by_css_selector("header #logout-link")
logoutBtn.click()

time.sleep(1)

try:
	dialog = browser.find_element_by_class_name("ui-dialog")
	if dialog.is_displayed():
		logoutBtn = dialog.find_element_by_id("LogOutLink")
		logoutBtn.click()
except NoSuchElementException:
	pass

time.sleep(3)
browser.quit()
