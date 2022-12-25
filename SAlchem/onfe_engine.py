# https://www.youtube.com/watch?v=1Va493SMTcY
# https://github.com/zzzeek/sqla_tutorial/tree/master/slides
import os
from sqlalchemy import create_engine, text


if os.path.exists('some.db'):
    os.remove('some.db')


# Create Table
engine = create_engine('sqlite:///some.db', future=True)
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE employee (emp_id INTEGER PRIMARY KEY, emp_name VARCHAR)"))
    conn.execute(text("CREATE TABLE employee_of_month (emp_id INTEGER PRIMARY KEY, emp_name VARCHAR)"))
    conn.execute(text("INSERT INTO employee(emp_name) VALUES (:name)"),
                 [{"name": "spongebob"}, {"name": "sandy"}, {"name": "squidward"}],)

print(type(engine))  # Checking what type of engine are we using?
connection = engine.connect()  # We are now connecting to the DB and then some.db file gets created.
print(connection)
print(connection.connection.connection)  # This is the actual sqlite connection.

stmt = text("SELECT emp_id, emp_name FROM employee where emp_id=:emp_id")
result = connection.execute(stmt, {"emp_id": 2})
row = result.first()  # Returns the first row and, it's not in tuple form. It acts mostly like a named tuple.
print(row)
print(row[1])
print(row.emp_name)
print(row.emp_id)
print(row['emp_name'])
print(row[0])
print(row._mapping["emp_name"])
result = connection.execute(stmt, {"emp_id": 2})
for emp_id, emp_name in result:
    print(f'employee id: {emp_id}   employee name: {emp_name}')
connection.close()


"""
# 3 ways of connecting
with engine.connect() as conn:
    # write the sql statements. This doesn't autocommit
    conn.execute(text("INSERT INTO employee(emp_name) VALUES (:name)"),
                 [{"name": "spongebob"}, {"name": "sandy"}, {"name": "squidward"}],)
    conn.commit()

with engine.begin() as conn:
    # write the sql statements. This does autocommit and closes the connection.
    conn.execute(text("INSERT INTO employee(emp_name) VALUES (:name)"),
             [{"name": "spongebob"}, {"name": "sandy"}, {"name": "squidward"}],)

with engine.connect() as conn:
    with conn.begin():
        # write the sql statements. This does autocommit and comes out of the transaction.
        conn.execute(text("INSERT INTO employee(emp_name) VALUES (:name)"),
             [{"name": "spongebob"}, {"name": "sandy"}, {"name": "squidward"}],)
    # But still maintains the connection
"""

if __name__ == '__main__':
    pass
