import peewee
from datetime import datetime

# Database for Betsy
database = peewee.SqliteDatabase("betsy.db")


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    username = peewee.CharField(unique=True)
    firstname = peewee.CharField()
    lastname = peewee.CharField()
    address_street = peewee.TextField()
    address_number = peewee.IntegerField()
    address_zipcode = peewee.CharField(max_length=6)
    address_city = peewee.TextField()
    billing_info = peewee.IntegerField()
    account_balance = peewee.DecimalField(
        default=0.00, decimal_places=2, auto_round=True
    )


class Tag(BaseModel):
    name = peewee.TextField(unique=True)


class Products(BaseModel):
    username = peewee.ForeignKeyField(User, backref="products")
    productname = peewee.CharField(max_length=20)
    description = peewee.CharField(max_length=100)
    unit_price = peewee.DecimalField(default=0.00, decimal_places=2, auto_round=True)
    quantity = peewee.IntegerField()

    class Meta:
        # Specifying unique multi-column index
        indexes = (
            (
                ("productname", "description"),
                True,
            ),
        )


class ProductTags(BaseModel):
    productname = peewee.ForeignKeyField(Products, backref="tags")
    tagname = peewee.ForeignKeyField(Tag, backref="tags")

    class Meta:
        # Specifying unique multi-column index
        indexes = (
            (
                ("productname", "tagname"),
                True,
            ),
        )


class Transaction(BaseModel):
    timestamp = peewee.DateTimeField(
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    seller = peewee.ForeignKeyField(User, backref="seller")
    buyer = peewee.ForeignKeyField(User, backref="buyer")
    purchased_product = peewee.ForeignKeyField(Products, null=False)
    purchased_quantity = peewee.IntegerField(
        null=False, constraints=[peewee.Check("purchased_quantity >= 1")]
    )
    total_price = peewee.DecimalField(default=0.00, decimal_places=2, auto_round=True)
