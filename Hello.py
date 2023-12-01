import streamlit as st
import pandas as pd
from PIL import Image
import gspread
from google.oauth2 import service_account
# Load the image for the page icon
im = Image.open("logo.png")

# Set Streamlit page configuration
st.set_page_config(
    page_title="Hello",
    page_icon=im,
    layout="wide",
)

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"
    ],
)
conn = connect(credentials=credentials)
client=gspread.authorize(credentials)

# Define custom styles for the main page and sidebar
main_style = """
<style>
body {
    background-color: #ffffff; /* White background for the main page */
}
</style>
"""

sidebar_style = """
<style>
[data-testid="stSidebar"] {
    background-color: #D3D3D3; /* Light grey background */
    color: #000000; /* Black text */
}
</style>
"""

# Apply main styles to the page
st.markdown(main_style, unsafe_allow_html=True)

# Define and apply custom styles for select input and list choices
select_input_style = """
<style>
/* The input itself */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    font-size: 16px !important;
}

/* The list of choices */
li>span {
    color: #333 !important;
    font-size: 16px;
    background-color: #ffff !important;
}

li {
    background-color: #ffff !important;
}
</style>
"""
st.markdown(select_input_style, unsafe_allow_html=True)

# Apply sidebar styles
st.markdown(sidebar_style, unsafe_allow_html=True)

# Define a color scheme dictionary
color_scheme = {
    "Overview": "#007bff",  # Blue
    "What Do They Need": "#28a745",  # Green
    "How Do They Choose": "#ffc107",  # Yellow
    "How Can We Serve Them": "#17a2b8"  # Cyan
}



sheet_id = '1Bs-YF1pQIYvMMD8Gn7FKkAcqZvMcAgyN_g2cjvDI8Yw'
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
database_df = pd.read_csv(csv_url, on_bad_lines='skip')


database_df = database_df.astype(str)
sheet_url = st.secrets["private_gsheets_url"] #this information should be included in streamlit secret
sheet = client.open_by_url(sheet_url).sheet1
sheet.update([database_df.columns.values.tolist()] + database_df.values.tolist())
st.success('Data has been written to Google Sheets')
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

def show_content_ideas(content_ideas):
    if content_ideas.empty:
        st.sidebar.write("No content ideas available for the selected criteria.")
    else:
        with st.sidebar.container():
            st.sidebar.markdown("<div style='border: 2px solid #4CAF50; padding: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
            st.sidebar.write("Content Ideas:")
            for index, row in content_ideas.iterrows():
                st.sidebar.markdown(f"<a href='{row['URL']}' target='_blank'>{row['Name']}</a>", unsafe_allow_html=True)

def display_info_with_cards(df, section, selected_value):
    if not df.empty:
        display_title = f"{section.capitalize()}: {selected_value}" if selected_value else section.capitalize()
        st.markdown(f"## {display_title}")

        for group, categories in group_headings[section].items():
            st.markdown(f"<h3>{group}</h3>", unsafe_allow_html=True)
            num_columns = len(categories)
            columns_container = st.columns(num_columns)

            for i, category in enumerate(categories):
                if category in df.columns:
                    content = df.iloc[0][category]
                    card_html = get_bootstrap_card_html(category, content, group, num_columns)
                    with columns_container[i]:
                        st.markdown(card_html, unsafe_allow_html=True)

def get_bootstrap_card_html(title, content, group, num_columns):
    card_color = color_scheme.get(group, "#6c757d") 
    card_width = "100%"
    return f"""
        <div style="width: {card_width}; margin: 2px; padding: 5px; 
                    border: 1px solid {card_color}; border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.15);">
           <b> <p style="color: {card_color}; margin-bottom: 0.5em;">{title}</p></b>
            <p style="font-size: 0.9em;">{content}</p>
        </div>
    """

def display_data_based_on_selection(industry_df, role_df, jtbd_df, selected_industry, selected_role, selected_job):
    # Pass the selected value to display_info_with_cards
    if selected_industry:
        display_info_with_cards(industry_df[industry_df['Industry'] == selected_industry], "industry", selected_industry)
    if selected_role:
        display_info_with_cards(role_df[role_df['Role'] == selected_role], "role", selected_role)
    if selected_job:
        display_info_with_cards(jtbd_df[jtbd_df['Job Name'] == selected_job], "job", selected_job)


def run():
    st.sidebar.success("Select some options.")
    # Load the CSV files
    industry_df = pd.read_csv('industry.csv')
    role_df = pd.read_csv('role.csv')
    jtbd_df = pd.read_csv('jtbd.csv')
    content_df = pd.read_csv('blog.csv')

    selected_industry = st.sidebar.selectbox("Select an Industry", [''] + list(industry_df['Industry'].unique()), key='select_industry')

    # Options for Role based on selected Industry
    if selected_industry:
        role_options = list(role_df[role_df['Industry'] == selected_industry]['Role'].unique())
    else:
        role_options = list(role_df['Role'].unique())

    selected_role = st.sidebar.selectbox("Select a Role", [''] + role_options, key='select_role')

    # Options for Job based on selected Role
    if selected_role:
        job_options = list(jtbd_df[jtbd_df['Mapped Role'] == selected_role]['Job Name'].unique())
    else:
        job_options = list(jtbd_df['Job Name'].unique())

    selected_job = st.sidebar.selectbox("Select a Job to be Done", [''] + job_options, key='select_job')

    display_data_based_on_selection(industry_df, role_df, jtbd_df, selected_industry, selected_role, selected_job)


    # Button in the sidebar for content ideas
    if st.sidebar.button("Get Content Ideas"):
        content_ideas = get_content_ideas(content_df, selected_industry, selected_role)
        show_content_ideas(content_ideas)

if __name__ == "__main__":
    run()


