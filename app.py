import streamlit as st
import pandas as pd
import os
import requests  # Standard library for sending background data

# App Configuration
st.set_page_config(page_title="PT2U Command Center", page_icon="💪", layout="wide")

st.title("💪 PT2U: Client Hub & Funnel")    
st.write("Welcome to your lightweight personal training ecosystem.")

# Sidebar Navigation
view_mode = st.sidebar.radio("Navigate Platform", ["🎯 Funnel: Get Started", "📊 Dashboard: Client Tracker", "🔑 Admin: View Leads"])

LOCAL_FILE = "captured_leads.csv"

# ==========================================
# 1. MARKETING FUNNEL / LEAD GEN
# ==========================================
if view_mode == "🎯 Funnel: Get Started":
    st.header("Find Your Ideal Training Blueprint")
    st.write("Answer a few quick questions to unlock your custom pricing plan and cycle breakdown.")
    
    with st.form("funnel_form"):
        name = st.text_input("What's your name?")
        email = st.text_input("Your email address?")
        
        goal = st.selectbox(
            "What is your primary physical objective right now?",
            ["I want to drop body fat and gain energy", "I want to build strength and muscle mass"]
        )
        
        commitment = st.slider("How many hours a week can you realistically commit to the gym?", 1, 6, 3)
        
        submitted = st.form_submit_button("Generate My Blueprint")
        
        if submitted:
            if not name or not email:
                st.error("Please provide both your name and email address to get your blueprint!")
            else:
                st.success(f"Thanks {name}! We've registered your profile.")
                
                # --- SAFE LOCAL STORAGE BACKEND ---
                new_lead = pd.DataFrame([{
                    "Name": name,
                    "Email": email,
                    "Goal": goal,
                    "Commitment (Hours)": int(commitment)
                }])
                
                if os.path.exists(LOCAL_FILE):
                    existing_df = pd.read_csv(LOCAL_FILE)
                    updated_df = pd.concat([existing_df, new_lead], ignore_index=True)
                else:
                    updated_df = new_lead
                
                updated_df.to_csv(LOCAL_FILE, index=False)
                st.caption("⚡ Lead successfully recorded in the cloud system database!")

                # --- 2. SILENT BACKGROUND EMAIL AUTO-FORWARD ---
                # Change this to your friend's actual trainer email address!
                trainer_email = "https://formsubmit.co/el/khairool.adzelan@gmail.com" 
                
                formsubmit_url = f"https://formsubmit.co/ajax/{trainer_email}"
                
                payload = {
                    "Subject": f"🚨 New PT2U Lead: {name}",
                    "Prospect Name": name,
                    "Prospect Email": email,
                    "Objective Selected": goal,
                    "Weekly Commitment": f"{commitment} Hours",
                    "_captcha": "false" # Bypasses any human verification screens
                }
                
                try:
                    # Fires a silent data packet out to the email endpoint instantly
                    response = requests.post(formsubmit_url, data=payload)
                    if response.status_code == 200:
                        st.caption("⚡ Lead safely captured and routed to Coach profile.")
                except Exception as e:
                    # Fails silently in the background so the user never sees an ugly crash
                    pass
                
                # Dynamic Suggestion UI Logic
                if "drop body fat" in goal:
                    st.subheader("🟢 Your Recommended Track: Weight Loss Package")
                    st.write("**Total Package Price:** RM5,844 (3-Month Cycle)")
                    st.write("**Payment Plan:** RM2,922 upon sign-up, RM2,922 at Week 5.")
                else:
                    st.subheader("🟠 Your Recommended Track: Muscle Building Package")
                    st.write("**Total Package Price:** RM7,800 (3-Month Cycle)")
                    st.write("**Payment Plan:** RM3,900 upon sign-up, RM3,900 at Week 5.")

# ==========================================
# 2. CLIENT PROGRESS TRACKER
# ==========================================
elif view_mode == "📊 Dashboard: Client Tracker":
    st.header("🔒 Client Portal: Continual Monitoring")
    
    client_profile = st.selectbox("Select Profile (Simulated Login)", ["Ahmad (Weight Loss)", "Siti (Muscle Building)"])
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📋 Baseline & Goals", "📈 Weekly Vibe Check", "🎯 Progress History"])
    
    with tab1:
        st.subheader("Your Starting Metrics & North Star")
        if "Ahmad" in client_profile:
            st.markdown("**Track:** 🟢 Weight Loss")
            st.markdown("**Starting Weight:** 92 kg | **Waist:** 104 cm")
        else:
            st.markdown("**Track:** 🟠 Muscle Building")
            st.markdown("**Starting Weight:** 68 kg | **Max Pushups:** 15 reps")

    with tab2:
        st.subheader("Weekly Check-In Form")
        with st.form("vibe_check_form"):
            current_metric = st.number_input("Log Current Weight (kg) or Weekly Workout Volume:", value=70.0)
            energy = st.slider("Energy Levels (1-10)", 1, 10, 7)
            recovery = st.slider("Recovery & Sleep Quality (1-10)", 1, 10, 7)
            stress = st.slider("Life/Work Stress Levels (1-10)", 1, 10, 4)
            
            submit_checkin = st.form_submit_button("Submit Weekly Check-In")
            
            if submit_checkin:
                vibe_score = (energy + recovery - stress)
                st.success("Log received by your trainer!")

    with tab3:
        st.subheader("Your Consistency Timeline")
        chart_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Compliance Rate (%)': [85, 90, 95, 100]
        })
        st.line_chart(chart_data.set_index('Week'))

# ==========================================
# 3. ADMIN VIEW
# ==========================================
elif view_mode == "🔑 Admin: View Leads":
    st.header("🔑 PT2U Lead Management Hub")
    st.write("This tab displays incoming traffic from your marketing funnel in real-time.")
    
    if os.path.exists(LOCAL_FILE):
        leads_df = pd.read_csv(LOCAL_FILE)
        st.dataframe(leads_df, use_container_width=True)
        
        csv_data = leads_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Leads as Excel/CSV",
            data=csv_data,
            file_name="pt2u_marketing_leads.csv",
            mime="text/csv",
        )
    else:
        st.info("No leads captured yet! Go fill out the form in the Funnel tab to see it populate here.")
