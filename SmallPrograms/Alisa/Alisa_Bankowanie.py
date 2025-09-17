import json

saldo = 0
users_file = 'users.json'  # File where user data will be stored

# Function to save users data to JSON
def save_users_data(users):
    with open(users_file, 'w') as f:
        json.dump(users, f)

# Function to load users data from JSON
def load_users_data():
    try:
        with open(users_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Deposit function
def wplata(saldo, username, users):
    kwota_wplata = int(input('Podaj kwote, ktora chcesz wplacic: '))
    if kwota_wplata > 0:
        saldo += kwota_wplata
        print('Pieniadze zostaly wplacone')
        users[username]['saldo'] = saldo  # Update user saldo in the users dictionary
        save_users_data(users)  # Save the updated data to JSON
    else:
        print('Pieniadze nie zostaly wplacone')
    opcje(saldo, username, users)

# Withdrawal function
def wyplata(saldo, username, users):
    kwota_wyplata = int(input('Podaj kwote, ktora chcesz wyplacic: '))
    if (kwota_wyplata <= saldo) and (kwota_wyplata > 0):
        saldo -= kwota_wyplata
        print('Pieniadze zostaly wyplacone')
        users[username]['saldo'] = saldo  # Update user saldo in the users dictionary
        save_users_data(users)  # Save the updated data to JSON
    else:
        print('Pieniadze nie zostaly wyplacone')
    opcje(saldo, username, users)

# Main options function
def opcje(saldo, username, users):
    opcja = input('''Wybierz opcje (3-5):
    3 = wplata
    4 = wyplata
    5 = sprawdzenie salda: ''')

    match opcja:
        case '3':
            wplata(saldo, username, users)
        case '4':
            wyplata(saldo, username, users)
        case '5':
            print(f'Twoje saldo wynosi {saldo}')
            opcje(saldo, username, users)
        case _:
            print('Taka opcja nie istnieje')

# Load or create account
def main():
    users = load_users_data()

    konto = input('Witamy w banku! Jezeli chcesz sie zalogowac, wpisz 2, jezeli nie masz konta, wpisz 1: ')

    match konto:
        case '1':
            imie1 = input('Podaj imie: ')
            login1 = input('Podaj login: ')
            haslo1_1 = input('Podaj haslo: ')
            haslo2_1 = input('Powtorz haslo: ')
            if haslo1_1 == haslo2_1:
                users[login1] = {'imie': imie1, 'haslo': haslo1_1, 'saldo': 0}  # Create new user
                save_users_data(users)  # Save new user to JSON
                print('Konto zostalo utworzone')
            else:
                print('Hasla sie nie zgadzaja')
        case '2':
            login = input('Podaj login: ')
            haslo = input('Podaj haslo: ')

            if login in users and users[login]['haslo'] == haslo:
                saldo = users[login]['saldo']
                print(f'Zostales zalogowany! Witaj {users[login]["imie"]}.')

                etap2 = input('Wybierz 3 jezeli chcesz wplacic, 4 jezeli chcesz wyplacic, 5 jezeli chcesz sprawdzic saldo: ')

                match etap2:
                    case '3':
                        wplata(saldo, login, users)
                    case '4':
                        wyplata(saldo, login, users)
                    case '5':
                        print(f'Twoje saldo wynosi: {saldo}')
                    case _:
                        print('Nieznana opcja')
            else:
                print('Zle dane logowania')
        case _:
            print('Nieznana opcja')

# Run the main function
main()
