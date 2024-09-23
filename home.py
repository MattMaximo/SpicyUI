import streamlit as st
import spice
import polars as pl
import os
import re

# Streamlit interface
st.title('Dune Query Interface')

# Input fields
api_key = st.text_input('Enter your Dune API Key', type='password')
query = st.text_input('Enter Dune Query ID')
params = st.text_area('Optional Parameters (e.g., {"network": "ethereum"})', '{}')
refresh = st.checkbox('Refresh (leaving unchecked will use cached results)', value=False)

# Function to extract query ID from URL or use the direct ID
def extract_query_id(query_input):
    if query_input.isdigit():
        return query_input
    match = re.search(r'queries/(\d+)', query_input)
    if match:
        return match.group(1)
    return 'custom_query'

# Button to run the query
if st.button('Run Query'):
    # Set the API key as an environment variable
    os.environ['DUNE_API_KEY'] = api_key

    # Parse parameters
    try:
        parameters = eval(params)
        if not isinstance(parameters, dict):
            st.error("Parameters must be a valid dictionary")
        else:
            # Extract query ID for naming the CSV
            query_id = extract_query_id(query)
            
            # Execute the query
            df = spice.query(query, parameters=parameters, refresh=refresh)
            st.success("Query executed successfully!")
            st.dataframe(df.to_pandas())  # Display as pandas DataFrame for Streamlit

            # Allow user to download the result as CSV with custom filename
            csv = df.write_csv()  # polars method to write CSV to string
            filename = f'{query_id}_results.csv'
            st.download_button(f'Download CSV ({filename})', csv, filename)
    except Exception as e:
        st.error(f"Error: {str(e)}")