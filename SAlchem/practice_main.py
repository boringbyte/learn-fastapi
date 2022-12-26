from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


"""
Establishing Connectivity - the Engine:
    sqlite      --> Refers to the type of database that we are communicating with.
    pysqlite    --> Refers to the DBAPI (third party driver that SQLAlchemy uses to interact with a particular DB.
    ///:memory: --> Location of the sample database (URL)
    echo        --> Prints the logs
    future      --> Uses 2.0 version syntax instead of 1.X syntax
    
    Create Engine Object:
    Engine object acts as a central source of connections to a particular database, providing both a factory as well 
    as a holding space called a connection pool for these database connections.
"""
SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:////home/siva/Desktop/Projects/learn-fastapi/SAlchem/sample.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)


if __name__ == '__main__':
    # Getting connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'hello world'"))
        print(result.all())

    # Getting connection and performing implicit commit
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE some_table"))
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{'x': 1, 'y': 1}, {'x': 2, 'y': 4}],
        )
        result = conn.execute(text("SELECT * FROM some_table"))
        print(result.all())

    # This style may be referred towards as begin once connection and will serve as block of SQL statements commit
    # within the 'with engine.begin()' block.
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 36}, {"x": 9, "y": 81}],
        )
        result = conn.execute(text("SELECT x, y FROM some_table"))
        print(result.all())

    # Fetching Rows
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))

        # Tuple assignment
        for x, y in result:
            print(x, y)

        # Integer Index
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            x, y = row
            print(x, y)

        # Attribute Name
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f'x: {row.x} y: {row.y}')

        # Mapping Access
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for dict_row in result.mappings():
            x = dict_row['x']
            y = dict_row['y']
            print(x, y)

    # Sending Parameters
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
        for row in result:
            print(f'x: {row.x} y: {row.y}')

    # Sending Multiple Parameters
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 11, "y": 121}, {"x": 12, "y": 144}],
        )

    # Executing with an ORM Session
    print('----------------------------------------------------------------------')
    stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
    with Session(engine) as session:
        result = session.execute(stmt, {'y': 6})
        for row in result:
            print(f'x: {row.x} y: {row.y}')

    with Session(engine) as session:
        result = session.execute(
            text("UPDATE some_table SET y=:y WHERE x=:x"),
            [{"x": 11, "y": 122}, {"x": 12, "y": 145}],
        )
        session.commit()
