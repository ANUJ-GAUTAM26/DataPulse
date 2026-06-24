from loader.db_connection import get_connection

conn = get_connection()

print("Connected to PostgreSQL successfully!")

conn.close()