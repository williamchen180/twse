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

def get_search_button():
	eles = br.find_elements( By.XPATH, '//input' )
	count = 0
	for e in eles:
		if e.get_attribute('value').find(u'搜尋') >= 0:
			count += 1
			if count == 2:
				break
	if e.get_attribute('value').find(u'搜尋')  == -1:
		print u'[搜尋] not found'
		return None
	else:
		return e

def get_back_button():
	back = br.find_element_by_id('ajax_back_button')
	return back

def get_number_news():
	ret = 0
	eles = br.find_elements( By.XPATH, '//input')
	for e in eles:
		if e.get_attribute('value').find(u'詳細資料') >= 0:
			ret += 1
	return ret

def get_number_of_news( no ):
	eles = br.find_elements( By.XPATH, '//input')
	for e in eles:
		if e.get_attribute('value').find(u'詳細資料') >= 0:
			if no == 0:
				return e
			no -= 1

	

	

	


br = webdriver.Firefox()
br.get( 'http://mops.twse.com.tw/mops/web/t05st01')

back = get_back_button() 

e = br.find_element_by_id('year')
e.send_keys('104')

e = br.find_element_by_id('co_id')
e.send_keys('2002')

search = get_search_button()
search.click()


number_news = get_number_news()

for i in range(0, number_news):
	e = get_number_of_news( i )
	e.click()
	sleep(1)
	back = get_back_button() 
	back.click()
	sleep(1)


