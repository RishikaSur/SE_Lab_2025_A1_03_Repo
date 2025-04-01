import sqlite3
from typing import Generator, Tuple

class Inventory:
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    def __init__(self):
        with self.conn:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS INV(PROD_NAME STRING PRIMARY KEY, QUANT INTEGER, COST REAL)"
            )

    def addItem(self, name, quant, cost):
        with self.conn:
            self.cursor.execute(
                "INSERT INTO INV VALUES('" + name + "', '" + str(quant) + "', '" + str(cost) + "')"
            )

    def removeItem(self, name):
        with self.conn:
            self.cursor.execute(
                "DELETE FROM INV WHERE PROD_NAME='" + name + "'"
            )

    def updateItem(self, name, quant=None, cost=None):
        with self.conn:
            if quant is not None:
                self.cursor.execute(
                    "UPDATE INV SET QUANT=" + str(quant) + " WHERE PROD_NAME='" + name + "'"
                )
            if cost is not None:
                self.cursor.execute(
                    "UPDATE INV SET COST=" + str(cost) + " WHERE PROD_NAME='" + name + "'"
                )

    def getItems(self):
        for row in self.cursor.execute("SELECT * FROM INV"):
            yield row

    def getItem(self, name):
        return self.cursor.execute(
            "SELECT * FROM INV WHERE PROD_NAME='" + name + "'"
        ).fetchone()

    def show(self):
        print("\nInventory List:")
        print("-" * 30)
        print("Product Name | Quantity | Cost per Item")
        print("-" * 30)
        for row in self.getItems():
            print(row[0] + " | " + str(row[1]) + " | " + str(row[2]))
        print("-" * 30)

inventory = Inventory()
