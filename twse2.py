#!/usr/bin/python
#coding=utf-8

# 公司不存在
# 資料庫中查無需求資料

import sys
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta
from BeautifulSoup import BeautifulSoup
from selenium.webdriver.common.by import By
import cPickle
import stockNumber
import datetime

import pprint
import os

def Now():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

class twse():
	def __init__(self, stockList = None):
		self.year = None
		self.stock = None
		self.stockList = stockList

	def dump_news(self):
		html = self.br.page_source
		soup = BeautifulSoup( html )
		tables = soup.findAll('table')
		for t in tables:
			if t.getText()[0:2] == u'序號':
				break
		if t == tables[-1]:
			print 'Unable to find 序號'
			return None
		try:
			td = t.findAll('td')
			news = {}
			news[ td[0].getText() ] = td[1].getText()
			news[ td[2].getText() ] = td[3].getText()
			news[ td[4].getText() ] = td[5].getText()
			news[ td[6].getText() ] = td[7].getText()
			news[ td[8].getText() ] = td[9].getText()
			news[ td[10].getText() ] = td[11].getText()
			news[ td[12].getText() ] = td[13].getText()
			news[ td[14].getText() ] = td[15].getText()
			news[ td[16].getText() ] = td[17].getText()
			news[ td[18].getText() ] = td[19].getText()
		except Exception as e:
			print 'something wrong. Retry'
			return None

		return news


	def wait_ready(self):
		WebDriverWait( self.br, 10).until( EC.presence_of_element_located( (By.ID, 'year')) )
		sleep(1)

	def get_search_button(self):
		self.wait_ready()
		eles = self.br.find_elements( By.XPATH, '//input' )
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

	def search(self):
		self.wait_ready()
		self.get_search_button().click()
		self.wait_ready()

	def get_back_button(self):
		self.wait_ready()
		back = self.br.find_element_by_id('ajax_back_button')
		self.wait_ready()
		return back

	def back(self):
		self.wait_ready()
		self.get_back_button().click()
		self.wait_ready()
	

	def get_number_news(self):
		self.wait_ready()
		ret = 0
		eles = self.br.find_elements( By.XPATH, '//input')
		for e in eles:
			if e.get_attribute('value').find(u'詳細資料') >= 0:
				ret += 1
		return ret

	def get_number_of_news(self,  no ):
		eles = self.br.find_elements( By.XPATH, '//input')
		for e in eles:
			if e.get_attribute('value').find(u'詳細資料') >= 0:
				if no == 0:
					return e
				no -= 1

	def get_stock_numbers(self):
		stocks = stockNumber.stockNumber()
		numbers = []
		for x in stocks:
			for y in stocks[x]:
				numbers.append(y[0].encode('ascii','ignore'))
		return numbers

	def prepare(self):
		self.br = webdriver.Firefox()
		#self.br = webdriver.Chrome('/Users/WilliamChen/Downloads/chromedriver')

		self.br.get( 'http://mops.twse.com.tw/mops/web/t05st01')

	def set_year(self, year):
		#if self.year == None:
		self.year = self.br.find_element_by_id('year')
		self.year.clear()
		self.year.send_keys( year )

	def set_stock(self, stock):
		#if self.stock == None:
		self.stock = self.br.find_element_by_id('co_id')
		self.stock.clear()
		self.stock.send_keys( stock )

	def get_data(self, stock, year):
		self.set_stock( stock )
		self.set_year( str(year) )

		self.search()
		self.wait_ready()

		if self.br.page_source.find(u'公司不存在') >= 0:
			return False
		if self.br.page_source.find(u'資料庫中查無需求資料') >= 0:
			return False

		number_news = self.get_number_news()
		print 'There are %d news from %s in %d' % (number_news, stock, year )

		year_news = []
		for i in range(0, number_news):
			while True:
				e = self.get_number_of_news(i)
				e.click()
				self.wait_ready()

				news = self.dump_news()
				if news == None:
					self.back()
				else:
					break

			year_news.append( news )
			self.back()

			print '%d done' % i, Now()

		return year_news


	def run(self):

		self.prepare()
		if self.stockList != None:
			numbers = self.stockList
		else:
			numbers = self.get_stock_numbers()

		try:
			for number in numbers:

				for year in range(104,94,-1):
					filename = 'news/%s_%d.cpickle' % (number, year ) 
					if os.path.isfile( filename ) == True:
						print 'skip:' + filename
						continue
					ret = self.get_data( number, year )
					self.back()
					if ret == False:
						break
					with open( filename ,'w') as f:
						cPickle.dump( ret, f )	
			return True
		except Exception as e:
			self.br.close()
			print e
			return e

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "usage: %s stock" % sys.argv[0]
		sys.exit(0)

	stockList=[]
	for x in sys.argv[1:]:
		with open( x, 'r' ) as f:
			l = cPickle.load( f )
		stockList += l

	print stockList


	while True:
		t = twse(stockList)
		ret = t.run()
		if ret == True:
			break
