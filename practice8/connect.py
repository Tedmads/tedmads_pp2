import psycopg2
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def connect():
    try:
        with get_connection() as conn:
            print("Connected to PostgreSQL")
            return conn
    except Exception as e:
        print(e)