# Practical task for M03T09

# Importing external modules
from datetime import datetime, date

# Initiating empty list and dictionary to be used when reading tasks and
# users text files, respectively.
tasks = []
user_dict = {}


def read_user_file():
    '''Reads the users.txt file then adds each key-value pair 
    (username-password pair) to the 'user_dict' dictionairy to be 
    used later on.

    Returns:
    dictionairy: user_dict (username as key: password as value)).
    '''
    # Read user.txt file
    try:
        with open("user.txt", "r") as file:
            for line in file:
                # Separate each line into a list [key, value]
                person = line.strip().split(", ")
                key = person[0]
                value = person[1]
                # Assign key-value pairs
                user_dict[key] = value
    except FileNotFoundError:
        # Error message if file does not exist
        print("The file 'user.txt' does not exist.")

    return user_dict


def read_tasks_file():
    '''Reads tasks.txt file then appends each task as a list inside
    the 'tasks' list.

    Returns:
    2D list: tasks (each index of tasks is a task)
    '''
    tasks.clear()  # Clear list each time to prevent duplication

    try:
        # Reads tasks.txt
        with open("tasks.txt", "r") as file:
            # Reads in each line as a string
            lines = file.readlines()
            for i, line in enumerate(lines):
                if not line.strip():
                    continue  # Skip empty lines

                # Reads each string into a list and define the properties
                # Format propperties as well
                tasks_lines = line.split(", ")
                emp = tasks_lines[0].strip().lower()
                title = tasks_lines[1].strip()
                descript = tasks_lines[2].strip()
                date_a = tasks_lines[3].strip()
                due = tasks_lines[4].strip()
                stat = tasks_lines[5].strip()

                # Put all properties of one task together and append to list
                task = [emp, title, descript, date_a, due, stat]
                tasks.append(task)
    except FileNotFoundError:
        # Error if file does not exist
        print("The file 'tasks.txt. does not exist.")

    return tasks


def update_tasks_file():
    '''Rewrites content of tasks list to tasks.txt so the information
    stays current and up to date.

    Returns:
    Prints a message if it was succesful or not.
    '''

    try:
        # Opens tasks file in write mode
        with open("tasks.txt", "w") as file:
            for task in tasks:
                # Join each inner list of tasks and ensure each task is
                # on it's own line then writes it to file.
                line = ", ".join(task) + "\n"
                file.write(line) 
        print("Tasks file was successfully updated with new informaiton")
    except FileNotFoundError as e:  # Error message
        print(f"Something went wrong: {e}")


def user_login():
    '''Reads users.txt file then asks user for login details.

    Returns:
    current_user (str) - 
    '''
    read_user_file()  # Reads user.txt file

    while True:
        # Prompt user for username and format
        user = input("Please enter your username: ").strip().lower()
        if user in user_dict:
            print(f"Hello, {user}.")
            current_user = user  # Sets current logged in user
            while True:
                # Prompt user for password and format
                passw = input("Please enter your password: ").strip().lower()
                if user_dict.get(user) == passw:
                    print("Login was successfull!")
                    return current_user  # Exit function after successfull login
                # Print error message of password is not correct
                else:
                    print("Invalid password. Please try again.")
        # Prints error message if username does not exist
        else:
            print(f"The username '{user}' does not exist.")


def reg_user():
    '''Ask 'admin' user for details of new user then writes
    these new details to user.txt file.
    '''
    while True:
        # Prompt for new username and format
        new_user = input("Please enter the new username: ").strip().lower()
        if new_user in user_dict:
            # Informs admin that the username already exists
            print("This username already exists. Please try again")
        else:
            print(f"Username {new_user} has been created")
            break  # Exit this loop if new username created

    # Prompt for new password and format
    new_passw = input("Please enter new password: ").strip().lower()
    while True:
        # Prompt to confirm new password and format
        conf_new_passw = input("Please confirm new password: ").strip().lower()
        if new_passw == conf_new_passw:
            # Assign new details as key-value pair
            user_dict[new_user] = conf_new_passw
            # Writes new details to user.txt
            with open("user.txt", "a") as file:
                file.write(f"\n{new_user}, {new_passw}")
            print("New user has successfully been registered")
            break  # Exit this loop if new details successfully added
        else:
            print("Confirmation password does not match new password.")


def add_task():
    '''Reads the tasks.txt file.
    
    Ask user for new task details:
    - emp: username to whom new task is to be assigned
    - title: title of new task
    - descript: description of new task
    - due_d_str: due date of new task

    Properties that are automatic (without prompting user):
    - date_a: date when new task is added
    - stat: Status of completion

    Appends new details to 'tasks' list after combining them 
    into one task
    
    Lastly calls update_tasks_file() function to update tasks.txt with
    new task information
    '''
    # Read in tasks.txt file so 'tasks' list is populated
    read_tasks_file()

    # Prompt user for new username
    while True:
        emp = input(
            "To whom do you want to assign a new task?: "
        ).strip().lower()  # Format details
        if emp in user_dict:
            break  # Exit this loop if a valid username was given
        else:
            print("This username does nto exist.")

    # Prompt user for title and description of task
    title = input("What is the title of the new task?: ").capitalize()
    descript = input("Please describe the new task: ").capitalize()
    
    while True:
        # Promt user for due date of task adn format it
        due_d_str = input("Please enter the due date (dd Mon YYYY): ").strip()
        # Format the input for due date
        try:
            parsed_due = datetime.strptime(due_d_str, "%d %b %Y")
            due = parsed_due.date().strftime("%d %b %Y")
            break  # Exit this loop is due date is valid
        except ValueError:
            # Error message for invalid input
            print(
                "Invalid due date input. Please enter date in format: 15 Oct 2025"
            )

    # Assignment date is always today in format dd Mon YYYY
    date_a = date.today().strftime("%d %b %Y")
    
    # Completion status of new task automatically set to 'No' 
    stat = "No"

    # Combine details of new task into 1 task item then append to list
    new_task = [emp, title, descript, date_a, due, stat]
    tasks.append(new_task)
    print("The new task has successfully been added.")

    # Update tasks.txt file with new task
    update_tasks_file()


def view_all():
    '''Reads tasks.txt file and prints details of each task in easy 
    to read format.
    '''
    read_tasks_file()  # Reads in updated tasks.txt file

    # Inform user if there are not tasks to view.
    if len(tasks) == 0:
        print("There are not tasks to view.")

    # Loop through each task and print details
    for i, task in enumerate(tasks):
        print("-" * 50)  # For separation of tasks (border)
        print(f"Task {i}:                 {task[1]}")
        print(f"Assigned to:            {task[0]}")
        print(f"Date assigned:          {task[3]}")
        print(f"Due date:               {task[4]}")
        print(f"Task complete?          {task[5]}")
        print(f'''Task description:\n{task[2]}''')
        print("-" * 50)  # Border


def view_mine():
    '''Reads tasks.txt file and prints tasks assigned to current
    logged in user.

    It then asks user if they want to edit a task and prompts user
    to enter task number. It then provides different editing options:
    - Mark as complete: Changes completion status of task to "Yes"
    - Edit: Provides choice of editing username to whom task is
        assigned or due date of task.
    
    After each edit, tasks.txt file is updated
    '''
    read_tasks_file()  # Reads in updated tasks.txt file

    # Inform user if there are not tasks to view.
    if len(tasks) == 0:
        print("There are not tasks to view.")

    for i, task in enumerate(tasks):
        # Assigns first item in task (username) to variable emp
        emp = task[0]

        # Only prints tasks assigned to logged in emp
        if logged_in == emp:
            print("-" * 50)  # Border
            print(f"Task {i}:                 {task[1]}")
            print(f"Assigned to:            {task[0]}")
            print(f"Date assigned:          {task[3]}")
            print(f"Due date:               {task[4]}")
            print(f"Task complete?          {task[5]}")
            print(f'''Task description:\n{task[2]}''')
            print("-" * 50)  # Border

    while True:
        # Prompt user to select a task to edit or exit(-1)
        select = int(input(
            "Would you like to edit a task? \n"
            "If yes, please enter the task number or '-1' to exit: ")
        )
        if select == -1:
            break  # Exit loop if used does not want to edit a task

        # Ensure selected task is within boundaries
        elif 0 <= select < len(tasks):
            while True:
                # Prompt user to choose between marking as complete or
                # editing
                choice = input(
                    "Please choose one of the following options: \n"
                    "1. Mark as complete\n"
                    "2. Edit\n" 
                    "3. Go back to task selection.\n"
                ).strip()  # Format input

                
                # If user wants to mark task as complete
                if choice == "1":
                    if tasks[select][5].lower() == "yes":
                        # If selected task is already complete
                        print(
                            "This task is already complete, "
                            "please choose another option."
                        )
                    else:
                        tasks[select][5] = "Yes"  # Mark task as complete
                        print("Selected task has been marked as complete.")
                        update_tasks_file() # Update tasks.txt file

                # If user wants to edit the task further
                elif choice == "2":
                    if tasks[select][5] == "No":  # Only edit incomplete tasks
                        while True:
                            # Ask user what they want to edit
                            edit = input(
                                "Please choose what you would like to edit by "
                                "entering the corresponding letter: \n"
                                "a. Username to whom task is assigned\n"
                                "b. Due date.\n" \
                                "c. Go back to edit selection\n"
                            ).strip().lower()  # Format input

                            # If user chooses to re-assign task
                            if edit == "a":
                                # Ask to whom they want to re-assign
                                while True:
                                    edited_user = input(
                                        "Please enter the username to whom " 
                                        "you want to re-assign this task?"
                                    ).strip().lower()  # Format input
                                    if edited_user in user_dict:
                                        # Set name to new name
                                        tasks[select][0] = edited_user
                                        print(
                                            "This task has been successfully "
                                            "re-ssigned")
                                        update_tasks_file() # Update tasks.txt
                                        break  # Exit loop after re-assignement
                                    else:
                                        # Error if name does not exit
                                        print("That username does not exist.")

                            # If user chooses to change due date
                            elif edit == "b":
                                while True:
                                    try:
                                        # Prompt user for new due date
                                        new_due_str = input(
                                            "Please enter the new due date "
                                            "in the following format: "
                                            "15 Oct 2019:"
                                        ).strip()  # Format input

                                        # Formate date string
                                        parsed_new = datetime.strptime(
                                            new_due_str, "%d %b %Y"
                                        )
                                        new_due = (
                                            parsed_new.date()
                                            .strftime("%d %b %Y")
                                        )
                                        # Set due date to new due date
                                        tasks[select][4] = new_due
                                        # Update tasks.txt file
                                        update_tasks_file()
                                        break  # Exit loop after update
                                    except ValueError:
                                        # Error for invalid date entry
                                        print(
                                            "Invalid date entry. "
                                            "Please use format: 15 Oct 2019"
                                        )
                            elif edit == "c":
                                break  # Exit loop to edit selection
                            else:
                                # Error if invalid choice was made
                                print(
                                    "Invalid choice. "
                                    "Please choose 'a', 'b' or 'c'.")
                    else:
                        # Informs user if tasks is not incomplete
                        print("Only incomplete tasks can be edited")
                        break
                elif choice == "3":
                    break  # Exit loop to go back to task selection
                else:
                    # Error message if invalid choice was made
                    print("Invalid choice. Please choose '1', '2' or '3'.")
        else:
            # Error message if invalid choice was made
            print(
                "Invalid selection. Please choose the task number or "
                "'-1' to exit: "
            )      


def view_completed():
    '''Reads tasks.txt and prints the task that are marked as complete.
    '''
    read_tasks_file()  # Reads updated tasks.txt file

    # Inform user if there are not tasks to view.
    if len(tasks) == 0:
        print("There are not tasks to view.")

    # Set complete to boolean value False
    complete = False

    for i, task in enumerate(tasks):
        if task[5].strip().lower() == "yes":
            # Change value of complete to True when a task marked as
            # complete is found then print task
            complete = True
            print("-" * 50)  # Border
            print(f"Task {i}:                 {task[1]}")
            print(f"Assigned to:            {task[0]}")
            print(f"Date assigned:          {task[3]}")
            print(f"Due date:               {task[4]}")
            print(f"Task complete?          {task[5]}")
            print(f'''Task description:\n{task[2]}''')
            print("-" * 50)  # Border
    if not complete:
        # Inform user if there are no complete tasks
        print("There are currently no completed tasks.")


def delete_task():
    '''Reads tasks.txt file and prints out the task numbers with
    their titles.

    It then asks the user which task to delte and updates the
    tasks.txt file.
    '''
    read_tasks_file()  # Reads updated tasks.txt file

    # Prints number and title of each task
    for i, task in enumerate(tasks):
        title = task[1].title()
        print(f"{i} {title}")

    # Prompt user for number of the task they wish to delete    
    del_nr = int(
        input("Enter the number of the task you would like to delete: ")
    )

    # Deletes the task from 'tasks' list
    for i, task in enumerate(tasks):
        if i == del_nr:
            del tasks[i]
    
    # Updates tasks.txt file with new tasks list (excl. deleted task)
    update_tasks_file()    


def generate_report():
    '''Reads tasks.txt and user.txt files and performs calculations 
    using the each task's properties especialy the:
    - username
    - assignment date
    - due date
    - completion status

    Generates to different text files (reports) and writes specific
    calculations to each:
    - task_overview.txt: contains task specific information
    - user.overview.txt: contains user specific information
    '''
    # Reads up to date tasks.txt file and user.txt file
    read_tasks_file()
    read_user_file()
    
    # Calculate total number of tasks and users
    total_num_tasks = len(tasks)
    total_num_users = len(user_dict)

    # Calculate total number of complete tasks
    complete_tasks = 0
    for task in tasks:
        if task[5].strip().lower() == "yes":
            complete_tasks += 1  # Increment 'complete' counter
    
    # Calculate total number of incomplete tasks
    incomplete_tasks = total_num_tasks - complete_tasks

    # Calculate total number of incomplete and overdue tasks
    overdue_tasks = 0
    today = date.today()  # Set today's date
    for task in tasks:
        due_str = task[4].strip()
        # Convert date string into date object to compare to dates
        due = datetime.strptime(due_str, "%d %b %Y").date()
        if task[5].strip().lower() == "no" and due < today:
            overdue_tasks += 1  # Increment 'overdue' counter
    try:
        # Caclculate pecentage of taks that are incomplete and overdue
        perc_incomplete = (incomplete_tasks/total_num_tasks) * 100
        perc_overdue = (overdue_tasks/total_num_tasks) * 100
    except ZeroDivisionError:
        # Set total number of tasks to 0
        total_num_tasks = 0

    # Generate task_overview.txt file and write calculate statistics
    # to file
    with open("task_overview.txt", "w") as file:
        file.write(f"TASK OVERVIEW OF BUSINESS:\n")
        file.write(f"Total number of tasks: {total_num_tasks}\n")
        file.write(f"Total number of completed tasks: {complete_tasks}\n")
        file.write(f"Total number of incomplete tasks: {incomplete_tasks}\n")
        file.write(
            "Total number of tasks that are incomplete and overdue: "
            f"{overdue_tasks}\n"
        )
        # Format percentage floats to 2 decimals
        file.write(
            "Percentage of tasks that are incomplete: "
            f"{perc_incomplete:.2f}%\n"
        )
        file.write(
            "Percentage of tasks that are incomplete and overdue: "
            f"{perc_overdue:.2f}%\n"
        )
    print("Task_overview report has successfully been created")

    # Generate user_overview.txt file and write total number of tasks
    # and users to file
    with open("user_overview.txt", "w") as file:
        file.write("USER OVERVIEW OF BUSINESS:\n")
        file.write(f"Total number of users registered: {total_num_users}\n")
        file.write(f"Total number of tasks: {total_num_tasks}\n\n")

        # Loop through users in user_dict
        for user_key in user_dict:
            # Initialize counters for each user's task statictics
            total_user_tasks = 0
            user_completed = 0
            user_incomplete = 0
            user_overdue = 0

            # Loop through each task to calculate current user's stats
            for task in tasks:
                # Assign username and completion status from every task
                emp = task[0].strip().lower() 
                stat = task[5].strip().lower()
                due_str = task[4].strip()
                # Convert date str into date object to compare to dates
                due = datetime.strptime(due_str, "%d %b %Y").date()

                # Check if task belongs to current user
                if emp ==  user_key.strip().lower():
                    total_user_tasks += 1  # Increment task count for this user

                    # Check if this task is complete
                    if stat == "yes":
                        user_completed += 1  # Increment 'complete' counter
                    else:
                        # If task is incomplete
                        user_incomplete += 1  # Increment 'incomplete' counter
                        # If incomplete task is also overdue
                        if due < today:
                            user_overdue += 1  # Increment 'overdue' counter
            try:
                # Calculate percentage statistics for each user
                perc_user_tasks = (total_user_tasks/total_num_tasks) * 100
                perc_user_completed = (user_completed/total_user_tasks) * 100
                perc_user_incomplete = (user_incomplete/total_user_tasks) * 100
                perc_user_overdue = (user_overdue/total_user_tasks) * 100
            except ZeroDivisionError:
                # Set percentages to 0 if total number of tasks or total
                # number of tasks per user is 0
                perc_user_tasks = 0
                perc_user_completed = 0
                perc_user_incomplete = 0
                perc_user_overdue = 0

            # Write the rest of the statistics to user_overview.txt   
            file.write(f"{user_key}\n")
            file.write(
                "Total number of tasks assigned to user: "
                f"{total_user_tasks}\n"
            )
            # Format percentage floats to 2 decimals
            file.write(
                "Percentage of tasks assigned to user: "
                f"{perc_user_tasks:.2f}%\n"
            )
            file.write(
                "Percentage of tasks assigned to user that are complete: "
                f"{perc_user_completed:.2f}%\n"
            )
            file.write(
                "Percentage of tasks assigned to user that are incomplete: "
                f"{perc_user_incomplete:.2f}%\n"
            )
            file.write(
                "Percentage of tasks assigned to user that are incomplete "
                f"and overdue: {perc_user_overdue:.2f}%\n"
            )
            file.write(f"\n")
    print("User_overview report has successfully been created")


def display_statistics():
    '''Reads the task_overview.txt and user_overview.txt files and
    displays the information in those files.

    If the user did not select to generate the reports before choosing
    to display the statistics, the function calls the generate_report 
    to make sure the reports do exist.
    '''
    # Generate or update the necessary text file before displaying
    generate_report()

    try:
        # Read task_overview.txt file and print each line
        with open("task_overview.txt", "r") as file:
            # Read all line into a list
            lines = file.readlines()
            print("TASK OVERVIEW:\n")  # Header

            # Print each task
            for line in lines:
                if not line.strip():
                    continue  # Skip empty lines
                print(line.strip())  # Strip extra whitespace
    except FileNotFoundError:
        print("The file 'task_overview.txt does not exist.")
    
    try:
        # Read user_overvie.txt file and print each line
        with open("user_overview.txt", "r") as file:
            # Read all line into a list
            lines = file.readlines()
            print("\nUSER OVERVIEW:\n")  # Header

            # Print each line
            for line in lines:
                print(line.strip())  # Strip extra whitespace
    except FileNotFoundError:
        print("The file 'user_overview.txt' does not exist.")

while True:
    # Ask if they want to login
    login_question = input("Do you want to log in? Yes/No: ").strip().lower()
    if login_question == "no":
        print("Exiting program.")
        break  # Exit program if user does not want to log in

    elif login_question == "yes":
        try:
            # Test to make sure the user credentials exist
            with open("user.txt", "r"):
                print("User.txt exists. Continuing to log in menu.")
        except FileNotFoundError:
            print("User data does not exist. Please ensure user.txt exist.")
            break  # Exit program if details do not exist
        # Call login function
        logged_in = user_login()

        while True:
            # Display the following menu if 'admin' logged in
            if logged_in == "admin":
                menu = input(
                    '''Select one of the following options:
            r - register a user
            a - add task
            va - view all tasks
            vm - view my tasks
            vc - view completed tasks
            del - delete tasks
            ds - dislpay statistics
            gr - generate reports
            e - exit
            : '''
                ).lower()

                # Call corresponding function based on admin's selection
                if menu == "r":
                    reg_user()  # Register a new user
                elif menu == "a":
                    add_task()  # Add a task
                elif menu == "va":
                    view_all()  # View all tasks
                elif menu == "vm":
                    view_mine()  # View only tasks assigned to admin
                elif menu == "vc":
                    view_completed()  # View all completed tasks
                elif menu == "del":
                    delete_task()  # Delete a specific task
                elif menu == "ds":
                    display_statistics()  # Display statistics from  reports
                elif menu == "gr":
                    generate_report()  # Generate reports
                elif menu == "e":
                    print("Goodbye!!!")
                    break  # Exit the menu (log out)
                else:
                    # Error message for invalid selection by admin
                    print("Invalid selection. Please try again")
            # Display the follwing menu is a non-admin user logged in
            elif logged_in != "admin":
                menu = input(
                    '''Select one of the following options:
            # a - add task
            # va - view all tasks
            # vm - view my tasks
            # e - exit
            # : '''
                ).lower()

                # Call corresponding function based on user's selection
                if menu == "a":
                    add_task()  # Add a task
                elif menu == "va":
                    view_all()  # View all tasks
                elif menu == "vm":
                    view_mine()  # View only tasks assigned to current user
                elif menu == "e":
                    print("Goodbye!!!")
                    break # Exit the menu (log out)
                else:
                    # Error message for invalid selection by user
                    print("Invalid choice. Please try again")
    else:
        # Error for invalid input
        print("Invalid input. Please enter Yes or No.")
