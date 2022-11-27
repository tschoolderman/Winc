import argparse
from argparse import RawDescriptionHelpFormatter


def convert_string(s):
    # Convert the given string to lowercase and strip whitespace
    string_check = s.lower().strip()
    return string_check


def convert_float(f):
    # Convert the given float to have 2 decimals
    float_check = "{0:.2f}".format(float(f))
    return float_check


def superpy_parser():
    """This function is used to make the argparser with several subparsers"""
    parser = argparse.ArgumentParser(
        prog="SuperPy",
        formatter_class=RawDescriptionHelpFormatter,
        description="""
                        Welcome to Superpy!
        ---------------------------------------------------
        The command-line interface for a supermarket app.
        Use the 'submenu -h' to view help for submenus.
        (e.g. 'buy -h').""",
        epilog="Thank you for using SuperPy. Have a nice day!",
    )
    subparser = parser.add_subparsers(dest="menu")

    # Submenu for buying items
    buy_parser = subparser.add_parser(
        "buy", help="Use the registry for bought products."
    )
    buy_parser.add_argument(
        "-p",
        "--product",
        metavar="",
        help="Enter the product name.",
        type=convert_string,
    )
    buy_parser.add_argument(
        "-m",
        "--price",
        metavar="",
        help="Enter the price of the purchase. In euros as 0.00 for 1 product.",
        type=convert_float,
    )
    buy_parser.add_argument(
        "-e",
        "--expiration",
        metavar="",
        help="Enter the expiration date. As YYYY-MM-DD.",
    )
    buy_parser.add_argument(
        "-q",
        "--quantity",
        metavar="",
        help="Enter the quantity of the purchase.",
        type=int,
    )

    # Submenu for selling items
    sell_parser = subparser.add_parser(
        "sell", help="Use the registry for sold products."
    )
    sell_parser.add_argument(
        "-p",
        "--product",
        metavar="",
        help="Enter the product name.",
        type=convert_string,
    )
    sell_parser.add_argument(
        "-m",
        "--price",
        metavar="",
        help="Enter the sell price. In euros as 0.00 for 1 product.",
        type=convert_float,
    )
    sell_parser.add_argument(
        "-q", "--quantity", metavar="", help="Enter the quantity sold.", type=int
    )

    # Submenu for expiring items
    expire_parser = subparser.add_parser(
        "expire", help="Use the registry for expiring products."
    )
    expire_parser.add_argument(
        "-p",
        "--product",
        metavar="",
        help="Enter the product name.",
        type=convert_string,
    )
    expire_parser.add_argument(
        "-m",
        "--price",
        metavar="",
        help="Enter the bought price. In euros as 0.00 for 1 product.",
        type=convert_float,
    )
    expire_parser.add_argument(
        "-q", "--quantity", metavar="", help="Enter the quantity sold.", type=int
    )
    # Submenu to view inventory. Takes no arguments.
    inventory_parser = subparser.add_parser(
        "inventory", help="Show a short overview of the current inventory."
    )

    # Submenu to view all expired products. Takes no arguments.
    expired_parser = subparser.add_parser(
        "view-expired", help="Check all expired products."
    )

    # Submenu to search for items
    search_parser = subparser.add_parser(
        "search", help="Search the inventory for items."
    )
    search_parser.add_argument(
        "-s", "--search", metavar="", help="Search the inventory for items."
    )

    # Submenu to change the current date percieved as "today"
    date_parser = subparser.add_parser("date", help="Change the date of the program.")
    date_parser.add_argument(
        "-a",
        "--advance_time",
        metavar="",
        help="Advance the date by an 'x' amount of days.",
        type=int,
    )

    # Submenu to get the revenue
    revenue_parser = subparser.add_parser(
        "revenue", help="Show the revenue of a specific time period."
    )
    revenue_parser.add_argument(
        "-r",
        "--review",
        metavar="",
        help="Show the revenue of the time specified as 'x' amount of days in the past or 0 for today.",
        type=int,
    )

    # Submenu to calculate the profit or loss made
    profit_parser = subparser.add_parser(
        "profit", help="Show the profit of a specific time period."
    )
    profit_parser.add_argument(
        "-p",
        "--profit",
        metavar="",
        help="Show the profit of the time specified as 'x' amount of days in the past or 0 for today.",
        type=int,
    )

    # Submenu to export files to excel
    export_parser = subparser.add_parser(
        "export", help="export the specified file to Excel."
    )
    export_parser.add_argument(
        "-e",
        "--export",
        metavar="",
        help="Export the specified file to Excel.",
        choices=["bought", "sold", "expired", "inventory"],
    )

    graph_parser = subparser.add_parser(
        "graph", help="Show a graph of the cashflow from the start-up."
    )
    return parser.parse_args()
