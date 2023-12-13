def createaccount():
    username = input("enter a new username: ")
    password = input("enter a password: ")
    score = 0  

    with open('data.dat', 'a') as file:
        file.write(f"{username},{password},{score}\n")

    print("account created successfully!")

def login():
    username = input("enter your username: ")
    password = input("enter your password: ")

    with open('data.dat', 'r') as file:
        for line in file:
            storedusername, storedpassword, score = line.strip().split(',')
            if username == storedusername:
                if password == storedpassword:
                    print(f"login successful. welcome {username}. your highest score is {score}")
                    import turtle as trtl
                    import random
                    trtl.mainloop()
                    return
                else:
                    print("incorrect password.")
                    return

    print("username not found. do you wanna create a new account? (y / n)")
    choice = input().lower()

    if choice == 'y':
        createaccount()
    else:
        print("Login canceled.")

if __name__ == "__main__":
    login()

