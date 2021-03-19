"""Shell test."""

# Local libraries
from cobus import Cobus

menu_options = """
1. Add a passenger.
2. Remove a passenger.
3. Save record state.
4. Clean passengers.
5. Clean record states.
6. Print local data.
7. Sync with server.
8. Sync with server on reverse.
100. Exitr
>>> """

cobus = Cobus(key_path='./firebasekey.json', unit_name='test', max_passengers=5, clean_at_startup=True)

while True:
    selector = input(menu_options)
    if selector == '100':
        print('[EXIT] Bye')
        break
    elif selector in ('1', '2'):
        if selector == '1':
            cobus.add_passenger()
        elif selector == '2':
            cobus.remove_passenger()
    elif selector == '3':
        cobus.push_record_state()
    elif selector == '4':
        cobus.clean_number_of_passengers()
    elif selector == '5':
        cobus.clean_record_states()
    elif selector == '6':
        print(cobus)
    elif selector == '7':
        cobus.sync_with_server()
    elif selector == '8':
        cobus.sync_with_server(reverse=True)
    else:
        print('[ERROR] Option not available.')
