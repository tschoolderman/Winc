import models
import os


def delete_database():
    """Delete existing database to get a fresh start each time."""
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "betsy.db")
    if os.path.exists(database_path):
        os.remove(database_path)
        print("Database deleted...")


def create_tables():
    """Make a connection to the database and create tables."""
    models.database.connect()
    print("Connected to the database...")
    models.database.create_tables(
        [
            models.User,
            models.Tag,
            models.Products,
            models.ProductTags,
            models.Transaction,
        ]
    )
    print("Tables created...")


def populate_test_database():
    """Fill the tables with predetermined data."""
    tag_data = [
        ("Fantasy"),
        ("Functional"),
        ("Kitchenware"),
        ("Food"),
        ("Drinks"),
        ("Electrical"),
        ("Weapon"),
        ("Toys"),
        ("Utilities"),
        ("Unknown"),
        ("Sports"),
    ]

    user_data = [
        (
            (
                "john55",
                "John",
                "Smith",
                "Sesamestreet",
                666,
                "1061SB",
                "Zwolle",
                111155553333,
            ),
            [
                (
                    "Football",
                    "Round air-filled object made of cowhide.",
                    2.99,
                    5,
                ),
                (
                    "Lego starship",
                    "A starship from a well-known franchise.",
                    99.99,
                    2,
                ),
            ],
        ),
        (
            (
                "elsa43",
                "Elsa",
                "Icequeen",
                "Arendellelane",
                15,
                "6622AB",
                "Arendelle",
                123456781234,
            ),
            [
                (
                    "Diamond Icicle",
                    "Sharp conal object made of ice.",
                    9.99,
                    6,
                ),
                (
                    "Hairpin",
                    "An object for placing your hair in a desired position.",
                    15.69,
                    4,
                ),
            ],
        ),
        (
            (
                "Winnie1",
                "Winnie",
                "the Pooh",
                "Tree",
                20,
                "1234HB",
                "Bunderbos",
                987432156549,
            ),
            [
                (
                    "Honey",
                    "Sweet sap the bees of Bunderbos made during Summer.",
                    5.49,
                    25,
                ),
                (
                    "Branch",
                    "Sturdy stick for hitting honeycombs.",
                    8.49,
                    5,
                ),
            ],
        ),
    ]

    producttag_data = (
        ("Football", ["Sports", "Utilities", "Toys"]),
        ("Lego starship", ["Toys", "Fantasy"]),
        ("Diamond Icicle", ["Weapon", "Food"]),
        ("Hairpin", ["Weapon", "Utilities"]),
        ("Honey", ["Food", "Unknown"]),
        ("Branch", ["Functional", "Weapon"]),
    )

    for tag in tag_data:
        # Fill the Tag table.
        tag = models.Tag.create(name=tag)

    for user, products in user_data:
        # Fill the user and products table with an automatic link.
        user = models.User.create(
            username=user[0],
            firstname=user[1],
            lastname=user[2],
            address_street=user[3],
            address_number=user[4],
            address_zipcode=user[5],
            address_city=user[6],
            billing_info=user[7],
        )

        for product in products:
            product = models.Products.create(
                username=user,
                productname=product[0],
                description=product[1],
                unit_price=product[2],
                quantity=product[3],
            )

    for product, tag in producttag_data:
        # Fill the ProductTags table as shown in the documents.
        d_product = models.Products.get(models.Products.productname == product)
        for tags in tag:
            d_tag = models.Tag.get(models.Tag.name == tags)
            models.ProductTags.create(productname=d_product, tagname=d_tag)


if __name__ == "__main__":
    delete_database()
    create_tables()
    populate_test_database()
