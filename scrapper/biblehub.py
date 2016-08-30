
from bs4 import BeautifulSoup
import os, re
import sqlite3


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
	

def extractVerses(page, book, chapter, version):	
	

	#----------------------
	# 1. Using BeautifulSoup tak page and remove foot Notes and Section Heads from page
	soup = BeautifulSoup(page, "html.parser")
	
	try:
		# removing footnotes from page
		footnotes_tag = soup.find("span", {"class": "mainfootnotes"}).extract()
		footnotes_tag = soup.find("span", {"class": "nivfootnote"}).extract()
	except:
		print("No footnotes in {} {}".format(book, chapter))
	
	try:
		# removing Section Heads from the content
		junk = soup.find_all("p", {"class": "sectionhead"})
		for i in junk:

			junk1 = i.extract()
	except:
		print("no Junk")
	#----------------------------
	# 2. the div that contains the Bible verses has a class of chap
	chapter_contents = soup.find("div", {"class": "chap"})
	#-----------
	# 3. Adjusting content to be on different lines
	better_contents = chapter_contents.prettify()
	file2 = open("testing", "w")
	print(better_contents, file = file2)
	file2.close()
	# 4. Removing final tags from page
	removed_tags = re.sub("(?<=<).*(?=>)|[<>]", '', str(better_contents))
	
	#testing chap 2 genesis
	file1 = open("testing1", 'w')
	print(removed_tags, file=file1)
	file1.close()
	# 5. Formating and removing white space.
	lines = removed_tags.split("\n")
	verse_number = 0
	verse_text = ""
	for line in lines:
	
		line = re.sub("^\s+", '', line)
		
		try:
			verse_number = int(line)
			if verse_number - 1  > 0:
				i = verse_number - 1
				print("{} {}".format(i, verse_text))
				#updateSQL(book, chapter, i, verse_text, version)
				verse_text = ""

		except ValueError:
			if bool(re.search(r'\w', line)):
				line = re.sub("[\n]", '', line)
				verse_text += " {}".format(line)
	
	# 7. print final verse
	print("{} {}".format(verse_number, verse_text))		
	#updateSQL(book, chapter, verse_number, verse_text, version)
	

def updateSQL(book, chapter, verse, text, version):
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





index = 2
index_max = 2
while index <= index_max:
	version = "NIV"
	book = "genesis"
	webpage = getPage("http://biblehub.com/niv/{}/{}.htm".format(book, index))
	extractVerses(webpage, book, index, version)
	index += 1





