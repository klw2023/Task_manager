'''task_manager.py'''
import os
from datetime import datetime

# If no user.txt file, write one with a default account
if not os.path.exists("users.txt"):
    with open("users.txt", "w", encoding= 'utf-8') as default_file:
        default_file.write('admin,password') # Read in user_data

# If no tasks.txt file, write one with a default account
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding = 'utf-8') as default_file:
        pass

def reg_user():
    '''allows a current user to register a new user thats then written in users.txt'''
    username = input("Enter username: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")

    # Check if passwords match
    if password != confirm_password:
        print("Passwords do not match.")
        return

    # Check if username is already taken
    with open("users.txt", "r", encoding='utf-8') as file:
        existing_users = file.readlines()
        existing_users = [user.strip().split(',')[0] for user in existing_users]

    if username in existing_users:
        print("Username taken.")
        return

    # If everything is fine, add the user to the file
    with open("users.txt", "a", encoding='utf-8') as file:
        file.write(f"\n{username},{password}")

    print("User registered successfully.")

def add_task():
    '''allows a user to add a task to task.txt'''
    assigned_to = input("Enter the username of the person whom the task is assigned to: ")
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the description of the task: ")
    due_date_str = input("Enter the due date of the task (in format YYYY-MM-DD): ")

    # Check if user exists
    with open("users.txt", "r", encoding='utf-8') as file:
        users = file.readlines()
        users = [user.strip().split(",")[0] for user in users]

    if assigned_to not in users:
        print("User does not exist.")
        return

    # Validate due date format
    try:
        datetime.strptime(due_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid due date format. Please use YYYY-MM-DD.")
        return

    # Write task details to file
    with open("tasks.txt", "a", encoding='utf-8') as file:
        file.write(f"{assigned_to},{task_title},{task_description},{due_date_str},not complete\n")

    print("Task added successfully.")

def view_mine(username):
    '''displays tasks data for current user'''
    # Read and display user's tasks
    with open("tasks.txt", "r", encoding='utf-8') as file:
        tasks = file.readlines()

    my_tasks = []
    for task in tasks:
        task_data = task.strip().split(",")
        if task_data[0] == username:
            my_tasks.append(task_data)

    if not my_tasks:
        print("No tasks assigned to you.")
        return

    while True:
        print("Your tasks:")
        for i, task in enumerate(my_tasks, 1):
            print(f"{i}. Assigned to: {task[0]}")
            print(f"   Title: {task[1]}")
            print(f"   Description: {task[2]}")
            print(f"   Due Date: {task[3]}")
            print(f"   Status: {'Complete' if task[4] == 'complete' else 'Not Complete'}")

        choice = input("Enter the number of the task to select it, or enter 'e' to return to the menu: ")

        if choice == 'e':
            return

        try:
            choice = int(choice)
            if 1 <= choice <= len(my_tasks):
                selected_task = my_tasks[choice - 1]
                print(f"You selected task: Title: {selected_task[1]}, Description: {selected_task[2]}, Due Date: {selected_task[3]}, Status: {'Complete' if selected_task[4] == 'complete' else 'Not Complete'}")

                action = input("Enter 'c' to mark as complete, 'e' to edit, or 'r' to return to the menu: ")

                if action == 'c':
                    # Mark task as complete
                    selected_task[4] = 'complete'
                    with open("tasks.txt", "w", encoding='utf-8') as file:
                        for task in tasks:
                            if task.strip().split(",") == selected_task:
                                task = ','.join(selected_task) + '\n'
                            file.write(task)
                    print("Task marked as complete.")
                elif action == 'e':
                    # Edit task
                    new_title = input("Enter new title (press Enter to keep existing): ")
                    new_description = input("Enter new description (press Enter to keep existing): ")
                    new_due_date = input("Enter new due date (in format YYYY-MM-DD, press Enter to keep existing): ")

                    if new_title:
                        selected_task[1] = new_title
                    if new_description:
                        selected_task[2] = new_description
                    if new_due_date:
                        selected_task[3] = new_due_date

                    with open("tasks.txt", "w", encoding='utf-8') as file:
                        for task in tasks:
                            if task.strip().split(",") == selected_task:
                                task = ','.join(selected_task) + '\n'
                            file.write(task)
                    print("Task edited successfully.")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except IndexError:
            print("Invalid task number. Please enter a valid number.")

def view_all():
    '''displays the all the task data'''
    # Read and display all tasks
    with open("tasks.txt", "r", encoding='utf-8') as file:
        tasks = file.readlines()

    if not tasks:
        print("No tasks available.")
        return

    print("All tasks:")
    for i, task in enumerate(tasks, 1):
        task_data = task.strip().split(",")
        print(f"{i}. Assigned to: {task_data[0]}")
        print(f"   Title: {task_data[1]}")
        print(f"   Description: {task_data[2]}")
        print(f"   Due Date: {task_data[3]}")
        print(f"   Status: {'Complete' if task_data[4] == 'complete' else 'Not Complete'}")
        print()  # Add a blank line between tasks

def display_stats(username, password):
    '''shows admin user only the total number of users and tasks'''
    # Check if user is admin
    if username != "admin" or password != "password":
        print("Please log in as admin to continue.")
        return

    # Count number of users
    with open("users.txt", "r", encoding='utf-8') as file:
        num_users = sum(1 for _ in file)

    # Count number of tasks
    with open("tasks.txt", "r", encoding='utf-8') as file:
        num_tasks = sum(1 for _ in file)

    # Display statistics
    print("Statistics:")
    print(f"Number of users: {num_users}")
    print(f"Number of tasks: {num_tasks}")

def generate_reports():
    '''two reports generated: task_overview.txt and user_overview.txt
    While open statements of each file to view what is written '''
    # Total number of tasks
    total_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    # Count tasks from file
    with open("tasks.txt", "r", encoding='utf-8') as file:
        for line in file:
            total_tasks += 1
            task_data = line.strip().split(",")
            if task_data[4] == "complete":
                completed_tasks += 1
            else:
                uncompleted_tasks += 1
                due_date = datetime.strptime(task_data[3], "%Y-%m-%d")
                if due_date < datetime.now():
                    overdue_tasks += 1

    # Calculate percentages
    if total_tasks > 0:
        percentage_overdue = (overdue_tasks / total_tasks) * 100
        percentage_incomplete = (uncompleted_tasks / total_tasks) * 100
    else:
        percentage_overdue = 0
        percentage_incomplete = 0

    # Write to tasks_overview.txt
    with open("tasks_overview.txt", "w", encoding='utf-8') as tasks_file:
        tasks_file.write("Tasks Overview:\n")
        tasks_file.write(f"Total number of tasks: {total_tasks}\n")
        tasks_file.write(f"Total number of complete tasks: {completed_tasks}\n")
        tasks_file.write(f"Total number of incomplete tasks: {uncompleted_tasks}\n")
        tasks_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        tasks_file.write(f"Percentage of incomplete tasks: {percentage_incomplete:.2f}%\n")
        tasks_file.write(f"Percentage of overdue tasks: {percentage_overdue:.2f}%\n")

    # Total number of users
    total_users = 0

    # Count users from file
    with open("users.txt", "r", encoding='utf-8') as file:
        total_users = sum(1 for line in file)

    # Write to user_overview.txt
    with open("user_overview.txt", "w", encoding='utf-8') as user_file:
        user_file.write("User Overview:\n")
        user_file.write(f"Total number of users in the program: {total_users}\n")
        user_file.write(f"Total number of tasks in the program: {total_tasks}\n")
        user_file.write(f"Total number of complete tasks: {completed_tasks}\n")
        user_file.write(f"Total number of incomplete tasks: {uncompleted_tasks}\n")
        user_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        user_file.write(f"Percentage of incomplete tasks: {percentage_incomplete:.2f}%\n")
        user_file.write(f"Percentage of overdue tasks: {percentage_overdue:.2f}%\n")

def login():
    '''While: login details are found in user.txt access is granted to menu'''
    print('Enter Login details to access database')
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Check if user is in the file and password is correct
        with open("users.txt", "r", encoding='utf-8') as file:
            users = file.readlines()
            users = [user.strip().split(",") for user in users]

        found = False
        for user in users:
            if user[0] == username and user[1] == password:
                print("Login successful.")
                found = True
                break

        if found:
            while True:
                print("Select one of the following options below:")
                print("r - Registering a user")
                print("a - Adding a task")
                print("va - View all tasks")
                print("vm - View my tasks")
                print("ds - Display statistics")
                print("gr - generate reports")
                print("e - Exit")

                choice = input("Enter your choice: ")

                if choice == 'r':
                    reg_user()
                elif choice == 'a':
                    add_task()
                elif choice == 'va':
                    view_all()
                elif choice == 'vm':
                    view_mine(username)
                elif choice == 'ds':
                    display_stats(username, password)
                elif choice == 'gr':
                    generate_reports()
                elif choice == 'e':
                    login()
                    return
                else:
                    print("Invalid choice. Please try again.")

        else:
            print("Incorrect login details. Please try again.")

#calls login function to start the program
login()
