# *******         TASK 26             *******
# *******    Compulsory Task 1        *******
# *******       task_manager.py       *******
# used help from https://www.programiz.com/python-programming/datetime/strftime to understand how to format the date
# into string with strftime() function.
# -------------------------------------------------  xxx -------------------------------------------------------------

# This program is a modification of task_manager.py of capstone 2. It provides extra options to 'admin' to generate
# reports, see statistics about tasks and users. It also restricts normal user other than admin to register new user
# and checks for username that already exist to prevent duplicate records.
# Here we have encapsulated the codes into functions to increase readability and for reusing it in future projects.

from datetime import *
import time
import os


def reg_user():

    user_file = open('user.txt', 'a+', encoding='utf-8')

    while True:
        new_username = input("Create Username : ")
        check_user = False
        user_file.seek(0)
        for each_line in user_file:
            line_list = each_line.split(", ")

            if line_list[0] == new_username:
                print("User name Exist. Try again !")
                check_user = True
                break

        if check_user:
            continue

        new_password = input("Create Password : ")
        password_confirmation = input("Confirm Password : ")

        if new_password == password_confirmation:
            user_file.write("\n" + new_username + ", " + new_password)
            user_file.close()
            print("Your User have been registered.")
            time.sleep(1)
            break
        else:
            print("Your passwords don't match. Try again")
            time.sleep(1)
            continue


def add_task():
    while True:
        print("Assigning task :\n ")
        username = input("Username : ")
        task_title = input("Task Title : ")
        task_desc = input("Task Description : ")
        task_due = input("Task Due Date. Eg 02 jan 2021: ")
        current_date = date.today()

        task_file = open('tasks.txt', 'a+', encoding='utf-8')
        task_file.write(f'\n{username}, {task_title}, {task_desc}, {current_date.strftime("%d %b %Y")}, {task_due}, No')
        print(f'Your Task has been assign to the user {username}.')
        time.sleep(1)
        reply = input("Do you want to continue assigning task. press n to exit or any key to continue: ").lower()
        if reply == 'n':
            task_file.close()
            break


def view_all():
    task_no = 0
    with open('tasks.txt', 'r', encoding='utf-8') as task_file:
        for each_line in task_file:

            if each_line.strip() == '':  # This check if there is any empty line in tasks file
                continue

            task_list = each_line.strip().split(", ")
            task_no += 1
            print(f'''
            {125 * '-'}
            Task No:            {task_no}
            Task:               {task_list[1]}
            Assigned to:        {task_list[0]}
            Date Assigned:      {task_list[3]}
            Due Date:           {task_list[4]}
            Task Complete:      {task_list[5]}
            Task Description:
            {task_list[2]}
            {125 * '-'} 
            ''')

        time.sleep(1)


def edit_task(task_no):

    content = ""
    # content1 = ""
    task_count = 0
    overwrite = True

    edit_choice = input(f'''
    Please select one of the options:
    m - Mark the task {task_no} as complete.
    e - Edit the task {task_no}.
    ''').lower()

    if edit_choice == 'm':
        task_file = open('tasks.txt', 'r', encoding='utf-8')
        for each_line in task_file:
            if each_line.strip() == '':
                continue
            task_count += 1
            task = each_line.strip().split(', ')
            if task_no == task_count:
                task[5] = 'Yes'
                content += ", ".join(task) + "\n"
            else:
                content += each_line
        task_file.close()

        task_file = open('tasks.txt', 'w', encoding='utf-8')
        task_file.write(content)
        task_file.close()

    elif edit_choice == 'e':
        task_file = open('tasks.txt', 'r', encoding='utf-8')
        for each_line in task_file:
            if each_line.strip() == '':
                continue
            task_count += 1
            task = each_line.strip().split(', ')
            # If the task number choose by the user which was then passed through function as argument is same as
            # one of the task in the file then we check if it is marked as completed or not to go further
            if task_no == task_count:

                if task[5] == 'Yes':
                    print("Your Task has already been completed. Cannot be edited")
                    overwrite = False
                    time.sleep(1)
                    break

                while True:

                    task_edit = input(f'''
                    What do you want to change :
                    user - Username for the task {task_no}.
                    date - Due date for the task {task_no}.
                    ''').lower()
                    if task_edit == "user":
                        edited_user = input("\t\t\t\t\tEnter new username : ").lower()
                        task[0] = edited_user

                    elif task_edit == "date":
                        edited_date = input("\t\t\t\t\tEnter the due date to edit Eg, '5 jan 2023' : ").lower()
                        task[4] = edited_date

                    else:
                        print("\t\t\t\t\tWrong choice. Enter either 'user' or 'date' to modify")
                        time.sleep(1)
                        continue
                    reply = input("\t\t\t\t\tcontinue changing task? Press 'n' to cancel/ any key to continue ").lower()
                    if reply == 'n':
                        content += ", ".join(task) + "\n"
                        break
                    else:
                        continue
            else:
                content += each_line

        task_file.close()

        if overwrite:
            task_file = open('tasks.txt', 'w', encoding='utf-8')
            task_file.write(content)
            task_file.close()

    else:
        print("Wrong choice. Enter either 'm' to mark task as complete or 'e' to edit task.")
        time.sleep(1)

# This function displays the tasks of logged-in user and allow the user to edit the task. This function takes
# task number as an input from the user and pass it on to edit_task() function as an argument to perform the edit.


def view_mine(login_username):
    back_to_main_menu = False

    with open('tasks.txt', 'r', encoding='utf-8') as task_file:

        while True:
            task_no = 0
            task_no_list = []

            task_file.seek(0)
            for each_line in task_file:
                if each_line.strip() == '':   # check if there is an empty line in tasks.txt
                    continue
                task_no += 1
                task_list = each_line.strip().split(", ")

                if task_list[0] == login_username:
                    task_no_list.append(task_no)
                    print(f'''
                    {125 * '-'} 
                    Task No             : {task_no}
                    Task                : {task_list[1]}
                    Assigned to         : {task_list[0]}
                    Date Assigned       : {task_list[3]}
                    Due Date            : {task_list[4]}
                    Task Complete       : {task_list[5]}
                    Task Description    :
                    {task_list[2]}
                    {125 * '-'} 
                    ''')
            time.sleep(1)

            while True:
                try:
                    task_no_choice = int(input(f"Enter a task number {task_no_list} or enter -1 to return to menu : "))
                    if task_no_choice == -1:
                        back_to_main_menu = True
                        break

                    if task_no_choice in task_no_list:
                        edit_task(task_no_choice)
                        break

                    else:
                        print(f"Wrong choice! Enter only Task {task_no_list}. Try Again")
                        time.sleep(1)
                        continue

                except ValueError:
                    print("Please enter a valid integer number")

            if back_to_main_menu:
                break

# This function evaluates details of all the tasks and also details of the tasks assign to each user and write them
# to task_overview.txt and user_overview.txt respectively.


def generate_report():
    # variables to hold tasks details for all user
    total_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0
    percentage_of_uncompleted = 0.0
    percentage_of_overdue = 0.0

    # variables to hold tasks details for specific user
    total_users = 0
    all_users = []
    user_dict = {}

    today = datetime.now()

    with open('user.txt', 'r', encoding='utf-8') as user_file:
        for each_line in user_file:
            each_user = each_line.strip('\n').split(', ')
            all_users.append(each_user[0])

    for username in all_users:
        total_users += 1

        # Here we create a 2D dictionary where, for every user we initialize the tasks details using key-value pair
        user_dict[username] = {
                                    'total_tasks': 0,
                                    'completed_task': 0,
                                    'uncompleted_task': 0,
                                    'overdue_task': 0,
                                    'task_%': 0.0,
                                    'completed_%': 0.0,
                                    'uncompleted_%': 0.0,
                                    'overdue_%': 0.0,
                                }

    with open('tasks.txt', 'r', encoding='utf-8') as task_file:

        for each_line in task_file:
            if each_line.strip() == '':
                continue
            task_list = each_line.strip('\n').split(', ')
            user = task_list[0]
            task_due_date = datetime.strptime(task_list[4], "%d %b %Y")

            # This section evaluates the details of tasks assigned to all user
            total_tasks += 1
            if task_list[5] == 'No':
                uncompleted_tasks += 1
                if today > task_due_date:
                    overdue_tasks += 1

            elif task_list[5] == 'Yes':
                completed_tasks += 1

            # This section evaluates the detail of tasks assigned to each user
            if user in all_users:
                user_dict[user]['total_tasks'] += 1
                if task_list[5] == 'No':
                    user_dict[user]['uncompleted_task'] += 1
                    if today > task_due_date:
                        user_dict[user]['overdue_task'] += 1

                elif task_list[5] == 'Yes':
                    user_dict[user]['completed_task'] += 1

    # Preventing division by zero error
    if not uncompleted_tasks == 0:
        percentage_of_uncompleted = round((uncompleted_tasks/total_tasks) * 100, 2)

    if not overdue_tasks == 0:
        percentage_of_overdue = round((overdue_tasks/total_tasks) * 100, 2)

    task_o_file = open('task_overview.txt', 'w+', encoding='utf-8')
    task_o_file.write(f'''Total number of Task                                : {total_tasks}
Total number of Completed tasks                     : {completed_tasks}
Total number of Uncompleted tasks                   : {uncompleted_tasks}
Total number of Overdue tasks                       : {overdue_tasks}
% of Task that are incomplete                       : {percentage_of_uncompleted}%
% of Task that are overdue                          : {percentage_of_overdue}%''')

    user_o_file = open('user_overview.txt', 'w+', encoding='utf-8')
    for user in all_users:

        user_dict[user]['task_%'] = round((user_dict[user]['total_tasks'] / total_tasks)*100, 2)

        # This if else statement prevents divide by zero error if no task has been completed
        if not user_dict[user]['completed_task'] == 0:
            user_dict[user]['completed_%'] = round((user_dict[user]['completed_task'] / user_dict[user]['total_tasks']) * 100, 2)

        if not user_dict[user]['uncompleted_task'] == 0:
            user_dict[user]['uncompleted_%'] = round((user_dict[user]['uncompleted_task'] / user_dict[user]['total_tasks']) * 100, 2)

        if not user_dict[user]['overdue_task'] == 0:
            user_dict[user]['overdue_%'] = round((user_dict[user]['overdue_task'] / user_dict[user]['total_tasks']) * 100, 2)

        user_o_file.write(f"{user}, {total_users}, {total_tasks}, {user_dict[user]['total_tasks']}, {user_dict[user]['task_%']}, {user_dict[user]['completed_%']}, {user_dict[user]['uncompleted_%']}, {user_dict[user]['overdue_%']}\n")

    user_o_file.close()
    print("The Report have been generated ")
    time.sleep(1)

# The function below displays the tasks and users details from task_overview.txt and user_overview.txt files
# generated with 'generate report' option. If the files do not exist then the files are first generated and then the
# details are displayed.


def display_statistics():
    display_once = True
    if not (os.path.exists('user_overview.txt') and os.path.exists('task_overview.txt')):
        generate_report()

    with open('task_overview.txt', 'r', encoding='utf-8') as task_o_file:
        print("\t\t\tTask overview:")
        print("\t\t\t------------- ")
        for each_line in task_o_file:
            print("\t\t\t" + each_line.strip())
    time.sleep(1)

    with open('user_overview.txt', 'r', encoding='utf-8') as user_o_file:

        print("\n\n\t\t\tUser Overview : ")
        print("\t\t\t------------- \n")
        for each_line in user_o_file:
            details = each_line.strip().split(', ')

            if display_once:
                print("\t\t\tTotal number of users registered                    : ", details[1])
                print("\t\t\tTotal number of tasks generated                     : ", details[2])
                display_once = False

            print(f'''
            User: {details[0]}
            Total tasks assigned to user                        : {details[3]}
            % of total tasks assigned to the user               : {details[4]} %
            % of completed tasks assigned to user               : {details[5]} %
            % of uncompleted tasks assigned to user             : {details[6]} %
            % of overdue tasks assigned to user                 : {details[7]} %
            ''')
    time.sleep(1)

# This Section of the program provide users with options on what they like to do, which include adding users, assigning
# tasks and viewing the tasks. It also displays extra menu if the logged-in user is an administrator.


def main_menu(administrator, login_username):
    while True:
        print('''
        Select one of the following Options below: 
        r -  Registering a user
        a -  Adding a task
        va - View all tasks
        vm - view my task''')

        if administrator:
            print('''\t\tgr - Generate Report
        ds - Display Statistics''')

        print("\t\te -  Exit")
        menu = input().lower()

    # If choice of user is 'r', then user is asked to create a username and password and confirm password. This section
    # of program then write the credential of the user to a file if both the passwords entered are same. The program
    # also checks if the user that is logged-in is 'admin' by the use of boolean flag administrator.

        if menu == 'r':
            if administrator:
                reg_user()
            else:
                print("You do not have permission to register a user ")
                time.sleep(1)

    # If user chooses 'a', then user is ask to assign a task to users. The task along with its details are then written
    # into the tasks.txt files on a new line.

        elif menu == 'a':
            add_task()

    # The next two options i.e, 'va' and 'vm' allow the user view all the tasks and view only their task respectively.
    # The tasks are read from the tasks.txt file and displayed in user-friendly output.

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine(login_username)

        elif menu == 'gr':
            generate_report()

        elif menu == 'ds':
            display_statistics()

    # This options allows the user to exit the program
        elif menu == 'e':
            print("GoodBye!!!")
            exit()

    # Finally this options the program to check for invalid input from the user
        else:
            print("You have made a wrong choice. Please Try again")
            time.sleep(1)


# This section of the program asks and checks for user credential until user enters a correct credential.Here the
# program loops through each and every line of user.txt file to fetch and match the 'username' and 'password' before
# continuing to next section of the program.we also check if the user is logged-in as admin and change the boolean
# value of administrator to true if it is the case.


def login_page():

    check_pass = False  # Boolean to check if credential match and exit while loop
    administrator = False  # Boolean to check if user is admin

    while True:
        login_username = input("Username : ")
        login_password = input("Password : ")
        with open('user.txt', 'r+', encoding='utf-8') as user_file_handle:

            # Go through each and every line to get username and password combination
            for line in user_file_handle:
                user_list = line.split(", ")

                # If the username and password matches stop further check by breaking the for loop. Here we also remove
                # the newline character from the end of the line.
                if login_username == user_list[0] and login_password == user_list[1].strip("\n"):
                    print("Password Matched ! \n")
                    check_pass = True
                    if login_username == 'admin':
                        administrator = True
                    time.sleep(1)
                    break

        # Also if the username and password is match break the while loop of login screen to enter the main program.
        if check_pass:
            main_menu(administrator, login_username)
        print("Invalid Username or Password. Try again !")
        time.sleep(1)


# This is the start point of the program. All other functionality has been wrapped into a function modules
login_page()
