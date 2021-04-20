# -*- coding: utf-8 -*-

import config

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from random import randint
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os, sys, inspect

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

import pathlib  
  
def configure_chrome_driver():  
	options = webdriver.ChromeOptions()  
	options.add_argument(f"user-data-dir={pathlib.Path(__file__).parent.absolute().joinpath('chrome-profile')}")  
	
	# disable image loading for better performance  
	# options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  
	
	path = pathlib.Path(__file__).parent.absolute().joinpath("chromedriver.exe")  
	
	the_driver = webdriver.Chrome(executable_path=config.DRIVER_EXECUTABLE_PATH, options=options)  
	#the_driver = webdriver.Chrome(executable_path=path, options=options)

	# page loading time and wait time for page reload  
	the_driver.set_page_load_timeout(5)  
	the_driver.implicitly_wait(2)  

	#the_driver = webdriver.Chrome('C:/Python/chromedriver.exe') # hardcode path
	return the_driver

def key_match(st_key, sl_key):
	# st_key: student_key
	# sl_key: slate key
	if st_key == sl_key: # match
		return True
	else: # no match
		return False


def format_slate_key_guess(sl_key):
	if '0' == sl_key[0]:
		return sl_key[1:]
	else:
		return sl_key

def get_code_from_school_name(input_string):
	c = '('
	indices = [pos for pos, char in enumerate(input_string) if char == c]
	index = indices[-1]    
	student_key = input_string[index:].replace("(","").replace(")","")
	return student_key

def AccountLogin(driver, username, password):
	driver.get("https://go.chapman.edu/manage//")
	sleep(3)
	
	driver.find_element_by_name('loginfmt').send_keys(username)

	driver.find_element_by_id("idSIButton9").click()
	
	driver.find_element_by_name('passwd').send_keys(password)

	sleep(1)  
	return

def compare_actions(driver, xpath_string):
	driver.find_element_by_xpath(xpath_string).click()
	return

def Consolidate_by_key(driver):
	driver.get("https://go.chapman.edu/manage/database/dedupe")
	input('Go to `Names` and Press ENTER: ')
	sleep(1)

	tr_list = driver.find_elements_by_class_name("table")
	   
	for elem in tr_list:
		listy = elem.find_elements_by_tag_name("tr")
		
		for e in reversed(listy):
			try:
				school_name_student_version = e.find_elements_by_tag_name("td")[1].text
				#student_name = e.find_elements_by_tag_name("td")[2].text
				slate_key_guess = format_slate_key_guess(e.find_elements_by_tag_name("td")[4].text)
				compare_button = e.find_elements_by_tag_name("td")[5]
				
				print(f"Master Record: {school_name_student_version}")
				
				student_key = get_code_from_school_name(school_name_student_version)
				if len(student_key): 
					print(f"Student Key: {student_key}")
					print(f"Slate Key:   {slate_key_guess}")
					match_bool = key_match(student_key, slate_key_guess)
					
					if match_bool == True:
						print("Match")
						compare_button.click()
						

						# Click Link and Update
						# Link and Uodate: //*[@id="response_form"]/div[3]/button[2]
						input("Press ENTER to `Link and Update`: ")
						sleep(1)
						driver.find_element_by_xpath("//*[@id='response_form']/div[3]/button[2]").click() 
						sleep(1)
						obj = driver.switch_to.alert
						obj = driver.switch_to.alert.accept()#obj.send_keys('enter')
						
					if match_bool == False:
						print('No Match')
						compare_button.click()
						
						input("Press ENTER to `Exclude`: ")
						# Exclude: //*[@id="response_form"]/div[3]/button[3]
						sleep(1)
						driver.find_element_by_xpath("//*[@id='response_form']/div[3]/button[3]").click()
						sleep(1)
						obj = driver.switch_to.alert
						obj = driver.switch_to.alert.accept()
						
			except:
				pass
				
			
			print()
			print('------------------------------------------------------------')
			
			sleep(1)   
	return
	

if __name__ == '__main__':
	print("Getting email/pass from config file...")

	driver = configure_chrome_driver()

	print('Logging in...')
	
	AccountLogin(driver, config.EMAIL, config.PASSWORD)
	
	Consolidate_by_key(driver)
	print('Completed')