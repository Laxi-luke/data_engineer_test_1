import psycopg2

conn = psycopg2.connect(
    dbname="swapi_data",
    user="test_user",
    password="user_password"
    )

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute("DROP SCHEMA public CASCADE;")
cur.execute("CREATE SCHEMA public;;")
conn.commit()