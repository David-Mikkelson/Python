import tkinter
from tkinter import messagebox

#Setting the defualt timer in seconds
DEFAULT_GAP = 25*60






#------------
# examples for pack()
#hi_there = tkinter.Label(root, text="hi there", bg="red", fg="white")
#i_there.pack(fill=tkinter.BOTH, expand=True)
class MainTimer:
	def __init__(self, master):
		self.master = master
		#-------------------
		# this creating the main gui Frame
		self.mainframe = tkinter.Frame(self.master, bg='white')
		self.mainframe.pack(fill=tkinter.BOTH, expand=True)
		
		#------------------
		# Var you can watch for changes
		# for timer
		self.timer_text = tkinter.StringVar()
		# When ever timer_text is (w)ritten to rerun build_timer
		self.timer_text.trace('w', self.build_timer)
		#Setup Variable and check for changes
		self.time_left = tkinter.IntVar()
		self.time_left.set(DEFAULT_GAP)
		self.time_left.trace('w', self.alert)
		self.running = False


		self.build_grid()
		self.build_banner()
		self.build_buttons()
		self.build_timer()

		self.update()

	def build_grid(self):
		#---------------------
		# weight=0 will not get bigger with resizing while 1 will
		self.mainframe.columnconfigure(0, weight=1)
		self.mainframe.rowconfigure(0, weight=0)
		self.mainframe.rowconfigure(1, weight=1)
		self.mainframe.rowconfigure(2, weight=0)

	def build_banner(self):
		banner = tkinter.Label(
			self.mainframe,
			background='red',
			text='Timer',
			fg='white',
			font=('Helvetica', 24)
			)
		banner.grid( row=0, column=0, sticky='ew', padx = 10, pady = 10)

	def build_buttons(self):
		#-------------------
		# building another frame inside mainframe for the buttons
		buttons_frame = tkinter.Frame(self.mainframe)
		buttons_frame.grid(row=2, column=0, sticky='nsew', pady = 10, padx = 10)	
		buttons_frame.columnconfigure(0, weight=1)
		buttons_frame.columnconfigure(1, weight=1)

		#---------------
		# Creating buttons
		self.start_button = tkinter.Button(
			buttons_frame,
			text="Start",
			command= self.start_timer
			)
		self.stop_button = tkinter.Button(
			buttons_frame,
			text="Stop",
			command= self.stop_timer
			)

		#---------------
		# putting the buttons on the grid
		self.start_button.grid(row=0, column=0, sticky='ew')
		self.stop_button.grid(row=0, column=1, sticky='ew')
		#----------------
		# Since you can't stop before it's running Stop will be disabled at the start
		self.stop_button.config(state=tkinter.DISABLED)

	def build_timer(self, *args):
		timer = tkinter.Label(
			self.mainframe,
			text=self.timer_text.get(),
			font=('Helvetica', 36)
			)
		timer.grid(row=1, column=0, sticky='nsew')

	def start_timer(self):
		self.time_left.set(DEFAULT_GAP)
		self.running = True
		# Making the Stop button enabled  and Start Disabled
		self.stop_button.config(state=tkinter.NORMAL)
		self.start_button.config(state=tkinter.DISABLED)

	def stop_timer(self):
		self.running = False
		self.stop_button.config(state=tkinter.DISABLED)
		self.start_button.config(state=tkinter.NORMAL)

	def minutes_seconds(self, seconds):
		return int(seconds/60), int(seconds%60)


	def update(self):
		time_left = self.time_left.get()

		if self.running and time_left:
			minutes, seconds = self.minutes_seconds(time_left)
			self.timer_text.set(
				#fill with up to 2 0
				'{:0>2}:{:0>2}'.format(minutes, seconds)
				)
			#reduce timer by 1
			self.time_left.set(time_left-1)
		else:
			self.stop_timer()
			minutes, seconds = self.minutes_seconds(DEFAULT_GAP)
			self.timer_text.set(
				#fill with up to 2 0
				'{:0>2}:{:0>2}'.format(minutes, seconds)
				)

		# after 1000 milseconds update again
		self.master.after(1000, self.update)

	def alert(self, *args):
		if not self.time_left.get():
			messagebox.showinfo('Timer Done!', 'Your timer is Done!')




#--------------------
# Starts GUI
if __name__ == "__main__":
	root = tkinter.Tk()
	MainTimer(root)
	root.mainloop()