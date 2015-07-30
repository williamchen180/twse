#!/usr/bin/python
#coding=utf-8


from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import cPickle


def stockNumber():


	url = "http://www.emega.com.tw/js/StockTable.htm"
	mech = Browser()
	page = mech.open(url)
	html = page.read()

	soup = BeautifulSoup( html.decode('big5', 'ignore').encode('utf8') )

	rows = soup.findAll('tr')

	matrix = []

	for (n, r)  in enumerate( rows ):
		cols = r.findAll('td')

		matrix.append([])
		

		for (m, c) in enumerate( cols ):
#			print c
			if m % 2 == 0:
				number = c.text.split('&')[0]
			else:
				name = c.text.split('&')[0].split(' ')[0] 

#				print number, len(number), number.isdigit(), name, len(name)

				t = (number, name ) 

				matrix[n].append(t)

	i = len( matrix );
	j = len( matrix[0] );


	Stock = {}

	for x in range(j):
		for y in range(i):
			try:
				s = matrix[y][x]

				if len(s[0]) == 0:
					continue
				
				if not s[0].isdigit():
					if len(s[0]) == 2:
						cate = s
						Stock[cate] = []
					else:
						continue

				else:
#					print "append: ", s[0]

					Stock[cate].append( s )
			except:
				pass

#		print Stock

	#print Stock
	return Stock


if __name__ == '__main__':
	Stock = stockNumber()
	for x in Stock:
		print '\n'
		print x[0], x[1]
		numbers = []
		for y in Stock[x]:
			print "    ", y[0], y[1],
			numbers.append(y[0])

		with open( x[0] + x[1] + '.cpickle', 'w') as f:
			cPickle.dump( numbers, f )
			



