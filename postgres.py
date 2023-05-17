import psycopg2
def connectPostgressDatabase():
    conn = psycopg2.connect(database="ztagziwi", user="ztagziwi", password="G0syey10_61gkqPxcarSWw3QXATyh2Zv", host="mahmud.db.elephantsql.com", port="5432")

    return conn


def getDbCursor(conn):
    cursor = conn.cursor()
    return cursor

conn = connectPostgressDatabase()
c = getDbCursor(conn)


c.execute('''CREATE TABLE light_meter_average (
    id SERIAL PRIMARY KEY,
    average FLOAT NOT NULL,
    reading_timestamp TIMESTAMP NOT NULL
);''')


conn.commit()
conn.close()