import tabulate as tb
from typing import Generator, Tuple
import sqlite3


class Inventory:
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    def __init__(self) -> None:
        with self.conn:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS INV(PROD_NAME STRING PRIMARY KEY, QUANT INTEGER, COST REAL)",
            )

    def addItem(self, name: str, quant: int, cost: float) -> None:
        with self.conn:
            self.cursor.execute(
                f"INSERT INTO INV VALUES('{name}', '{quant}', '{cost}')",
            )

    def removeItem(self, name: str) -> None:
        with self.conn:
            self.cursor.execute(
                f"DELETE FROM INV WHERE PROD_NAME='{name}'",
            )

    def updateItem(
        self, name: str, quant: int | None = None, cost: float | None = None
    ) -> None:
        with self.conn:
            if quant:
                self.cursor.execute(
                    f"UPDATE INV SET QUANT={quant} WHERE PROD_NAME='{name}'",
                )
            if cost:
                self.cursor.execute(
                    f"UPDATE INV SET COST={cost} WHERE PROD_NAME='{name}'",
                )

    def getItems(self) -> Generator:
        for row in self.cursor.execute("SELECT * FROM INV"):
            yield row

    def getItem(self, name: str) -> Tuple:
        return self.cursor.execute(
            f"SELECT * FROM INV WHERE PROD_NAME='{name}'"
        ).fetchone()

    def show(self) -> None:
        print(
            tb.tabulate(
                tabular_data=self.getItems(),
                headers=["Product Name", "Quantity", "Cost per Item"],
                tablefmt="outline",
                numalign="center",
                stralign="center",
            )
        )


inventory = Inventory()
