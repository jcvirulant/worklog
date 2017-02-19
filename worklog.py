import datetime
import time
import re
import os

from task import Task
# create a instance of Task
task = Task()


def help_text():
	print("*"*10)
	msg = ("Welcome to the worklog app.\n"
				"The app lets you record and query\n"
				"day to day tasks.\n"
				"".strip().replace('\t',''))
	display_message(msg)
	

def file_exists():
	return os.path.isfile('worklog.csv')


def type_of_search_info():
	"""this method asks the user for a 
	type of search"""
	
	display_message("Your search options")
	search_type = input("find by d[ate]\n"
			 								"find by t[ime]\n"
			 								"find by e[xact] search\n"
			 								"find by p[attern]\n"
											"find by r[ange] \n"
											">> ".replace('\t','').lower())	
	if search_type not in "dtepr" or not search_type:
		clear_screen()
		input("Did not recognise your search option! [press enter]")
		type_of_search_info()
	else:
		return search_type
	

def get_chosen_date(options, option):
	"""this function takes a dict
	and an option, it checks for the
	option in the dictionary and returns
	the corresponding date"""
	
	clear_screen()
	date = ""
	#looping around each options
	for key,value in options.items():
		# if the option is the key then thats the date the user choose
		if option == key:
			date = value
		else:
			pass
	return date

	
def print_tasks_by_date(date):
	""" this function takes a date,
	iterates through each dict in the 
	list, checks for the date in each 
	dict, if it is print out that dict"""
	
	results = []
	clear_screen()
	display_message("Here are your results")
	content = task.read_all_tasks()
	#print out the headers
	print_headers()
	# loop around the list to get each dict
	for dictionary in content:
		if date == dictionary["Date"]:
			print("{ID},{Date},{Task_name},{Time_spent},{Notes}".format(**dictionary))
	print("*"*50)
		

def display_message(msg):
	"""this method takes a message
	and prints it with a bit of styling
	around it"""
	
	clear_screen()
	print("*"*50)
	print(msg)
	print("*"*50)
	print("")
	
  
def date_options(dates):
	"""This method will takes a list 
	of dates and prints it out in numerical
	order"""

	clear_screen()
	display_message("Here are your options to choose from")
	count = 0
	for key,val in dates.items():
		count+=1
		print("{} {}".format(count,val))
	print("*"*50)
  

def get_notes_from_user():
	"""this method asks the user
	to supply notes for the task"""
	
	notes = input("Any notes to enter for this task >> ")
	if not  notes:
		input("You have not entered any notes! [press enter]")
	else:
		return notes
    

def get_task_name():
	"""asks the user for the task name """
	
	task = input("Please enter the name of the task >> ")
	if not task:
		input("You have not entered a task! [press enter]")
		return get_task_name()
	else:
		return task
    

def get_task_time():
	"""getting the time taken
	to complete a task"""
	
	task_time = input("How long did your task take?\n"
										"enter in the format HH:MM\n"
										"example 1hour 40 mnts would be 01:40\n"
										" >> ".strip().replace("\t",""))
	
	if not_valid_time(task_time):
		input("You did not enter the date in\n"
				 "the correct format!! [press enter] >> ")
		return get_task_time()
	else:
		return task_time

		
def display_options(dates):
	"""this method takes a dict of
	dates and prints it to the console"""

	clear_screen()
	display_message("Here are you options")
	for key,val in dates.items():
		print("{} {}".format(key,val))
		

def get_task_choice(results):
	"""this method requests the user
	to enter a option based on a list of
	dates or tasks"""
	
	choice = input("Please select a choice, "
								 "where 1 is the first task "
								 "in the list >> ")
	if not choice:
		input("Please select a task! [press enter]")
		return get_task_choice(results)
	else:
		try:
			choice = int(choice)
		except ValueError:
			input("Your choice should be a number! [press enter]")
			return get_task_choice()
  
	for key, val in results.items():
		if key == choice:
			return val

				
def show_results(results):
	"""this method takes a list,
	checks to see if its empty,
	if not its contents are printed
	to the console"""
	
	count = 0
	if len(results) < 1:
		clear_screen()
		display_message("Sorry, your search came up with no results!")
	else:
		display_message("Here are your options")
		print_results(results)


def print_results(results):
	"""this method takes a list
	of dicts and prints them to 
	the console"""
	
	#print out the headers
	print_headers()
	for dictionary in results:
		# loop around each dict if the dates are the same print them
		print("{ID},{Date},{Task_name},{Time_spent},{Notes}".format(**dictionary))
	#print an empty line
	print("")
	

def print_headers():
	print("{},{},{},{},{}".format(
		    task.headers[0],
				task.headers[1],
				task.headers[2],
				task.headers[3],
				task.headers[4],
		))
		

def get_option():
	"""this method asks the user to select an 
	option from a list of dates"""
	
	try:
		option = int(input("Please select a option, where 1 is\n"
											 "the first option in the list >> ".replace('\t','').lower()))
	except ValueError:
		input("Please select a valid option!!. e.g 1 represents "
					"first date in the list [press enter] ")
		return get_option()
	else:
		return option
	

def perform_search_by_date():
	""" this method performs the 
	search by date"""
	
	#get all the dates in the file
	options = task.get_dates()
	#print out all the dates
	date_options(options)
	# get an option from the user
	option = get_option()
	# returns the date the user chose to search by
	date = get_chosen_date(options, option)
	# print the tasks by chosen date
	print_tasks_by_date(date)
	

def perform_search_by_time():
	""" this method performs 
	the search by time"""
	
	clear_screen()
	# get time spent the user wants to search by
	minutes = get_user_minutes()
	# get all tasks by the time spent
	results = task.get_tasks_by_time(minutes)
	# show results
	show_results(results)
	

def perform_search_by_text():
	"""this method performs a search
	by text"""
	
	clear_screen()
	queried_string = get_queried_string()
	# get all task by the matching minutes
	results = task.get_tasks_by_text(queried_string)
	# show results
	show_results(results)
	

def perform_search_by_pattern():
	""" this method performs the search
	by a entered regex pattern"""
	
	# user should be able to enter a pattern
	# as for a pattern from the user
	pattern = get_user_pattern()
	# get all tasks that match that pattern
	results = task.get_tasks_by_pattern(pattern)
	# show results
	show_results(results)	
		

def perform_search_by_range():
	"""this method performs a search
	based on a date range"""
	
	clear_screen()
	# getting the first date in range
	date_1 = get_first_date_range()
	# gettting the second date in range
	date_2 = get_second_date_range()
	# get all tasks in the range
	results = task.get_tasks_by_range(date_1, date_2)
	show_results(results)
	
	
def perform_search(option):
	"""this function takes an option
	i.e d = date, t=time and so on,
	based on that the correct functions
	are called """
	
	if option =="d":
		perform_search_by_date()
	elif option=="t":
		perform_search_by_time()
	elif option=="e":
		perform_search_by_text()
	elif option=="p":
		perform_search_by_pattern()
	elif option == "r":
		perform_search_by_range()
	else:
		pass
  

def get_first_date_range():
	""" this method gets the first 
	date range from the user"""
	
	date_1 = input("Enter date range one\n"
								 "in the format %d/%m/%y\n"
								 ">>  ".replace("\t","").strip())
	try:
			date_1 = datetime.datetime.strptime(date_1, '%d/%m/%Y')
	except:
			input("Please check the date format! [ press enter ]")
			return get_first_date_range()
	else:
			return date_1

		
def get_second_date_range():
	""" this method gets the second
	date range from the user"""
	
	date_2 = input("Enter date range two\n"
								 "in the format %d/%m/%y\n"
								 ">>  ".replace("\t","").strip())
	try:
		date_2 = datetime.datetime.strptime(date_2, '%d/%m/%Y')
	except:
		input("Please check the date format! [press enter]")
		return get_second_date_range()
	else:
		return date_2
	

def search_by_range(date_1, date_2):
	""" this function takes two dates and
	checks for a range, if the task is in the 
	range, it gets added to the list"""
	
	results = []
	content = read_file()
	for line in content:
		task_date = extract_date(line)
		if task_date >=date_1 and task_date <=date_2:
			results.append(line)
		else:
			pass
	return results
	
	
def get_user_pattern():
	clear_screen()
	pattern = input("Please enter a regular expression'\n"
									"to be matched against a task name or notes\n"
									"the taskname or notes >> ".replace("\t","").strip())
	if not pattern:
		input("Please enter a regular expression! [press enter]")
		return get_user_pattern()
	else:
		return pattern


def display_pattern_results(mylist):
	""" This function takes a list,
	    prints out the contents of 
			the list with a numerical representation
			preceding each result"""
	
	count = 0
	if not mylist:
		display_message("Your expression returned no results!")
	else:
		display_message("Here are your results!")
		for task in mylist:
			count +=1
			print("{} {}".format(count,task))

			
def get_queried_string():
	"""this method requests the user to 
	enter a search text"""
	
	result = input("Please enter text to "
								 "to match against the task name"
								 "or notes "
								 ">> ".replace("\t","").strip())
	# validate the string
	if not result:
		input("Please enter a search term [press enter]")
		return get_queried_string()
	else:
		return result
                

def not_valid_date(user_input):
	""" This method takes a user_input
	and validates it against a date 
	format"""

	try:
			user_input = datetime.datetime.strptime(user_input, '%d/%m/%Y')
	except:
			return True
	else:
			return False


def not_valid_time(user_input):
	"""This method takes user_input
	and validates it against a time
	format"""
	
	try:
		user_input = datetime.datetime.strptime(user_input,'%H:%M')
	except:
		return True
	else:
		return False
	

def get_user_minutes():
	"""this method request the minutes
	from the user. Validates it,
	if it fails, i.e user has not entered a 
	number, it requests the user to enter again"""
	
	display_message("Enter time taken on tasks!")
	minutes = input("Use the format HH:MM,\n"
									"where 1 hour 40 mnts would be\n"
									"entered as 01:40 >>  ".strip().replace('\t',''))
	
	if not_valid_time(minutes):
		input("Please check your input!!\n"
					"Enter minutes in the format %H:%M [press enter]")
		return get_user_minutes()
	else:
		minutes = time.strptime(minutes,'%H:%M')
		return minutes


def get_edited_task_name(result):
	""" this method takes a result which is
	a dict in a list, old task name is displayed
	and a request for new one is made and returned"""
	
	task_name = ""
	# task is a dict
	task = result[0]
	
	old_taskname = task["Task_name"]
	task_name = input("Your old task name was: {}\n"
										"Please enter a new task name\n"
										">> ".format(old_taskname))
	if  not task_name:
		task_name = old_taskname
		return task_name
	else:
		return task_name
	

def get_edited_time(result):
	""" this method takes a result which is
	a dict in a list, old task name is displayed
	and a request for new one is made and returned"""
	
	print("*"*50)
	new_time = None
	# task is a dict
	task = result[0]
	
	old_time = task["Time_spent"]
	new_time = input("Time spent on this task was:  {}.\n"
										"Enter new Time spent\n"
										"Please use the format HH:MM >> ".format(old_time))
	if not new_time:
		new_time = old_time
		return new_time
	else:
		return new_time
	

def get_edited_notes(result):
	""" this method takes a result which is
	a dict in a list, old task name is displayed
	and a request for new one is made and returned"""
	
	print("*"*50)
	new_time = None
	# task is a dict
	task = result[0]
	
	old_note = task["Notes"]
	new_note = input("your previous notes where : {}.\n"
										"Enter new notes for this task\n"
										">> ".format(old_note))
	if not new_note:
		# if nothing is edited the oldvalue becomes the new
		new_note = old_note
		return new_note
	else:
		return new_note


def clear_screen():
	try:
		os.system('cls')
	except:
		os.system('clear')
	else:
		print("\033c", end="")


def create_task():
	clear_screen()
	display_message("Please create a new task!")
	task.task_name = get_task_name()
	task.time_spent = get_task_time()
	task.notes = get_notes_from_user()
	# create a dict of the task info
	task_as_dict = task.task_as_dict()
	# write the task to the file
	task.write_task(task_as_dict)
	
	
def edit_task():
	clear_screen()
	all_tasks = task.read_all_tasks()
	# show all the tasks
	show_results(all_tasks)
	# get an option()
	option = get_option()
	# get the edited task
	result = task.edit_task(option)
	# get edited information
	display_message("Please edit your task")
	task.date = result[0]['Date']
	task.task_name = get_edited_task_name(result)
	task.time_spent = get_edited_time(result)
	task.notes = get_edited_notes(result)
	# build the edited content
	message = task.build_edited_content(option)
	# print the message to the console
	display_message(message)

	
def delete_task():
	clear_screen()
	all_tasks = task.read_all_tasks()
	# show all the tasks
	show_results(all_tasks)
	# get an option()
	option = get_option()
	# delete the selected task
	message = task.build_deleted_content(option)
	# print the message to the console
	display_message(message)
	

help_text()


def main():
	while True:
		user_input = input(" N[ew task] F[ind task] E[dit] D[elete] Q[uit] H[elp] >> ").lower()
		print("*"*50)
		if user_input not in "nfqhed" or not user_input:
			clear_screen()
			display_message("That was not a valid selection!")
			continue
		elif user_input=="n":
			create_task()
		#check to see if the file exists
		elif not file_exists():
			input("Sorry you have not saved any tasks yet! [press enter]")
			return main()
		elif user_input == "h":
			clear_screen()
			help_text()
		elif user_input=="f":
			clear_screen()
			search_type = type_of_search_info()
			perform_search(search_type)
		elif user_input=="e":
			edit_task()
		elif user_input=="d":
			delete_task()
		else:
			break
			
						
main()