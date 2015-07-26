#!/usr/bin/python
#coding=utf-8

import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from datetime import date, timedelta
from BeautifulSoup import BeautifulSoup
from selenium.webdriver.common.by import By

import psutil


br = webdriver.Firefox()

br.get( 'http://mops.twse.com.tw/mops/web/t05st01')

back = br.find_element_by_id('ajax_back_button')

e = br.find_element_by_id('year')
e.send_keys('104')

e = br.find_element_by_id('co_id')
e.send_keys('2002')


eles = br.find_elements( By.XPATH, '//input' )

count = 0
for e in eles:
	if e.get_attribute('value').find(u'搜尋') >= 0:
		count += 1
		if count == 2:
			break

if e.get_attribute('value').find(u'搜尋')  == -1:
	print u'[搜尋] not found'
	sys.exit(0)

search = e

search.click()
	
eles = br.find_elements( By.XPATH, '//input')

for e in eles:
	print e.get_attribute('value')
	if e.get_attribute('value').find(u'詳細資料') >= 0:
		e.click()
		sleep(5)
		back.click()
		sleep(5)
	else:
		print 'not found'

