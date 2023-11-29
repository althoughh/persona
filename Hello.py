import streamlit as st
import pandas as pd
# Define the group headings outside the functions to make it globally accessible
group_headings = {
    "industry": {
        "Overview": ["Industry Overview", "Regulatory Environment", "Impact on Operations"],
        "What Do They Need": ["Industry-Specific Needs", "Key Drivers for Background Checks", "Challenges and Concerns"],
        "How Do They Choose": ["Preferred Features in a Solution", "Decision Influencers"],
        "How Can We Serve Them": ["Common Roles Involved in Hiring Process", "Messaging and Communication"]
    },
    "role": {
        "Overview": ["Role", "Responsibilities"],
        "What Do They Need": ["Triggers", "Challenges/Pain Points", "Optimum Solution"],
        "How Do They Choose": ["Role in Buying Decision", "Role in Buying Committee", "Decision Making Criteria", "Buyer Journey"],
        "How Can We Serve Them": ["Messaging Needs", "Influences"]
    },
    "job": {
        "Overview": ["Job Name", "Importance"],
        "What Do They Need": ["Current Solutions", "Pain Points"],
        "How Do They Choose": ["Trigger"],
        "How Can We Serve Them": ["How Zinc Work Helps"]
    }
}
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
    display_data_based_on_selection(industry_df, role_df, jtbd_df, selected_industry, selected_role, selected_job)

def display_data_based_on_selection(industry_df, role_df, jtbd_df, selected_industry, selected_role, selected_job):
    if selected_industry:
        display_info_with_cards(industry_df[industry_df['Industry'] == selected_industry], "industry")
    if selected_role:
        display_info_with_cards(role_df[role_df['Role'] == selected_role], "role")
    if selected_job:
        display_info_with_cards(jtbd_df[jtbd_df['Job Name'] == selected_job], "job")
    # Injecting Bootstrap CSS
    st.markdown("""
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    """, unsafe_allow_html=True)

    # Display information based on selection
    if selected_industry:
        display_info_with_cards(industry_df[industry_df['Industry'] == selected_industry], "industry")  # Lowercase "industry"
    if selected_role:
        display_info_with_cards(role_df[role_df['Role'] == selected_role], "role")  # Lowercase "role"
    if selected_job:
        display_info_with_cards(jtbd_df[jtbd_df['Job Name'] == selected_job], "job")  # Lowercase "job"



def display_info_with_cards(df, section):
    if not df.empty:
        # Define the color scheme for each group
        color_scheme = {
            "Overview": "primary",
            "What Do They Need": "success",
            "How Do They Choose": "warning",
            "How Can We Serve Them": "info"
        }

        # Use the correct group headings based on the section
        for group, columns in group_headings[section].items():
            st.markdown(f"<h3 style='color: {color_scheme[group]};'>{group}</h3>", unsafe_allow_html=True)
            columns_container = st.columns(4)  # Adjust the number of columns as needed
            for i, column in enumerate(columns):
                if column in df.columns:
                    content = df.iloc[0][column]
                    card_html = get_bootstrap_card_html(column, content, color_scheme[group])
                    with columns_container[i % 4]:  # Adjust the modulo as per the number of columns
                        st.markdown(card_html, unsafe_allow_html=True)


   

        

def get_bootstrap_card_html(title, content, card_color):
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
