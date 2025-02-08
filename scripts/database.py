import logging
import pyodbc

logging.basicConfig(level=logging.ERROR, filename='database.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def connect_db():
    try:
        connection = pyodbc.connect(
            r"DRIVER={ODBC Driver 18 for SQL Server};"
            r"SERVER=DESKTOP-F6LIGO6\SQLEXPRESS;"
            r"DATABASE=PostManager;"
            r"Trusted_Connection=yes;"
            r"TrustServerCertificate=yes"
        )
        connection.autocommit = True
        return connection
    except pyodbc.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None
