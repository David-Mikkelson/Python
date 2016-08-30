
from bs4 import BeautifulSoup
import os, re
import sqlite3
from bibleinfo import *

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

conn = sqlite3.connect('tutorial.db')
c = conn.cursor()

#--------------------------------
# program is a webscraper for Bible verses from the biblehub.com
# right now it only scrapes and a page from the method getPage and extractVerses puts the verses in a file. 
# later it will create and add to a database that can be turned into a Bible trivia game.




def getPage(name):
	#https://www.biblegateway.com/passage/?search=Genesis+1&version=NIV
	#https://biblehub.com/niv/genesis/1.htm")
	#Examples of format:
		#getPage("http://biblehub.com/niv/{}/{}.htm".format(book, index))
	html = urlopen(name)
	page = html.read()
	return page
	
def pageCleanUp(page):
	#page = open("gen3", 'r')
	soup = BeautifulSoup(page, "html.parser")
	
	try:
		# removing footnotes from page
		footnotes_tag = soup.find("span", {"class": "mainfootnotes"}).extract()
		footnotes_tag = soup.find("span", {"class": "nivfootnote"}).extract()
	except:
		pass
	
	try:
		# removing Section Heads from the content
		junk = soup.find_all("p", {"class": "sectionhead"})
		junk += soup.find("p", {"class" : "ntext"})
		junk += soup.find("p", {"class" : "ntext2"})
		for i in junk:

			junk1 = i.extract()
	except:
		print("no Junk")

	verses_only = soup.find_all("p")
	return verses_only

def extractVerses(page, book, chapter, version):	
	#--------------------------
	# Start with initializing variables
	verse_number = 0
	verse_text = ""
	

	for p in page:
		# creating each tag in it's own line
		p = p.prettify()
		# removing the final tags 
		p = re.sub("(?<=<).*(?=>)|[<>]", '', p)
		# spliting on new lines in order to remove all the empty lines that removing tags just created
		lines = p.split('\n')
		for line in lines:
			# Removing the starting whitespace
			line = re.sub("^\s+", '', line)
			
			try:
				# see if the line is a number and put it into the verse_number variable
				verse_number = int(line)
				if verse_number - 1  > 0:
					# if we are moving to the next verse, update last verse and clear text
					i = verse_number - 1
					print("{} {}".format(i, verse_text))
					updateSQL(book, chapter, i, verse_text, version)
					verse_text = ""
			except:
				if bool(re.search(r'\w', line)):
					# if the line is text remove the new line char and add it to the text
					line = re.sub("[\n]", '', line)
					verse_text += " {}".format(line)

	#update the last verse on the page
	print("{} {}".format(verse_number, verse_text))
	updateSQL(book, chapter, verse_number, verse_text, version)
	
	

def updateSQL(book, chapter, verse, text, version):
	#updateSQL(book, chapter, verse_number, verse_text, version)

	# 1. Check to see if table exists 
	# 2. Check to see if verse is already in the database
	# 3. if not insert
	c.execute("CREATE TABLE IF NOT EXISTS bibleVerses (ID TEXT, book TEXT, chapter INTEGER, verse INTEGER, verse_text TEXT, version TEXT, UNIQUE(ID))")

	#Create ID
	ID = "{}-{}-{}".format(book, chapter, verse)
	table_data = "'{}', '{}', {}, {}, '{}', '{}'".format(ID, book, chapter, verse, text, version)
	table_row = "ID, book, chapter, verse, verse_text, version"
	c.execute("INSERT OR IGNORE INTO bibleVerses ({}) VALUES ({})".format(table_row, table_data))
	conn.commit()

def askForBook():
	# returns 3 things the Books Name, Number of chapters, and index of biblehubs name
	bookRequested = input('Enter the name of the Bible book you would like to put into the database: ')
	try:
		# if Chapter_total[bookRequested]:
		# 	print("great : {} has {} chapters".format(bookRequested, Chapter_total[bookRequested]))
		# 	return (bookRequested, Chapter_total[bookRequested])
		Number = Chapters[Books_of_the_Bible.index(bookRequested.lower())]
		print("Great: {} has {} chapters".format(bookRequested, Number))
		return (bookRequested, Number, Books_of_the_Bible.index(bookRequested.lower()))
	except:
		print("That book is not in my library.  Please try again.")
		askForBook()

def mainProgram():
	(book, index_max, name_index) = askForBook()
	index = 1
	bookForHub = biblehub_names[name_index]
	while index <= index_max:
		
		version = "NIV"
		print("{} Chapter {} out of {}".format(book, index, index_max))
		webpage = getPage("http://biblehub.com/niv/{}/{}.htm".format(bookForHub, index))
		webpage = pageCleanUp(webpage)
		extractVerses(webpage, book, index, version)
		index += 1

mainProgram()



