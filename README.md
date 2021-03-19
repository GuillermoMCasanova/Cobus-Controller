# Cobus controller
Provide a class for a control of number of passengers in public transport. Don't initialize more than one instance of this class with the same unit_name, it could genereate inconsistences at database.

# System requirements

    sudo apt install sox 

# Cobus class

## __init\__(self, unit_name, max_passengers, clean_at_startup=False)
Initialize the instance.
- unit_name must be unique.
- max_passengers is the maximum number of passengers allowed in bus.
- clean_at_startup is dangerous, if it is True, delete the previus data about this unity.

## __str\__(self)
Return a string expression with data about instance.

## update_number_of_passengers(self, action, number=1, on_server=True)
add and substract values from number of passengers. If on_server is True the changes will be reflected at database, else the changes only storaged locally. If the number of passengers is greater than max limit allowed then raise a sound alert.

## add_passenger(self, on_server=True)
Add 1 to number of passengers. If on_server is True the changes will be reflected at database, else the changes only storaged locally.

## remove_passenger(self, on_server=True)
Remove 1 to number of passengers. If on_server is True the changes will be reflected at database, else the changes only storaged locally.

## push_record_state(self, on_server=True)
Save a time point on record of states with the current state. If on_server is True the changes will be reflected at database, else the changes only storaged locally. If the number of passengers is greater than max limit allowed then raise a sound alert.

## clean_number_of_passengers(self)
Set number_of_passengers to zero in current state locally and at database.

## clean_record_states(self)
Delete all state recordos locally and at database.

## sync_with_server(self, reverse=False)
If reverse is True, get the database data and set this on local storage, else set local data at database.

## alert(self, frequency, duration, repetitions)
Raise a sound alert (Only on linux).

## check_state(self, raise_alert=True)
Return True only if number of passengers is less than max passenger allowed, else return False. If raise_alert is True and number of passengers is greater than max passenger allowed then emit a sound alert.