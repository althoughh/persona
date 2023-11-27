import streamlit as st
import pandas as pd

# Set the page config at the very start
st.set_page_config(
    page_title="Zinc Persona Generator",
    page_icon="👋",
)

def run():
    st.write("# Persona maker 👋")
    st.sidebar.success("Select some options.")
    st.markdown("""
        This is a cool tool for Machine Learning and Data Science projects.
        **👈 Select a role, or job to be done from the sidebar.**
    """)

    # Reading CSV files
    industry_df = pd.read_csv('https://raw.githubusercontent.com/.../industry.csv')
    jtbd_df = pd.read_csv('https://raw.githubusercontent.com/.../jtbd.csv')
    role_df = pd.read_csv('https://raw.githubusercontent.com/.../role.csv')

    # Sidebar Dropdown for Role selection
    selected_role = st.sidebar.selectbox("Select a Role", options=role_df['Role'].unique())

    # Display role information
    role_info = role_df[role_df['Role'] == selected_role]
    if not role_info.empty:
        st.subheader(f"Information for Role: {selected_role}")
        for column in role_info.columns:
            st.write(f"**{column}:** {role_info.iloc[0][column]}")

    # Sidebar Dropdown for Job to be Done selection, shown only if a role is selected
    if selected_role:
        filtered_jtbd = jtbd_df[jtbd_df['Mapped Role'] == selected_role]
        selected_job = st.sidebar.selectbox("Select a Job to be Done", options=[''] + list(filtered_jtbd['Job Name'].unique()))

        # Display JTBD information only if a job is selected
        if selected_job:
            job_info = filtered_jtbd[filtered_jtbd['Job Name'] == selected_job]
            for column in job_info.columns:
                st.write(f"**{column}:** {job_info.iloc[0][column]}")

if __name__ == "__main__":
    run()
