import streamlit as st
import pandas as pd
import sqlite3
import re
from io import StringIO
import openai as OpenAI

# Configure OpenAI API key
OpenAI.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state for database management
if 'db_initialized' not in st.session_state:
    st.session_state['db_initialized'] = False

st.session_state['table_rows'] = {}

DB_PATH = "synthetic_data.db"

# Utility functions
def detect_tables(schema):
    """Extract table names from SQL schema."""
    return re.findall(r"CREATE TABLE\s+(\w+)", schema, re.IGNORECASE)

def create_database(schema):
    """Create and initialize the database from schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    commands = schema.split(';')
    for command in commands:
        if "CREATE TABLE" in command.upper():
            tablename = re.findall(r"CREATE TABLE\s+(\w+)", command, re.IGNORECASE)
            if tablename:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tablename[0]}'")
                if cursor.fetchone():
                    print(f"Table {tablename[0]} already exists. Skipping creation.")
                    continue
        try:
            cursor.execute(command)
        except sqlite3.OperationalError as e:
            print(f"An error occurred: {e}")
            return

    conn.commit()
    conn.close()
    st.session_state['db_initialized'] = True

def insert_data(table_name, data):
    """Insert data into the specified table in the database, ensuring column count matches."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Retrieve column information from the database for the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    column_info = cursor.fetchall()
    num_columns = len(column_info)

    # Identify the primary key column
    primary_key_column = None
    for column in column_info:
        if column[5] == 1:  # Column index 5 in the result is the "pk" flag (1 if primary key)
            primary_key_column = column[1]  # Column index 1 is the name of the column
            break

    if not primary_key_column:
        print(f"No primary key found for the table {table_name}.")
        return None

    # Prepare the SQL statement
    placeholders = ', '.join(['?'] * num_columns)
    sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

    inserted_rows = 0
    for idx, row in data.iterrows():
        # # Validate foreign keys here before inserting
        # is_valid = validate_foreign_keys(table_name, row, cursor)
        # Ensure the row has the correct number of columns
        if len(row) == num_columns:
            try:
                cursor.execute(sql, tuple(row))
                conn.commit()
                inserted_rows += 1
            except sqlite3.IntegrityError as e:
                print(f"Integrity error on inserting data into {table_name}: {e}")
                continue  # Optionally, continue to the next row or handle differently
        else:
            print(f"Column mismatch: The table {table_name} expects {num_columns} columns, but the provided data row has {len(row)} columns.")

    # Fetch the maximum index (primary key value) from the table
    cursor.execute(f"SELECT MAX({primary_key_column}) FROM {table_name}")
    max_index = cursor.fetchone()[0]

    conn.close()
    print(f"Inserted {inserted_rows} rows into {table_name} successfully.")

    # Return the maximum index found in the table
    return inserted_rows, max_index

def verify_inserts(table_name):
    """Query the database to count rows and display some sample data to verify inserts."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    print(f"Total rows in {table_name}: {row_count}")

    if row_count > 0:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
        sample_data = cursor.fetchall()
        print(f"Sample data from {table_name}: {sample_data}")

    conn.close()

import time
import random
def openai_generator(schema, table_and_rows, chunk_size=200):
    """Generate data using OpenAI API."""
    final_output = {}
    table_rows_dict = {table.split(':')[0]: int(table.split(':')[1]) for table in table_and_rows.split(", ")}
    
    for table, rows_requested in table_rows_dict.items():
        rows_generated = 0
        i = 0
        while rows_generated < rows_requested:
            rows_to_generate = min(chunk_size, rows_requested - rows_generated)
            try:
                time.sleep(35)  # Add a delay to avoid API rate limits
                response = OpenAI.chat.completions.create(
                    model="gpt-3.5-turbo",  # Adjust the model as per requirement
                    messages=[
                        {"role": "system", 
                         "content": 
                             "You are a data curator who is an expert at generating realistic synthetic data."
                             },
                        {"role": "user",
                         "content":
                            f"Generating unique dataset {random.randint(1, 100000)}. Analyze the following schema - {schema}. Please generate {rows_to_generate} entries to populate the {table} table in valid CSV format with the correct header for each column. The data generated needs to be consistent with the foreign and primary keys. Generate primary keys starting at {i}. Do not include any additional text like 'certainly... here you go' or unnecessary characters, only response with the requested data."}
                    ],
                    max_tokens=1500
                )
                if response.choices[0].message.content.strip():  # Check if text is not empty
                    tdf = pd.read_csv(StringIO(response.choices[0].message.content.strip()))
                    # table_tmp.append(pd.read_csv(StringIO(response.choices[0].message.content.strip())))
                    rowgen, max_index = insert_data(table, tdf)
                    rows_generated += rowgen
                    i += max_index + 1
                    # verify_inserts(table)  # Verify and display results after inserts
            except Exception as e:
                print(f"An error occurred while generating data for {table}: {e}")
                continue
                # return None  # Early exit on failure
    
    return final_output

st.title("Synthetic Database Generator")
uploaded_schema = st.sidebar.file_uploader("Upload SQL schema", type=['sql'])
if uploaded_schema:
    schema_content = uploaded_schema.getvalue().decode("utf-8")
    st.session_state['schema'] = schema_content
    st.session_state['tables'] = detect_tables(schema_content)

if 'schema' in st.session_state:
    st.text_area("Schema Preview", st.session_state['schema'], height=300)
    if not st.session_state['db_initialized']:
        if st.button("Create Database"):
            create_database(st.session_state['schema'])

# Streamlit app interface logic for generating and inserting data
if 'tables' in st.session_state and st.session_state['db_initialized']:
    st.write("Detected tables and row configurations:")
    for table in st.session_state.tables:
        st.session_state.table_rows[table] = st.sidebar.number_input(f"Number of rows for {table}:", min_value=1, value=15, step=1, key=table)


    table_and_rows = ", ".join([f"{table}: {st.session_state.table_rows[table]}" for table in st.session_state['tables']])
    if st.button("Generate and Insert Data"):
        dataframes_dict = openai_generator(st.session_state['schema'], table_and_rows, 100)

if st.button("Download Database"):
    with open(DB_PATH, "rb") as file:
        st.download_button("Download SQLite Database", file, file_name="synthetic_data.db", mime="application/octet-stream")

# st.write("Session State:", st.session_state)
