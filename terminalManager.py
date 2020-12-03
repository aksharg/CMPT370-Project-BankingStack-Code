from register import register
from login import login
import person

def main():
    loop = True
    process = "main"
    current_user = None
    person_path = None
    person_process = "person_main"

    while loop:
        if process == "main":
            print("######## Main ########")
            user_input = input("Enter your command: ")
            if user_input == "login":
                process = "login"
            elif user_input == "register":
                process = "register"
            elif user_input == "help":
                print("login    - Login to existing account")
                print("register - Register a new account")
                print("help     - Displays this list of commands")
                print("exit     - Exit program")
            elif user_input == "exit":
                loop == False
                print("Goodbye")
                break
            else:
                print("Invalid command - For list of commands type: help")
            print()
        elif process == "login":
            print("######## Login ########")
            print("To return to Main type: back")
            username_input = input("Username: ")
            if username_input == "back":
                process = "main"
                print()
                continue
            elif username_input == "exit":
                loop == False
                print("Goodbye")
                break
            password_input = input("Password: ")
            if username_input == "back":
                process = "main"
                print()
                continue
            elif username_input == "exit":
                loop == False
                print("Goodbye")
                break
            success = login(username_input, password_input)
            if success[0]:
                print("Successful login of " + username_input)
                process = "person"
                person_path = success[1]
                current_user = username_input
            else:
                print(success[1])
            print()
        elif process == "register":
            print("######## Register ########")
            print("Please enter your account information.")
            print("To return to Main type: back")
            username_input = input("Username: ")
            if username_input == "back":
                process = "main"
                print()
                continue
            if username_input == "exit":
                loop == False
                print("Goodbye")
                break
            password_input = input("Password: ")
            if username_input == "back":
                process = "main"
                print()
                continue
            elif username_input == "exit":
                loop == False
                print("Goodbye")
                break
            email_input = input("Email: ")
            if username_input == "back":
                process = "main"
                print()
                continue
            elif username_input == "exit":
                loop == False
                print("Goodbye")
                break
            success = register(username_input, password_input, email_input)
            if success[0]:
                print("Successful register of " + username_input)
                process = "main"
            else:
                print(success[1])
            print()
        elif process == "person":
            key = None
            if person_process == "person_main":
                print("######## Account ########")
                user_input = input("Enter your command: ")
                if user_input == "changeUsername":
                    person_process = "changeUsername"
                elif user_input == "changePassword":
                    person_process = "changePassword"
                elif user_input == "changeEmail":
                    person_process = "changeEmail"
                elif user_input == "logout":
                    process = "main"
                    person_process = "person_main"
                    current_user = None
                    print()
                    continue
                elif user_input == "help":
                    print("changeUsername - Change your username")
                    print("changePassword - Change your password")
                    print("changeEmail    - Change your email")
                    print("logout         - Logout of your account")
                    print("help           - Displays this list of commands")
                    print("exit           - Exit program")
                elif user_input == "exit":
                    loop == False
                    print("Goodbye")
                    break
                else:
                    print("Invalid command - For list of commands type: help")
            elif person_process == "changeUsername":
                new_username = input("New username: ")
                if username_input == "logout":
                    process = "main"
                    person_process = "person_main"
                    current_user = None
                    print()
                    continue
                elif username_input == "exit":
                    loop == False
                    print("Goodbye")
                    break
                if key == None:
                    file = open("systemKey.key", "rb")
                    key = file.read()
                    file.close()
                success = person.updateUserCredentialUsername(person_path, new_username, key)
                person.updateUserUsername("users.json", current_user, new_username, key)
                if success[0]:
                    current_user = new_username
                print(success[1])
                person_process = "person_main"
            elif person_process == "changePassword":
                new_password = input("New password: ")
                if username_input == "logout":
                    process = "main"
                    person_process = "person_main"
                    current_user = None
                    print()
                    continue
                elif username_input == "exit":
                    loop == False
                    print("Goodbye")
                    break
                if key == None:
                    file = open("systemKey.key", "rb")
                    key = file.read()
                    file.close()
                success = person.changePswd(person_path, new_password, key)
                print(success[1])
                person_process = "person_main"
            elif person_process == "changeEmail":
                new_email = input("New email: ")
                if username_input == "logout":
                    process = "main"
                    person_process = "person_main"
                    current_user = None
                    print()
                    continue
                elif username_input == "exit":
                    loop == False
                    print("Goodbye")
                    break
                if key == None:
                    file = open("systemKey.key", "rb")
                    key = file.read()
                    file.close()
                success = person.updateEmail(person_path, new_email, key)
                print(success[1])
                person_process = "person_main"
            print()
            
# def checkForCommand(input):
#     if input == "back":
#         process = "main"
#         continue
#     elif username_input == "exit":
#         loop == False
#         print("Goodbye")
#         break

if __name__ == "__main__":
    main()
