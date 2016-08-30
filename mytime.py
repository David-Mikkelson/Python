import time



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

		