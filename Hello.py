import streamlit as st
import pandas as pd

def run():
    st.sidebar.success("Select some options.")

    # Load the CSV files
    industry_df = pd.read_csv('industry.csv')
    jtbd_df = pd.read_csv('jtbd.csv')
    role_df = pd.read_csv('role.csv')

    # Sidebar Dropdowns
    selected_industry = st.sidebar.selectbox("Select an Industry", [''] + list(industry_df['Industry'].unique()))
    selected_role = st.sidebar.selectbox("Select a Role", [''] + list(role_df[role_df['Industry'] == selected_industry]['Role'].unique()) if selected_industry else [])
    selected_job = st.sidebar.selectbox("Select a Job to be Done", [''] + list(jtbd_df[jtbd_df['Mapped Role'] == selected_role]['Job Name'].unique()) if selected_role else [])

    # Injecting Bootstrap CSS
    st.markdown("""
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    """, unsafe_allow_html=True)

    # Display role information using Bootstrap cards
    if selected_role:
        role_info = role_df[role_df['Role'] == selected_role]
        if not role_info.empty:
            for column in role_info.columns:
                content = role_info.iloc[0][column]
                card_html = get_bootstrap_card_html(column, content)
                st.markdown(card_html, unsafe_allow_html=True)

def get_bootstrap_card_html(title, content):
    return f"""
        <div class="card border-success mb-3" style="max-width: 18rem;">
            <div class="card-header bg-transparent border-success">{title}</div>
            <div class="card-body text-success">
                <h5 class="card-title">{title}</h5>
                <p class="card-text">{content}</p>
            </div>
            <div class="card-footer bg-transparent border-success">Footer</div>
        </div>
    """

if __name__ == "__main__":
    run()
