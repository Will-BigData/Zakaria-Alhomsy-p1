from database import connect
from bson.objectid import ObjectId # type: ignore
from logger import start_logging

logger = start_logging()
class Store:
    def __init__(self):
        # Connect to MongoDB 
        self.db = connect()
        self.products = self.db.products
        self.users = self.db.users
        self.purchases = self.db.purchases
        self.logs = self.db.logs


    

    # CRUD for Users
    def create_user(self, username, password, role):
        user_data = {
            "username": username,
            "password": password,
            "balance": 0,
            "role": role
        }
        result = self.users.insert_one(user_data)
        logger.info(f"Added user: {username}")
        return result.inserted_id  


    def get_balance(self,username):
        user = self.users.find_one({"username": username})
        return user.get("balance")

    def update_balance(self,username,balance):
        updated = self.users.update_one(
            {"username": username},
            {"$inc": {"balance": float(balance)}}
        )
        logger.info(f"updated balance for user: {username}")
        return updated.modified_count

    def dec_balance(self,username,balance):
        updated = self.users.update_one(
            {"username": username},
            {"$inc": {"balance": -float(balance)}}
        )
        logger.info(f"updated balance for user: {username}")
        return updated.modified_count

    def login(self, username, password):
        user = self.users.find_one({"username": username, "password": password})
        logger.info(f"login sucessful for user : {username}")
        return user

    def get_all_usernames(self,role):
        usernames = []
        for user in self.users.find({"role": role}, {"_id": 0, "username": 1}):  
            usernames.append(user['username'])
        return usernames

    def update_user_role(self, username, new_role):
        logger.info(f"updated role for user: {username}")
        result = self.users.update_one(
            {"username": username},  
            {"$set": {"role": new_role}}  
    )

    def delete_user(self, username):
        result = self.users.delete_one({"_id": ObjectId(username)})
        logger.info(f"deleted user: {username}")
        return result.deleted_count  # Return the count of deleted documents

    # CRUD for Products
    def create_product(self, name, price, stock):
        product_data = {
            "name": name,
            "price": price,
            "stock": stock
        }
        result = self.products.insert_one(product_data)
        logger.info(f"created product: {name}")
        return result.inserted_id

    def get_all_products(self):
        product_list = list(self.products.find({}, {"_id": 0, "name": 1, "price": 1, "stock": 1}))
        return product_list

    def get_stock(self,product):
        product = self.products.find_one({"name": product}, {"_id": 0, "stock": 1})
        return product.get("stock")

    def get_price(self,product):
        product = self.products.find_one({"name": product}, {"_id": 0, "price": 1})
        return product.get("price")

    def update_product(self, product_name, name, price ,stock):
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if price is not None:
            update_data["price"] = price
        if stock is not None:
            update_data["stock"] = stock
        logger.info(f"updated product: {product_name}")
        result = self.products.update_one({"name": product_name}, {"$set": update_data})
        return result.modified_count

    def delete_product(self, product_name):
        # Remove a product based on its name
        result = self.products.delete_one({"name": product_name})
        logger.info(f"deleted product: {product_name}")
        return result.deleted_count

    # CRUD for Orders
    def create_order(self, username, product, quantity,price):
        order_data = {
            "username": username,
            "product": product,
            "quantity": quantity,
            "amount_spent":price
        }
        result = self.purchases.insert_one(order_data)
        logger.info(f"created order for : {username}")
        return result.inserted_id

    def read_order(self, username):
        return list(self.purchases.find({"username": username}))

    def get_all_orders(self):
        return list(self.purchases.find())

    def get_logs(self):
        return list(self.logs.find())