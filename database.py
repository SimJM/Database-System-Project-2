import psycopg2


# Function to connect to the PgSQL database
def connect():
    # Edit your configurations below
    conn = psycopg2.connect(
        dbname='estherteo',
        user='estherteo',
        password='password',
        host='localhost',
        port='5432'
    )
    return conn
