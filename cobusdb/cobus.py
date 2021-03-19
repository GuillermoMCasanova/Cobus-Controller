"""Cobus controler."""

# Firebase admin
import firebase_admin
from firebase_admin import db

# Standard library
from datetime import datetime
import os


class Cobus:
    """
    Cobus.

    Provide a class for a control of number of passengers in public transport.
    Don't initialize more than one instance of this class with the same unit_name, it
    could genereate inconsistences at database.
    """

    def __init__(self, key_path, unit_name, max_passengers, clean_at_startup=False):
        """
        __init__.

        Initialize the instance.
        unit_name must be unique.
        max_passengers is the maximum number of passengers allowed in bus.
        clean_at_startup is dangerous, if it is True, delete the previus data about this unity.
        """
        # Credential validation
        self.credential = firebase_admin.credentials.Certificate('./firebasekey.json')
        # App initialize
        self.app = firebase_admin.initialize_app(
            credential=self.credential,
            options={
                'databaseURL': 'https://cobus-e38dc-default-rtdb.firebaseio.com/'
            })
        # Collections reference
        self.current_state_db = firebase_admin.db.reference('/{}/current_state'.format(unit_name))
        self.record_states_db = firebase_admin.db.reference('/{}/record_states'.format(unit_name))
        # Attributes
        self.unit_name = unit_name
        self.max_passengers = max_passengers
        if clean_at_startup:
            # Init data with zeros and empty values
            self.clean_number_of_passengers()
            self.clean_record_states()
        else:
            # Get initial data from server
            self.sync_with_server()

    def update_number_of_passengers(self, action, number=1, on_server=True):
        """
        update_number_of_passengers.

        add and substract values from number of passengers. If on_server is True
        the changes will be reflected at database, else the changes only storaged
        locally. If the number of passengers is greater than max limit allowed then
        raise a sound alert.
        """

        if action == 'add':
            self.number_of_passengers += number
        elif action == 'remove':
            if number > self.number_of_passengers:
                print('[WARNING] Could not save negative number of passengers. Saving 0 instead.')
                self.alert(frequency=500, duration=1, repetitions=1)
            self.number_of_passengers = max(self.number_of_passengers-number, 0)

        self.check_state()

        if on_server:
            try:
                self.current_state_db.set({
                    'number_of_passengers': self.number_of_passengers
                })
                print('[SUCCESS] Number of passengers modified on server.')
                return True
            except Exception:
                print('[ERROR] could not perform this action..')
                return False
        else:
            print('[SUCCESS] Number of passengers modified locally.')
            return True

    def add_passenger(self, on_server=True):
        """
        add_passenger.

        Add 1 to number of passengers. If on_server is True the changes will be reflected
        at database, else the changes only storaged
        locally.
        """

        return self.update_number_of_passengers(action='add', on_server=on_server)

    def remove_passenger(self, on_server=True):
        """
        remove_passenger.

        Remove 1 to number of passengers. If on_server is True the changes will be reflected
        at database, else the changes only storaged locally.
        """

        return self.update_number_of_passengers(action='remove', on_server=on_server)

    def push_record_state(self, on_server=True):
        """
        push_record_state.

        Save a time point on record of states with the current state. If on_server is True the changes
        will be reflected at database, else the changes only storaged locally. If the number of passengers
        is greater than max limit allowed then raise a sound alert.
        """

        state = {
            'datetime': str(datetime.now()),
            'number_of_passengers': self.number_of_passengers
        }
        self.record_states.insert(0, state)

        if len(self.record_states) > 100:
            self.record_states.pop()

        if on_server:
            try:
                self.record_states_db.push(state)
                print('[SUCCESS] Record state saved on server.')
                return True
            except Exception:
                print('[ERROR] Could not perform this action.')
                return False
        else:
            print('[SUCCESS] Record state saved locally.')

    def clean_number_of_passengers(self):
        """
        clean_number_of_passengers.

        Set number_of_passengers to zero in current state locally and at database.
        """

        self.number_of_passengers = 0
        try:
            self.current_state_db.set({
                'number_of_passengers': 0
            })
            return True
        except Exception:
            print('[ERROR] Could not perform this action.')
            return False

    def clean_record_states(self):
        """
        clean_record_states.

        Delete all state recordos locally and at database.
        """

        self.record_states = []
        try:
            self.record_states_db.set({})
            self.push_record_state()
            return True
        except Exception:
            print('[ERROR] Could not perform this action.')
            return False

    def sync_with_server(self, reverse=False):
        """
        sync_with_server.

        If reverse is True, get the database data and set this on local storage, else set local
        data at database.
        """

        try:
            if reverse:
                self.number_of_passengers = self.current_state_db.get().get('number_of_passengers', 0)
                self.record_states = list(self.record_states_db.order_by_key().limit_to_first(99).get().values())
                self.check_state()
            else:
                self.current_state_db.set({'number_of_passengers': self.number_of_passengers})
                self.record_states_db.set({})
                for record in self.record_states:
                    self.record_states_db.push(record)
            return True
        except Exception:
            print('[ERROR] Could not perform this action.')
            return False

    def alert(self, frequency, duration, repetitions):
        """
        alert.

        Raise a sound alert (Only on linux).
        """

        for _ in range(repetitions):
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, frequency))

    def check_state(self, raise_alert=True):
        """
        check_state.

        Return True only if number of passengers is less than max passenger allowed, else return False.
        If raise_alert is True and number of passengers is greater than max passenger allowed then emit
        a sound alert.
        """

        state = self.number_of_passengers <= self.max_passengers
        if not state and raise_alert:
            self.alert(frequency=300, duration=0.5, repetitions=2)
        return state

    def __str__(self):
        """
        __str__.

        Return a string expression with data about instance.
        """

        data = 'Number of passengers: {}\nRecord states: {}\n'.format(self.number_of_passengers, self.record_states)
        return data
