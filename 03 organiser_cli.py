import os
import re
import datetime


class Organiser:

    def __init__(self):
        self.todo_list, self.appointments, self.daily_done_tasks = self.load_save_file()

    def load_save_file(self):
        todo_list = []
        appointments = {}
        daily_done_tasks = []

        if os.path.exists('organiser.txt'):
            file = open('organiser.txt', 'r', encoding='utf-8')
            data = file.read()
            if data:
                date, data = data.split('#')
                todo_list, appointments_data, daily_done_tasks = data.split('&')

                if todo_list:
                    todo_list = todo_list.split('|')

                if appointments_data:
                    appointments_data = appointments_data.split('|')
                    for i in range(0, len(appointments_data), 3):
                        appointment = appointments_data[i]
                        term = appointments_data[i+1]
                        user_term = appointments_data[i+2]
                        appointments[appointment] = {'term': term, 'user_term': user_term}

                if daily_done_tasks:
                    daily_done_tasks = daily_done_tasks.split('|')
                    new_day = self.check_for_new_day(date)
                    if new_day:
                        daily_done_tasks.clear()

        else:
            open('organiser.txt', 'x', encoding='utf-8')

        return todo_list, appointments, daily_done_tasks

    def save_data(self):
        current_time = self.get_current_time()
        appointments_list = []
        for appointment, data in self.appointments.items():
            appointments_data = f'{appointment}|{data["term"]}|{data["user_term"]}'
            appointments_list.append(appointments_data)
        data = f'{"|".join(self.todo_list)}&{"|".join(appointments_list)}&{"|".join(self.daily_done_tasks)}'
        data_to_write = f'{current_time}#{data}'
        save_file = open('organiser.txt', 'w', encoding='utf-8')
        save_file.write(data_to_write)
        save_file.close()

    def get_current_time(self):
        current_time = str(datetime.datetime.now())[:16]

        return current_time

    def check_for_new_day(self, last_recorded_time: str) -> bool:
        current_time = self.get_current_time()
        current_day = current_time[:10]
        last_recorded_day = last_recorded_time[:10]

        if current_day == last_recorded_day:
            return False
        return True

    def check_for_passed_appointments(self):
        current_time = self.get_current_time()
        passed_appointments = []

        for appointment, data in self.appointments.items():
            term = data['term']
            user_term = data['user_term']

            if current_time > term:
                passed_appointments.append(appointment)

                print(f'You had an appointment "{appointment}" for {user_term}. Did you meet it? [y/n]')
                answer = input()
                if answer.lower() == 'y':
                    self.daily_done_tasks.append(appointment)

        for item in passed_appointments:
            self.appointments.pop(item)

    def enter_task(self, tasks: list):
        while True:
            print('Please enter the new task, or [b] to go back:')
            command = input()

            if command == 'b':
                return tasks

            tasks.append(command)

    def list_tasks(self, tasks: list):
        if tasks:
            for i in range(len(tasks)):
                counter = i + 1
                print(f'[{counter}] - {tasks[i]}')
        else:
            print('Nothing for now.')

    def todo_delete_task(self):
        while True:
            print('Please enter task number, or [b] to go back:')
            number = input()

            if number == 'b':
                break

            elif number.isdigit():
                number = int(number)
                index = number - 1

                if index in range(len(self.todo_list)):
                    answer = input('Did you complete the task? [y]/[n]: ')
                    if answer.lower() == 'y':
                        self.daily_done_tasks.append(self.todo_list.pop(index))
                    else:
                        self.todo_list.pop(index)
                else:
                    print('Please enter a valid number.')

            else:
                print('Please enter a valid command.')

    def validate_term(self, term):
        pattern = r'([\d]{2})-([\d]{2})-([\d]{4})\s([\d]{2}):([\d]{2})'
        match = re.search(pattern, term)

        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            hour = match.group(4)
            minute = match.group(5)
            result = f'{year}-{month}-{day} {hour}:{minute}'

            return result

    def schedule_appointment(self):

        while True:
            flag = False
            appointment = input('Enter the appointment, or [b] to go back: ')
            if appointment.lower() == 'b':
                break
            while True:
                user_term = input('Enter term in the format [dd-mm-yyyy hh:mm], or [b] to go back: ')
                if user_term.lower() == 'b':
                    flag = True
                    break

                term = self.validate_term(user_term)

                if term is None:
                    print('Please enter term in the right format.')

                else:
                    self.appointments[appointment] = {'term': term, 'user_term': user_term}
                    print(f'Appointment "{appointment}" scheduled for {user_term}.')

                    self.appointments = dict(sorted(self.appointments.items(), key=lambda x: x[1]['term']))
                    flag = True
                    break

            if flag:
                break

    def list_appointments(self):
        if self.appointments:
            counter = 0
            for appointment, data in self.appointments.items():
                counter += 1
                user_term = data['user_term']
                print(f'[{counter}] - {appointment} - {user_term}')

        else:
            print('No appointments for now.')

    def cancel_appointment(self):
        while True:
            number = input('Enter the number of the appointment, or [b] to go back: ')
            if number.lower() == 'b':
                break
            elif number.isdigit():
                number = int(number)

                if number - 1 in range(len(self.appointments)):
                    counter = 0
                    for appointment in self.appointments.keys():
                        counter += 1
                        if number == counter:
                            self.appointments.pop(appointment)
                            print(f'Appointment "{appointment}" canceled.')
                            break

                else:
                    print('Please enter a valid number.')
            else:
                print('Please enter a valid command.')

    def modify_todo(self):
        while True:
            print('Enter [e] to enter a new task, [l] to list all tasks, [d] to delete a task, or [b] to go back:')
            command = input()

            if command.lower() == 'e':
                self.todo_list = self.enter_task(self.todo_list)

            elif command.lower() == 'l':
                self.list_tasks(self.todo_list)

            elif command.lower() == 'd':
                self.todo_delete_task()

            elif command.lower() == 'b':
                break

            else:
                print('Please enter a valid command.')

    def modify_appointments(self):
        while True:
            print('Enter [e] to enter an appointment, [l] to list all appointments, [c] to cancel an appointment, '
                  'or [b] to go back:')
            command = input()

            if command.lower() == 'e':
                self.schedule_appointment()

            elif command.lower() == 'l':
                self.list_appointments()

            elif command.lower() == 'c':
                self.cancel_appointment()

            elif command.lower() == 'b':
                break
            else:
                print('Please enter a valid command.')

    def modify_done_tasks(self):
        while True:
            print('Enter [r] to report a done task, [l] to list the done tasks for the day, or [b] to go back:')
            command = input()

            if command.lower() == 'r':
                self.daily_done_tasks = self.enter_task(self.daily_done_tasks)

            elif command.lower() == 'l':
                self.list_tasks(self.daily_done_tasks)

            elif command.lower() == 'b':
                break

            else:
                print('Please enter a valid command.')

    def run(self):
        self.check_for_passed_appointments()

        while True:
            print('Enter [td] for to do list, [ap] for with appointments, [dt] for done tasks, or '
                  '[s] to save and exit:')
            command = input()

            if command.lower() == 'td':
                self.modify_todo()

            elif command.lower() == 'ap':
                self.modify_appointments()

            elif command.lower() == 'dt':
                self.modify_done_tasks()

            elif command.lower() == 's':
                self.save_data()
                break
            else:
                print('Please enter a valid command.')


organiser = Organiser()
organiser.run()
