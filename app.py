import streamlit as st
import pandas as pd
import re

# Set page configuration
st.set_page_config(
    page_title="Hockey Canada Rules: Quick Reference",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define Canada Red color
CANADA_RED = "#C8102E"

# Custom CSS for a more professional layout with Canada Red theme
st.markdown(f"""
<style>
    /* Page background */
    .main-content {{
        background-color: #FFFFFF;
        padding: 1rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }}

    /* Header styles */
    .main-header {{
        background-color: {CANADA_RED};
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 2rem;
    }}
    .main-header h1 {{
        margin: 0;
        font-size: 2rem;
    }}

    /* Sidebar container */
    .sidebar-container {{
        background-color: #FFF;
        border-radius: 6px;
        padding: 1rem;
        border: 1px solid #EEE;
        margin-bottom: 1rem;
    }}
    .sidebar-title {{
        font-weight: 600;
        color: {CANADA_RED};
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }}
    .sidebar-icon {{
        margin-right: 6px;
        color: {CANADA_RED};
        vertical-align: middle;
    }}

    /* Collapsable expander styling */
    .st-expander {{
        border: 1px solid #DDD !important;
        border-radius: 6px !important;
        margin-bottom: 1rem !important;
    }}
    .st-expander > div > label {{
        padding: 0.6rem 1rem !important;
        font-weight: 600;
        color: {CANADA_RED};
    }}

    /* Section headings */
    h3 {{
        color: {CANADA_RED};
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }}

    /* Rule table styling */
    .stDataFrame > div {{
        max-width: 100%;
    }}

    /* Footer styling */
    .footer {{
        text-align: center;
        padding: 1rem 0;
        margin-top: 3rem;
        border-top: 1px solid #eee;
        color: #999;
        font-size: 0.85rem;
    }}
</style>
""", unsafe_allow_html=True)

# Custom page header
st.markdown("""
<div class="main-header">
  <h1>Hockey Canada Rules Reference</h1>
</div>
""", unsafe_allow_html=True)

# Improved helper function to sort rule numbers correctly
def numeric_sort_key(rule_num):
    # Remove parentheses and any letters for sorting
    base_rule = rule_num.split('(')[0].strip()
    
    # Split by periods to handle decimal points correctly
    parts = base_rule.split('.')
    
    # Convert each part to integers for proper numerical sorting
    # This ensures 1.10 comes after 1.9, not before 1.2
    result = []
    for part in parts:
        try:
            result.append(int(part))
        except ValueError:
            # If conversion fails, use the original string
            result.append(part)
    
    return result

# Helper function to get section icon
def get_section_icon(section):
    icons = {
        "PLAYING AREA": "🏟️",
        "TEAMS": "👥",
        "EQUIPMENT": "🏒",
        "TYPES OF PENALTIES": "⚠️",
        "OFFICIALS": "👮",
        "GAME FLOW": "⏱️",
        "PHYSICAL FOULS": "💥",
        "RESTRAINING FOULS": "🛑",
        "STICK FOULS": "🏑",
        "OTHER FOULS": "⚖️",
        "MALTREATMENT": "🚫"
    }
    return icons.get(section, "📖")

# Helper function to get base rule number without parentheses
def get_base_rule_number(rule_number):
    return rule_number.split('(')[0].strip()

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("hockey_rules.csv")
    
    # Create a section order mapping based on rulebook structure
    # Rules are organized in sections with numbers 1-11
    section_order = {
        "PLAYING AREA": 1,
        "TEAMS": 2,
        "EQUIPMENT": 3,
        "TYPES OF PENALTIES": 4,
        "OFFICIALS": 5,
        "GAME FLOW": 6,
        "PHYSICAL FOULS": 7,
        "RESTRAINING FOULS": 8,
        "STICK FOULS": 9,
        "OTHER FOULS": 10,
        "MALTREATMENT": 11
    }
    
    # Add a numerical column for section ordering
    df['section_order'] = df['Section'].map(section_order)
    
    # Add base rule number (without parentheses) for grouping
    df['base_rule'] = df['Rule #'].apply(get_base_rule_number)
    
    return df, section_order

df, section_order = load_data()

# Remove fancy markdown from the sidebar
with st.sidebar:
    # Minimal text label for search
    st.write("Keyword Search")

    # Use session_state to store query so we can clear it
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""

    # Text input for search with a proper label
    search_input = st.text_input(
        "Search term",  # Providing a non-empty label
        value=st.session_state["search_query"],
        label_visibility="collapsed"  # Hide the label visually
    )
    st.session_state["search_query"] = search_input

    # Clear search button
    if st.button("Clear Search", key="clear_btn"):
        st.session_state["search_query"] = ""
        st.rerun()  # Using st.rerun() instead of deprecated st.experimental_rerun()

    # ---------------------------------------------
    # Section filtering with checkboxes
    st.write("Sections to display")
    all_sections = df["Section"].unique()
    # Sort sections by their numeric order defined in section_order
    all_sections_sorted = sorted(all_sections, key=lambda s: section_order.get(s, 9999))

    # Provide a "Select All" option
    select_all = st.checkbox("Select All", value=True, key="select_all")
    
    selected_sections = []
    for sec in all_sections_sorted:
        # Default to checked if select_all is true
        checked = st.checkbox(sec, value=select_all, key=f"cb_{sec}")
        if checked:
            selected_sections.append(sec)
    # ---------------------------------------------

# Use st.session_state["search_query"] for filtering
search_query = st.session_state["search_query"]

# Create a fresh copy of the dataframe to work with
filtered_df = df.copy()

# Apply search filter if there is a query
if search_query:
    filtered_df = filtered_df[
        (filtered_df["Rule Name"].str.contains(search_query, case=False)) |
        (filtered_df["Description"].str.contains(search_query, case=False)) |
        (filtered_df["Rule #"].str.contains(search_query, case=False))
    ]
    # Show how many are found
    st.write(f"Found {len(filtered_df)} matching rules.")

# Apply the section filter if there are selected sections
if selected_sections:
    filtered_df = filtered_df[filtered_df["Section"].isin(selected_sections)]

# Add sort_key column to a proper copy of the DataFrame
filtered_df.loc[:, 'sort_key'] = filtered_df['base_rule'].apply(numeric_sort_key)
filtered_df = filtered_df.sort_values(by='sort_key')

# Get the unique sections to display
sections = filtered_df.sort_values("section_order")["Section"].unique()

# Wrap main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Configure column widths for the dataframe
column_config = {
    "Rule #": st.column_config.TextColumn(
        "Rule #",
        width="small",  # Set to small to take minimum required width
        help="Rule number reference"
    ),
    "Description": st.column_config.TextColumn(
        "Description",
        width="large",  # Make description take up most of the space
        help="Rule description"
    )
}

# Display sections in the main area
for section in sections:
    section_df = filtered_df[filtered_df["Section"] == section].copy()
    rule_count = len(section_df)
    if rule_count == 0:
        continue

    # Add icon
    section_icon = get_section_icon(section)
    section_num = section_order[section]

    with st.expander(f"{section_icon} {section_num}. {section} ({rule_count} rules)", expanded=bool(search_query)):
        # Process base rules in order
        # Add sort_key to this DataFrame too using .loc to avoid SettingWithCopyWarning
        section_df.loc[:, 'sort_key'] = section_df['base_rule'].apply(numeric_sort_key)
        section_df = section_df.sort_values(by='sort_key')
        
        base_rules_ordered = []
        for _, row in section_df.iterrows():
            if row['base_rule'] not in base_rules_ordered:
                base_rules_ordered.append(row['base_rule'])

        for base_rule in base_rules_ordered:
            base_rule_items = section_df[section_df['base_rule'] == base_rule].copy()
            rule_names = base_rule_items["Rule Name"].unique()

            for rule_name in rule_names:
                rule_items = base_rule_items[base_rule_items["Rule Name"] == rule_name].copy()

                st.markdown(f"### {base_rule} {rule_name}")
                rule_items = rule_items.sort_values(by="Rule #")  # sorts subsections like (a), (b)
                table_df = rule_items[["Rule #", "Description"]].reset_index(drop=True)
                
                # Display dataframe with column configuration for optimal widths
                st.dataframe(
                    table_df, 
                    hide_index=True, 
                    use_container_width=True,
                    column_config=column_config
                )

# Footer
st.markdown("""
<div class="footer">
  © 2025 Patrick A. Mikkelsen · Powered by Streamlit
</div>
""", unsafe_allow_html=True)

# Close main content container
st.markdown('</div>', unsafe_allow_html=True)
