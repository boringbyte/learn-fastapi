"""
Postgres and Python
    - Use the psycopg library to create databases and insert data
    - Understand parameterized queries, including avoiding SQL-injection
    - Database transactions
    - Read and clean data from a CSV to insert into a postgres database
"""


import psycopg


connection = psycopg.connect(host="localhost", dbname="adventureworks")
connection.execute("INSERT INTO students (name, favorite_food) VALUES (%s, %s)", ("byte", "tuna"))
results = connection.execute("SELECT * FROM students;")
print(results.fetchall())

name = "Dan"
food = "Bagels"
connection.execute("INSERT INTO student (name, favorite_food) VALUES (%(name)s, %(food)s)",
                   {'name': name, 'food': food})

"""
    Transactions
    - A group of SQL statements that run together, one after another. If any of these statements fail, they'll all
      get reversed.
    - Begin a transaction with `BEGIN TRANSACTION`
    - After running all the related transactions, save them in the database with `COMMIT`
    - If there's a problem, undo all the queries in the transaction with `ROLLBACK`
"""

