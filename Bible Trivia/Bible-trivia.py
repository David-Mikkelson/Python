import os, re
import sqlite3, random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


#-----------------------
#  change to location of the database
#
c = sqlite3.connect('bible-trivia.db')

#-----------------------
# These are the answers the program will search for in the database
trivia_answers = ['eternal', 'burden', 'jerusalem', 'kingdom', 'rulers', 'authority', 'disciples',  
				'compassion', 'daughter', 'instructed', 'prophet', 'children', 'bethany', 'fig', 'temple', 'pharisees', 'mountain', 
				'kingdom', 'light', 'heaven', 'father', 'judged', 'servant', 'teacher', 'sheep', 'jesus', 'crowd', 'condemn', 'prince',
				'home', 'fish', 'faith', 'human', 'person', 'loaves', 'mercy', 'child', 'brother', 'Galilee', 'answered']



class TriviaFrame:

	def __init__(self, root):
		style = ttk.Style()
		style.theme_use('classic')

		#-------------------------------------
		# setup Variables 
		self.my_score = 0
		self.my_right = 0
		self.my_done  = 0


		#----------------------------------------
		#    Top frame has Title, directions and score
		self.one = Frame(root)
		self.one.pack(padx = 5, pady = 5)

		self.big_title  = ttk.Label(self.one, text = 'Bible Trivia')
		self.big_title.config(font = ("Ariel", 24), background = 'white')
		self.directions = ttk.Label(self.one, text = 'Fill in the Blank(s) with a Single word')
		self.directions.config(font = ("Ariel", 18), background = 'white')
		self.scoring    = ttk.Label(self.one, text = 'Score {}  {} of {} Ready to go!'.format(self.my_score, self.my_right, self.my_done))
		self.scoring.config(font = ("Ariel", 18), background = 'white')
		
		self.big_title.pack()
		self.directions.pack()
		self.scoring.pack()

		#-------------------------------------------
		# Setup first question
		(self.real_answer, self.book, self.chapter, self.verse, self.sentence) = getTriviaquestion('Matthew')

		#-------------------------------------------
		# Setup Frame for question
		self.two = Frame(root)
		self.two.pack(padx = 5, pady = 5)

		self.question_text = ttk.Label(self.two, text = '{}'.format(self.sentence), wraplength=500, background = 'white')
		self.question_text.pack()

		#---------------------------------------------
		# Answer and submit buttons
		self.three = Frame(root)
		self.three.pack(padx = 5, pady = 5)
		
		d = ttk.Label(self.three, text = '                ', background = 'white')
		self.users_answer  = ttk.Entry(self.three, width = 30)
		self.submit_button = ttk.Button(self.three, text = 'Submit Answer', command = lambda: clickButtonAnswer(self))
		self.reset_button  = ttk.Button(self.three, text = 'Reset', command = lambda: clickButtonreset(self))		

		d.grid(row = 0, column = 0)
		self.users_answer.grid( row = 0, column = 1, sticky = 'ws', pady = 3, ipady = 5, ipadx = 5)
		self.submit_button.grid(row = 1, column = 1, sticky = 'ws')
		self.reset_button.grid( row = 1, column = 2, sticky = 'es')
		


		def clickButtonAnswer(self):
			answer = self.users_answer.get().lower()
			self.users_answer.delete(0, 'end')
			if(answer == self.real_answer):
				self.my_score += 100
				self.my_right += 1
				self.my_done  += 1
				if self.my_done == 10:
					messagebox.showinfo(title = 'Great Job!', message = 'Your score is: {}   {} Right'.format(self.my_score, self.my_right))
					clickButtonreset(self)
				else:
					messagebox.showinfo(title = 'Great Job!', message = 'Keep going, your score is: {} '.format(self.my_score))
			else:
				self.my_done += 1
				messagebox.showinfo(title = 'OOP\'S Close', message = 'the Answer was {} \nThe Answer is found in {} {}:{}'.format(self.real_answer, self.book, self.chapter, self.verse))


			(self.real_answer, self.book, self.chapter, self.verse, self.sentence) = getTriviaquestion('Matthew')
			self.question_text.config(text = '{}'.format(self.sentence))
			self.scoring.config(text = 'Score {}  {} of {}'.format(self.my_score, self.my_right, self.my_done))			

		def clickButtonreset(self):
			self.my_score = 0
			self.my_right = 0
			self.my_done  = 0
			(self.real_answer, self.book, self.chapter, self.verse, self.sentence) = getTriviaquestion('Matthew')
			self.question_text.config(text = '{}'.format(self.sentence))
			self.scoring.config(text = 'Score {}  {} of {} Ready to go!'.format(self.my_score, self.my_right, self.my_done))			











def createdb():
	c = sqlite3.connect('/Users/Dmikkelson/Documents/Class-work/python/drills/bible-trivia.db')
	c.execute("CREATE TABLE niv (BOOK TEXT, CHAPTER INT, VERSE INT, WORDS TEXT)")
	c.execute('drop table if exists test')
	c.commit()



def fixVerseFile(fname):
	#---------------------------------------------
	# open file and setup var's for going through each verse
	inputFile = open(fname, 'r')
	lines = inputFile.readlines()
	book = fname.split('-')[0]
	current_text = ""
	verse_index = 1
	for line in lines:
		line = line.strip()
		if 'chapter ' in line:
			#--------------------------------------
			# Setup for the next chapter
			if verse_index != 1: 
				pass
				#inputVerses(book, chapter, verse_index, current_text)
				#print("\n", line)
				
			chapter = line.split(' ')[1].strip()
			verse_index = 1
			current_text = ""
			continue
		#------------------------------------
		# Check for blank lines
		if "" == line: continue
		
		#------------------------------------
		# remove extra quotes  check out regexr.com
		line = re.sub("\[[1-9][0-9]\]|\[\w\]", "", line)
		
		#------------------------------------
		# split up the line and look for verse markers 
		wordInLine = line.split(' ')
		for w in wordInLine:
			try:
				w = int(w)
				if w == 1: continue
				if  verse_index < w:
					#print('\n')
					inputVerses(book, chapter, verse_index, current_text)
					current_text = ""
					verse_index += 1
					continue
			except:
				pass
			current_text += '{} '.format(w)
			



def inputVerses(book, chapter, verse, words):
                #----------------------------------------
                # inserting a row into the database
	values = "'{}', '{}', '{}', ".format(book, chapter, verse)
	try:
		c.execute("INSERT INTO niv (BOOK, CHAPTER, VERSE, WORDS) VALUES ({} '{}')".format(values, words))
		c.commit()
		
	except:
		print('Failed to INSERT values')
		print("INSERT INTO niv (BOOK, CHAPTER, VERSE, WORDS) VALUES ({} '{}')".format(values, words))
		return False

def getTriviaquestion(book):
	return_answer = trivia_answers[random.randint(0, len(trivia_answers) - 1)]
	print(return_answer)
	possible_qestions = c.execute("SELECT * FROM niv WHERE WORDS LIKE '% {}%'".format(return_answer))
	p = possible_qestions.fetchall()
	if len(p) == 1:
		references = p
	else:
		references = p[random.randint(0, len(p) - 1)]
	book 	= references[0] 
	chapter = references[1]
	verse 	= references[2] 
	sentence= references[3]
	pattern = re.compile(return_answer, re.IGNORECASE)
	sentence = pattern.sub("____________", sentence)
	question = [return_answer, book, chapter, verse, sentence]
	print(sentence)
	return (question)


def main():
        root =Tk()
        frame = TriviaFrame(root) 
        root.mainloop()

if __name__ == "__main__": main()


