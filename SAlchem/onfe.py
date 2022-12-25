# https://www.youtube.com/watch?v=1Va493SMTcY
from sqlalchemy import create_engine, text


engine = create_engine('sqlite:///some.db', future=True)
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
for emp_id, emp_name in result:
    print(f'employee id: {emp_id}   employee name: {emp_name}')
connection.close()


# 3 ways of connecting
with engine.connect() as conn:
    # write the sql statements. This doesn't autocommit
    pass

with engine.begin():
    # write the sql statements. This does autocommit and closes the connection.
    pass

with engine.connect() as conn:
    with conn.begin():
        # write the sql statements. This does autocommit and comes out of the transaction.
        conn.execute(stmt)
    # But still maintains the connection

if __name__ == '__main__':
    pass
