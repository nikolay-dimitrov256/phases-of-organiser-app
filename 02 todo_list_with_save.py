import os


def enter_new_task(todo_list: list) -> list:
    while True:
        print('Please enter the new task, or empty field to exit:')
        new_task = input()

        if new_task == '':
            return todo_list

        todo_list.append(new_task)


def list_all_tasks(todo_list):
    for i in range(len(todo_list)):
        counter = i + 1
        print(f'[{counter}] - {todo_list[i]}')


def delete_task(todo_list: list) -> list:
    print('Please enter the number of the task to delete:')
    task_number = input()

    if task_number.isdigit():
        task_number = int(task_number)
        index = task_number - 1

        if index in range(len(todo_list)):
            todo_list.pop(index)
        else:
            print('Please enter a valid number.')

    else:
        print('Please enter a number.')

    return todo_list


def load_save_file() -> list:
    todo_list = []
    if not os.path.exists('todo.txt'):
        open('todo.txt', 'x', encoding='utf-8')
    else:
        file = open('todo.txt', 'r', encoding='utf-8')
        data = file.read()
        todo_list = data.split('|')

    return todo_list


def save_data(todo_list: list):
    savefile = open('todo.txt', 'w', encoding='utf-8')
    savefile.write('|'.join(todo_list))
    savefile.close()


def base_function():
    todo_list = load_save_file()

    while True:
        print('Enter [e] to enter a new task, [l] to list all tasks, [d] to delete a task, or [s] to save and exit:')
        command = input()

        if command.lower() == 'e':
            todo_list = enter_new_task(todo_list)

        elif command.lower() == 'l':
            list_all_tasks(todo_list)

        elif command.lower() == 'd':
            todo_list = delete_task(todo_list)

        elif command.lower() == 's':
            save_data(todo_list)
            break


base_function()
