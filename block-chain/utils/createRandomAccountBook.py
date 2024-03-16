import json
import random
import string

def generate_account_book(i):
    balance = random.randint(1, 100) 
    return balance

account_book = {}

for i in range(100):
    addr="192.168.42." + str(i)
    balance = generate_account_book(i)
    account_book[addr] = balance

with open('account_book.json', 'w') as file:
    json.dump(account_book, file, indent=4)

print("finish")

    