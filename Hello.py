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

    # Display information in grid layout with different card styles
    if selected_industry:
        display_info_with_cards(industry_df[industry_df['Industry'] == selected_industry], "industry")
    if selected_role:
        display_info_with_cards(role_df[role_df['Role'] == selected_role], "role")
    if selected_job:
        display_info_with_cards(jtbd_df[jtbd_df['Job Name'] == selected_job], "job")

def display_info_with_cards(df, section):
    if not df.empty:
        columns = st.columns(4)  # Adjust the number of columns as needed
        for i, column in enumerate(df.columns):
            with columns[i % 4]:  # Adjust the modulo as per the number of columns
                content = df.iloc[0][column]
                card_html = get_bootstrap_card_html(column, content, section)
                st.markdown(card_html, unsafe_allow_html=True)

def get_bootstrap_card_html(title, content, section):
    if section == "industry":
        # Customize for industry
        card_color = "primary"
    elif section == "role":
        # Customize for role
        card_color = "success"
    else:
        # Customize for job
        card_color = "warning"

    return f"""
        <div class="card border-{card_color} mb-3" style="max-width: 18rem;">
            <div class="card-header bg-transparent border-{card_color}">{title}</div>
            <div class="card-body text-{card_color}">
                <h5 class="card-title">{title}</h5>
                <p class="card-text">{content}</p>
            </div>
            <div class="card-footer bg-transparent border-{card_color}">Footer</div>
        </div>
    """

if __name__ == "__main__":
    run()
