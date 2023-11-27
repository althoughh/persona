import streamlit as st
import pandas as pd

def run():
    st.sidebar.success("Select some options.")

    # Load the CSV files
    industry_df = pd.read_csv('industry.csv')
    jtbd_df = pd.read_csv('jtbd.csv')
    role_df = pd.read_csv('role.csv')

    # Sidebar Dropdown for Industry selection
    selected_industry = st.sidebar.selectbox("Select an Industry", options=industry_df['Industry'].unique())
 # Display industry information in separate boxes
    industry_info = industry_df[industry_df['Industry'] == selected_industry]
   if not industry_info.empty:
        for column in industry_info.columns:
            with st.container():
                st.markdown(f"**{column}**")
                st.text_area("", industry_info.iloc[0][column], height=100, key=f"industry_{column}")

    # Filter roles and jtbd based on the selected industry
    filtered_role = role_df[role_df['Industry'] == selected_industry]

    # Sidebar Dropdown for Role selection based on Industry
    selected_role = st.sidebar.selectbox("Select a Role", options=[''] + list(filtered_role['Role'].unique()))

    # Display role information in styled boxes
    if selected_role:
        role_info = filtered_role[filtered_role['Role'] == selected_role]
        if not role_info.empty:
            for column in role_info.columns:
                with st.container():
                    st.markdown(f"**{column}**")
                    st.text_area("", role_info.iloc[0][column], height=100, key=f"role_{column}")

        # Filtered JTBD based on the selected role
        filtered_jtbd = jtbd_df[jtbd_df['Mapped Role'] == selected_role]
        selected_job = st.sidebar.selectbox("Select a Job to be Done", options=[''] + list(filtered_jtbd['Job Name'].unique()))

        # Display JTBD information in styled boxes if a job is selected
        if selected_job:
            job_info = filtered_jtbd[filtered_jtbd['Job Name'] == selected_job]
            for column in job_info.columns:
                with st.container():
                    st.markdown(f"**{column}**")
                    st.text_area("", job_info.iloc[0][column], height=100, key=f"jtbd_{column}")

if __name__ == "__main__":
    run()
