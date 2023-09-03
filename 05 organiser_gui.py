import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import Calendar
import os
import datetime


class Organiser:
    def __init__(self):
        self.todo_list, self.appointments, self.daily_done_tasks, self.notes = self.load_save_file()

        self.create_widgets()
        self.place_widgets()

        self.list_items(self.todo_text_field, self.todo_list)
        appointments_as_list = self.format_appointment_to_string()
        self.list_items(self.appointments_textbox, appointments_as_list)
        self.list_items(self.done_text, self.daily_done_tasks)
        self.list_items(self.notes_text_field, [note for note in self.notes.keys()])

    def create_widgets(self):
        self.root = tk.Tk()
        self.root.title('Organiser')

        self.save_button = ttk.Button(self.root, text='Save', command=self.save_data)

        # Creates the widget, containing the tabs, and the tabs
        self.tab_control = ttk.Notebook(self.root)
        self.todo_tab = ttk.Frame(self.tab_control)
        self.appointments_tab = ttk.Frame(self.tab_control)
        self.done_tasks_tab = ttk.Frame(self.tab_control)
        self.notes_tab = ttk.Frame(self.tab_control)

        # Adds the tabs to the tab control widget
        self.tab_control.add(self.todo_tab, text='To do list')
        self.tab_control.add(self.appointments_tab, text='Appointments')
        self.tab_control.add(self.done_tasks_tab, text='Done tasks')
        self.tab_control.add(self.notes_tab, text='Notes')

        # Widgets for the to do list tab:
        self.todo_top_separator = ttk.Separator(self.todo_tab)
        self.todo_enter_label = ttk.Label(self.todo_tab, text='Enter a new task here:', foreground='green')
        self.todo_entry = ttk.Entry(self.todo_tab, width=50)
        self.todo_entry.focus_set()  # Puts the marker in the entry field, so the user can write without clicking it
        self.todo_entry.bind('<Return>', self.todo_new_task)  # Binds the 'Enter' key to the self.todo_new_task method
        self.todo_enter_button = ttk.Button(self.todo_tab, text='Enter', command=self.todo_new_task)
        self.todo_first_separator = ttk.Separator(self.todo_tab, orient='horizontal')
        self.todo_tasks_label = ttk.Label(self.todo_tab, text='Tasks to do:', foreground='green')
        self.todo_text_field = scrolledtext.ScrolledText(self.todo_tab, width=50, height=7)
        self.todo_text_field['state'] = 'disabled'
        self.todo_refresh_button = ttk.Button(self.todo_tab, text='Refresh',
                                              command=lambda: self.list_items(self.todo_text_field, self.todo_list))
        self.todo_second_separator = ttk.Separator(self.todo_tab, orient='horizontal')
        self.todo_remove_label = ttk.Label(self.todo_tab, text='Delete a task:', foreground='green')
        self.completed_check = tk.IntVar()
        self.todo_check_completed = ttk.Checkbutton(self.todo_tab, onvalue=1, offvalue=0, text='Completed',
                                                    variable=self.completed_check)
        self.todo_selected_task = tk.StringVar()
        self.todo_list_box = ttk.Combobox(self.todo_tab, textvariable=self.todo_selected_task, width=50)
        self.todo_list_box['values'] = self.todo_list
        self.todo_list_box['state'] = 'readonly'
        self.todo_delete_button = ttk.Button(self.todo_tab, text='Delete', command=self.todo_delete_task)

        # Widgets for the appointments tab
        self.appointments_first_separator = ttk.Separator(self.appointments_tab)
        self.appointments_label = ttk.Label(self.appointments_tab, text='You have the following appointments:',
                                            foreground='green')
        self.appointments_textbox = scrolledtext.ScrolledText(self.appointments_tab, width=50, height=7)
        self.appointments_textbox['state'] = 'disabled'
        self.appointments_refresh_button = ttk.Button(self.appointments_tab, text='Refresh',
                                                      command=self.refresh_appointments)
        self.appointments_second_separator = ttk.Separator(self.appointments_tab)
        self.appointments_schedule_button = ttk.Button(self.appointments_tab, text='Schedule appointment',
                                                       command=self.schedule_appointment)
        self.appointments_edit_button = ttk.Button(self.appointments_tab, text='Edit appointment',
                                                   command=self.edit_appointment)
        self.appointments_cancel_app_button = ttk.Button(self.appointments_tab, text='Cancel appointment',
                                                         command=self.cancel_appointment)

        # Widgets for the done tasks tab
        self.done_first_separator = ttk.Separator(self.done_tasks_tab)
        self.done_report_task_entry = ttk.Entry(self.done_tasks_tab, width=50)
        self.done_report_task_entry.bind('<Return>', self.report_done_task)
        # self.done_report_task_entry.focus_set()
        self.done_report_task_button = ttk.Button(self.done_tasks_tab, text='Report done task')
        self.done_label = ttk.Label(self.done_tasks_tab, text='Done tasks for the day:', foreground='green')
        self.done_text = scrolledtext.ScrolledText(self.done_tasks_tab, width=50, height=7)
        self.done_text['state'] = 'disabled'
        self.done_refresh_button = ttk.Button(self.done_tasks_tab, text='Refresh',
                                              command=lambda: self.list_items(self.done_text, self.daily_done_tasks))
        self.done_second_separator = ttk.Separator(self.done_tasks_tab)

        # Widgets for the notes tab
        self.notes_first_separator = ttk.Separator(self.notes_tab)
        self.notes_list_label = ttk.Label(self.notes_tab, text='Current notes:', foreground='green')
        self.notes_text_field = scrolledtext.ScrolledText(self.notes_tab, height=7, width=50)
        self.notes_text_field['state'] = 'disabled'
        self.notes_refresh_button = ttk.Button(self.notes_tab, text='Refresh',
                                               command=lambda: self.list_items(self.notes_text_field,
                                                                               [note for note in self.notes.keys()]))
        self.notes_second_separator = ttk.Separator(self.notes_tab)
        self.notes_add_note_button = ttk.Button(self.notes_tab, text='Add note', command=self.add_note)
        self.notes_third_separator = ttk.Separator(self.notes_tab)
        self.notes_select_note_label = ttk.Label(self.notes_tab, text='Select a note:', foreground='green')
        self.notes_selected_note = tk.StringVar()
        self.notes_menu = ttk.Combobox(self.notes_tab, textvariable=self.notes_selected_note, width=50)
        self.notes_menu['values'] = [note for note in self.notes.keys()]
        self.notes_menu['state'] = 'readonly'
        self.notes_view_edit_button = ttk.Button(self.notes_tab, text='View/Edit', command=self.view_edit_note)

    def place_widgets(self):
        self.tab_control.pack(expand=1, fill='both', padx=5)
        self.save_button.pack(pady=10)

        # Widgets for the to do list tab:
        self.todo_top_separator.grid(row=0, columnspan=2, pady=5, sticky='we')
        self.todo_enter_label.grid(row=1, column=0, sticky=tk.W)
        self.todo_entry.grid(row=2, column=0)
        self.todo_enter_button.grid(row=2, column=1, padx=5)
        self.todo_first_separator.grid(row=3, columnspan=2, pady=5, sticky='we')
        self.todo_tasks_label.grid(row=4, column=0, sticky=tk.W)
        self.todo_text_field.grid(row=5, column=0, columnspan=2)
        self.todo_refresh_button.grid(row=6, column=0, pady=5, sticky=tk.W)
        self.todo_second_separator.grid(row=7, columnspan=2, pady=5, sticky='we')
        self.todo_remove_label.grid(row=8, column=0, sticky=tk.W)
        self.todo_check_completed.grid(row=9, column=0, sticky=tk.W)
        self.todo_list_box.grid(row=10, column=0, sticky=tk.W)
        self.todo_delete_button.grid(row=10, column=1, padx=5)

        # Widgets for the appointments tab
        self.appointments_first_separator.grid(row=0, columnspan=3, pady=5, sticky='we')
        self.appointments_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.appointments_textbox.grid(row=2, column=0, columnspan=3)
        self.appointments_refresh_button.grid(row=3, column=0, pady=5, sticky=tk.W)
        self.appointments_second_separator.grid(row=4, columnspan=3, pady=5, sticky='we')
        self.appointments_schedule_button.grid(row=5, column=0, sticky=tk.W)
        self.appointments_edit_button.grid(row=5, column=1, sticky=tk.EW)
        self.appointments_cancel_app_button.grid(row=5, column=2, sticky=tk.E)

        # Widgets for the done tasks tab
        self.done_first_separator.grid(row=0, columnspan=2, pady=5, sticky='we')
        self.done_label.grid(row=3, column=0, sticky=tk.W)
        self.done_text.grid(row=4, columnspan=2)
        self.done_refresh_button.grid(row=5, column=0, pady=5, sticky=tk.W)
        self.done_second_separator.grid(row=2, columnspan=2, pady=5, sticky='we')
        self.done_report_task_entry.grid(row=1, column=0, sticky=tk.W)
        self.done_report_task_button.grid(row=1, column=1, sticky=tk.W)

        # Widgets for the notes tab
        self.notes_first_separator.grid(row=0, columnspan=2, pady=5, sticky='we')
        self.notes_list_label.grid(row=1, column=0, sticky=tk.W)
        self.notes_text_field.grid(row=2, columnspan=2)
        self.notes_refresh_button.grid(row=3, column=0, pady=5, sticky=tk.W)
        self.notes_second_separator.grid(row=4, columnspan=2, pady=5, sticky='we')
        self.notes_add_note_button.grid(row=5, column=0, sticky='w')
        self.notes_third_separator.grid(row=6, columnspan=2, pady=5, sticky='we')
        self.notes_select_note_label.grid(row=7, column=0, sticky=tk.W)
        self.notes_menu.grid(row=8, column=0, sticky=tk.W)
        self.notes_view_edit_button.grid(row=8, column=1)

    def load_save_file(self):
        todo_list = []
        appointments = {}
        daily_done_tasks = []
        notes = {}

        if os.path.exists('organiser.txt'):
            file = open('organiser.txt', 'r', encoding='utf-8')
            data = file.read()
            file.close()
            if data:
                date, data = data.split('#')
                todo_list_data, appointments_data, daily_done_tasks_data, notes_data = data.split('&')

                if todo_list_data:
                    todo_list = todo_list_data.split('|')

                if appointments_data:
                    appointments_data = appointments_data.split('|')
                    for i in range(0, len(appointments_data), 3):
                        appointment = appointments_data[i]
                        term = appointments_data[i + 1]
                        user_term = appointments_data[i + 2]
                        appointments[appointment] = {'term': term, 'user term': user_term}

                if daily_done_tasks_data:
                    daily_done_tasks = daily_done_tasks_data.split('|')
                    new_day = self.check_for_new_day(date)
                    if new_day:
                        daily_done_tasks.clear()

                if notes_data:
                    notes_data = notes_data.split('|')
                    for i in range(0, len(notes_data), 3):
                        title = notes_data[i]
                        content = notes_data[i+1]
                        time_modified = notes_data[i+2]

                        notes[title] = {'content': content, 'time modified': time_modified}

        else:
            open('organiser.txt', 'x', encoding='utf-8')

        return todo_list, appointments, daily_done_tasks, notes

    def save_data(self):
        current_time = self.get_current_time()

        appointments_list = []
        for appointment, data in self.appointments.items():
            appointments_data = f'{appointment}|{data["term"]}|{data["user term"]}'
            appointments_list.append(appointments_data)

        notes_list = []
        for title, data in self.notes.items():
            note_data = f'{title}|{data["content"]}|{data["time modified"]}'
            notes_list.append(note_data)

        data = (f'{"|".join(self.todo_list)}&{"|".join(appointments_list)}&{"|".join(self.daily_done_tasks)}&'
                f'{"|".join(notes_list)}')
        data_to_write = f'{current_time}#{data}'
        save_file = open('organiser.txt', 'w', encoding='utf-8')
        save_file.write(data_to_write)
        save_file.close()

    def get_current_time(self):
        current_time = str(datetime.datetime.now())[:16]
        current_time = current_time.replace('-', '/')

        return current_time

    def check_for_new_day(self, last_recorded_time: str) -> bool:
        current_time = self.get_current_time()
        current_day = current_time[:10]
        last_recorded_day = last_recorded_time[:10]

        if current_day == last_recorded_day:
            return False
        return True

    def list_items(self, text_field: scrolledtext.ScrolledText, data: list):
        text_field['state'] = 'normal'
        text_field.delete('1.0', tk.END)

        row = 1.0

        for item in data:
            text_field.insert(str(row), item + '\n')
            row += 1

        text_field['state'] = 'disabled'

    def todo_new_task(self, event=None):
        '''

        :param event: Optional parameter. It's activated when 'Enter' is pressed to call the method.
        :return: None
        '''
        new_task = self.todo_entry.get()
        if new_task:  # The entry field is not empty
            self.todo_list.append(new_task)
            self.todo_entry.delete(0, tk.END)
            self.list_items(self.todo_text_field, self.todo_list)
            self.todo_list_box['values'] = self.todo_list
            self.todo_entry.focus_set()

    def todo_delete_task(self):
        task_to_delete = self.todo_selected_task.get()

        # If the user didn't select a task, or the task is invalid, exit from the method
        if not task_to_delete or task_to_delete not in self.todo_list:
            return None

        task_completed = self.completed_check.get()

        # Update the to do list and the display widgets with its content
        self.todo_list.remove(task_to_delete)
        self.list_items(self.todo_text_field, self.todo_list)
        self.todo_list_box['values'] = self.todo_list
        self.todo_selected_task.set('')

        if task_completed:
            # Move the task to the daily done tasks and update the display widget
            self.daily_done_tasks.append(task_to_delete)
            self.list_items(self.done_text, self.daily_done_tasks)

    def format_appointment_to_string(self):
        appointments_as_list = []

        for appointment, data in self.appointments.items():
            text = f'{data["user term"]} - {appointment}'
            appointments_as_list.append(text)

        return appointments_as_list

    def refresh_appointments(self):
        appointments_as_list = self.format_appointment_to_string()
        self.list_items(self.appointments_textbox, appointments_as_list)

    def schedule_appointment(self):
        self.schedule_window = tk.Toplevel(self.appointments_tab)
        self.schedule_window.title('Schedule appointment')
        self.schedule_window_first_separator = ttk.Separator(self.schedule_window)
        self.schedule_window_name_label = ttk.Label(self.schedule_window, text='Enter the appointment:',
                                                    foreground='green')
        self.schedule_window_entry = ttk.Entry(self.schedule_window, width=50)
        self.schedule_window_entry.focus_set()
        self.schedule_window_second_separator = ttk.Separator(self.schedule_window)
        self.schedule_window_date_label = ttk.Label(self.schedule_window, text='Pick a date:', foreground='green')
        self.schedule_window_cal = Calendar(self.schedule_window, selectmode='day', date_pattern='yyyy/mm/dd')
        self.schedule_window_third_separator = ttk.Separator(self.schedule_window)
        self.schedule_window_time_label = ttk.Label(self.schedule_window, text='Set time:', foreground='green')
        self.schedule_window_time_picker = TimePicker(self.schedule_window)

        self.schedule_window_first_separator.grid(row=0, columnspan=2, pady=5, sticky='we')
        self.schedule_window_name_label.grid(row=1, column=0, padx=5, sticky=tk.W)
        self.schedule_window_entry.grid(row=2, column=0, padx=5)
        self.schedule_window_second_separator.grid(row=3, columnspan=2, pady=5, sticky='we')
        self.schedule_window_date_label.grid(row=4, column=0)
        self.schedule_window_cal.grid(row=5, column=0)
        self.schedule_window_third_separator.grid(row=6, columnspan=2, pady=5, sticky='we')
        self.schedule_window_time_label.grid(row=7, column=0)
        self.schedule_window_time_picker.widget_frame.grid(row=8, column=0, pady=5)

        self.schedule_window_submit_button = ttk.Button(self.schedule_window, text='Submit',
                                                        command=self.submit_appointment)
        self.schedule_window_submit_button.grid(row=10, column=0)



    def submit_appointment(self):
        appointment = self.schedule_window_entry.get()
        if appointment:  # Te user entered an appointment
            date = self.schedule_window_cal.get_date()
            user_date = f'{date[8:10]}/{date[5:7]}/{date[0:5]}'
            hour = int(self.schedule_window_time_picker.hour_string.get())
            minute = int(self.schedule_window_time_picker.minute_string.get())
            term = f'{date} {hour:02d}:{minute:02d}'
            user_term = f'{user_date} {hour:02d}:{minute:02d}'

            self.appointments[appointment] = {'term': term, 'user term': user_term}
            self.appointments = dict(sorted(self.appointments.items(), key=lambda x: x[1]['term']))
            appointments_as_list = self.format_appointment_to_string()
            self.schedule_window_entry.delete(0, tk.END)
            self.list_items(self.appointments_textbox, appointments_as_list)
            self.schedule_window.withdraw()

    def edit_appointment(self):
        self.edit_appointment_window = tk.Toplevel(self.appointments_tab)
        self.edit_appointment_window.title('Edit appointment')

        self.edit_appointment_window_first_separator = ttk.Separator(self.edit_appointment_window)
        self.edit_appointment_window_chose_label = ttk.Label(self.edit_appointment_window,
                                                             text='Select an appointment:', foreground='green')
        self.edit_appointment_selected = tk.StringVar()
        self.edit_appointment_window_list_box = ttk.Combobox(self.edit_appointment_window,
                                                             textvariable=self.edit_appointment_selected, width=50)
        self.edit_appointment_window_list_box['values'] = [appointment for appointment in self.appointments.keys()]
        self.edit_appointment_window_list_box['state'] = 'readonly'
        self.edit_appointment_window_second_separator = ttk.Separator(self.edit_appointment_window)
        self.edit_appointment_window_date_label = ttk.Label(self.edit_appointment_window, text='Pick a date:',
                                                            foreground='green')
        self.edit_appointment_window_cal = Calendar(self.edit_appointment_window, selectmode='day',
                                                    date_pattern='yyyy/mm/dd')
        self.edit_appointment_window_third_separator = ttk.Separator(self.edit_appointment_window)
        self.edit_appointment_window_time_label = ttk.Label(self.edit_appointment_window, text='Set time:',
                                                            foreground='green')
        self.edit_appointment_window_time_picker = TimePicker(self.edit_appointment_window)
        self.edit_appointment_window_fourth_separator = ttk.Separator(self.edit_appointment_window)
        self.edit_appointment_window_submit_button = ttk.Button(self.edit_appointment_window, text='Submit',
                                                                command=self.submit_edited_appointment)


        self.edit_appointment_window_first_separator.grid(row=0, columnspan=2, pady=5, sticky='we')
        self.edit_appointment_window_chose_label.grid(row=1, column=0, sticky=tk.W)
        self.edit_appointment_window_list_box.grid(row=2, column=0, padx=5)
        self.edit_appointment_window_second_separator.grid(row=3, columnspan=2, pady=5, sticky='we')
        self.edit_appointment_window_date_label.grid(row=4, column=0)
        self.edit_appointment_window_cal.grid(row=5, column=0)
        self.edit_appointment_window_third_separator.grid(row=6, columnspan=2, pady=5, sticky='we')
        self.edit_appointment_window_time_label.grid(row=7, column=0)
        self.edit_appointment_window_time_picker.widget_frame.grid(row=8, column=0)
        self.edit_appointment_window_fourth_separator.grid(row=9, columnspan=2, pady=5, sticky='we')
        self.edit_appointment_window_submit_button.grid(row=10, column=0, pady=5)

    def submit_edited_appointment(self):
        appointment = self.edit_appointment_selected.get()
        if not appointment:
            return None

        date = self.edit_appointment_window_cal.get_date()
        user_date = f'{date[8:10]}/{date[5:7]}/{date[0:5]}'
        hour = int(self.schedule_window_time_picker.hour_string.get())
        minute = int(self.schedule_window_time_picker.minute_string.get())
        term = f'{date} {hour:02d}:{minute:02d}'
        user_term = f'{user_date} {hour:02d}:{minute:02d}'

        self.appointments[appointment] = {'term': term, 'user term': user_term}
        self.appointments = dict(sorted(self.appointments.items(), key=lambda x: x[1]['term']))
        appointments_as_list = self.format_appointment_to_string()
        self.edit_appointment_selected.set('')
        self.list_items(self.appointments_textbox, appointments_as_list)
        self.edit_appointment_window.withdraw()

    def cancel_appointment(self):
        self.cancel_appointment_window = tk.Toplevel(self.appointments_tab)
        self.cancel_appointment_window.title('Cancel appointment')

        self.cancel_appointment_window_first_sep = ttk.Separator(self.cancel_appointment_window)
        self.cancel_appointment_window_label = ttk.Label(self.cancel_appointment_window, text='Select an appointment:',
                                                         foreground='green')
        self.cancel_appointment_selected = tk.StringVar()
        self.cancel_appointment_window_list_box = ttk.Combobox(self.cancel_appointment_window,
                                                               textvariable=self.cancel_appointment_selected, width=50)
        self.cancel_appointment_window_list_box['values'] = [appointment for appointment in self.appointments.keys()]
        self.cancel_appointment_window_list_box['state'] = 'readonly'
        self.cancel_appointment_delete_button = ttk.Button(self.cancel_appointment_window, text='Delete',
                                                           command=self.submit_deleted_appointment)

        self.cancel_appointment_window_first_sep.grid(row=0, column=0, pady=5, sticky='we')
        self.cancel_appointment_window_label.grid(row=1, column=0, sticky=tk.W)
        self.cancel_appointment_window_list_box.grid(row=2, column=0)
        self.cancel_appointment_delete_button.grid(row=3, column=0, pady=5)

    def submit_deleted_appointment(self):
        appointment_to_delete = self.cancel_appointment_selected.get()
        if not appointment_to_delete:
            return None

        del self.appointments[appointment_to_delete]
        self.appointments = dict(sorted(self.appointments.items(), key=lambda x: x[1]['term']))
        appointments_as_list = self.format_appointment_to_string()
        self.cancel_appointment_selected.set('')
        self.list_items(self.appointments_textbox, appointments_as_list)
        self.cancel_appointment_window.withdraw()

    def report_done_task(self, event=None):
        task = self.done_report_task_entry.get()
        if not task:  # The entry field is empty
            return None

        self.daily_done_tasks.append(task)
        self.list_items(self.done_text, self.daily_done_tasks)
        self.done_report_task_entry.delete(0, tk.END)
        self.done_report_task_entry.focus_set()

    def add_note(self):
        self.add_note_window = tk.Toplevel(self.notes_tab)
        self.add_note_window.title('Add note')

        self.add_note_window_first_sep = ttk.Separator(self.add_note_window)
        self.add_note_window_title_label = ttk.Label(self.add_note_window, text='Title:', foreground='green')
        self.add_note_window_entry = ttk.Entry(self.add_note_window, width=50)
        self.add_note_window_entry.focus_set()
        self.add_note_window_second_sep = ttk.Separator(self.add_note_window)
        self.add_note_window_content_label = ttk.Label(self.add_note_window, text='Content:', foreground='green')
        self.add_note_window_text = scrolledtext.ScrolledText(self.add_note_window, height=10, width=50)
        self.add_note_window_third_sep = ttk.Separator(self.add_note_window)
        self.add_note_window_submit_button = ttk.Button(self.add_note_window, text='Submit',
                                                        command=self.submit_new_note)

        self.add_note_window_first_sep.grid(row=0, column=0, pady=5, sticky='we')
        self.add_note_window_title_label.grid(row=1, column=0, padx=5,sticky=tk.W)
        self.add_note_window_entry.grid(row=2, column=0, padx=5, sticky='w')
        self.add_note_window_second_sep.grid(row=3, column=0, pady=5, sticky='we')
        self.add_note_window_content_label.grid(row=4, column=0, padx=5,sticky='w')
        self.add_note_window_text.grid(row=5, column=0, padx=5)
        self.add_note_window_third_sep.grid(row=6, column=0, pady=5, sticky='we')
        self.add_note_window_submit_button.grid(row=7, column=0)

    def submit_new_note(self):
        title = self.add_note_window_entry.get()
        if not title or title in self.notes.keys():
            return None

        content = self.add_note_window_text.get('1.0', tk.END)
        time_modified = self.get_current_time()

        self.notes[title] = {'content': content, 'time modified': time_modified}
        self.notes = dict(sorted(self.notes.items(), key=lambda x: x[1]['time modified'], reverse=True))
        self.list_items(self.notes_text_field, [note for note in self.notes.keys()])
        self.notes_menu['values'] = [note for note in self.notes.keys()]
        self.add_note_window_entry.delete(0, tk.END)
        self.add_note_window_text.delete('1.0', tk.END)
        self.add_note_window.withdraw()

    def view_edit_note(self):
        title = self.notes_selected_note.get()
        if not title:
            return None

        content = self.notes[title]['content']

        self.view_note_window = tk.Toplevel(self.notes_tab)
        self.view_note_window.title('View or edit note')
        self.view_note_window_first_sep = ttk.Separator(self.view_note_window)
        self.view_note_window_title_label = ttk.Label(self.view_note_window, text='Title:', foreground='green')
        self.view_note_window_entry = ttk.Entry(self.view_note_window, width=50)
        self.view_note_window_entry.insert(0, title)
        self.view_note_window_entry['state'] = 'disabled'
        self.view_note_window_second_sep = ttk.Separator(self.view_note_window)
        self.view_note_window_text = scrolledtext.ScrolledText(self.view_note_window, height=10, width=50)
        self.view_note_window_text.insert('1.0', content)
        self.view_note_window_third_sep = ttk.Separator(self.view_note_window)
        self.view_note_window_edit_button = ttk.Button(self.view_note_window, text='Edit',
                                                       command=lambda: self.edit_note(title))
        self.view_note_window_delete_button = ttk.Button(self.view_note_window, text='Delete',
                                                         command=lambda: self.delete_note(title))

        self.view_note_window_first_sep.grid(row=0, columnspan=2, pady=5, sticky='we')
        self.view_note_window_title_label.grid(row=1, column=0, padx=5,sticky='w')
        self.view_note_window_entry.grid(row=2, column=0, padx=5,sticky='w')
        self.view_note_window_second_sep.grid(row=3, columnspan=2, pady=5,sticky='we')
        self.view_note_window_text.grid(row=4, columnspan=2, padx=5)
        self.view_note_window_third_sep.grid(row=5, columnspan=2, pady=5, sticky='we')
        self.view_note_window_delete_button.grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.view_note_window_edit_button.grid(row=6, column=1, padx=5, pady=5, sticky='e')

    def edit_note(self, title: str):
        content = self.view_note_window_text.get('1.0', tk.END)
        time_modified = self.get_current_time()
        self.notes[title]['content'] = content
        self.notes[title]['time modified'] = time_modified
        self.notes = dict(sorted(self.notes.items(), key=lambda x: x[1]['time modified']))
        self.list_items(self.notes_text_field, [note for note in self.notes.keys()])
        self.view_note_window.withdraw()

    def delete_note(self, title: str):
        del self.notes[title]
        notes_list = [note for note in self.notes.keys()]
        self.list_items(self.notes_text_field, notes_list)
        self.notes_selected_note.set('')
        self.notes_menu['values'] = notes_list
        self.view_note_window.withdraw()

    def display_test(self):
        hour = int(self.schedule_window_time_picker.hour_string.get())
        minute = int(self.schedule_window_time_picker.minute_string.get())
        date = self.schedule_window_cal.get_date()
        print(date)
        print(type(date))
        print(f'Hour: {hour:02d}')
        print(type(self.schedule_window_time_picker.hour_string.get()))
        print(f'Minute: {minute:02d}')
        print(type(self.schedule_window_time_picker.minute_string.get()))

    def run(self):
        self.root.mainloop()


class TimePicker:
    def __init__(self, parent):
        self.parent = parent
        self.widget_frame = ttk.Frame(self.parent)
        self.hour_string = tk.StringVar()
        self.hour_string.set('0')
        self.minute_string = tk.StringVar()
        self.minute_string.set('0')
        self.hour_label = ttk.Label(self.widget_frame, text='Hour:')
        self.minute_label = ttk.Label(self.widget_frame, text='Minute:')
        self.font = 'Arial', 18
        self.hour_spin = ttk.Spinbox(self.widget_frame, from_=0, to=23, wrap=True, textvariable=self.hour_string,
                                     font=self.font, width=2, state='readonly')
        self.minute_spin = ttk.Spinbox(self.widget_frame, from_=0, to=59, wrap=True, textvariable=self.minute_string,
                                       font=self.font, width=2, state='readonly')

        self.hour_label.grid(row=0, column=0, padx=2, sticky=tk.W)
        self.minute_label.grid(row=0, column=1, padx=2, sticky=tk.W)
        self.hour_spin.grid(row=1, column=0, padx=5)
        self.minute_spin.grid(row=1, column=1, padx=5)


organiser = Organiser()
organiser.run()
