import sqlite3, sys
import re, os, time
import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
dataBase = 'test.db'
table_name = "AccessTable"
conn = sqlite3.connect(dataBase)
currentCategories = []


class GetTheWord:
	def __init__(self, master):
		self.master = master
		self.master.title("Finding Passwords")
		#self.master.option_add("*Background", "grey")
		
		#--------------------
		# Adding top level menubar for program
		self.master.option_add('*tearOff', False)
		menubar = Menu(self.master)
		self.master.config(menu = menubar)
		file = Menu(menubar)
		edit = Menu(menubar)
		help_ = Menu(menubar)
		menubar.add_cascade(menu = file, label = 'File')
		menubar.add_cascade(menu = edit, label = 'Edit')
		menubar.add_cascade(menu = help_, label = 'Help')
		#file.add_command(label = 'New', command = lambda: print('New File'))
		file.add_command(label = 'New Database', command = lambda: CreateNewDB())

		#-----------------------------------
		# Creating Tabs 
		# f1 will be The Password Search tab
		# f2 will be the Databasse Update tab
		self.n = ttk.Notebook(self.master, width=325, height=250)
		
		self.f1 = ttk.Frame(self.n)   # first page, which would get widgets gridded into it
		self.f2 = ttk.Frame(self.n)   # second page
		
		self.n.add(self.f1, text='Find Passwords')
		self.n.add(self.f2, text='Update Passwords')

		self.n.pack(fill=tkinter.BOTH, expand=False)
		#------------------
		# The Layout of the tabs
		self.configuref1()
		self.configuref2()

	def configuref1(self):
		#-----------------------------
		# The Layout of the Password search Side 
		
		# Setup Drop down menu
		lst1 = ['Category','Site']
		self.Selected = tkinter.StringVar()
		self.Selected.set('Category')
		drop = tkinter.OptionMenu(self.f1, self.Selected, *lst1)
		drop.grid(row=0, column=0, sticky='w', padx = 10, pady = 10)
		
		#--------------------------
		# Setup Input Type for user
		self.input_box =  Entry(self.f1, width=20)
		self.input_box.grid(row=0, column=1, sticky='w', padx = 10, pady = 10)
		#------------------
		# Setup Find Button
		self.find_button = tkinter.Button(
							self.f1,
							text="Find",
							command= self.findSelected,
							relief="sunken"
							)
		self.find_button.grid(row=1, column=0, sticky='ew')

	
	def configuref2(self):
		#---------
		# Banner
		ttk.Label(self.f2, text = 'Updating Passwords', anchor='center').grid(row=0, column=0, columnspan=2)
		#--------
		# Insert Category
		ttk.Label(self.f2, text = 'Category').grid(row=1, column=0, sticky='wnes')
		self.update_Category =  Entry(self.f2, width=20)
		self.update_Category.grid(row=1, column=1, sticky='w', padx = 10, pady = 10)
		#--------
		# Insert Site
		ttk.Label(self.f2, text = 'Web Site').grid(row=2, column=0, sticky='wnes')
		self.update_Site =  Entry(self.f2, width=20)
		self.update_Site.grid(row=2, column=1, sticky='w', padx = 10, pady = 10)
		#--------
		# Insert Login
		ttk.Label(self.f2, text = 'Login').grid(row=3, column=0, sticky='wnes')
		self.update_Login =  Entry(self.f2, width=20)
		self.update_Login.grid(row=3, column=1, sticky='w', padx = 10, pady = 10)
		#--------
		# Insert Password
		ttk.Label(self.f2, text = 'Password').grid(row=4, column=0, sticky='wnes')
		self.update_Password =  Entry(self.f2, width=20)
		self.update_Password.grid(row=4, column=1, sticky='w', padx = 10, pady = 10)
		#--------
		# Update button
		self.Update_old_button = tkinter.Button(
							self.f2,
							text="Update Existing",
							command= self.UpdateOld
							)
		self.Update_old_button.grid(row=5, column=0, sticky='ew')
		#--------
		# Update Button
		self.Update_button = tkinter.Button(
							self.f2,
							text="Create New",
							command= self.UpdateNew
							)
		self.Update_button.grid(row=5, column=1, sticky='ew')

	def UpdateOld(self, *args):
		#c.execute("UPDATE {tn} SET {cn}=('Hi World') WHERE {idf}=(123456)".format(tn=table_name, cn=column_name, idf=id_column))
		#-------------------------
		# Get information from the form
		C = self.update_Category.get()
		S = self.update_Site.get()
		L = self.update_Login.get()
		P = self.update_Password.get()

		#-------------------------
		# Check to see if it Exists
		try:
			#----------------------------------
			# We need to check if there are more than one account at a web site.
			sql_call = conn.execute("SELECT * FROM AccessTable WHERE Site is '{}'".format(S)).fetchall()
			last_login = list(sql_call[-1])[3]
			for login_row in sql_call:
				login_row = list(login_row)
				if login_row[3] == L:				
					#---------------
					# This is the row that needs updating, get the row number to update
					row_number = login_row[0]
					conn.execute("UPDATE AccessTable SET Pass = '{}' WHERE Utime='{}'".format(P, row_number))
					conn.commit()
					self.ClearUpdateForm()
					messagebox.showinfo('Account Updated', 'Success! Update Complete')
					break
				elif login_row[3] == last_login:
					#---------------
					# Can Not Find Row to be updated
					messagebox.showinfo("Account Login Doesn't Exist for this Web Site", 'Please Use Create New if the information is correct')
				
		except:
			messagebox.showinfo("Account Doesn't Exist", 'Please Use Create New if the information is correct')
		

	def UpdateNew(self, *args):
		#-------------------------
		# Get information from the form
		C = self.update_Category.get()
		S = self.update_Site.get()
		L = self.update_Login.get()
		P = self.update_Password.get()
		#---------------------
		# Check if All data is present
		if (C and S and L and P):
			try:
				#Check to see if the Site and Login are already in the Database
				w = str(conn.execute("SELECT Login FROM AccessTable WHERE Site is '{}'".format(S)).fetchall()).split("'")[1]
				if(L == w):
					messagebox.showinfo('Account Already Created', 'Please Use Update Existing if you want to make changes')
				else:
					info = "'{}', '{}', '{}', '{}'".format(C,S,L,P)
					complete = insertRecord(info)
					if complete:
						self.ClearUpdateForm()
			except:
				info = "'{}', '{}', '{}', '{}'".format(C,S,L,P)
				complete = insertRecord(info)
				if complete:
					self.ClearUpdateForm()

		else:
			messagebox.showinfo('Missing Information', 'Please Enter all Fields')			


	def findSelected(self, *args):
		I = self.input_box.get()
		S = self.Selected.get()
		#print(self.Selected.get(), self.input_box.get())
		self.input_box.delete(0, 'end')
		if I == "":
			messagebox.showinfo('Missing Information', 'Please Enter search Parameters!')

		elif S == "Category":
			#------------------
			# using SQL to get all the login's and pass words in the Category given
			if I not in currentCategories:
				# if there is nothing in currentCategories
				if not currentCategories:
					messagebox.showinfo('No Categories', 'There is no Entries in Categories yet.')
				else:
					messagebox.showinfo('Not a Category', 'Please Enter one of the following: \n{}'.format(currentCategories))
			else:
				message = ""
				a = conn.execute("SELECT * FROM AccessTable WHERE Category is '{}'".format(I)).fetchall()
				for response in a:
					u, cat, site, login, Pass, a1, a2, a3 = response
					#print(cat, site, login)
					message += "{} : {} : {} \n".format(site, login, Pass)

				messagebox.showinfo('Category: {}'.format(I), '{}'.format(message))


		elif S == "Site":
			a = conn.execute("SELECT * FROM AccessTable WHERE Site is '{}'".format(I)).fetchall()
			if not a:
				messagebox.showinfo('Site not Found: {}'.format(I), 'Please pick another site to check')
			else:
				message = ""
				for response in a:
					u, cat, site, login, Pass, a1, a2, a3 = response
					#print(cat, site, login)
					message += "{} : {} : {} \n".format(site, login, Pass)

				messagebox.showinfo('Category: {}'.format(I), '{}'.format(message))

		else:
			pass
	def ClearUpdateForm(self, *args):
		self.update_Category.delete(0, 'end')
		self.update_Site.delete(0, 'end')
		self.update_Login.delete(0, 'end')
		self.update_Password.delete(0, 'end')


def Setup():
	createTable()
	#a = conn.execute("SELECT Category FROM AccessTable GROUP BY Category ").fetchall()
	a = str(conn.execute("SELECT Category FROM AccessTable GROUP BY Category ").fetchall()).split("'")
	i = 1
	while i < len(a):
		if (i % 2 == 1):
			currentCategories.append(a[i])
		i += 1
	
def insertRecord(data):
	#info = "'Banking', 'BOA', 'JohnDoe', 'notforyou'"
 	#insertRecord(info)
	
	# if this is the first entry, it'll need a number.
	try:
		index = int(str(conn.execute("SELECT MAX(Utime) FROM AccessTable").fetchall()).split(',')[0].replace('[(', '')) + 1
	except:
		index = 1

	columns = "'Utime', 'Category', 'Site', 'Login', 'Pass'"
	conn.execute("INSERT INTO AccessTable ({}) VALUES ({}, {});".format(columns, index, data))
	failed = conn.commit()
	if not failed:
		messagebox.showinfo('Thank you', 'Successful! You have Updated the database')
		# In order to update the Category list
		Setup()
		return True

def createTable():
	# key, Category, site, login, password, answer1, answer2, answer3
	conn.execute("CREATE TABLE IF NOT EXISTS AccessTable ( Utime INTEGERPRIMARY KEY, Category TEXT, Site TEXT, Login TEXT, Pass TEXT, Answer1 TEXT, Answer2 TEXT, Answer3 TEXT)")
	conn.commit()

def CreateNewDB():
	#-------------------- 
	# 1. Create archive name for old dataBase
	# 2. reconnect to database, which creates new file
	# 3. Create new Table for database
	time_tag = time.ctime()
	for c in [':', ' ']: time_tag = time_tag.replace(c, "")
	archive_name = "database-archive" + time_tag
	#renaming the old database for safety
	os.rename(dataBase,archive_name)
	# 2
	conn = sqlite3.connect(dataBase)
	# 3
	Setup()



if __name__ == "__main__":
	Setup()
	root = tkinter.Tk()
	style = ttk.Style()
	style.theme_use('classic')
	GetTheWord(root)
	root.mainloop()
