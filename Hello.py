import streamlit as st
import pandas as pd

def run():
    st.sidebar.success("Select some options.")

    # Load the CSV files
    industry_df = pd.read_csv('path/to/industry.csv')
    jtbd_df = pd.read_csv('path/to/jtbd.csv')
    role_df = pd.read_csv('path/to/role.csv')

    # Sidebar Dropdown for Industry selection
    selected_industry = st.sidebar.selectbox("Select an Industry", options=industry_df['Industry_Column_Name'].unique())

    # Display industry information
    industry_info = industry_df[industry_df['Industry_Column_Name'] == selected_industry]
    if not industry_info.empty:
        st.subheader(f"Information for Industry: {selected_industry}")
        for column in industry_info.columns:
            st.write(f"**{column}:** {industry_info.iloc[0][column]}")
    else:
        st.write("No additional information available for this industry.")

    # Filter roles and jtbd based on the selected industry
    filtered_role = role_df[role_df['industry'] == selected_industry]
    filtered_jtbd = jtbd_df[jtbd_df['industry'] == selected_industry]

    # Sidebar Dropdown for Role selection based on Industry
    if selected_industry:
        selected_role = st.sidebar.selectbox("Select a Role", options=[''] + list(filtered_role['Role'].unique()))

        # Display role information
        if selected_role:
            role_info = filtered_role[filtered_role['Role'] == selected_role]
            if not role_info.empty:
                st.subheader(f"Information for Role: {selected_role}")
                for column in role_info.columns:
                    st.write(f"**{column}:** {role_info.iloc[0][column]}")
            
            # Sidebar Dropdown for Job to be Done selection based on Role
            filtered_jtbd = filtered_jtbd[filtered_jtbd['Mapped Role'] == selected_role]
            selected_job = st.sidebar.selectbox("Select a Job to be Done", options=[''] + list(filtered_jtbd['Job Name'].unique()))

            # Display JTBD information only if a job is selected
            if selected_job:
                job_info = filtered_jtbd[filtered_jtbd['Job Name'] == selected_job]
                for column in job_info.columns:
                    st.write(f"**{column}:** {job_info.iloc[0][column]}")

if __name__ == "__main__":
    run()
