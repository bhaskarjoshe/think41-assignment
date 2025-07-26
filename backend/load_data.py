import csv
import os

import psycopg2

DB_NAME = "think41assignment"
DB_USER = "bhaskar"
DB_PASSWORD = "bhaskar"
DB_HOST = "localhost"
DB_PORT = "5432"

tables = [
    "distribution_centers",
    "inventory_items",
    "order_items",
    "orders",
    "products",
    "users",
]


def populate_table_from_csv(cursor, table_name, csv_file):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        columns = ",".join(headers)
        placeholders = ",".join(["%s"] * len(headers))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        for row in reader:
            cleaned_row = [None if val == "" else val for val in row]
            cursor.execute(insert_query, cleaned_row)


def main():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    for table in tables:
        csv_file = f"./data/{table}.csv"
        if os.path.exists(csv_file):
            print(f"Populating {table} from {csv_file}...")
            try:
                populate_table_from_csv(cursor, table, csv_file)
                print(f"{table} populated successfully.")
            except Exception as e:
                print(f"Error populating {table}: {e}")
        else:
            print(f"CSV file {csv_file} not found. Skipping.")

    cursor.close()
    conn.close()
    print("Data population complete.")


if __name__ == "__main__":
    main()
