from sqlalchemy import select, create_engine, MetaData, insert
from sqlalchemy.orm import Session
from metadata_main import user_table, User, Address
from engine_main import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
metadata_obj = MetaData()


if __name__ == '__main__':
    # The select() SQL Expression Construct
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    metadata_obj.drop_all(engine)
    metadata_obj.create_all(engine)
    with engine.connect() as conn:
        result = conn.execute(
            insert(user_table),
            [
                {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"}
            ]
        )

    stmt1 = select(user_table).where(user_table.c.name == "spongebob")  # Core Table
    with engine.connect() as conn:
        for row in conn.execute(stmt1):
            print(row)
    print('-----------------------------------------------------------------')

    stmt2 = select(User).where(User.name == "spongebob")  # ORM entities
    with Session(engine) as session:
        for row in session.execute(stmt2):
            print(row)
    print('-----------------------------------------------------------------')

    # Setting the COLUMNS and FROM clause
    print(select(user_table))  # Selecting all columns from the user_table
    print(select(user_table.c.name, user_table.c.fullname))  # Selecting 'name' and 'fullname' columns from user_table
    with Session(engine) as session:
        row = session.execute(select(User)).first()
        print(row)
    print('-----------------------------------------------------------------')

    # Selecting ORM Entities and Columns
    print(select(User))  # Selecting all columns from the User table
    print(select(User.name, User.fullname))  # Selecting 'name' and 'fullname' columns from User table
    print('-----------------------------------------------------------------')

    with Session(engine) as session:
        user = session.scalars(select(User)).first()  # scalars method will return a ScalarResult object that delivers
        # the first "column" of each row at once, in this case, instances of the User class.
        print(user)
        row = session.execute(select(User.name, User.fullname)).first()
        print(row)
    print('-----------------------------------------------------------------')

    stmt3 = select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
    with Session(engine) as session:
        session.execute(stmt3)
    print('-----------------------------------------------------------------')

    # Selecting from Labeled SQL Expressions. This is similar to renaming column expression using 'AS' something simple.
    stmt4 = select(
        ("Username: " + user_table.c.name).label("username"),
    ).order_by(user_table.c.name)
    with engine.connect() as conn:
        for row in conn.execute(stmt4):
            print(f"{row.username}")
