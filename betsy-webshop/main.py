__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import User, Products, Tag, ProductTags, Transaction
import peewee
from textblob import TextBlob


def main():
    pass


def search(term):
    corrected_word = TextBlob(term).correct()
    query = (
        Products.select(Products.productname, Products.description)
        .where(
            (Products.productname.contains(corrected_word))
            | (Products.description.contains(corrected_word))
        )
        .order_by(Products.productname)
    )
    try:
        query.get()  # Checks whether there is an actual query
        for products in query:
            found_item = products.productname
            return found_item
    except peewee.DoesNotExist:
        # When no match is found
        return "Item not found. Please check your spelling."


def list_user_products(user_id):
    # Join the Products and User tables
    query = (
        Products.select(Products.username, Products.productname)
        .join(User, on=(User.id == Products.username_id))
        .where(Products.username_id == user_id)
    )
    # Create a list of available products
    product_list = []
    for product in query:
        product_list.append(product.productname)
    return product_list


def list_products_per_tag(tag_id):
    # Join the Products and Tags tables with help from ProductTags table
    query = (
        Products.select(
            ProductTags, Products.id, Products.productname, Tag.id, Tag.name
        )
        .join(ProductTags, on=(Products.id == ProductTags.productname_id))
        .join(Tag, on=(Tag.id == ProductTags.tagname_id))
        .where(ProductTags.tagname_id == tag_id)
    )
    # Create a list of available products
    product_list = []
    for product in query:
        product_list.append(product.productname)
    return product_list


def add_product_to_catalog(user_id, product):
    # Create a new instance in the Products table
    Products.create(
        username=User.get(User.id == user_id),
        productname=product[0],
        description=product[1],
        unit_price=product[2],
        quantity=product[3],
    )

    # Get a list of all tags
    tag_list = list(product[4:])

    # Get the last added item as a string
    latest = Products.alias()
    latest_item = latest.select(latest.productname, peewee.fn.MAX(latest.id))
    for product in latest_item:
        most_recent_product = product.productname

    # Create a data object to use to make a new instance for the ProductTags table
    producttag_data = (
        (
            most_recent_product,
            tag_list,
        ),
    )
    for item, tag in producttag_data:
        d_product = Products.get(Products.productname == item)
        for tags in tag:
            d_tag = Tag.get(Tag.name == tags)
            ProductTags.get_or_create(productname=d_product, tagname=d_tag)

    for row in Products.select().order_by(Products.id.desc()).dicts():
        return f"The product as shown below has been added to the database:\n{row}"


def update_stock(product_id, new_quantity):
    (Products.update(quantity=new_quantity).where(Products.id == product_id).execute())
    return f"Quantity of item with product_id {product_id} has been updated."


def purchase_product(product_id, buyer_id, quantity):
    # Select product based on id
    query = Products.select().where(Products.id == product_id)
    # Get the unit_price of the product
    price = Products.get(Products.id == product_id).unit_price
    # Get the seller_id
    seller = (
        User.select(User.id, User.username)
        .join(Products)
        .where(Products.id == product_id)
        .get()
    )
    # Get the seller's account_balance
    seller_account_balance = (
        User.select(User.id, User.account_balance)
        .join(Products)
        .where(Products.id == product_id)
        .get()
        .account_balance
    )
    for product in query:
        if product.quantity >= quantity:
            # Create an instance for the transaction between users
            Transaction.create(
                seller=seller,
                buyer=buyer_id,
                purchased_product=product_id,
                purchased_quantity=quantity,
                total_price=(price * quantity),
            )
            # Update the Products table with the new quantity
            new_quantity = product.quantity - quantity
            update_stock(product_id, new_quantity)
            # Update the seller's account balance with the total_price sold
            new_balance = seller_account_balance + (price * quantity)
            (
                User.update(account_balance=new_balance)
                .where(User.id == seller)
                .execute()
            )
            return "Enjoy your purchase."
        else:
            return "There is not enough in stock to meet demand."


def remove_product(product_id):
    try:
        # Checks if the product is available, if so delete it.
        Products.select().where(Products.id == product_id).get()
        Products.delete().where(Products.id == product_id).execute()
        return "The product has been removed."
    except Products.DoesNotExist:
        # When the query cannot be executed.
        return "Failed to remove item. No such item in shop."


if __name__ == "__main__":
    main()
    # print(search("Football"))
    # print(search("Fotball"))
    # print(search("Sweet sap"))
    # print(search("Sweet sop"))
    # print(list_user_products(1))
    # print(list_user_products(2))
    # print(list_user_products(3))
    # print(list_products_per_tag(1))
    # print(list_products_per_tag(8))
    # print(list_products_per_tag(3))
    # print(
    #     add_product_to_catalog(
    #         1,
    #         [
    #             "Cast iron pan",
    #             "A tool for cooking stuff.",
    #             11.25,
    #             6,
    #             "Utilities",
    #             "Unknown",
    #         ],
    #     )
    # )
    # print(update_stock(4, 15))
    # print(update_stock(5, 5))
    # print(remove_product(2))
    # print(purchase_product(3, 3, 3))
