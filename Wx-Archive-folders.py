import wx, os
import shutil, time
import sqlite3 
import mytime
#---------------------------
# Setup where you would like the database setup
conn = sqlite3.connect('wx-archive.db')


class Frame(wx.Frame):
	def __init__(self, title):
		wx.Frame.__init__(self, None, title =title, size = (550, 250))
		self.panel = wx.Panel(self)
		#-----------------------------------------------------------------------
		# Setup directories
		self.destination_folder = False
		self.source_folder = False

		#setup for opening instructions on the top of the page
		wx.StaticText(self.panel, label = 'File Archive Manager', pos = (175,10))
		wx.StaticText(self.panel, label = 'Make sure you have choosen the correct Source and Destination folders', pos = (20,24))
		#-------------------------------------------------------------------------
		# Source file questions
		self.sf = wx.StaticText(self.panel, label = 'Source:',  pos = (20, 75))
		self.source = wx.Button(self.panel, label = 'Source Folder', pos = (15, 45))
		self.source.Bind(wx.EVT_BUTTON, self.pick_source)
		#    Display for last time the check was run on this Folder
		self.sftime = wx.StaticText(self.panel, label = 'Last Archive:',  pos = (225, 100))

		#-------------------------------------------------------------------------
		# Destination folder selection:
		self.df = wx.StaticText(self.panel, label = 'Destination: ',  pos = (20, 160))
		self.dest = wx.Button(self.panel, label = 'Destination Folder', pos = (15, 120))
		self.dest.Bind(wx.EVT_BUTTON, self.pick_destination)
		
		#------------------------------------------------------------------------
		# Archive Button
		self.dest = wx.Button(self.panel, label = 'Archive', pos = (15, 190))
		self.dest.Bind(wx.EVT_BUTTON, self.clickToArchive)						

	#----------------------------------------------------------------------
	#
	def pick_source(self, event):

		# Show the DirDialog and return directory

		dlg = wx.DirDialog(self, "Choose a directory:",
		                   style=wx.DD_DEFAULT_STYLE
		                   #| wx.DD_DIR_MUST_EXIST
		                   #| wx.DD_CHANGE_DIR
		                   )
		if dlg.ShowModal() == wx.ID_OK:self.source_folder = dlg.GetPath()  
		self.sf.Destroy()
		self.sf = wx.StaticText(self.panel, label = 'Source: {}'.format(self.source_folder), pos = (20, 75))	       
		#-------------------------------------------------
		# Checking database to see when the last Archiving was done on this folder
		try:
			db_output = conn.execute("SELECT MAX(Utime), Sfolder, Rtime FROM Archive_dates WHERE Sfolder = '{}'".format(self.source_folder))
			d = str(db_output.fetchall()).split('\'')
			self.sftime.Destroy()
			self.sftime = wx.StaticText(self.panel, label = 'Last Archive: {}'.format(d[3]),  pos = (225, 100))
		except:
			#self.sftime.Destroy()
			#self.sftime = wx.StaticText(self.panel, label = 'Last Archive: Never',  pos = (225, 100))
			pass

		dlg.Destroy()
        
		
	#----------------------------------------------------------------------	
	
	def pick_destination(self, event):
		# Show the DirDialog and return directory
		dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
		
		if dlg.ShowModal() == wx.ID_OK:self.destination_folder = dlg.GetPath()
		self.df.Destroy()
		self.df = wx.StaticText(self.panel, label = 'Destination: {}'.format(self.destination_folder), pos = (20, 160))	       
		dlg.Destroy()
		
	#----------------------------------------------------------------------
	# Check that folders are selected and they are different, then Archive files less than 24 hours old  
	def clickToArchive(self, event):
		#------------------------------
		# Error checking first
		if self.destination_folder and self.source_folder and (self.source_folder != self.destination_folder):
			all_files = os.listdir(self.source_folder)
			self.archive_files = []
			current_time = int(time.time())
			print(all_files)
			#--------------------------------------
			# Checking age of a file and archiving if needed
			for fname in all_files:
				current = '{}/{}'.format(self.source_folder, fname)
				file_age = str(os.stat(current)).split(',')[8].split('=')[1]
				delta = current_time - int(file_age)
				print('{} : {}'.format(fname, delta))
				if(delta < 86401): shutil.copy2(current, self.destination_folder)
				if(delta < 86401): print(current)
			#--------------------------------
			# Creating values for SQL table and Inserting when Archiving is done
			import mytime
			t = real_time()
			values_sql = "'{}', '{}', '{}', '{}'".format(self.source_folder, self.destination_folder, t.Utime, t.stamp)
			conn.execute("INSERT INTO Archive_dates (Sfolder, Dfolder, Utime, Rtime) VALUES ({})".format(values_sql))
			conn.commit()
			#--------------------------------
			# Opening popup so user knows it is complete
			dlg =wx.MessageDialog(None, 'All files that were created of modified in the last 24 hours where Archived', 'Thanks', wx.OK)
			dlg.ShowModal()
			dlg.Destroy()

		else:
			#-----------------------------
			# Creating a pop up window to remind the user that they need to choose folders first
			dlg =wx.MessageDialog(None, 'Please pick both source and Destination folders', 'helpful message', wx.OK)
			dlg.ShowModal()
			dlg.Destroy()

class real_time():
	def __init__(self):
		month_label = {1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May',
					   6 : 'June', 7 : 'July', 8 : 'August', 9 : 'September', 
					   10 : 'October', 11 : 'November', 12 : 'December'}
		self.year   =  time.localtime()[0] 
		self.month  =  time.localtime()[1]
		self.day    =  time.localtime()[2]
		self.hour   =  time.localtime()[3]
		if(time.localtime()[4] < 10):
			self.minute = '0{}'.format(time.localtime()[4])
		else:
			self.minute =  time.localtime()[4]
		self.time   =  '{}:{}'.format(self.hour, self.minute)
		self.stamp  =  '{} on {} {}'.format(self.time, month_label[self.month], self.year) 
		self.Utime  = time.time()
	






app = wx.App()
frame = Frame('Archive')
frame.Show()
app.MainLoop()
