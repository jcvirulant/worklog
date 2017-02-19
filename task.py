import datetime,time
import csv, os, re

class Task:
	date= None
	task_name = None
	time_spent = None
	notes = None
	headers = ["ID","Date","Task_name","Time_spent","Notes"]
	
	
	def __init__(self):
		self.date = datetime.date.today().strftime('%d/%m/%Y')
		
	
	def file_exists(self):
		"""check to see if a file has been created"""
		return os.path.isfile('worklog.csv')
	
	
	def task_as_dict(self):
		"""this method returns the task info
		in the form of a dict"""
		
		if not self.file_exists():
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
		file_exists = self.file_exists()
		with open('worklog.csv','a') as mycsv:
			writer = csv.DictWriter(mycsv,fieldnames=self.headers)
			# prevent the header from repeating 
			if not file_exists:
				writer.writeheader()
				writer.writerow(task)
			else:
				writer.writerow(task)
			
	
	def get_last_task_id(self):
		""" this method gets the id
		of the last task and increments it
		by one i.e acting as an auto increment 
		field"""
		
		content = self.read_all_tasks()
		# check to see if the list is empty, if it is the ID will be 1
		if len(content) < 1 :
			return 1
		else:
			last_item = len(content)-1
			# get the last dict in the list
			last_dict = content[last_item]
			# get the id from that dict
			ID = int(last_dict['ID'])
			ID+=1
			return ID
		
	
	def read_all_tasks(self):
		""" this method read and returns
		all the tasks in the file as a list 
		of dictionaries"""
		
		# a list of dictionaries
		tasks = []
		with open('worklog.csv','r') as mycsv:
			reader = csv.DictReader(mycsv,delimiter = ',')
			for row in reader:
				tasks.append(row)
		return tasks
	
	
	
	def edit_task(self, pk):
		""" this method will take a 
		pk or id, match the task by id
		and then update it"""
		
		# take a pk and return the corresponding task
		pk = int(pk)
		content = self.read_all_tasks()
		result = []
		for mydict in content:
			# get the task id
			ID = int(mydict["ID"])
			# if pk == id return the task
			if ID == pk:
				result.append(mydict)
			else:
				pass
		return result
			
		
	def build_edited_content(self, pk):
		""" this method takes a pk, matches the pk to the ID
		of the task and removes that task.This is achived
		by ignoring the task added to the list when the id's
		match"""
		
		pk = int(pk)
		content = self.read_all_tasks()
		edited_content = []
		for mydict in content:
			# get the task id
			ID = int(mydict["ID"])
			if ID == pk:
				# write the update the task 
				row ={"ID": ID,"Date":self.date,'Task_name': self.task_name,
							'Time_spent': self.time_spent,'Notes': self.notes}
				edited_content.append(row)
			else:
				# else write the same task back to the file
				edited_content.append(mydict)
		# write the new content
		message = self.write_content(edited_content, 'e')
		return message
		
	
	def build_deleted_content(self, pk):
		""" this method takes a pk, matches the pk to the ID
		of the task and only updates that task with the
		new content, last the list is sent to another
		method to be writen out to a brand new file"""
		
		
		pk = int(pk)
		content = self.read_all_tasks()
		deleted_content = []
		for mydict in content:
			# get the task id
			ID = int(mydict["ID"])
			if ID == pk:
				# ignore this task i,e acting as a delete
				pass
			else:
				# else write the same task back to the file
				deleted_content.append(mydict)
		# write the new content
		message = self.write_content(deleted_content, 'd')
		return message
		
	
	def write_content(self, content, orp):
		""" this method takes a list of
		dicts and an operation i.e editing or deleting,
		loops around and writes each dict to the file """
		
		# delete the existing file
		os.remove('worklog.csv')
		message = ""
		try:
			for task in content:
				self.write_task(task)
		except:
			if orp.lower()=="e":
				message = "There was an issue editing the task!"
			else:
				message = "There was an issue deleting the task!"
		else:
			if orp.lower()=="e":
				message = "Task edited successfully"
			else:
				message = "Task deleted successfully"
		return message
				
			
	def get_dates(self):
		"""this method returns all
		the dates in the file in the form
		of a dict"""
		
		content = self.read_all_tasks()
		results = {}
		count = 0
		for dictionary in content:
			date = dictionary['Date']
			# prevent duplicates dates from being added
			if date in results.values():
				pass
			else:
				count+=1
				results[count]= date
		return results
	
	
	def get_tasks_by_time(self, supplied_time):
		""" this  method takes a time object,
		matches the time supplied with the time
		in each task, if they match, the task is
		added to a list, once done the return type
		is a list of dictionaries"""
		
		results = []
		content = self.read_all_tasks()
		for mydict in content:
			task_time = mydict['Time_spent']
			# convert time to a time object
			task_time = time.strptime(task_time, '%H:%M')
			if task_time == supplied_time:
				results.append(mydict)
			else:
				pass
		return results
	
	
	
	def get_tasks_by_text(self, supplied_text):
		""" this  method takes a text,
		matches the text supplied against 
		the task name and Notes, if there
		is a match adds the dict to a list called
		results, return type is a list of dicts"""
		
		supplied_text = supplied_text.lower()
		results = []
		content = self.read_all_tasks()
		for mydict in content:
			task_name = mydict['Task_name'].lower()
			notes = mydict['Notes'].lower()
			if supplied_text in task_name:
				results.append(mydict)
			elif supplied_text in notes:
				results.append(mydict)
			else:
				pass
		return results
	
	
	def get_tasks_by_pattern(self, pattern):
		"""this method takes a regex patter,
		check the pattern against the task name
		or notes, if they match the result is
		added to a list"""
		
		results = []
		content = self.read_all_tasks()
		for mydict in content:
			task = mydict['Task_name']
			note = mydict['Notes']
			task_result = re.findall(r'{}'.format(pattern),task,re.I|re.M|re.X)
			note_result = re.findall(r'{}'.format(pattern),note,re.I|re.M|re.X)
			if task_result:
				results.append(mydict)
			elif note_result:
				results.append(mydict)
			else:
				pass
		return results
	
	
	def get_tasks_by_range(self, date1, date2):
		"""this method takes to dates, checks
		to see if a task in range of these two dates.
		If they are add them to the results and return 
		results"""
		
		results = []
		content = self.read_all_tasks()
		for mydict in content:
			task_date = mydict['Date']
			task_date = datetime.datetime.strptime(task_date, '%d/%m/%Y')
			if task_date >= date1 and task_date <= date2:
				results.append(mydict)
			else:
				pass
		return results
			
			
		
		
		
			
		
		
		
		
		
		
			
				
					

