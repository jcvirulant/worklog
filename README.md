# worklog
A console app that lets you add, edit, delete and search work logs

#example code

```

def main():
	while True:
		user_input = input(" N[ew task] F[ind task] E[dit] D[elete] Q[uit] H[elp] >> ").lower()
		print("*"*50)
		if user_input not in "nfqhed" or not user_input:
			clear_screen()
			alert_message("That was not a valid selection!")
			continue
		elif user_input=="n":
			create_task()
		#check to see if the file exists
		elif not task.file_exists():
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

```
# To run the app
just run the file worklog.py
