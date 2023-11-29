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

def get_content_ideas(df, selected_industry, selected_role):
    base_url = "https://zincwork.com/blog/"
    if selected_industry:
        df = df[df[selected_industry]]
    if selected_role:
        df = df[df[selected_role]]

    df['URL'] = base_url + df['Slug']
    return df[['Name', 'URL']]

def display_info_with_cards(df, section):
    if not df.empty:
        st.markdown(f"## {section.capitalize()}")  # Title for the container

        # Define the color scheme for each group
        color_scheme = {
            "Overview": "primary",
            "What Do They Need": "success",
            "How Do They Choose": "warning",
            "How Can We Serve Them": "info"
        }

        # Use the correct group headings based on the section
        for group, categories in group_headings[section].items():
            st.markdown(f"<h3 style='color: {color_scheme[group]};'>{group}</h3>", unsafe_allow_html=True)
            
            # Adjust the number of columns dynamically based on the number of categories
            num_columns = len(categories)
            columns_container = st.columns(num_columns)

            for i, category in enumerate(categories):
                if category in df.columns:
                    content = df.iloc[0][category]
                    card_html = get_bootstrap_card_html(category, content, color_scheme[group], num_columns)
                    with columns_container[i]:
                        st.markdown(card_html, unsafe_allow_html=True)

def get_bootstrap_card_html(title, content, card_color, num_columns):
    card_width = "100%"  # Adjust the width to 100% of the column
    return f"""
        <div style="width: {card_width}; margin: 2px; padding: 5px; border: 1px solid {card_color}; border-radius: 5px;">
            <h4 style="color: {card_color};">{title}</h4>
            <p style="font-size: 0.9em;">{content}</p>
        </div>
    """


def show_content_ideas(content_ideas):
    if content_ideas.empty:
        st.sidebar.write("No content ideas available for the selected criteria.")
    else:
        with st.sidebar.container():
            st.sidebar.markdown("<div style='border: 2px solid #4CAF50; padding: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
            st.sidebar.write("Content Ideas:")
            for index, row in content_ideas.iterrows():
                st.sidebar.markdown(f"<a href='{row['URL']}' target='_blank'>{row['Name']}</a>", unsafe_allow_html=True)
            st.sidebar.markdown("</div>", unsafe_allow_html=True)

def display_data_based_on_selection(industry_df, role_df, jtbd_df, selected_industry, selected_role, selected_job):
    if selected_industry:
        display_info_with_cards(industry_df[industry_df['Industry'] == selected_industry], "industry")
    if selected_role:
        display_info_with_cards(role_df[role_df['Role'] == selected_role], "role")
    if selected_job:
        display_info_with_cards(jtbd_df[jtbd_df['Job Name'] == selected_job], "job")

def run():
    st.sidebar.success("Select some options.")
   
    # Load the CSV files
    industry_df = pd.read_csv('industry.csv')
    jtbd_df = pd.read_csv('jtbd.csv')
    role_df = pd.read_csv('role.csv')
    content_df = pd.read_csv('blog.csv')

    # Sidebar Dropdowns
    selected_industry = st.sidebar.selectbox("Select an Industry", [''] + list(industry_df['Industry'].unique()))
    selected_role = st.sidebar.selectbox("Select a Role", [''] + list(role_df[role_df['Industry'] == selected_industry]['Role'].unique()) if selected_industry else [])
    selected_job = st.sidebar.selectbox("Select a Job to be Done", [''] + list(jtbd_df[jtbd_df['Mapped Role'] == selected_role]['Job Name'].unique()) if selected_role else [])

    display_data_based_on_selection(industry_df, role_df, jtbd_df, selected_industry, selected_role, selected_job)

    # Injecting Bootstrap CSS
    st.markdown("""
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    """, unsafe_allow_html=True)

    # Button in the sidebar for content ideas
    if st.sidebar.button("Get Content Ideas"):
        content_ideas = get_content_ideas(content_df, selected_industry, selected_role)
        show_content_ideas(content_ideas)

if __name__ == "__main__":
    run()
