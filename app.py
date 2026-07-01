import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# App Configuration
st.set_page_config(page_title="PT2U Command Center", page_icon="💪", layout="wide")

st.title("💪 PT2U: Client Hub & Funnel")
st.write("Welcome to your lightweight personal training ecosystem.")

# Sidebar Navigation
view_mode = st.sidebar.radio("Navigate Platform", ["🎯 Funnel: Get Started", "📊 Dashboard: Client Tracker"])

# Initialize Google Sheets Connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    conn = None

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
        
        commitment = st.slider("How many hours a week can you realistically commit to the gym?", 1, 6, 3)
        
        submitted = st.form_submit_button("Generate My Blueprint")
        
        if submitted:
            if not name or not email:
                st.error("Please provide both your name and email address to get your blueprint!")
            else:
                st.success(f"Thanks {name}! We've registered your profile.")
                
                # --- BACKEND DATABASE INTERACTION ---
                if conn is not None:
                    try:
                        # Read existing data from 'leads' worksheet inside your pt2u_leads file
                        existing_data = conn.read(worksheet="leads", ttl=5)
                        
                        # Create a row DataFrame for the new lead
                        new_lead = pd.DataFrame([{
                            "name": name,
                            "email": email,
                            "goal": goal,
                            "commitment": int(commitment)
                        }])
                        
                        # Combine old data with new row
                        updated_data = pd.concat([existing_data, new_lead], ignore_index=True)
                        
                        # Write it back to Google Sheets
                        conn.update(worksheet="leads", data=updated_data)
                        st.caption("⚡ Lead securely synchronized to PT2U backend.")
                    except Exception as db_err:
                        st.warning("Could not sync to Google Sheets. Make sure Secrets and permissions are correct.")
                        st.caption(f"Error details: {db_err}")
                else:
                    st.info("Database connection not established yet. Add your Secrets configuration.")
                
                # Dynamic Suggestion UI Logic
                if "drop body fat" in goal:
                    st.subheader("🟢 Your Recommended Track: Weight Loss Package")
                    st.write("**Total Package Price:** RM5,844 (3-Month Cycle)")
                    st.write("**Payment Plan:** RM2,922 upon sign-up, RM2,922 at Week 5.")
                    st.info("💡 Next Step: Your coach will reach out to schedule your Baseline Assessment and set up your nutrition tracker!")
                else:
                    st.subheader("🟠 Your Recommended Track: Muscle Building Package")
                    st.write("**Total Package Price:** RM7,800 (3-Month Cycle)")
                    st.write("**Payment Plan:** RM3,900 upon sign-up, RM3,900 at Week 5.")
                    st.info("💡 Next Step: Your coach will reach out to map your progressive overload targets and supplement regime!")

# ==========================================
# 2. CLIENT PROGRESS TRACKER
# ==========================================
elif view_mode == "📊 Dashboard: Client Tracker":
    st.header("🔒 Client Portal: Continual Monitoring")
    
    # Mock Database Selector for Client Login
    client_profile = st.selectbox("Select Profile (Simulated Login)", ["Ahmad (Weight Loss)", "Siti (Muscle Building)"])
    st.divider()
    
    # Profile Tabs
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
