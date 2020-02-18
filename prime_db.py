import os
import time

import psycopg2

HOST, DATABASE = os.getenv('POSTGRES_HOST'), os.getenv('POSTGRES_DB')
USER, PASSWORD = os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD')


def connect():
    connection = None

    try:
        connection = psycopg2.connect(**{"host": HOST, "database": DATABASE, "user": USER, "password": PASSWORD})
        return 0
    except (Exception, psycopg2.DatabaseError):
        return 1
    finally:
        if connection:
            connection.close()


if __name__ == '__main__':
    while True:
        if connect() == 0:
            break

        print('sleeping for 3s..')
        time.sleep(3)
