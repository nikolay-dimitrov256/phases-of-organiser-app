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


def base_function():
    todo_list = []

    while True:
        print('Enter [e] to enter a new task, [l] to list all tasks, [d] to delete a task, or [q] to quit:')
        command = input()

        if command.lower() == 'e':
            todo_list = enter_new_task(todo_list)

        elif command.lower() == 'l':
            list_all_tasks(todo_list)

        elif command.lower() == 'd':
            todo_list = delete_task(todo_list)

        elif command.lower() == 'q':
            exit()


base_function()
