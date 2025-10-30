"""##########################PASSWORD MANAGER.PY############################### """

import os
from getpass import getpass
from utils.user_manager import new_user, check_user
from utils.hash_manager import generate_hash, store_key
from utils.encryptor import encrypt_data
from utils.decryptor import decrypt_cipher
from utils.file_manager import encrypt_file, decrypt_file, show_data_file

#display principal menu and return user's choice 

def clear() ->None:
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_1() -> int:

    print('''
        ##############################################################
#                                                            #
#   #####     ###    #####   #####   #####   #####   #####   #
#   #   #   #   #   #       #       #       #       #   ##   #
#   #####   #####   #####   #####   # ###   #####   #####    #
#   #       #   #       #       #   #   #   #       #   #    # 
#   #       #   #   #####   #####   #####   #####   #   #    #
#                                                            #
#                         By Laurent12-shanks                #
#                                                            #
#####################################################
Options
- - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
1. Register a new user (generate & store master password)
2. Login as existing user
3. Exit Program
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ''')

    while True:
        try:
            choice = int(input("Enter your choice(1-3): "))
            if choice in (1, 2, 3):
                actions = {1: "REGISTER NEW USER", 2: "LOGIN EXISTING USER", 3: "EXIT PROGRAM"}
                print(f" You selected: {actions[choice]}")
                return choice
            else:
                print("Please choose between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number (1-3).")


#memu function when user chooses the authentificate option(2)
def menu_2():
    print('''
    Options
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1. Crypt some passwords
2. Display my data
3. Decrypt my password
4. exit
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ''')

    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
            if choice in (1, 2, 3, 4):
                actions = {1: "ENCRYPT NEW PASSWORD", 2: "DISPLAY DATA", 3: "DECRYPT PASSWORD", 4: "EXIT SESSION"}
                print(f"You selected: {actions[choice]}")
                return choice
            else:
                print("Please choose between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number (1-4).")


def main() -> None:
    clear()
    choice_1 = menu_1()

    if choice_1 == 1:
        username, password = new_user()
        stored_hash = generate_hash( password)
        store_key(username, stored_hash)

    elif choice_1 == 2:  #Authentification
        username = input("your name is : ").strip()
        password = getpass(prompt="Your password ").strip()

        if check_user(username, password):  #check sucessed
            while True:
                choice = menu_2()

                if choice == 1:      #crypt
                    encrypt_data(username, password)
                    encrypt_file(username, password)
                    
                elif choice == 2:    #displaying
                    if decrypt_file(username, password):
                        show_data_file(username)
                    else:
                        print("No data stored yet")
                    encrypt_file(username, password)

                elif choice == 3:    #decrypt
                    if decrypt_file(username, password):
                        pwd_decrypted = decrypt_cipher(username, password)
                        if pwd_decrypted:
                            print(pwd_decrypted, "is copied to clipboard")
                        else:
                            print("Password is none or no service recorded ")
                        encrypt_file(username, password)
                    else:
                        print("No data stored")

                elif choice == 4:
                    print("Logged out.")
                    break

                else:
                    print("Logged out.")

        else:  #check failed
            print("Authentication failed. Please try again.")

    elif choice_1 == 3:
        print("Goodbye!")

    else:
        print("Goodbye!")


if __name__ == '__main__':
    main()
