# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Zinc Persona Generator",
        page_icon="👋",
    )

    st.write("# Persona maker 👋")

    st.sidebar.success("Select some options.")

    st.markdown(
        """
This is a cool tool        Machine Learning and Data Science projects.
        **👈 Select a role, or job to be done f
     
    """
    )

# Example for reading a CSV file
industry_df = pd.read_csv('https://raw.githubusercontent.com/althoughh/persona/main/Untitled%20spreadsheet%20-%20industry.csv')
jtbd_df = pd.read_csv('https://raw.githubusercontent.com/althoughh/persona/main/Untitled%20spreadsheet%20-%20jtbd.csv')
role_df = pd.read_csv('https://raw.githubusercontent.com/althoughh/persona/main/Untitled%20spreadsheet%20-%20role.csv')

# Dropdown for Role selection
selected_role = st.selectbox("Select a Role", options=role_df['Role'].unique())
# Filter the jtbd_df based on the selected role
filtered_jtbd = jtbd_df[jtbd_df['Mapped Role'] == selected_role]
# Dropdown for Job to be Done selection
selected_job = st.selectbox("Select a Job to be Done", options=filtered_jtbd['Job Name'].unique())
# Filter the data based on the selected job
job_info = filtered_jtbd[filtered_jtbd['Job Name'] == selected_job]
# Get the data for the selected role
role_info = role_df[role_df['Role'] == selected_role]

# Display the role information
if not role_info.empty:
    st.subheader(f"Information for Role: {selected_role}")
    for column in role_info.columns:
        st.write(f"**{column}:** {role_info.iloc[0][column]}")
else:
    st.write("No additional information available for this role.")

# Check if a role is selected before displaying JTBD options
if selected_role:
    # Filter the jtbd_df based on the selected role
    filtered_jtbd = jtbd_df[jtbd_df['Mapped Role'] == selected_role]

    # Dropdown for Job to be Done selection
    selected_job = st.selectbox("Select a Job to be Done", options=[''] + list(filtered_jtbd['Job Name'].unique()))

    # Display JTBD information only if a job is selected
    if selected_job:
        # Filter the data based on the selected job
        job_info = filtered_jtbd[filtered_jtbd['Job Name'] == selected_job]

        # Display the job information
        for column in job_info.columns:
            st.write(f"**{column}:** {job_info.iloc[0][column]}")
else:
    st.write("Please select a role to see the Jobs to be Done.")

if __name__ == "__main__":
    run()
