import streamlit as st
import pandas as pd

def run():
    st.sidebar.success("Select some options.")

    # Load the CSV files
    industry_df = pd.read_csv('https://raw.githubusercontent.com/althoughh/persona/main/Untitled%20spreadsheet%20-%20industry%20(1).csv')
    jtbd_df = pd.read_csv('https://raw.githubusercontent.com/althoughh/persona/main/Untitled%20spreadsheet%20-%20jtbd.csv')
    role_df = pd.read_csv('https://raw.githubusercontent.com/althoughh/persona/main/Untitled%20spreadsheet%20-%20role.csv')

    # Sidebar Dropdown for Industry selection
    selected_industry = st.sidebar.selectbox("Select an Industry", options=industry_df['Industry'].unique())

    # Filter roles and jtbd based on the selected industry
    # Assuming 'Industry_Column_Name' in role_df and jtbd_df links to the industry
    filtered_role = role_df[role_df['Industry'] == selected_industry]
    filtered_jtbd = jtbd_df[jtbd_df['Industry'] == selected_industry]

    # Sidebar Dropdown for Role selection based on Industry
    selected_role = st.sidebar.selectbox("Select a Role", options=filtered_role['Role'].unique())

    # Display role information
    role_info = filtered_role[filtered_role['Role'] == selected_role]
    if not role_info.empty:
        st.subheader(f"Information for Role: {selected_role}")
        for column in role_info.columns:
            st.write(f"**{column}:** {role_info.iloc[0][column]}")

    # Sidebar Dropdown for Job to be Done selection based on Role
    if selected_role:
        filtered_jtbd = filtered_jtbd[filtered_jtbd['Mapped Role'] == selected_role]
        selected_job = st.sidebar.selectbox("Select a Job to be Done", options=[''] + list(filtered_jtbd['Job Name'].unique()))

        # Display JTBD information only if a job is selected
        if selected_job:
            job_info = filtered_jtbd[filtered_jtbd['Job Name'] == selected_job]
            for column in job_info.columns:
                st.write(f"**{column}:** {job_info.iloc[0][column]}")

if __name__ == "__main__":
    run()
