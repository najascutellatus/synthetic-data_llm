import streamlit as st
import openai as OpenAI
import pandas as pd
import numpy as np
import json
import re
import zipfile
from io import BytesIO
import base64

# Initialize session state variables if they are not already initialized
if 'schema' not in st.session_state:
    st.session_state.schema = ""
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = False
if 'tables_detected' not in st.session_state:
    st.session_state.tables_detected = False
if 'table_rows' not in st.session_state:
    st.session_state.table_rows = {}
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""

# Your existing API key setup
OpenAI.api_key = st.secrets["OPENAI_API_KEY"]

def fileparser(definition_schema):
    # this method decodes the sql file
    content = definition_schema.getvalue().decode("utf-8")
    return content

def detect_tables(schema):
    # this currently works with sql, need to be updated to handle json inputs
    pattern = re.compile(r"CREATE TABLE\s+([a-zA-Z_][a-zA-Z0-9_]*)", re.IGNORECASE)
    # Find all matches in the schema text
    tables = pattern.findall(schema)
    return tables

def openai_generator(schema, table_and_rows):
    MAX_TOKENS = 4096
    #returns an sql file for populating
    try:
        response = OpenAI.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful data analyst expert at generating synthetic data."},
            {"role": "user", "content": f"Analyze the following schema - {schema}. The following are the specification for the number of rows for each table - {table_and_rows}. Generate only csv entries to populate the tables. Separate each csv file with --- and add name of csv file before the entries. Include a heading row. Do not include any additional text"}
        ])
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def download_zip(output_text):
    # Split the output into different CSV files based on '---' delimiter
    sections = [section.strip() for section in output_text.strip().split('---') if section]
    
    # Initialize a bytes buffer for the zip file
    zip_buffer = BytesIO()

    # Create a zip file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for section in sections:
            # Split the section into the filename and data
            title, *data = section.split('\n')
            csv_content = '\n'.join(data)
            # Write the CSV file to the zip
            zip_file.writestr(title, csv_content)
    
    # Prepare the zip file for download
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

# Streamlit app code begins here
st.title("Relational Database Generator")
st.text("This webapp accepts a SQL schema and generates a synthetic database")

uploaded_schema = st.file_uploader("Upload a SQL file", type=["sql", "json"])

# Check if a file has been uploaded
if uploaded_schema is not None:
    # Process the uploaded file
    schema = fileparser(uploaded_schema)
    st.session_state.schema = schema  # Store the processed schema in session state
    st.session_state.uploaded = True  # Indicate that a file has been successfully uploaded

# Show the text area for the schema if a file has been uploaded
if st.session_state.uploaded:
    # Display the schema text area with the current schema from session state
    st.session_state.schema = st.text_area("Uploaded SQL Schema", value=st.session_state.schema, height=200, help="The SQL schema from your uploaded file.")

# Button to detect tables, shown only if a schema has been uploaded
if st.session_state.uploaded and st.button("Detect Tables"):
    # Detect tables from the schema and update session state
    st.session_state.tables = detect_tables(st.session_state.schema)
    st.session_state.tables_detected = True  # Mark tables as detected
    # Initialize or reset the row numbers for the detected tables
    for table in st.session_state.tables:
        st.session_state.table_rows[table] = 10

# Display detected tables and row configuration inputs if tables have been detected
if st.session_state.tables_detected:
    st.write("Detected tables and row configurations:")
    for table in st.session_state.tables:
        # Input for specifying the number of rows for each table
        st.session_state.table_rows[table] = st.number_input(f"Number of rows for {table}:", min_value=0, value=st.session_state.table_rows[table], step=1, key=table)

    # Button to confirm the number of rows for each table
    if st.button('Confirm Row Numbers'):
        # Generate and display the configurations
        table_and_rows = ", ".join([f"{table}: {st.session_state.table_rows[table]}" for table in st.session_state.tables])
        output_text = openai_generator(st.session_state.schema,table_and_rows)
        if output_text:
            st.session_state.output_text = output_text

# Show the generated data and download button if the data has been generated
if st.session_state.output_text:
    st.text_area("Synthetic Generated Database", value=st.session_state.output_text, height=400, help="Generated Database based on provided configuration.")
    # Button for downloading the data as a ZIP file
    #if st.button('Download Database'):
    zip_file = download_zip(st.session_state.output_text)
    st.download_button(
            label="Download Database as ZIP",
            data=zip_file,
            file_name="database.zip",
            mime='application/zip'
        )