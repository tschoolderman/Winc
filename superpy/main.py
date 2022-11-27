"""SUPERPY, by Thomas Schoolderman.
A supermarket application."""

# Imports
import csv
from datetime import date
from datetime import datetime
from datetime import timedelta
import os
from parser_superpy import superpy_parser
from tabulate import tabulate
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from functools import reduce


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    pass


# Defining constants.
BOUGHT_FILE = "bought_products.csv"
SOLD_FILE = "sold_products.csv"
INVENTORY_FILE = "inventory.csv"
EXPIRED_FILE = "expired_products.csv"
DATE_FILE = "date.txt"

SUPERPY_PATH = os.getcwd()

BOUGHT_FILE_PATH = os.path.join(SUPERPY_PATH, BOUGHT_FILE)
SOLD_FILE_PATH = os.path.join(SUPERPY_PATH, SOLD_FILE)
INVENTORY_FILE_PATH = os.path.join(SUPERPY_PATH, INVENTORY_FILE)
EXPIRED_FILE_PATH = os.path.join(SUPERPY_PATH, EXPIRED_FILE)
DATE_FILE_PATH = os.path.join(SUPERPY_PATH, DATE_FILE)

COLUMNS_BOUGHT = [
    "id",
    "product_name",
    "quantity",
    "date",
    "price",
    "expiration_date",
    "cost",
]
COLUMNS_SOLD = [
    "id",
    "product_name",
    "quantity",
    "date",
    "price",
    "income",
]
COLUMNS_EXPIRED = [
    "id",
    "product_name",
    "quantity",
    "date",
    "price",
    "loss",
]
COLUMNS_INVENTORY = ["product_name", "quantity"]


def get_date():
    """This function is used to get the date from the date.txt file."""
    with open("date.txt", "rb") as file:
        line = file.readline().decode()
        return line


def changing_date(a):
    """This function handles the changing of the date perceived as 'today'."""

    # Get the old date before changing to the new 'today'.
    old_date = get_date()
    # If no argument is passed into the parser. Set the date for the actual "today".
    if a.advance_time == (0 or None):
        with open(DATE_FILE_PATH, "w") as file:
            file.write(date.today().strftime("%Y-%m-%d"))

    # Increments the date in 'date.txt' with the user-specified day(s).
    else:
        today = datetime.strptime(get_date(), "%Y-%m-%d").date()
        with open(DATE_FILE_PATH, "w") as file:
            new_date = (today + timedelta(days=a.advance_time)).strftime("%Y-%m-%d")
            file.write(new_date)

    # Get the new date of 'today'.
    new_today = get_date()
    # Clean out expired products automatically
    # Make a copy to prevent "settingwithcopywarning" error
    df = pd.read_csv("bought_products.csv", index_col="id")
    expired_df = df.loc[(df["expiration_date"] < get_date())].copy()
    mask = (expired_df["expiration_date"] >= old_date) & (
        expired_df["expiration_date"] < new_today
    )
    expired_df = expired_df.loc[mask]
    print(f'\n{tabulate(expired_df,headers=COLUMNS_BOUGHT,tablefmt="fancy_outline",)}')

    return f"\nThe date has been set to {get_date()}. Please review the products and manually expire, if necessary.\n"


def buying(buy):
    """This function handles the buying of products."""

    # Dictionary for writing rows.
    buy_row = {
        "product_name": buy.product,
        "quantity": buy.quantity,
        "date": get_date(),
        "price": buy.price,
        "expiration_date": buy.expiration,
        "cost": "{0:.2f}".format(int(buy.quantity) * float(buy.price)),
    }

    # Function to append new items to existing csv file.
    with open(BOUGHT_FILE_PATH, mode="a", newline="") as bought_file:
        bought_writer = csv.DictWriter(
            bought_file,
            fieldnames=COLUMNS_BOUGHT,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )

        # Create an id for the bought product.
        id = 0
        for row in open(BOUGHT_FILE_PATH):
            id += 1
        id2 = {"id": id}  # Make a dictionary of the id.
        buy_row.update(id2)  # Append the dict to the front of buy_row.
        bought_writer.writerow(buy_row)

    # Function to add the bought product to the inventory.
    with open(INVENTORY_FILE_PATH, mode="r", newline="") as inv_file:
        inv_reader = csv.reader(
            inv_file,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        lines = []  # Placeholder for rows in csv file
        for row in inv_reader:
            lines.append(row)  # Append all rows as list
        # Check if the bought product is already available
        if any(buy.product in i for i in lines) is True:
            for i in lines:
                if i[0] == buy.product:
                    # Increase the product quantity when available
                    x = int(i[1]) + buy.quantity
                    i[1] = x
                    with open(INVENTORY_FILE_PATH, mode="w", newline="") as inv_file:
                        inv_writer = csv.writer(
                            inv_file,
                            delimiter=",",
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL,
                        )
                        # Write the new quantity to csv
                        inv_writer.writerows(lines)
        else:
            # Append a new row if product is new
            with open(INVENTORY_FILE_PATH, mode="a", newline="") as inv_file:
                inv_writer = csv.writer(
                    inv_file,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                )
                inv_list = [buy.product, buy.quantity]
                inv_writer.writerow(inv_list)
    return f"\n{get_date()} >> Added {buy.product}({buy.quantity}).\n"


def selling(sell):
    """This function handles the selling of products."""

    # Dictionary for writing rows.
    sell_row = {
        "product_name": sell.product,
        "quantity": sell.quantity,
        "date": get_date(),
        "price": sell.price,
        "income": "{0:.2f}".format(int(sell.quantity) * float(sell.price)),
    }

    # Reducing quantity of inventory by amount sold
    with open(INVENTORY_FILE_PATH, mode="r", newline="") as inv_file:
        inv_reader = csv.reader(
            inv_file,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        lines = []  # Placeholder for rows in csv file
        for row in inv_reader:
            lines.append(row)  # Append all rows as list
        # Check if the sold product is available
        if any(sell.product in i for i in lines) is True:
            for i in lines:
                if i[0] == sell.product:
                    # Decrease the product quantity when available
                    x = int(i[1]) - sell.quantity
                    i[1] = x
                    if x >= 0:
                        with open(
                            INVENTORY_FILE_PATH, mode="w", newline=""
                        ) as inv_file:
                            inv_writer = csv.writer(
                                inv_file,
                                delimiter=",",
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                            )
                            # Write the new quantity to csv
                            inv_writer.writerows(lines)

                        with open(SOLD_FILE_PATH, mode="a", newline="") as sold_file:
                            sold_writer = csv.DictWriter(
                                sold_file,
                                fieldnames=COLUMNS_SOLD,
                                delimiter=",",
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                            )
                            # Create an id for the sold product.
                            id = 0
                            for row in open(SOLD_FILE_PATH):
                                id += 1
                            id2 = {"id": id}  # Make a dictionary of the id.
                            sell_row.update(
                                id2
                            )  # Append the dict to the front of sell_row.
                            sold_writer.writerow(sell_row)
                            print(
                                f"\n{get_date()} >> Sold {sell.product}({sell.quantity}).\n"
                            )
                    else:
                        print(
                            f"{view_inventory()}\nNot enough in stock! Check the stock and try again.\n"
                        )
        else:
            print("\nSorry. This product is not available in this store.\n")


def expired(expired):
    """This function handles the expiration of products."""

    # Dictionary for writing rows.
    expired_row = {
        "product_name": expired.product,
        "quantity": expired.quantity,
        "date": get_date(),
        "price": expired.price,
        "loss": "{0:.2f}".format(int(expired.quantity) * float(expired.price)),
    }

    # Reducing quantity of inventory by amount sold
    with open(INVENTORY_FILE_PATH, mode="r", newline="") as inv_file:
        inv_reader = csv.reader(
            inv_file,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        lines = []  # Placeholder for rows in csv file
        for row in inv_reader:
            lines.append(row)  # Append all rows as list
        # Check if the sold product is available
        if any(expired.product in i for i in lines) is True:
            for i in lines:
                if i[0] == expired.product:
                    # Decrease the product quantity when available
                    x = int(i[1]) - expired.quantity
                    i[1] = x
                    if x > 0:
                        with open(
                            INVENTORY_FILE_PATH, mode="w", newline=""
                        ) as inv_file:
                            inv_writer = csv.writer(
                                inv_file,
                                delimiter=",",
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                            )
                            # Write the new quantity to csv
                            inv_writer.writerows(lines)

                        with open(EXPIRED_FILE_PATH, mode="a", newline="") as sold_file:
                            sold_writer = csv.DictWriter(
                                sold_file,
                                fieldnames=COLUMNS_EXPIRED,
                                delimiter=",",
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                            )
                            # Create an id for the sold product.
                            id = 0
                            for row in open(EXPIRED_FILE_PATH):
                                id += 1
                            id2 = {"id": id}  # Make a dictionary of the id.
                            expired_row.update(
                                id2
                            )  # Append the dict to the front of sell_row.
                            sold_writer.writerow(expired_row)
                            print(
                                f"\n{get_date()} >> The {expired.product}({expired.quantity}) has expired.\n"
                            )
                    else:
                        print(
                            f"{view_inventory()}\nNot enough in stock to expire! Check the stock and try again.\n"
                        )
        else:
            print("\nWe do not have this product.\n")


def view_inventory():
    """This function returns the current inventory."""
    inv_reader = csv.reader(open(INVENTORY_FILE_PATH, "r"))
    inventory = []
    # Read the file and append the rows in a list.
    for row in inv_reader:
        inventory.append(row)

    # Using tabulate, create a tabel of the list acquired by reading.
    inv_table = tabulate(
        inventory,
        headers=("product", "quantity"),
        tablefmt="fancy_outline",
        colalign=(
            "center",
            "center",
        ),
    )
    return f"\nThe current inventory is:\n{inv_table}\n"


def view_expired():
    """This function returns all expired products."""
    df = pd.read_csv(EXPIRED_FILE_PATH, index_col="id")
    return f'\n{tabulate(df,headers=COLUMNS_BOUGHT,tablefmt="fancy_outline",)}\n'


def search_inventory(search):
    """This function searches the current inventory for the user-specified item."""
    inv_reader = csv.reader(open(INVENTORY_FILE_PATH, "r"), delimiter=",")
    total_list = []
    searched_item = []
    for row in inv_reader:
        # Looks for the search parameter in product_name.
        if search.search == row[0]:
            total_list.append(row[0:2])  # Appends name and quantity.
            searched_item.append(int(row[1]))  # Returns the total of searched item.

    return f"\nThe current stock for {search.search}: {sum(searched_item)}\n"


def revenue(r):
    """This function calculates the revenue of a user-specified time period."""
    # Get the current "today" from the date.txt
    today = datetime.strptime(get_date(), "%Y-%m-%d").date()
    # Let the user specify the amount of days in the past
    user_specified_date = (today - timedelta(days=r.review)).strftime("%Y-%m-%d")

    # Read and sort the csv file based on the amount of days in the past
    df = pd.read_csv(SOLD_FILE_PATH)
    df = df.loc[df["date"] >= user_specified_date]
    revenue_x = (df["quantity"] * df["price"]).sum()
    return f"\nRevenue of {user_specified_date}: {revenue_x}.\n"


def export_to_excel(e):
    """This function exports the desired files to .xlsx based on the input."""
    if e.export == "bought":
        df = pd.read_csv(BOUGHT_FILE_PATH)
        df.to_excel("bought.xlsx")
        return f"The {e.export} file has been exported to Excel"
    elif e.export == "sold":
        df = pd.read_csv(SOLD_FILE_PATH)
        df.to_excel("sold.xlsx")
        return f"The {e.export} file has been exported to Excel"
    elif e.export == "expired":
        df = pd.read_csv(EXPIRED_FILE_PATH)
        df.to_excel("expired.xlsx")
        return f"The {e.export} file has been exported to Excel"
    elif e.export == "inventory":
        df = pd.read_csv(INVENTORY_FILE_PATH)
        df.to_excel("inventory.xlsx")
        return f"The {e.export} file has been exported to Excel"
    else:
        return "\nPlease choose one of the following: bought, sold, expired or inventory.\n"


def profits(profit):
    """This function calculates the profits made of a user-specified time period."""

    # Get the current "today" from the date.txt
    today = datetime.strptime(get_date(), "%Y-%m-%d").date()
    # Let the user specify the amount of days in the past
    user_specified_date = (today - timedelta(days=profit.profit)).strftime("%Y-%m-%d")

    # Read the csv and calculate the income based on date
    sold_df = pd.read_csv("sold_products.csv")
    sold_df = sold_df.loc[sold_df["date"] >= user_specified_date]
    income = sold_df["income"].sum()

    # Read the csv and calculate the cost of products based on date
    bought_df = pd.read_csv("bought_products.csv")
    bought_df = bought_df.loc[bought_df["date"] >= user_specified_date]
    cost = bought_df["cost"].sum()

    # Read the csv and calculate the loss based on expired products
    expired_df = pd.read_csv("expired_products.csv")
    expired_df = expired_df.loc[expired_df["date"] >= user_specified_date]
    loss = expired_df["loss"].sum()

    # Return the profit or loss made based on cost, loss and income
    return "{0:.2f}".format(float((income - (cost + loss))))


def show_graph():
    """This function shows a graph of the income, cost and loss."""

    # Define the window of the graph
    plt.style.use("dark_background")
    plt.rcParams["figure.figsize"] = [10, 4]
    plt.rcParams["figure.autolayout"] = True

    # Read csv files
    df2 = pd.read_csv("bought_products.csv", index_col="id")
    df2 = df2.groupby("date", as_index=False)["cost"].sum().copy()

    df3 = pd.read_csv("sold_products.csv", index_col="id")
    df3 = df3.groupby("date", as_index=False)["income"].sum().copy()

    df4 = pd.read_csv("expired_products.csv", index_col="id")
    df4 = df4.groupby("date", as_index=False)["loss"].sum().copy()

    # Merge the dataframes into a single dataframe
    dfs = [df2, df3, df4]
    final_df = reduce(
        lambda left, right: pd.merge(left, right, on=["date"], how="outer"), dfs
    )
    final_df = final_df.sort_values(by=["date"])
    # Using interpolate to compensate for NaN values in the dataframe
    final_df = final_df.interpolate(method="linear", limit_direction="forward", axis=0)
    # Add a new column to the dataframe
    final_df["profit"] = final_df["income"] - (final_df["cost"] + final_df["loss"])

    # Define the line for the cost
    plt.plot(
        final_df["date"],
        final_df["cost"],
        color="#746AB0",
        lw=2,
        marker="o",
        label="cost",
    )

    # Define the line for the loss
    plt.plot(
        final_df["date"],
        final_df["loss"],
        color="#FFCE30",
        lw=2,
        linestyle="dotted",
        marker="o",
        label="loss",
    )

    # Define the line for the income
    plt.plot(
        final_df["date"],
        final_df["income"],
        color="#E83845",
        lw=2,
        marker="o",
        label="income",
    )

    # Define the line for the profit
    plt.plot(
        final_df["date"],
        final_df["profit"],
        color="#00A36C",
        lw=2,
        linestyle="dashed",
        marker="o",
        label="profit",
    )

    # Define the layout of the graph window and show the graph
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0.0)
    plt.title("Cash flow per date")
    plt.xlabel("Date")
    plt.ylabel("Cashflow in euro's")
    plt.show()


if __name__ == "__main__":
    args = superpy_parser()
    if args.menu == "buy":
        print(buying(args))
    elif args.menu == "sell":
        selling(args)
    elif args.menu == "expire":
        expired(args)
    elif args.menu == "inventory":
        print(view_inventory())
    elif args.menu == "view-expired":
        print(view_expired())
    elif args.menu == "search":
        print(search_inventory(args))
    elif args.menu == "date":
        print(changing_date(args))
    elif args.menu == "revenue":
        print(revenue(args))
    elif args.menu == "profit":
        print(profits(args))
    elif args.menu == "export":
        print(export_to_excel(args))
    elif args.menu == "graph":
        show_graph()
