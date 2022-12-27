# This file is about inserting rows with Core
from sqlalchemy import create_engine, select, insert
from metadata_main import user_table, address_table, metadata_obj
from engine_main import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


if __name__ == '__main__':
    stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")  # Using named tuple format
    print(stmt)
    compiled = stmt.compile()
    print(compiled.params)
    metadata_obj.drop_all(engine)
    metadata_obj.create_all(engine)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        print(result.inserted_primary_key)

    with engine.connect() as conn:
        result = conn.execute(
            insert(user_table),
            [
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"}
            ]
        )  # using list of dictionary format
        print(result.inserted_primary_key_rows)

    # Insert... from Select
    select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
    insert_stmt = insert(address_table).from_select(["user_id", "email_address"], select_stmt)
    print(insert_stmt)

    # Insert.. Returning
    insert_stmt2 = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
    print(insert_stmt2)
    print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))
