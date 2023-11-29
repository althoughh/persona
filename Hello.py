import streamlit as st
import pandas as pd


st.set_page_config(page_title="The Ramsey Highlights", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 350px;
        margin-left: -350px;
    }
     
    """,
    unsafe_allow_html=True,
)


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
    if selected_industry:
        df = df[df[selected_industry]]
    if selected_role:
        df = df[df[selected_role]]

    return df['Name']  # Assuming 'Name' column contains the content titles


def run():
    # ... [earlier parts of your code]

def run():
    st.sidebar.success("Select some options.")
    
    # Load the CSV files
    industry_df = pd.read_csv('industry.csv')
    jtbd_df = pd.read_csv('jtbd.csv')
    role_df = pd.read_csv('role.csv')
    content_df = pd.read_csv('blog.csv')  # Ensure this is the correct path to your CSV

    # Sidebar Dropdowns
    selected_industry = st.sidebar.selectbox("Select an Industry", [''] + list(industry_df['Industry'].unique()))
    selected_role = st.sidebar.selectbox("Select a Role", [''] + list(role_df[role_df['Industry'] == selected_industry]['Role'].unique()) if selected_industry else [])
    selected_job = st.sidebar.selectbox("Select a Job to be Done", [''] + list(jtbd_df[jtbd_df['Mapped Role'] == selected_role]['Job Name'].unique()) if selected_role else [])

    display_data_based_on_selection(industry_df, role_df, jtbd_df, selected_industry, selected_role, selected_job)

    # Button to Get Content Ideas
    if st.button("Get Content Ideas"):
        content_ideas = get_content_ideas(content_df, selected_industry, selected_role)
        
        if content_ideas.empty:
            st.write("No content ideas available for the selected criteria.")
        else:
            st.write("Content Ideas:")
            for idea in content_ideas:
                st.write(idea)




    
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
        <div class="card border-{card_color} mb-3" style="width: {card_width};">
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
