import os
import datetime
from plyer import notification
import time


class Notifier:

    def __init__(self):
        self.appointments_for_the_day = self.load_data()
        self.first_notification = False

    def load_data(self):
        appointments_for_the_day = {}

        if os.path.exists('organiser.txt'):
            file = open('organiser.txt', 'r', encoding='utf-8')
            data = file.read()
            if data:
                date, data = data.split('#')
                data = data.split('&')
                appointments_data = data[1]

                if appointments_data:
                    appointments_data = appointments_data.split('|')
                    for i in range(0, len(appointments_data), 3):
                        appointment = appointments_data[i]
                        term = appointments_data[i+1]
                        user_term = appointments_data[i+2]

                        if self.check_for_current_day(term):
                            appointments_for_the_day[appointment] = \
                                {'term': term, 'user_term': user_term}

        return appointments_for_the_day

    def get_current_time(self):
        current_time = str(datetime.datetime.now())[:16]

        return current_time

    def check_for_current_day(self, term: str) -> bool:
        current_time = self.get_current_time()
        current_day = current_time[:10]
        term_date = term[:10]

        if current_day == term_date:
            return True

        return False

    def initial_notification(self):
        current_time = self.get_current_time()
        for appointment, data in self.appointments_for_the_day.items():
            term = data['term']

            if current_time > term:
                continue

            user_term = data['user_term']
            current_message = f'{appointment} at {user_term[11:]}'

            notification.notify(
                title='You have appointment today.',
                message=current_message
            )

        self.first_notification = True

    def delete_appointment(self, appointment):
        del self.appointments_for_the_day[appointment]

    def run(self):
        if not self.first_notification:
            self.initial_notification()

        for appointment, data in self.appointments_for_the_day.items():

            current_time = datetime.datetime.now()
            current_hour = current_time.hour
            current_minute = current_time.minute
            current_time_in_minutes = current_hour * 60 + current_minute

            term = self.appointments_for_the_day[appointment]['term']
            term_hour = int(term[11:13])
            term_minute = int(term[14:16])
            term_time_in_minutes = term_hour * 60 + term_minute

            notification_time_in_minutes = term_time_in_minutes - 60

            if current_time_in_minutes > term_time_in_minutes:  # The moment has passed
                continue

            if notification_time_in_minutes < 0:  # Unlikely we'll have an appointment in the night
                continue

            sleep_time_in_minutes = notification_time_in_minutes - current_time_in_minutes
            sleep_time_in_minutes = sleep_time_in_minutes if sleep_time_in_minutes >= 0 else 0

            time.sleep(sleep_time_in_minutes * 60)

            user_term = self.appointments_for_the_day[appointment]['user_term']
            current_message = f'{appointment} at {user_term[11:]}'

            notification.notify(
                title='You have an upcoming appointment',
                message=current_message
            )


        # while self.appointments_for_the_day:
        #     flag = False
        #
        #     for appointment, data in self.appointments_for_the_day.items():
        #         current_time = self.get_current_time()
        #         target_time = data['term']
        #
        #         if current_time > target_time:
        #             self.delete_appointment(appointment)
        #             break
        #
        #         user_term = data['user_term']
        #         notification_hour = int(target_time[11:13]) - 1
        #         notification_time = f'{target_time[:11]}{notification_hour}{target_time[13:]}'
        #
        #         while True:
        #             current_time = self.get_current_time()
        #             if current_time >= notification_time:
        #                 current_message = f'{appointment} at {user_term[11:]}'
        #                 notification.notify(
        #                     title='You have an upcoming appointment',
        #                     message=current_message
        #                 )
        #                 self.delete_appointment(appointment)
        #                 flag = True
        #                 break
        #
        #             time.sleep(5*60)
        #
        #     if flag:
        #         break


notifier = Notifier()
notifier.run()
