from cobusdb.cobus import Cobus


def main():
    # TO DO
    cobus = Cobus(key_path='./firebasekey.json', unit_name='unit_a', max_passengers=20, clean_at_startup=True)


if __name__ == '__main__':
    main()
