import streamlit as st
import pandas as pd
import os
import requests  # Required for our background email API

# ==========================================
# APP CONFIGURATION
# ==========================================
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
        email = st.text_input("Your best email address?")
        goal = st.selectbox(
            "What is your primary physical objective right now?", 
            ["I want to drop body fat and gain energy", "I want to build strength and muscle mass"]
        )
        commitment = st.slider("Gym Commitment (Hours/Week)", 1, 6, 3)
        
        submitted = st.form_submit_button("Generate My Blueprint")
        
        if submitted:
            if not name or not email:
                st.error("Please provide both your name and email address to get your blueprint!")
            else:
                st.success(f"Thanks {name}! Your customized blueprint is ready below.")
                
                # --- A. SAVE TO LOCAL SERVER FILE ---
                new_lead = pd.DataFrame([{"Name": name, "Email": email, "Goal": goal, "Commitment": commitment}])
                if os.path.exists(LOCAL_FILE):
                    existing_df = pd.read_csv(LOCAL_FILE)
                    updated_df = pd.concat([existing_df, new_lead], ignore_index=True)
                else:
                    updated_df = new_lead
                updated_df.to_csv(LOCAL_FILE, index=False)
                
                # --- B. SILENT BACKGROUND EMAIL AUTO-FORWARD ---
                # ⚠️ REPLACE THIS WITH YOUR FRIEND's REAL EMAIL!
                trainer_email = "khairool.adzelan@gmail.com" 
                
                formsubmit_url = f"https://formsubmit.co/ajax/{trainer_email}"
                
                # The structured data packet
                payload = {
                    "Subject": f"🚨 New PT2U Lead: {name}",
                    "Prospect Name": name,
                    "Prospect Email": email,
                    "Objective Selected": goal,
                    "Weekly Commitment": f"{commitment} Hours",
                    "_captcha": "false" 
                }
                
                # The security headers to prove we aren't a spam bot
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
                }
                
                try:
                    # Send the data packet
                    response = requests.post(formsubmit_url, json=payload, headers=headers)
                    if response.status_code == 200:
                        st.caption("⚡ Lead securely captured and routed to Coach profile.")
                    else:
                        st.warning(f"Email server responded with code: {response.status_code}")
                except Exception as e:
                    st.error(f"Background routing error: {e}")

                # --- C. DISPLAY BLUEPRINT IMMEDIATELY TO CUSTOMER ---
                if "drop body fat" in goal.lower():
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
            st.markdown("**The 'Why':** To feel energetic playing with my kids.")
            st.markdown("**Starting Weight:** 92 kg | **Waist:** 104 cm")
            st.markdown("**Constraints:** 3 hours/week max commitment")
        else:
            st.markdown("**Track:** 🟠 Muscle Building")
            st.markdown("**The 'Why':** To look confident and strong for my wedding.")
            st.markdown("**Starting Weight:** 68 kg | **Max Pushups:** 15 reps")
            st.markdown("**Constraints:** 4 hours/week commitment")

    with tab2:
        st.subheader("Weekly Check-In Form")
        st.write("Keep your coach updated on your physical and psychological stress load.")
        
        with st.form("vibe_check_form"):
            current_metric = st.number_input("Log Current Weight (kg) or Weekly Workout Volume:", value=70.0)
            energy = st.slider("Energy Levels (1-10)", 1, 10, 7)
            recovery = st.slider("Recovery & Sleep Quality (1-10)", 1, 10, 7)
            stress = st.slider("Life/Work Stress Levels (1-10)", 1, 10, 4)
            
            submit_checkin = st.form_submit_button("Submit Weekly Check-In")
            
            if submit_checkin:
                vibe_score = (energy + recovery - stress)
                st.success("Log received by your trainer!")
                
                if vibe_score >= 10:
                    st.balloons()
                    st.success("🟢 Traffic Light Status: GREEN. You are crushing it! Keep following the baseline script.")
                elif 5 <= vibe_score < 10:
                    st.warning("🟡 Traffic Light Status: YELLOW. Nice consistency. Focus on getting an extra 1L of water and 30 mins of sleep tonight.")
                else:
                    st.error("🔴 Traffic Light Status: RED. High fatigue/stress detected. Your coach has been notified to modify your upcoming sessions.")

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
