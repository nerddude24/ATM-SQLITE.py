from account import Account
import json
import os
import sqlite3

accounts = {}
data_path = "accounts.db"
active_account = None

con = sqlite3.connect(data_path)
c = con.cursor()


def check_for_accounts():
    global accounts
    try:
        c.execute(
            """CREATE TABLE IF NOT EXISTS accounts(
            name TEXT,
            password TEXT,
            credit INTEGER
        );"""
        )
        con.commit()
        c.execute("SELECT * FROM accounts")
        accs = c.fetchall()
        con.commit()
        for i, account in enumerate(accs):
            accounts[str(i)] = {
                "name": account[0],
                "password": account[1],
                "credit": account[2],
            }
    except:
        print("ERROR")


def login():
    global active_account
    if len(accounts) <= 0:
        print("NO ACCOUNTS FOUND, PLEASE CREATE ONE.")
        main()
        return
    acc = Account("", "", 0)
    acc.name = input("Enter your name\n>").strip()
    acc.password = input("Enter your password\n>").strip()

    users = [accounts[str(x)] for x in range(0, len(accounts))]
    for i, user in enumerate(users):
        if user == {
            "name": acc.name,
            "password": acc.password,
            "credit": user["credit"],
        }:
            acc.credit = user["credit"]
            acc.index = i
            active_account = acc
            print("You have succesfully logged in!")
            main()
            return

    print("Wrong password or username, try again\n\n\n")
    login()


def signup():
    global accounts
    acc = Account("", "", 0)
    while True:
        name = input("Please enter your name\n>").strip()
        if name == "":
            print("Name can't be empty...")
            continue
        for i in range(0, len(accounts)):
            if name == accounts[str(i)]["name"]:
                print(f"ACCOUNT WITH NAME: '{name}' ALREADY EXISTS")
                main()
                return
        acc.name = name
        break
    while True:
        password = input("Please enter your password\n>").strip()
        password_confirm = input("Please confirm your password again\n>").strip()
        if password == password_confirm:
            if password == "":
                print("ERR PASSWORD EMPTY\n\n\n")
                continue
            acc.password = password
            break
        else:
            print("ERR PASSWORD INCORRECT\n\n\n")

    while True:
        credit = input("How much money do you want to deposit?\n>")
        if credit.isnumeric():
            acc.credit = int(credit)
            break
        else:
            print("error credit is a number idiot.")

    if not str(len(accounts)) in accounts:
        accounts[str(len(accounts))] = {
            "name": acc.name,
            "password": acc.password,
            "credit": acc.credit,
        }
    else:
        accounts[str(len(accounts) + 1)] = {
            "name": acc.name,
            "password": acc.password,
            "credit": acc.credit,
        }
    save_data_to_file()
    main()


def save_data_to_file():
    c.execute("DELETE FROM accounts;")
    con.commit()
    c.execute("VACUUM;")
    con.commit()
    for i in range(0, len(accounts)):
        c.execute(
            "INSERT INTO accounts VALUES (:name, :password, :credit)",
            {
                "name": accounts[str(i)]["name"],
                "password": accounts[str(i)]["password"],
                "credit": accounts[str(i)]["credit"],
            },
        )
        con.commit()


def get_operation():
    res = input(">").lower().strip()

    if res == "login" or res == "log":
        login()
        return
    elif res == "signup" or res == "sign":
        signup()
        return
    elif res == "users":
        users = [accounts[str(x)] for x in range(0, len(accounts))]
        names = [x["name"] for x in users]
        print(names)
    elif res == "help":
        print(
            """  Commands: 
    >login
    >signup
    >users  shows users saved
    >help   shows this
    >exit   exits the ATM Machine
        """
        )
    elif res == "exit":
        return
    else:
        print("err, please choose either login or signup\n")

    get_operation()


def reorder_accounts(temp, id):
    global accounts
    for x in range(1, len(temp) + 1):
        if x > int(id):
            temp[str(id)] = temp.pop(str(x))
            id = str(x)

    accounts = temp
    save_data_to_file()


def remove_active_account():
    global active_account
    acc_id = active_account.index
    accounts_temp = accounts
    accounts_temp.pop(str(acc_id))
    reorder_accounts(accounts_temp, acc_id)

    active_account = None
    main()


def get_operation_loggedin():
    global active_account
    res = input(">").strip().lower()
    if res == "deposit":
        try:
            amount = abs(int(input("How much do you want to deposit?\n>>>")))
            x = str(int(active_account.credit) + amount)
            active_account.credit = x
            accounts[str(active_account.index)] = {
                "name": active_account.name,
                "password": active_account.password,
                "credit": active_account.credit,
            }
            save_data_to_file()
            print(f"You now have {active_account.credit}$.")
        except:
            print("err, please try again")
    elif res == "withdraw":
        try:
            amount = abs(int(input("How much do you want to withdraw?\n>>>")))
            x = str(int(active_account.credit) - amount)
            active_account.credit = x
            accounts[str(active_account.index)] = {
                "name": active_account.name,
                "password": active_account.password,
                "credit": active_account.credit,
            }
            save_data_to_file()
            print(f"You now have {active_account.credit}$.")
        except:
            print("err, please try again")
    elif res == "logout":
        active_account = None
    elif res == "del acc":
        ans = input("ARE YOU SURE? (Y/N)\n>").strip().lower()
        if ans == "y":
            remove_active_account()
            return
    elif res == "exit":
        return
    else:
        print("unkown command\n")

    main()


def main():
    if active_account == None:
        check_for_accounts()
        print(
            f"[{len(accounts)} Accounts Found], Would you like to login or signup? (login/signup/help)"
        )
        get_operation()
        return
    else:
        print(
            f"You have {active_account.credit}$, What would like to do? (deposit, withdraw, logout,del acc)"
        )
        get_operation_loggedin()
        return


main()
con.close()
