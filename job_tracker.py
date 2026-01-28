import streamlit as st
import pandas as pd
from datetime import date

# Page Configuration
st.set_page_config(page_title="Strategic Job Tracker", layout="wide")

# Initialize Session State for Data Persistence
if 'job_data' not in st.session_state:
    st.session_state.job_data = pd.DataFrame(columns=[
        "Date", "Company", "Role", "Type", "HR Contact", "Status", "Notes"
    ])

def save_application(date_app, company, role, app_type, contact, status, notes):
    new_entry = pd.DataFrame([{
        "Date": date_app,
        "Company": company,
        "Role": role,
        "Type": app_type,
        "HR Contact": contact,
        "Status": status,
        "Notes": notes
    }])
    st.session_state.job_data = pd.concat([st.session_state.job_data, new_entry], ignore_index=True)

# Sidebar Navigation
page = st.sidebar.radio("Navigate", ["Application Tracker", "Strategic Hunt & Advice"])

# --- PAGE 1: APPLICATION TRACKER ---
if page == "Application Tracker":
    st.title("📊 Application Command Center")
    
    # Input Form
    with st.expander("➕ Log a New Interaction", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            d_date = st.date_input("Date", date.today())
            d_company = st.text_input("Organization Name")
        with col2:
            d_role = st.text_input("Role / Title")
            d_type = st.selectbox("Interaction Type", ["Formal Application", "LinkedIn DM", "Referral Chat", "Recruiter Call", "Cold Email"])
        with col3:
            d_contact = st.text_input("Contact Person/Email")
            d_status = st.selectbox("Current Status", ["Applied", "Conversation Started", "Interviewing", "Offer", "Rejected", "Ghosted"])
        
        d_notes = st.text_area("Key Notes / Follow-up Plan")
        
        if st.button("Add Entry"):
            save_application(d_date, d_company, d_role, d_type, d_contact, d_status, d_notes)
            st.success(f"Logged interaction with {d_company}!")
            st.rerun()

    # Dashboard & Filters
    st.divider()
    st.subheader("Your Pipeline")
    
    if not st.session_state.job_data.empty:
        # Filters
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            status_filter = st.multiselect("Filter by Status", st.session_state.job_data['Status'].unique())
        with f_col2:
            type_filter = st.multiselect("Filter by Type", st.session_state.job_data['Type'].unique())
        
        # Apply Filters
        df_view = st.session_state.job_data
        if status_filter:
            df_view = df_view[df_view['Status'].isin(status_filter)]
        if type_filter:
            df_view = df_view[df_view['Type'].isin(type_filter)]
            
        # Editable Dataframe
        edited_df = st.data_editor(
            df_view,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Applied", "Conversation Started", "Interviewing", "Offer", "Rejected", "Ghosted"],
                    required=True
                )
            }
        )
        # Update session state if edited
        st.session_state.job_data = edited_df
    else:
        st.info("No applications tracked yet. Use the form above to get started.")

# --- PAGE 2: STRATEGIC ADVICE ---
elif page == "Strategic Hunt & Advice":
    st.title("🎯 Targeted Strategy: Ops & Program Management")
    st.markdown("Tailored recommendations based on your background in Logistics, EV, and Startups.")

    tab1, tab2, tab3 = st.tabs(["Target Industries", "Resume Hooks", "Search Tactics"])

    with tab1:
        st.header("Where You Fit Best")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("1. EV & Clean Mobility")
            st.write("*Why:* You have direct experience managing asset pilferage and claims at *Battery Smart*.")
            st.write("*Target Orgs:*")
            st.markdown("- *OEMs:* Ather Energy, Ola Electric, TVS Electric")
            st.markdown("- *Infra/MaaS:* BluSmart, Yulu, Zypp Electric, Bolt.Earth")
            st.info("Focus on roles like: City Operations Head, Asset Manager, Program Manager - Trust & Safety")

        with col_b:
            st.subheader("2. Logistics & E-commerce")
            st.write("*Why:* Your tenure at *Delhivery* (FTL ops) and *Shiprocket* (Weight discrepancies) proves you can handle high-volume supply chains.")
            st.write("*Target Orgs:*")
            st.markdown("- *Carriers:* Blue Dart, Xpressbees, Ecom Express")
            st.markdown("- *Platforms:* Flipkart, Amazon, Meesho, Udaan")
            st.info("Focus on roles like: Network Design Manager, First Mile/Last Mile Ops Lead, Process Excellence Lead")
        
        st.subheader("3. Quick Commerce & Food Tech")
        st.write("*Why:* Your entrepreneurial stint with *OTG* (Food Truck) combined with logistics tech makes you a dual threat here.")
        st.write("*Target Orgs:* Swiggy (Instamart), Zomato, Zepto, Blinkit, Rebel Foods")

    with tab2:
        st.header("Power Metrics for Your Pitch")
        st.markdown("When reaching out to recruiters, use these exact numbers from your experience to grab attention:")
        
        st.success("*The 'Cost Saver' Hook:*\n"
                   "\"I implemented tracking systems that saved *₹8.5 Lakh/month* by reducing manual intervention.\" (from your Shiprocket experience)")
        
        st.success("*The 'Scale' Hook:*\n"
                   "\"I drove a *400% growth* in FTL transactions and turned GMV positive.\" (from your Delhivery experience)")
        
        st.success("*The 'Problem Solver' Hook:*\n"
                   "\"I improved asset recovery rates from *40% to 65%* through on-ground interventions and process SOPs.\" (from your Battery Smart experience)")

    with tab3:
        st.header("Effective Hunt Tactics")
        st.markdown("""
        *1. The 'Founder' Angle*
        Don't hide your OTG entrepreneurship. Position it as "Product & P&L Ownership." 
        Pitch: "I don't just execute operations; I understand the P&L because I've run my own business."

        *2. Value-Based Networking*
        Instead of "Are you hiring?", send a DM saying:
        > "I saw [Company] is expanding its EV fleet. At Battery Smart, I helped recover ₹94L/month in claims—would love to share how similar dispute workflows could aid your fleet security."

        *3. Target 'Series B' Startups*
        Your experience at Shiprocket and Battery Smart is ideal for startups hitting their growth phase (Series B/C) that need to fix messy processes. They value the "Ex-Unicorn" tag.
        """)
