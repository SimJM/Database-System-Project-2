import psycopg2


# Function to connect to the PgSQL database
def connect():
    # Edit your configurations below
    conn = psycopg2.connect(
        dbname='TPC-H',
        user='user',
        password='password',
        host='localhost',
        port='5432'
    )
    return conn
