"""
import_data.py
-------------------------------------------
Loads all CSV files from data/raw/ into the
SQLite database defined in config.py.
-------------------------------------------
"""

import pandas as pd
from pathlib import Path
from config import DATA_RAW, get_connection

def load_csv_to_sql():
    # Connect to SQLite DB
    conn = get_connection()
    cursor = conn.cursor()

    print("==========================================")
    print("   CSV → SQLite Data Import Started")
    print("==========================================\n")

    # List all CSV files in data/raw/
    csv_files = list(DATA_RAW.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in:", DATA_RAW)
        return

    for file_path in csv_files:
        table_name = file_path.stem  # file name without .csv

        print(f"Loading: {file_path.name} → Table: {table_name}")

        # Load CSV
        df = pd.read_csv(file_path)

        # Write to SQL
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f"✔ Loaded {len(df)} rows into '{table_name}' table.\n")

    print("==========================================")
    print("   All CSV Files Imported Successfully")
    print("==========================================")

    conn.close()


if __name__ == "__main__":
    load_csv_to_sql()
