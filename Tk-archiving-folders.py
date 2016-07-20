from tkinter import *
from tkinter import ttk
import shutil
import os, time
import sqlite3



conn = sqlite3.connect('/Users/Dmikkelson/Documents/Class-work/python/drills/tk-archive.db')

class Moving:

        def __init__(self, root): 
                style = ttk.Style()
                style.theme_use('classic')
                # Open variables
                self.Adir = '/Users/Dmikkelson/Documents/Class-work/python/A/'
                self.saveFolder = '/Users/Dmikkelson/Documents/Class-work/python/save_folder/'
                self.notArchivedFiles = []
                self.dailyArchive = []
                # Frame One will be for directions and moving folders
                self.one = Frame(root)
                self.one.pack(padx = 5, pady = 5)
                #------------------------------------------------
                # Weclome message to user
                label1 = ttk.Label(self.one, text = 'Please verify the age of the files before archiving')
                label1.pack(side = 'top')
                label1.config(font = ("Ariel", 14), background = 'white')
                #------------------------------------------------
                # Archive buttons
                b1 = ttk.Button(self.one, text = 'Complete Archive', command = lambda: self.clickButton())
                b1.pack(side = 'left')
                b2 = ttk.Button(self.one, text = 'Daily Archive', command = lambda: self.clickdaily())
                b2.pack(side = 'left')
              
                #----------------------------------------------
                # Frame Two will be for showing the directories
                self.two = Frame(root)
                self.two.pack(padx = 10, pady= 10)
                self.createAview()
                
                #----------------------------------------------
                # Updating the last time the Archive was run.
                self.three = Frame(root)
                self.three.pack()
                last_archived = str(conn.execute("SELECT max(Utime), Rtime FROM DATE_INFO").fetchall()).split("'")[1]
                self.label2 = ttk.Label(self.three, text = 'Last Archived: {}'.format(last_archived))
                self.label2.pack(side = 'bottom')
                self.label2.config(font = ("Ariel", 14), background = 'white')


        def checkArchive(self, fname):
                name = '{}{}'.format(self.Adir, fname)
                archivename = '{}{}'.format(self.saveFolder, fname)
                file_age = str(os.stat(name)).split(',')[8].split('=')[1]
                if os.path.isfile(archivename):
                        archiveFileAge = str(os.stat(archivename)).split(',')[8].split('=')[1]
                        delta = int(file_age) - int(archiveFileAge)
                        if(delta == 0):return('complete')
                
                self.notArchivedFiles.append(fname)
                return('incomplete')
                        
                                
                                
        def getAge(self, fname):
                name = '{}{}'.format(self.Adir, fname)
                file_age = str(os.stat(name)).split(',')[8].split('=')[1]
                
                delta = self.time_now - int(file_age)
                print('delta {}'.format(delta))
                days = 0
                hours = 0
                if(delta > 59):
                        minutes = int(delta / 60)
                else:
                        return('0:01')
                
                if(minutes > 60):
                        while(minutes > 59):
                                hours += 1
                                minutes -= 60
                if(hours > 23):
                        while (hours > 23):
                                days += 1
                                hours -= 24
                print(minutes)
                print('{} days {}:{}'.format(days, hours, int(minutes)))

                if(days == 0):
                        self.dailyArchive.append(fname)
                        if(minutes < 10): return('{}:0{}'.format(hours, int(minutes)))        
                        return('{}:{}'.format(hours, minutes))

                else:
                        return('{} days'.format(days))
                
        def moveafile(self, fname):
                self.Atreeview.delete(fname)
                self.indexB += 1
                self.Btreeview.insert('B', self.indexB, fname, text = fname)
                shutil.move('{}{}'.format(self.Adir, fname), self.saveFolder)
                
        def createAview(self):
                self.Atreeview = ttk.Treeview(self.two)
                self.Atreeview.grid(row = 0, column = 0,)
                filesInA = os.listdir(self.Adir)

                self.Atreeview.heading('#0', text = 'Active Folder')
                # Age column
                self.Atreeview.config(columns = ('Age', 'Status'))
                self.Atreeview.column('Age', width = 60, anchor = 'ne')
                self.Atreeview.heading('Age', text = 'Age')
                # Status
                self.Atreeview.column('Status', width = 75)
                self.Atreeview.heading('Status', text = 'Status')
                
                self.time_now = int(time.time())
                for i, name in enumerate(filesInA):
                    ftime = self.getAge(name)
                    status = self.checkArchive(name)
                    self.Atreeview.insert('', i, name, text = name)
                    self.Atreeview.set(name, 'Age', ftime)
                    self.Atreeview.set(name, 'Status', status)
                    self.indexA = i
                            

        def clickButton(self):
                for fname in self.notArchivedFiles:
                        current = '{}{}'.format(self.Adir, fname)
                        shutil.copy2(current, self.saveFolder)
                        status = self.checkArchive(fname)
                        self.Atreeview.set(fname, 'Status', status)
                self.changeUpdateStatus()


        def clickdaily(self):
                print("Hello")
                print(self.dailyArchive)
                for fname in self.dailyArchive:
                        print(fname)
                        current = '{}{}'.format(self.Adir, fname)
                        shutil.copy2(current, self.saveFolder)
                        status = self.checkArchive(fname)
                        self.Atreeview.set(fname, 'Status', status)
                self.changeUpdateStatus()

        def changeUpdateStatus(self):
                # 
                columns = "'Utime', 'Rtime'"
                d = real_time()
                conn.execute("INSERT INTO DATE_INFO ({}) VALUES ({});".format(columns, d.db))
                conn.commit()
                self.label2.config(text = 'Last Archived: {}'.format(d.stamp))



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
        self.Utime  = int(time.time())
        self.db     = "{}, '{}'".format(self.Utime, self.stamp)

                

                


def main():
        root =Tk()
        move = Moving(root) 
        root.mainloop()

if __name__ == "__main__": main()
