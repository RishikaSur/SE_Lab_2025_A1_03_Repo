from db import inventory as inv


def show():
    while True:
        ch = int(
            input(
                """
Welcome to the Inventory

1) Add Item
2) Remove Item
3) Update Item information
4) View Inventory
5) Back

Enter choice: """
            )
        )
        if ch == 1:
            add()
        elif ch == 2:
            remove()
        elif ch == 3:
            update()
        elif ch == 4:
            inv.show()
        elif ch == 5:
            return
        else:
            print("Bad Choice. Try again")
            continue


def add():
    name = input("Enter item name: ")
    quant = int(input("Enter quantity of item: "))
    cost = float(input("Enter cost of item: "))

    inv.addItem(name, quant, cost)
    print(f"{name} has been added to the inventory")


def remove():
    name = input("Enter item name to remove: ")

    inv.removeItem(name)
    print(f"{name} has been removed from the inventory")


def update():
    name = input("Enter item name to update: ")
    quant = input("Enter additional quantity added[N/n to skip]: ")
    cost = input("Enter new cost[N/n to skip]: ")

    row = inv.getItem(name)

    quant = int(quant) if quant.lower() != "n" else None
    cost = float(cost) if cost.lower() != "n" else None

    inv.updateItem(name, row[1] + quant, cost)
