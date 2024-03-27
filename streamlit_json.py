import streamlit as st
import openai as OpenAI
import json

# Configure OpenAI API key
OpenAI.api_key = st.secrets["OPENAI_API_KEY"]

def fileparser(definition_schema):
    """Decodes the uploaded JSON file."""
    content = json.loads(definition_schema.getvalue().decode("utf-8"))
    return content

def format_instruction(schema, n=5):
    """Formats the instruction to ChatGPT to ensure consistent response format."""
    instruction = f"Generate SQL INSERT statements for the following tables, providing {n} records for each table. The response should be a valid SQL dump file containing table creation and insert. The tables are as follows:\n\n"

    for table in schema["tables"]:
        column_names = [column["name"] for column in table["columns"]]
        instruction += f"Table: {table['name']}, Fields: {', '.join(column_names)}\n"
    instruction += "\nPlease format the INSERT statements as follows for each table:\n\n"
    instruction += "INSERT INTO table_name (field1, field2, ...) VALUES (value1, value2, ...);\n..."
    return instruction

def generate_synthetic_data(instruction, attempts=3):
    """Generates synthetic data in a structured format, retrying a specified number of attempts."""
    for _ in range(attempts):
        try:
            response = OpenAI.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an SQL expert and have no issues generating more than 5 rows of data.."},
                    {"role": "user", "content": instruction}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return ""
    return ""

# Streamlit Webapp Interface
st.title("Relational Database Generator")
st.text("This webapp accepts a database schema and generates a synthetic database.")

definition_schema = st.file_uploader("Upload a JSON file", type="json")

if definition_schema is not None:
    schema = fileparser(definition_schema)
    structured_instruction = format_instruction(schema, n=10)
    st.text_area("Formatted Instruction", value=structured_instruction, height=300, help="Formatted instruction for generating synthetic data.")
    
    if st.button("Generate Synthetic Data"):
        synthetic_data = generate_synthetic_data(structured_instruction)
        if synthetic_data:  # Only display if synthetic_data is not empty
            st.text_area("Synthetic SQL Data", value=synthetic_data, height=600, help="Synthetic SQL INSERT statements generated based on the schema.")

