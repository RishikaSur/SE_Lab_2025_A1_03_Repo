
from db import inventory as inv

def show():
    while True:
        ch = int(
            input(
                """
Welcome to the Inventory

1) Buy Item
2) View Inventory
3) Back

Enter choice: """
            )
        )
        if ch == 1:
            update()
        elif ch == 2:
            inv.show()
        elif ch == 3:
            return
        else:
            print("Bad Choice. Try again")
            continue

def update():
    while True:
        name = input("Enter item name: ")
        quant = int(input("Enter quantity of item: "))

        row = inv.getItem(name)

        total_cost = row[2] * quant
        confirm = input(str(quant) + " units of " + name + " at " + str(row[2]) + " each.\nTotal cost: " + str(total_cost) + "/-\nBuy[y/n]: ")

        if confirm.lower() == "y":
            inv.updateItem(name, row[1] - quant, row[2])
            break
