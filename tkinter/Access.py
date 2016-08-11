import sqlite3
import re
import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
dataBase = 'test.db'
conn = sqlite3.connect(dataBase)
currentCategories = []


class GetTheWord:
	def __init__(self, master):
		self.master = master
		self.master.title("Finding Passwords")
		
		#-----------------------------------
		# Creating Tabs
		self.n = ttk.Notebook(self.master, width=300, height=250)
		
		self.f1 = ttk.Frame(self.n)   # first page, which would get widgets gridded into it
		self.f2 = ttk.Frame(self.n)   # second page
		
		self.n.add(self.f1, text='Find Passwords')
		self.n.add(self.f2, text='Update Passwords')

		self.n.pack(fill=tkinter.BOTH, expand=False)
		self.configuref1()
		self.configuref2()

	def configuref1(self):
		self.getPassword_frame = tkinter.Frame(self.f1)
		self.getPassword_frame.grid(row=2, column=0, sticky='nsew', pady = 10, padx = 10)
		#-----------------------------------------------
		# Setup Drop down menu
		lst1 = ['Category','Site']
		self.Selected = tkinter.StringVar()
		self.Selected.set('Category')
		drop = tkinter.OptionMenu(self.getPassword_frame, self.Selected, *lst1)
		drop.grid(row=0, column=0, sticky='w', padx = 10, pady = 10)
		
		#-----------------------------------------------
		# Setup Input Type for user
		self.input_box =  Entry(self.getPassword_frame, width=20)
		self.input_box.grid(row=0, column=1, sticky='w', padx = 10, pady = 10)
		#-----------------------------------------------
		# Setup Find Button
		self.find_button = tkinter.Button(
							self.getPassword_frame,
							text="Find",
							command= self.findSelected
							)
		self.find_button.grid(row=1, column=0, sticky='ew')

	
	def configuref2(self):
		#--------------------------
		# Banner
		ttk.Label(self.f2, text = 'Updating Passwords').grid(row=0, column=0, columnspan=2)
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
							text="Update Old",
							command= self.UpdateOld
							)
		self.Update_old_button.grid(row=5, column=0, sticky='ew')
		#--------
		# Update Button
		self.Update_button = tkinter.Button(
							self.f2,
							text="Update New",
							command= self.UpdateNew
							)
		self.Update_button.grid(row=5, column=1, sticky='ew')

	def UpdateOld(self, *args):
		pass

	def UpdateNew(self, *args):
		pass

	def findSelected(self, *args):
		I = self.input_box.get()
		S = self.Selected.get()
		print(self.Selected.get(), self.input_box.get())
		self.input_box.delete(0, 'end')
		if I == "":
			messagebox.showinfo('Missing Information', 'Please Enter search Parameters!')

		elif S == "Category":
			#------------------
			# using SQL to get all the login's and pass words in the Category given
			if I not in currentCategories:
				messagebox.showinfo('Not a Category', 'Please Enter one of the following: \n{}'.format(currentCategories))
			else:
				message = ""
				a = conn.execute("SELECT * FROM AccessTable WHERE Category is '{}'".format(I)).fetchall()
				for response in a:
					u, cat, site, login, Pass, a1, a2, a3 = response
					print(cat, site, login)
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
					print(cat, site, login)
					message += "{} : {} : {} \n".format(site, login, Pass)

				messagebox.showinfo('Category: {}'.format(I), '{}'.format(message))

		else:
			pass


def SetupCategory():
	#a = conn.execute("SELECT Category FROM AccessTable GROUP BY Category ").fetchall()
	a = str(conn.execute("SELECT Category FROM AccessTable GROUP BY Category ").fetchall()).split("'")
	i = 1
	while i < len(a):
		if (i % 2 == 1):
			currentCategories.append(a[i])
		i += 1
	

SetupCategory()


if __name__ == "__main__":
	root = tkinter.Tk()

	GetTheWord(root)
	root.mainloop()
