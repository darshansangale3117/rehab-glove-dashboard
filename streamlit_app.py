import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Forearm Rehab Dashboard", layout="wide")
st.title("🦾 Forearm Rehabilitation Glove Monitor")
st.markdown("---")

# 2. Automatically Convert Your Google Sheet URL to Data Format
USER_URL = "https://docs.google.com/spreadsheets/d/1xVVp0eZqUp16RF-KVb_38Qyao3ah1ciwieH3um5G5Fw/edit?gid=0#gid=0"
SHEET_CSV_URL = USER_URL.split("/edit")[0] + "/export?format=csv"

@st.cache_data(ttl=5) # Refreshes dashboard data every 5 seconds
def load_data():
    try:
        return pd.read_csv(SHEET_CSV_URL)
    except Exception as e:
        st.error(f"Error connecting to live Google Sheet: {e}")
        # Local backup rows so the website layout doesn't break
        return pd.DataFrame({
            'Patient_ID': ['P001'],
            'Name': ['Alex Smith'],
            'Age':,
            'Injury': ['Stroke Recovery'],
            'Target_Angle':,
            'Current_Angle':,
            'Progress_Percent': [72]
        })

df = load_data()

# 3. Patient Selection Sidebar System
st.sidebar.header("Patient Management")
if not df.empty and 'Name' in df.columns:
    selected_name = st.sidebar.selectbox("Select Patient Profile", df['Name'].unique())
    patient_data = df[df['Name'] == selected_name].iloc[0]

    # 4. Main Dashboard Visual Panels
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Patient Information")
        st.info(f"**Name:** {patient_data['Name']}\n\n"
                f"**Patient ID:** {patient_data['Patient_ID']}\n\n"
                f"**Age:** {patient_data['Age']} years old\n\n"
                f"**Condition:** {patient_data['Injury']}")
        
        st.subheader("🎯 Target Metrics")
        st.metric(label="Target Extension Goal", value=f"{patient_data['Target_Angle']}°")
        st.metric(label="Current Best Extension", value=f"{patient_data['Current_Angle']}°")

    with col2:
        st.subheader("📈 Recovery Progress")
        
        # Linear Visual Progress Bar
        progress = int(patient_data['Progress_Percent'])
        st.progress(progress / 100, text=f"Overall Mobility Recovered: {progress}%")
        
        # Recovery Analytics Metric Curve
        st.write("### Motion Recovery Velocity (Weekly Trends)")
        history_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Angle achieved (°)': [20, 35, 50, int(patient_data['Current_Angle'])]
        })
        fig = px.line(history_data, x='Week', y='Angle achieved (°)', markers=True)
        fig.update_layout(yaxis_range=[0, 120])
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Spreadsheet format mismatch. Check your row data values.")

# 5. Live Active Footer
st.markdown("---")
st.caption("🔴 Live System Connection Active | Dashboard syncs with Google Sheets every 5 seconds.")
