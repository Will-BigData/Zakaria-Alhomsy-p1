from storeModel import Store
import logging
from pymongo import MongoClient # type: ignore
from pymongo.errors import ConnectionFailure # type: ignore
import database

store = Store()

def log(message):
    logging.info(message)

def modify():
    print("which product would you like to modify: ")
    products = store.get_all_products()
    product_names = [p['name'].lower() for p in products]
    
    for p in products:
        print(p)
    modify = input().lower()
    while modify not in product_names:
        print("Invalid product name. Please enter a valid product name.")
        modify = input().lower()
    selected_product = next(p for p in products if p['name'].lower() == modify)


        # Ask which fields to update
    new_name, new_price, new_stock = None, None, None
    if input("Do you want to update the name? (y/n): ").lower() == 'y':
        new_name = input("Enter the new name: ")
        while not new_name.isalpha():
            print("Invalid input. Name should only contain letters.")
            new_name = input("Enter the new name: ")

    if input("Do you want to update the price? (y/n): ").lower() == 'y':
        new_price = input("Enter the new price: ")
        while True:
            try:
                new_price = float(new_price)
                if new_price > 0:
                    break
                else:
                    print("Invalid input. Price must be a positive number.")
            except ValueError:
                print("Invalid input. Please enter a valid price (e.g., 19.99).")
                new_price = float(new_price)
    if input("Do you want to update the stock? (y/n): ").lower() == 'y':
        new_stock = input("Enter the new stock amount: ")
        while not new_stock.isdigit() or int(new_stock) < 0:
            print("Invalid input. Stock should be a non-negative integer.")
            new_stock = input("Enter the new stock amount: ")
        new_stock = int(new_stock)  # Convert validated input to int


    result = store.update_product(selected_product['name'], new_name, new_price, new_stock)
    if result > 0:
        print("Product updated successfully!")
    else:
        print("No changes made to the product.")

def purchase(username,balance):
    print("which product would you like to purchase: ")
    products = store.get_all_products()
    product_names = [p['name'].lower() for p in products]
    
    for p in products:
        print(p)
    modify = input().lower()
    while modify not in product_names:
        print("Invalid product name. Please enter a valid product name.")
        modify = input().lower()
    selected_product = next(p for p in products if p['name'].lower() == modify)

    stock = store.get_stock(modify)
    price = store.get_price(modify)
    print("how many would you like to purchase")
    amount = input()

    while True:
        first = True
        if not amount.isdigit() :
            print("Invalid input. amount should be a non-negative integer")
        elif int(amount) < 0:
            print("Invalid input. amount  should not exceed amount available.")
        elif int(amount) > stock:
            print("Invalid input. amount  should not exceed amount available.")
        else:
            first=False
        if(float(amount) * float(price) > float(balance)):
            print("insufficent funds, purchase exceeds balance")
        else:   
            if(first == False):
                break
        print("how many would you like to purchase")
        amount= input()
    amount = float(amount)

    #update stock
    #update balance
    if(amount == stock):
        store.delete_product(modify)
    pricePaid = amount * float(price)
    change = float(balance) - pricePaid
    #print("c")
    #print(pricePaid)
    store.update_product(modify,None,None,int(stock-amount))
    store.dec_balance(username,pricePaid)  

    store.create_order(username,modify,amount,pricePaid) 







def removeProduct():
    print("which product would you like to remove: ")
    products = store.get_all_products()
    product_names = [p['name'].lower() for p in products]
    
    for p in products:
        print(p)
    remove = input().lower()
    while remove not in product_names:
        print("Invalid product name. Please enter a valid product name.")
        remove = input().lower()
    selected_product = next(p for p in products if p['name'].lower() == remove)
    
    store.delete_product(remove)   

def storePrompt(user):
    print("hello " + user['username']+ " your current balance is: " + str(store.get_balance(user['username'])))
    purchasing = True
    while purchasing:
        print("What would you like to do: Add balance(a), Check balance(b), View and purchase products(v), View purchase history(h), exit(e)")
        userInput = input().lower()
        while userInput != 'a' and userInput != 'v' and userInput != 'h'  and userInput != 'b' and userInput != 'e':
            print("invalid input, please enter: Add balance(a), Check balance(b), View and purchase products(v), View purchase history(h), exit(e)")
            userInput = input().lower()
        if(userInput == 'a'):
            print("how much would you like to add to your balance, please only input positive nondecimal numbers and you can only add a maximum of 500 at a time")
            balanceinput = input()
            while not (balanceinput.isdigit() and 1 <= int(balanceinput) < 501):
                print("invalid input, please only input positive nondecimal numbers under 501")
                balanceinput = input()
            store.update_balance(user['username'],balanceinput)
        elif(userInput == 'b'):
            print("your current balance is: " + str(float(store.get_balance(user['username']))))
        elif(userInput== 'e'):
            purchasing = False
            print("Thank you for shopping with us!")
        elif(userInput== 'h'):
            orders = store.read_order(user['username'])
            for order in orders:
                order_to_print = {key: value for key, value in order.items() if key != '_id'}
                print(order_to_print)
        elif(userInput == 'v'):
            purchase(user['username'],str(store.get_balance(user['username'])))
                

def adminPrompt():
    cont = True
    while(cont):
        print("What would you like to do: check purchase logs(p), check db logs(d), promote user(a), demote admin(u), add item(i), modify item(m) remove item(r),view inventory, exit(e)")
        adminInput = input().lower()
        while adminInput != 'p' and adminInput != 'd' and adminInput != 'a' and adminInput != 'u' and adminInput != 'i' and adminInput != 'r' and adminInput != 'e'and adminInput != 'm' and adminInput != 'v':
            print("invalid input please enter: check purchase logs(p), check db logs(d), promote user(a), demote admin(u), add item(i), modify item(m) remove item(r),view inventory, exit(e)")
            adminInput = input().lower()
        if(adminInput == 'p'):
            orders = store.get_all_orders()
            for order in orders:
                order_to_print = {key: value for key, value in order.items() if key != '_id'}
                print(order_to_print)
        elif (adminInput =='a'):
            userList = store.get_all_usernames("user")
            print(userList)
            print("which user would you like to promote to admin")
            promote = input().lower()
            while promote not in userList:
                print("user does not exist please only enter a valid user from this list: ")
                print(userList)
                promote = input().lower()
            store.update_user_role(promote,"admin")
            print("sucessfully updated " + promote + " to admin")
        elif (adminInput =='u'):
            userList = store.get_all_usernames("admin")
            print(userList)
            print("which user would you like to demote to user (cannot demote admin)")
            demote = input().lower()
            while demote  not in userList or demote == "admin":
                print("user does not exist please only enter a valid user from this list, not including admin: ")
                print(userList)
                demote  = input().lower()
            store.update_user_role(demote ,"user")
            print("sucessfully updated " + demote  + " to user")
        elif (adminInput =='d'):
            logs = store.get_logs()
            for log in logs:
                log_to_print = {key: value for key, value in log.items() if key != '_id'}
                print(log_to_print)
        elif (adminInput =='i'):
            print("Enter item name to add ")
            itemName = input().strip().lower()
            while not itemName.isalpha():
                print("Invalid input. Item name must contain letters only and cannot be empty. Please enter a valid item name: ")
                itemName = input().strip().lower()
            print("Enter amount of stock: ")
            while True:
                stockAmount = input().strip()
                if stockAmount.isdigit() and int(stockAmount) > 0:
                    stockAmount = int(stockAmount)  # Convert to integer after validation
                    break
                else:
                    print("Invalid input. Please enter a positive whole number for stock amount.")

            print("Enter item price: ")
            while True:
                itemPrice = input().strip()
                try:
                    itemPrice = float(itemPrice)  # Try converting to float
                    if itemPrice > 0:
                        break
                    else:
                        print("Invalid input. Price must be a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a valid price (e.g., 19.99).")

            store.create_product(itemName,itemPrice,stockAmount)

        elif (adminInput =='r'):
            removeProduct()
        elif (adminInput =='m'):
            modify()
            
        elif(adminInput== 'e'):
            cont = False
        elif(adminInput == 'v'):
            products = store.get_all_products()
            product_names = [p['name'].lower() for p in products]
            for p in products:
                print(p)

def login():
    print("Please enter your username")
    username = input().lower()
    print("Please enter your password")
    password = input().lower()
    user = store.login(username, password)
    success = False
    while(success == False):
        if user:
            #print("login sucessful")
            success = True
        else:
            print("invalid username or password, please try again")
            print("Please enter your username")
            username = input().lower()
            print("Please enter your password")
            password = input().lower()
            user = store.login(username, password)
    if(user['role'] == 'user'):
        storePrompt(user)
    else:
        adminPrompt()


def create_account():
    print("Please enter a username")
    newUsername = input().lower()
    existing_user = store.users.find_one({"username": newUsername})
    while existing_user is not None:
        print("Username taken, please enter a different username")
        newUsername = input().lower()
        existing_user = store.users.find_one({"username": newUsername})
    print("Please enter a password")
    password = input().lower()
    user = store.create_user(newUsername, password,"user")
    print("You have logged into your new account")
    storePrompt(user)
    

def main():
    
    #prompt starts here
    loopOn = True
    while(loopOn):
        print("create account(c) or login to existing user(l)")
        accInput = input().lower()
        while(accInput != 'c' and accInput != 'l'):
            print("invalid input, please enter (c) to create an account or (l) to login to an existing user")
            accInput = input().lower()
        if(accInput == 'c'):
            create_account()
            loopOn = False
        else:
            login()
            loopOn = False
    loopTwo = True
    

if __name__ == "__main__":
    main()
