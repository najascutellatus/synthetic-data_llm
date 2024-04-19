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
                    st.warning(f"Table {tablename[0]} already exists. Skipping creation.")
                    continue
        try:
            cursor.execute(command)
        except sqlite3.OperationalError as e:
            st.error(f"An error occurred: {e}")
            return

    conn.commit()
    conn.close()
    st.session_state['db_initialized'] = True

def insert_data(table_name, data):
    """Insert data into the specified table in the database, ensuring column count matches."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Retrieve column count from the database for the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    column_info = cursor.fetchall()
    num_columns = len(column_info)

    # Prepare the SQL statement
    placeholders = ', '.join(['?'] * num_columns)
    sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

    inserted_rows = 0
    for idx, row in data.iterrows():
        # Ensure the row has the correct number of columns
        if len(row) == num_columns:
            try:
                cursor.execute(sql, tuple(row))
                conn.commit()
                inserted_rows += 1
            except sqlite3.IntegrityError as e:
                st.error(f"Integrity error on inserting data into {table_name}: {e}")
                continue  # Optionally, continue to the next row or handle differently
        else:
            st.error(f"Column mismatch: The table {table_name} expects {num_columns} columns, but the provided data row has {len(row)} columns.")

    conn.close()
    st.success(f"Inserted {inserted_rows} rows into {table_name} successfully.")

def verify_inserts(table_name):
    """Query the database to count rows and display some sample data to verify inserts."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    st.write(f"Total rows in {table_name}: {row_count}")

    if row_count > 0:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
        sample_data = cursor.fetchall()
        st.write(f"Sample data from {table_name}: {sample_data}")

    conn.close()

import random
def openai_generator(schema, table_and_rows, chunk_size=100):
    """Generate data using OpenAI API."""
    final_output = {}
    table_rows_dict = {table.split(':')[0]: int(table.split(':')[1]) for table in table_and_rows.split(", ")}
    

    for table, rows_requested in table_rows_dict.items():
        rows_generated = 0
        table_tmp = []
        while rows_generated < rows_requested:
            rows_to_generate = min(chunk_size, rows_requested - rows_generated)
            try:
                response = OpenAI.chat.completions.create(
                    model="gpt-3.5-turbo",  # Adjust the model as per requirement
                    messages=[
                        {"role": "system", "content": "You are a data curator who is an expert at generating realistic synthetic data."},
                        {"role": "user", "content": f"Generating unique dataset {random.randint(1, 100000)}. Analyze the following schema - {schema}. Please generate {rows_to_generate} entries to populate the {table} table in valid CSV format with the correct header for each column. The data generated needs to be consistent with the foreign and primary keys. Do not include any additional text like 'certainly... here you go' or unnecessary characters, only response with the requested data."}
                    ],
                    max_tokens=1500
                )
                if response.choices[0].message.content.strip():  # Check if text is not empty
                    table_tmp.append(pd.read_csv(StringIO(response.choices[0].message.content.strip())))
                rows_generated += rows_to_generate
            except Exception as e:
                st.error(f"An error occurred while generating data for {table}: {e}")
                continue
                # return None  # Early exit on failure
        if table_tmp:
            final_output[table] = pd.concat(table_tmp, ignore_index=True)
        else:
            st.error(f"No data was generated for {table}.")
            return None  # Early exit if no data is generated
    
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
    st.write("Configuration for Data Generation:")
    chunk_size = st.sidebar.number_input('Chunk Size', value=200, min_value=100, max_value=1000, step=100)
    total_records = st.sidebar.number_input('Total Records per Table', value=10000, min_value=1000, max_value=50000, step=1000)

    table_and_rows = ", ".join([f"{table}: {total_records}" for table in st.session_state['tables']])
    if st.button("Generate and Insert Data"):
        dataframes_dict = openai_generator(st.session_state['schema'], table_and_rows, chunk_size)
        if dataframes_dict is not None:
            for table, df in dataframes_dict.items():
                insert_data(table, df)
                verify_inserts(table)  # Verify and display results after inserts
            st.success("Data successfully generated and inserted into the database.")
        else:
            st.error("Failed to generate data. Please check the logs for errors.")

if st.button("Download Database"):
    with open(DB_PATH, "rb") as file:
        st.download_button("Download SQLite Database", file, file_name="synthetic_data.db", mime="application/octet-stream")

st.write("Session State:", st.session_state)
