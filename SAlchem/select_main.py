from sqlalchemy import select, create_engine, MetaData, insert, text, literal_column
from sqlalchemy import and_, or_, func, desc
from sqlalchemy.orm import Session, aliased
from metadata_main import user_table, address_table, User, Address
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

    # Selecting with Textual Column Expressions
    stmt5 = select(text("'some phrase'"), user_table.c.name).order_by(user_table.c.name)
    with engine.connect() as conn:
        print(conn.execute(stmt5).all())

    # Same above functionality, but using literal_column() for single column
    stmt6 = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(user_table.c.name)
    with engine.connect() as conn:
        for row in conn.execute(stmt6):
            print(f'{row.p}, {row.name}')

    # The WHERE clause
    print(user_table.c.name == "squidward")
    print('-' * 50)
    print(address_table.c.user_id > 10)
    print('-' * 50)
    print(select(user_table).where(user_table.c.name == "squidward"))
    print('-' * 50)
    print(select(address_table.c.email_address).where(user_table.c.name == "suidward",
                                                      address_table.c.user_id == user_table.c.id))
    print('-' * 50)
    print(
        select(Address.email_address).where(
            and_(
                or_(User.name == "squidward", User.name == "sandy"),
                Address.user_id == User.id,
            )
        )
    )
    print('-' * 50)
    print(select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants"))
    print('-' * 50)

    # Explicit FROM clauses and JOINs
    print(select(user_table.c.name))  # If we set a single column from a particular Table
    print('-' * 50)
    # If we were to put columns from two tables, then we get a comma-separated FROM clause:
    print(select(user_table.c.name, address_table.c.email_address))
    print('-' * 50)

    # JOINS
    # The first is the Select.join_from() method, which allows us to indicate the left and right side of the JOIN
    # explicitly:
    print(
        select(user_table.c.name, address_table.c.email_address).join_from(
            user_table, address_table
        )
    )
    print('-' * 50)
    # The other is the Select.join() method, which indicates only the right side of the JOIN, the left
    # hand-side is inferred:
    print(select(user_table.c.name, address_table.c.email_address).join(address_table))
    print('-' * 50)
    # We also have the option to add elements to the FROM clause explicitly, if it is not inferred the way we want from
    # the columns' clause. We use the Select.select_from() method to achieve this, as below where we establish
    # user_table s the first element in the FROM clause and Select.join() to establish address_table as the second:
    print(select(address_table.c.email_address).select_from(user_table).join(address_table))
    print('-' * 50)
    # If we don't have what we are looking for in the SELECT clause
    print(select(func.count("*")).select_from(user_table))
    print('-' * 50)

    # Setting the ON Clause
    # Both Select.join() and Select.join_from() accept an additional argument for the ON clause
    print(
        select(address_table.c.email_address)
        .select_from(user_table)
        .join(address_table, user_table.c.id == address_table.c.user_id)
    )
    print('-' * 50)

    # OUTER and FULL join
    # There is also a method Select.outerjoin() that is equivalent to using .join(..., isouter=True).
    print(select(user_table).join(address_table, isouter=True))
    print('-' * 50)
    print(select(user_table).join(address_table, full=True))
    print('-' * 50)

    # ORDER BY, GROUP BY, HAVING
    # ORDER BY
    print(select(user_table).order_by(user_table.c.name))
    print('-' * 50)
    print(select(User).order_by(User.fullname.desc()))
    print('-' * 50)

    # Aggregate functions with GROUP BY/HAVING
    count_fn = func.count(user_table.c.id)
    print(count_fn)
    print('-' * 50)

    with engine.connect() as conn:
        result = conn.execute(
            select(User.name, func.count(Address.id).label("count"))
            .join(Address)
            .group_by(User.name)
            .having(func.count(Address.id) > 1)
        )
        print(result.all())
    print('-' * 50)

    # Ordering or Grouping by a Label
    stmt7 = (select(Address.user_id, func.count(Address.id)
                    .label('num_addresses'))
                    .group_by('user_id')
                    .order_by('user_id', desc('num_addresses')))
    print(stmt7)
    print('-' * 50)

    # Using Aliases
    user_alias_1 = user_table.alias()
    user_alias_2 = user_table.alias()
    print(select(user_alias_1.c.name, user_alias_2.c.name)
          .join_from(user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id))
    print('-' * 50)

    # ORM Entity Aliases
    address_alias_1 = aliased(Address)
    address_alias_2 = aliased(Address)
    print(
        select(User)
        .join_from(User, address_alias_1)
        .where(address_alias_1.email_address == "patrick@aol.com")
        .join_from(User, address_alias_2)
        .where(address_alias_2.email_address == "patrick@gmail.com")
    )
    print('-' * 50)

    # Subqueries and CTEs
    subq1 = (select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
             .group_by(address_table.c.user_id)
             .subquery())
    print(subq1)
    print('-' * 50)
    print(select(subq1.c.user_id, subq1.c.count))
    print('-' * 50)
    stmt8 = select(user_table.c.name, user_table.c.fullname, subq1.c.count).join_from(user_table, subq1)
    print(stmt8)
    print('-' * 50)

    # Common Table Expressions (CTEs)
    subq2 = (select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
             .group_by(address_table.c.user_id)
             .cte())
    stmt9 = select(user_table.c.name, user_table.c.fullname, subq2.c.count).join_from(user_table, subq2)
    print(stmt9)
    print('-' * 50)

    # ORM Entity Subqueries/CTEs
    subq3 = select(Address).where(~Address.email_address.like("%@aol.com")).subquery()
    address_subq = aliased(Address, subq3)
    stmt10 = (
        select(User, address_subq)
        .join_from(User, address_subq)
        .order_by(User.id, address_subq.id)
    )
    with Session(engine) as session:
        for user, address in session.execute(stmt10):
            print(f"{user} {address}")
    print('-' * 50)

    cte_obj = select(Address).where(~Address.email_address.like("%@aol.com")).cte()
    address_cte = aliased(Address, cte_obj)
    stmt = (
        select(User, address_cte)
        .join_from(User, address_cte)
        .order_by(User.id, address_cte.id)
    )
    with Session(engine) as session:
        for user, address in session.execute(stmt):
            print(f"{user} {address}")
    print('-' * 50)

    # Scalar and Correlated Subqueries
    # A scalar subquery is a subquery that returns exactly zero or one row and exactly one column.
    subq3 = (
        select(func.count(address_table.c.id))
        .where(user_table.c.id == address_table.c.user_id)
        .scalar_subquery()
    )
    print(subq3)
    print('-' * 50)
    print(subq3 == 5)
    print('-' * 50)