import seller as slr
import buyer as byr
from db import inventory as inv

while True:
    ch = int(
        input(
            """
Welcome to the Inventory

1) Buyer
2) Seller
3) View inventory
4) Exit

Enter choice: """
        )
    )
    if ch == 1:
        byr.show()
    elif ch == 2:
        slr.show()
    elif ch == 3:
        inv.show()
    elif ch == 4:
        exit()
    else:
        print("Bad Choice. Try again")
        continue
