import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the App
st.title("Spreadsheet Dashboard Creator")

# File Upload Section
st.sidebar.header("Upload Spreadsheet")
file = st.sidebar.file_uploader("Upload your Excel or CSV file", type=["xlsx", "xls", "csv"])

if file:
    try:
        # Determine file type and load data
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.sidebar.success("File uploaded successfully!")

        # Display the DataFrame
        st.write("### Preview of the Data")
        st.dataframe(df.head())

        # Select Column for Analysis
        st.sidebar.header("Visualization Settings")
        numeric_columns = df.select_dtypes(include=['number']).columns
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns

        if not numeric_columns.empty and not categorical_columns.empty:
            x_axis = st.sidebar.selectbox("Select X-axis column", categorical_columns)
            y_axis = st.sidebar.selectbox("Select Y-axis column", numeric_columns)

            # Plotly Visualization
            st.write("### Interactive Visualization")
            chart = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
            st.plotly_chart(chart, use_container_width=True)

        else:
            st.warning("Ensure your dataset has both categorical and numeric columns for dashboard creation.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.sidebar.info("Awaiting file upload...")
