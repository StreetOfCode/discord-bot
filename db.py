import psycopg2
from config import DB_CONNECTION_STRING

db = psycopg2.connect(DB_CONNECTION_STRING)

def add_test(value):
    cursor = db.cursor()
    cursor.execute("INSERT INTO TEST(test) VALUES('"+value +"')")
    db.commit()
