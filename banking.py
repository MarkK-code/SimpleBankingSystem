import sqlite3
import random
import math

conn = sqlite3.connect('card.s3db')
cursor = conn.cursor()
command1 = """CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)"""
cursor.execute(command1)
conn.commit()


def luhn_fifteen(number):
    lund_num = 0
    for n in range(15):
        if n % 2 == 0:
            num = int(number[n]) * 2
            if num > 9:
                lund_num += (num - 9)
            else:
                lund_num += num
        else:
            lund_num += int(number[n])
    return lund_num


def luhn_number():
    l_num = str(4000000000000000 + random.randint(0, 9999999999))
    lund = luhn_fifteen(l_num)
    if lund % 10 == 0:
        client_num = l_num[0:15] + "0"
    else:
        lundup = int(math.ceil(lund / 10.0)) * 10
        last_num = lundup - lund
        client_num = l_num[0:15] + str(last_num)
    return client_num


def luhn_check(card_number):
    validity = False
    if len(card_number) < 16:
        print("Probably you made a mistake in the card number. Please try again!")
    else:
        lund = luhn_fifteen(card_number)
        if lund % 10 == 0:
            if card_number[15] == "0":
                validity = True
        else:
            l_validity = lund + int(card_number[15])
            if l_validity % 10 == 0:
                validity = True
    if validity == False:
        print("Probably you made a mistake in the card number. Please try again!")
    return validity


def create_account():
    print("\nYour card has been created")
    print("Your card number:")
    client_num = luhn_number()
    print(client_num)
    cursor.execute("INSERT INTO card(id, number) VALUES (?, ?);", [id, str(client_num)])
    conn.commit()
    print("Your card PIN:")
    client_pin = random.randrange(1000, 9999, 4)
    print(str(client_pin) + "\n")
    cursor.execute("UPDATE card SET pin = ? WHERE id = ?", [str(client_pin), id])
    conn.commit()


def adding_income(card_number):
    income = int(input("Enter income:\n"))
    balance = cursor.execute("SELECT balance FROM card WHERE number=?", [card_number]).fetchall()
    total_balace = income + int(balance[0][0])
    cursor.execute("UPDATE card SET balance = ? WHERE number = ?", [total_balace, card_number])
    conn.commit()
    print("Income was added!")


def succesful_transfering(transfer_card, my_card):
    money_transfer = int(input("Enter how much money you want to transfer:\n"))
    my_balance = cursor.execute("SELECT balance FROM card WHERE number=?", [my_card]).fetchall()
    conn.commit()
    if money_transfer > int(my_balance[0][0]):
        print("Not enough money!")
    else:
        print("Success!")
        old_balace = cursor.execute("SELECT balance FROM card WHERE number=?", [transfer_card]).fetchall()
        tot_balace = money_transfer + int(old_balace[0][0])
        new_balace = int(my_balance[0][0]) - money_transfer
        cursor.execute("UPDATE card SET balance = ? WHERE number = ?", [tot_balace, transfer_card])
        cursor.execute("UPDATE card SET balance = ? WHERE number = ?", [new_balace, my_card])
        conn.commit()


def balance(my_card):
    balance = cursor.execute("SELECT balance FROM card WHERE number=?", [my_card])
    print("\nBalance: " + str(balance))


def closing(my_card):
    cursor.execute("DELETE FROM card WHERE number = ?", [my_card])
    conn.commit()
    print("The account has been closed!")

num = ""
clients = {}
id = 0
while num != "0":
    print("1. Create an account\n2. Log into account\n0. Exit""")
    num = input()
    if num == "1":
        id += 1
        create_account()
    elif num == "2":
        print("\nEnter your card number:")
        card_num = input()
        card_list = cursor.execute("SELECT number, pin FROM card WHERE number=?", [str(card_num)]).fetchall()
        if card_list != []:
            card_number = card_list[0][0]
            pin_db = card_list[0][1]
        else:
            card_num = "None"
        print("Enter your PIN:")
        card_pin = input()
        if card_num != "None":
            if pin_db == card_pin:
                print("\nYou have successfully logged in!")
                cond = True
                while cond:
                    print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                    log = input()
                    if log == "1":
                        balance(card_num)
                    if log == "2":
                        adding_income(card_num)
                    if log == "3":
                        print("Transfer\nEnter card number:")
                        transfer_card = input()
                        if transfer_card == card_num:
                            print("You can't transfer money to the same account!")
                        else:
                            transfer_card_validity = luhn_check(transfer_card)
                            if transfer_card_validity == True:
                                card_trans_db = cursor.execute("SELECT number FROM card WHERE number=?", [transfer_card]).fetchall()
                                if card_trans_db == []:
                                    print("Such a card does not exist.")
                                else:
                                    succesful_transfering(transfer_card, card_num)
                    if log == "4":
                        closing(card_num)
                    if log == "5":
                        print("You have successfully logged out!\n")
                        cond = False
                    if log == "0":
                        exit()
            else:
                print("Wrong card number or PIN\n")
        else:
            print("Wrong card number or PIN\n")
print("Bye!")
