from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session
from metadata_main import user_table, User, Address
from practice_main import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


if __name__ == '__main__':
    # The select() SQL Expression Construct
    stmt1 = select(user_table).where(user_table.c.name == "spongebob")  # Table
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
    print(select(user_table))
    print(select(user_table.c.name, user_table.c.fullname))
    print('-----------------------------------------------------------------')

    # Selecting ORM Entities and Columns
    print(select(User))
    print(select(User.name, User.fullname))
    print('-----------------------------------------------------------------')

    with Session(engine) as session:
        user = session.scalars(select(User)).first()
        row = session.execute(select(User.name, User.fullname)).first()
        print(user)
        print(row)
    print('-----------------------------------------------------------------')

    with Session(engine) as session:
        session.execute(
            select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
        )
    print('-----------------------------------------------------------------')
    print('still incomplete')
