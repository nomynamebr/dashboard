import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Multi-Tab Dashboard")

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    xls = pd.ExcelFile(uploaded_file)
    sheets = xls.sheet_names

    # Sort sheets based on their numerical prefix
    def extract_number(sheet_name):
        return int(sheet_name.split('-')[0]) if sheet_name[0].isdigit() else float('inf')

    sorted_sheets = sorted(sheets, key=extract_number)

    for sheet in sorted_sheets:
        st.header(sheet)
        df = pd.read_excel(xls, sheet_name=sheet)

        if sheet == "5-mfa_password":
            col1, col2, col3 = st.columns(3)
            min_password_length = df['minimum_password_length'].values[0]
            col1.metric("Minimum Password Length", min_password_length)
            if min_password_length >= 10:
                col1.success("Meets security standards")
            else:
                col1.warning("Below recommended length")
            col2.metric("Invalid Login Threshold", df['invalid_login_threshold'].values[0])
            col3.metric("Invalid Login Treatment", df['invalid_login_treatment'].values[0])

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=min_password_length,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Password Strength", 'font': {'size': 24}},
                gauge={
                    'axis': {'range': [None, 20], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 8], 'color': 'red'},
                        {'range': [8, 12], 'color': 'yellow'},
                        {'range': [12, 20], 'color': 'green'}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 10}}))
            st.plotly_chart(fig)

        elif sheet == "6-cookie_overview":
            st.title("Cookie Overview Dashboard")

            # Create columns for filters at the top of the page
            col1, col2 = st.columns(2)

            with col1:
                auto_blocking_filter = st.selectbox("Filter by Auto-blocking:", ["All", True, False])

            with col2:
                auto_scan_filter = st.selectbox("Filter by Auto-scan:", ["All", True, False])

            # Apply filters
            filtered_df = df

            if auto_blocking_filter != "All":
                filtered_df = filtered_df[filtered_df['auto_blocking_enabled'] == auto_blocking_filter]

            if auto_scan_filter != "All":
                filtered_df = filtered_df[filtered_df['auto_scan'] == auto_scan_filter]

            # Display charts
            col3, col4 = st.columns(2)

            with col3:
                st.subheader("Auto-blocking Overview")
                fig_auto_blocking = px.pie(filtered_df, names='auto_blocking_enabled', title="Auto-blocking Enabled")
                st.plotly_chart(fig_auto_blocking, use_container_width=True)

            with col4:
                st.subheader("Auto-scan Overview")
                fig_auto_scan = px.pie(filtered_df, names='auto_scan', title="Auto-scan Enabled")
                st.plotly_chart(fig_auto_scan, use_container_width=True)

            # Display filtered sites
            st.subheader("Filtered Sites")
            st.dataframe(filtered_df[['url', 'auto_blocking_enabled', 'auto_scan', 'total_cookies']])

        elif sheet == "2-data_systems":#done
          # Create filters
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                data_type_options = ['All'] + list(df['data_type'].unique())
                selected_data_type = st.selectbox("Filter by Data Type:", data_type_options)

            with col2:
                connector_type_options = ['All'] + list(df['ds_connector_type'].unique())
                selected_connector_type = st.selectbox("Filter by Connector Type:", connector_type_options)

            with col3:
                state_options = ['All'] + list(df['state'].unique())
                selected_state = st.selectbox("Filter by State:", state_options)

            with col4:
                workflow_enabled_options = ['All', True, False]
                selected_workflow_enabled = st.selectbox("Filter by Workflow Enabled:", workflow_enabled_options)

            # Apply filters
            filtered_df = df

            if selected_data_type != 'All':
                filtered_df = filtered_df[filtered_df['data_type'] == selected_data_type]

            if selected_connector_type != 'All':
                filtered_df = filtered_df[filtered_df['ds_connector_type'] == selected_connector_type]

            if selected_state != 'All':
                filtered_df = filtered_df[filtered_df['state'] == selected_state]

            if selected_workflow_enabled != 'All':
                filtered_df = filtered_df[filtered_df['workflow_enabled'] == selected_workflow_enabled]

            

            # Create visualizations
            col1, col2, col3 = st.columns(3)

            # Display summary statistics
            st.subheader("Summary Statistics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Data Systems", len(filtered_df))
            col2.metric("Unique Connector Types", filtered_df['ds_connector_type'].nunique())
            col3.metric("Workflows Enabled", filtered_df['workflow_enabled'].sum())

            with col1:
                data_type_counts = filtered_df['data_type'].value_counts().reset_index()
                data_type_counts.columns = ['data_type', 'count']
                fig1 = px.pie(data_type_counts, names='data_type', values='count', title='Data Type Distribution')
                fig1.update_traces(textposition='inside', textinfo='value+label')
                st.plotly_chart(fig1)
            
            with col3:
                fig2 = px.bar(filtered_df['ds_connector_type'].value_counts(), title='Connector Type Distribution')
                st.plotly_chart(fig2)
            # Display filtered data
            st.subheader("Filtered Data Systems")
            st.dataframe(filtered_df[['name', 'data_type', 'ds_connector_type', 'state', 'workflow_enabled']])
   
        elif sheet == "1-pod":#done
            st.subheader("Pod Overview")

            # Create three columns for filters
            col1, col2, col3 = st.columns(3)

            with col1:
                status_options = ['All'] + list(df['status'].unique())
                selected_status = st.selectbox("Filter by Status:", status_options)

            with col2:
                version_options = ['All'] + list(df['cluster_current_version'].unique())
                selected_version = st.selectbox("Filter by Pod Version:", version_options)

            with col3:
                auto_update_options = ['All', True, False]
                selected_auto_update = st.selectbox("Filter by Auto-update:", auto_update_options)

            # Apply filters
            filtered_df = df
            if selected_status != 'All':
                filtered_df = filtered_df[filtered_df['status'] == selected_status]
            if selected_version != 'All':
                filtered_df = filtered_df[filtered_df['cluster_current_version'] == selected_version]
            if selected_auto_update != 'All':
                filtered_df = filtered_df[filtered_df['auto_update'] == selected_auto_update]

            # Create visualizations
            fig1 = px.bar(filtered_df, x='name', y='connector_thread_count', 
                        color='status', title='Connector Thread Count by Pod',
                        hover_data=['name', 'status', 'cluster_current_version', 'auto_update'])
            st.plotly_chart(fig1)

            fig3 = px.histogram(filtered_df, x='cluster_current_version', title='Pod Version Distribution')
            st.plotly_chart(fig3)

            # New pie chart for auto-update distribution
            #st.subheader("POD Auto-Update")
            auto_update_counts = df['auto_update'].value_counts()
            fig_auto_update = px.pie(
                values=auto_update_counts.values,
                names=auto_update_counts.index,
                title="POD - Auto-Update"
            )
            st.plotly_chart(fig_auto_update)

           

            # Display filtered data
            st.subheader("Filtered Pod Data")
            st.dataframe(filtered_df[['name', 'status', 'connector_thread_count', 'cluster_current_version', 'auto_update']])

        elif sheet == "7-dsr_count":
            col1, col2, col3 = st.columns(3)
            col1.metric("Business Associated Units", df['business_associated_units_cnt'].values[0])
            col2.metric("Total Forms", df['forms_cnt'].values[0])
            col3.metric("Published Forms", df['forms_published_cnt'].values[0])

        elif sheet == "3-private_cloud_storage":#done
            if 'display_name' in df.columns:
                display_name = df['display_name'].iloc[0]
                st.metric("Display Name", display_name)
            else:
                st.error("The 'display_name' column was not found in the sheet.")

            allocated_storage_gb = round(df['storage_size'].values[0] / (1024**3), 2)
            st.metric("Storage Size (GB)", allocated_storage_gb)
            
        elif sheet == "4-csv_export": #done
           # Display the DataFrame
            st.dataframe(df)

            # Display summary statistics
            st.subheader("Summary Statistics")
            col1, col2 = st.columns(2)

            current_value = df['configValue'].values[0]
            recommended_value = ".zip"

            col1.metric("Current Configuration", current_value)
            col2.metric("Recommended Configuration", recommended_value)

            # Display comparison result
            if current_value == recommended_value:
                st.success("The current configuration matches the recommended format.")
            else:
                st.warning("The current configuration does not match the recommended format.")

            # Explanation
            st.subheader("Explanation")
            st.write("""
            The current configuration uses 'csv.gz' as the compressed CSV format. 
            However, the recommended format is '.zip'. 
            Using '.zip' can provide better compatibility and easier handling for most users.
            """)

            # Recommendation
            st.subheader("Recommendation")
            st.write("""
            Consider changing the 'setting_export_compressed_csv_format' to '.zip' 
            for improved compatibility and user experience.
            """)
        
        st.write("---")
else:
    st.info("Please upload an Excel file to begin.")
