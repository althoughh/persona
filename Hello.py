import streamlit as st
import pandas as pd
pip install st-card-component
from st_card_component import st_card

# Example usage

def run():
    st.sidebar.success("Select some options.")

    # Load the CSV files
    industry_df = pd.read_csv('industry.csv')
    jtbd_df = pd.read_csv('jtbd.csv')
    role_df = pd.read_csv('role.csv')


    # Sidebar Dropdown for Industry selection
    selected_industry = st.sidebar.selectbox("Select an Industry", options=[''] + list(industry_df['Industry'].unique()))

    if selected_industry:
        industry_info = industry_df[industry_df['Industry'] == selected_industry]

        # Define the groups for the cards
        groups = [
            ["Industry Overview", "Industry-Specific Needs", "Regulatory Environment"],
            ["Common Roles Involved in Hiring Process", "Challenges and Concerns", "Key Drivers for Background Checks"],
            ["Decision Influencers", "Preferred Features in a Solution", "Impact on Operations"],
            ["Messaging and Communication"]
        ]

        # Injecting Bootstrap CSS
        st.markdown("""
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        """, unsafe_allow_html=True)

        # Display the cards in a grid layout
        for group in groups:
            with st.container():
                for field in group:
                    content = industry_info[field].values[0] if field in industry_info else "No information"
                    st.markdown(get_card_html(field, content), unsafe_allow_html=True)

def get_card_html(title, content):
    return f"""
        <div class="card bg-light mb-3" style="max-width: 18rem;">
            <div class="card-header">{title}</div>
            <div class="card-body">
                <p class="card-text">{content}</p>
            </div>
        </div>
    """
   
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
