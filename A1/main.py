import sqlite3

# Inventory Class
class Inventory:
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    def __init__(self):
        with self.conn:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS INV(PROD_NAME STRING PRIMARY KEY, QUANT INTEGER, COST REAL)"
            )

    def add_item(self, name, quant, cost):
        with self.conn:
            self.cursor.execute(
                "INSERT INTO INV VALUES('" + name + "', '" + str(quant) + "', '" + str(cost) + "')"
            )

    def remove_item(self, name):
        with self.conn:
            self.cursor.execute(
                "DELETE FROM INV WHERE PROD_NAME='" + name + "'"
            )

    def update_item(self, name, quant=None, cost=None):
        with self.conn:
            if quant is not None:
                self.cursor.execute(
                    "UPDATE INV SET QUANT=" + str(quant) + " WHERE PROD_NAME='" + name + "'"
                )
            if cost is not None:
                self.cursor.execute(
                    "UPDATE INV SET COST=" + str(cost) + " WHERE PROD_NAME='" + name + "'"
                )

    def get_items(self):
        return self.cursor.execute("SELECT * FROM INV").fetchall()

    def get_item(self, name):
        return self.cursor.execute(
            "SELECT * FROM INV WHERE PROD_NAME='" + name + "'"
        ).fetchone()

    def show_inventory(self):
        print("\nInventory List:")
        print("-" * 30)
        print("Product Name | Quantity | Cost per Item")
        print("-" * 30)
        for row in self.get_items():
            print(row[0] + " | " + str(row[1]) + " | " + str(row[2]))
        print("-" * 30)

inventory = Inventory()

# Buyer Functions
def buyer_menu():
    while True:
        ch = input(
            """
Welcome to the Inventory

1) Buy Item
2) View Inventory
3) Back

Enter choice: """
        )

        if ch == "1":
            buy_item()
        elif ch == "2":
            inventory.show_inventory()
        elif ch == "3":
            return
        else:
            print("Invalid choice. Try again.")

def buy_item():
    while True:
        name = input("Enter item name: ")
        quant = int(input("Enter quantity of item: "))

        row = inventory.get_item(name)
        if row is None:
            print("Item not found.")
            continue

        total_cost = row[2] * quant
        confirm = input(str(quant) + " units of " + name + " at " + str(row[2]) + " each.\nTotal cost: " + str(total_cost) + "/-\nBuy[y/n]: ")

        if confirm.lower() == "y":
            new_quantity = row[1] - quant
            if new_quantity < 0:
                print("Not enough stock available.")
            else:
                inventory.update_item(name, new_quantity, row[2])
                print("Purchase successful!")
            break

# Seller Functions
def seller_menu():
    while True:
        ch = input(
            """
Welcome to the Inventory

1) Add Item
2) Remove Item
3) Update Item
4) View Inventory
5) Back

Enter choice: """
        )

        if ch == "1":
            add_item()
        elif ch == "2":
            remove_item()
        elif ch == "3":
            update_item()
        elif ch == "4":
            inventory.show_inventory()
        elif ch == "5":
            return
        else:
            print("Invalid choice. Try again.")

def add_item():
    name = input("Enter item name: ")
    quant = int(input("Enter quantity: "))
    cost = float(input("Enter cost: "))

    inventory.add_item(name, quant, cost)
    print(name + " has been added to the inventory.")

def remove_item():
    name = input("Enter item name to remove: ")

    inventory.remove_item(name)
    print(name + " has been removed from the inventory.")

def update_item():
    name = input("Enter item name to update: ")
    quant = input("Enter additional quantity [N/n to skip]: ")
    cost = input("Enter new cost [N/n to skip]: ")

    row = inventory.get_item(name)
    if row is None:
        print("Item not found.")
        return

    new_quant = int(quant) + row[1] if quant.lower() != "n" else row[1]
    new_cost = float(cost) if cost.lower() != "n" else row[2]

    inventory.update_item(name, new_quant, new_cost)
    print("Updated " + name + " in the inventory.")

# Main Menu
while True:
    ch = input(
        """
Welcome to the Inventory System

1) Buyer
2) Seller
3) View Inventory
4) Exit

Enter choice: """
    )

    if ch == "1":
        buyer_menu()
    elif ch == "2":
        seller_menu()
    elif ch == "3":
        inventory.show_inventory()
    elif ch == "4":
        exit()
    else:
        print("Invalid choice. Try again.")
