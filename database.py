import psycopg2


# Function to connect to the PgSQL database
def connect():
    # Edit your configurations below
    conn = psycopg2.connect(
        dbname='dbname',
        user='user',
        password='pwd',
        host='host',
        port='port'
    )
    return conn
