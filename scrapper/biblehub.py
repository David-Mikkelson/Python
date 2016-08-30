
from bs4 import BeautifulSoup
import os, re
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


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
	

def extractVerses(page, book, chapter, FILE):	
	#----------------------
	# 1. Using BeautifulSoup tak page and remove foot Notes and Section Heads from page
	soup = BeautifulSoup(page, "html.parser")
	# removing footnotes from page
	footnotes_tag = soup.find("span", {"class": "mainfootnotes"}).extract()
	footnotes_tag = soup.find("span", {"class": "nivfootnote"}).extract()
	# removing Section Heads from the content
	junk = soup.find_all("p", {"class": "sectionhead"})
	for i in junk:
		junk1 = i.extract()

	#----------------------------
	# 2. the div that contains the Bible verses has a class of chap
	chapter_contents = soup.find("div", {"class": "chap"})
	#-----------
	# 3. Adjusting content to be on different lines
	better_contents = chapter_contents.prettify()
	# 4. Removing final tags from page
	removed_tags = re.sub("(?<=<).*(?=>)|[<>]", '', str(better_contents))
	
	# 5. Adding file for temp output
	outfile = open(FILE, 'a')
	print("{} {}".format(book, chapter))
	print("{} {}".format(book, chapter), file = outfile)

	# 6. Formating and removing white space.
	lines = removed_tags.split("\n")
	verse_number = 0
	verse_text = ""
	for line in lines:
		line = re.sub("^\s+", '', line)
		try:
			verse_number = int(line)
			if verse_number - 1  > 0:
				print("{} {}".format(verse_number - 1, verse_text))
				print("{} {}".format(verse_number - 1, verse_text), file = outfile)
				verse_text = ""

		except ValueError:
			if bool(re.search(r'\w', line)):
				line = re.sub("[\n]", '', line)
				verse_text += " {}".format(line)
	
	# 7. print final verse
	print("{} {}".format(verse_number, verse_text))		
	print("{} {}".format(verse_number - 1, verse_text), file = outfile)
	# 8. close file
	outfile.close()




index = 1
index_max = 5
while index <= index_max:
	book = "genesis"
	webpage = getPage("http://biblehub.com/niv/{}/{}.htm".format(book, index))
	extractVerses(webpage, book, index, "biblehub-{}".format(book))
	index += 1





