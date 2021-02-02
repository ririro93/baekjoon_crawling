import sqlite3

# connect to db
conn = sqlite3.connect('times.db')

# create cursor
cursor = conn.cursor()

# insert data
cursor.execute("INSERT INTO customers VALUES ('Mary', 'Brown', 'mary@codemny.com')")

# commit to db
conn.commit()

# close connection
conn.close()