import csv
import uuid
import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'alx_user',
        password = 'asdffdsa'
    )

    return connection

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE if not EXISTS ALX_prodev")

def connect_to_prodev():
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'alx_user',
        password = 'asdffdsa',
        database="ALX_prodev"
    )

    return connection

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) NOT NULL PRIMARY KEY,   -- UUID stored as 36-char string
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX (user_id)
        )
    """)

def insert_data(connection, data):
    cursor = connection.cursor()
    try:
        users = []
        with open(data, '+r') as file:
            content = csv.DictReader(file)
            for row in content:
                row["user_id"] = str(uuid.uuid4())
                row["age"] = float(row["age"])
                sql = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
                values = (row["user_id"] , row["name"] , row["email"] , float(row["age"] ))
                cursor.execute(sql, values)
                
                
    except(UnicodeDecodeError, FileNotFoundError) as e:
        print(f"An error occurred: {e}")

    connection.commit()