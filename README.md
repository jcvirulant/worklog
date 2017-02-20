# worklog
A terminal application to prepare better timesheets for a company. The program writes and reads work data such as 
time spent on task, task completion date and other information in a CSV file.

#example code

```python

import datetime
import time
import csv
import os
import re


class Task:
	date= None
	task_name = None
	time_spent = None
	notes = None
	headers = ["ID", "Date", "Task_name", "Time_spent", "Notes"]
	
	
	def __init__(self):
		self.date = datetime.date.today().strftime('%d/%m/%Y')
		
	
	def task_as_dict(self):
		"""this method returns the task info
		in the form of a dict"""
		
		if not os.path.isfile('worklog.csv'):
			ID = 1
		else:
			# get the last task id
			ID = self.get_last_task_id()
		row = {'ID':ID,'Date':self.date,'Task_name':self.task_name,
				'Time_spent':self.time_spent,'Notes':self.notes}
		return row
	
	
	def write_task(self, task):
		"""this method takes a dictionary
		as a task and writes it to the file"""
		
		# check to see if the file exists 
		file_exists = os.path.isfile('worklog.csv')
		with open('worklog.csv','a') as mycsv:
			writer = csv.DictWriter(mycsv,fieldnames=self.headers)
			# prevent the header from repeating 
			if not file_exists:
				writer.writeheader()
				writer.writerow(task)
			else:
				writer.writerow(task)

```
# To run the app
just run the file worklog.py
