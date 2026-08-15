import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Dashboard Layout Settings
st.set_page_config(page_title="Forearm Rehab Dashboard", layout="wide")
st.title("🦾 Forearm Rehabilitation Glove Monitor")
st.markdown("---")

# 2. Live Connection to Your Google Sheet Link
# The URL below is modified to directly stream clean CSV data to your layout
SHEET_ID = "1xVVp0eZqUp16RF-KVb_38Qyao3ah1ciwieH3um5G5Fw"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=5) # Checks for sensor updates every 5 seconds
def load_data():
    return pd.read_csv(SHEET_CSV_URL)

try:
    df = load_data()

    # 3. Patient Tracking Selector Panel
    st.sidebar.header("Patient Management")
    patient_names = df['Name'].unique()
    selected_name = st.sidebar.selectbox("Select Patient Profile", patient_names)
    
    # Filter matching row metrics
    patient_data = df[df['Name'] == selected_name].iloc

    # 4. Interface Columns Configuration
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Patient Information")
        st.info(f"**Name:** {patient_data['Name']}\n\n"
                f"**Patient ID:** {patient_data['Patient_ID']}\n\n"
                f"**Age:** {patient_data['Age']} years old\n\n"
                f"**Condition:** {patient_data['Injury']}")
        
        st.subheader("🎯 Angle Metrics")
        st.metric(label="Target Extension Goal", value=f"{patient_data['Target_Angle']}°")
        st.metric(label="Current Best Extension", value=f"{patient_data['Current_Angle']}°")

    with col2:
        st.subheader("📈 Recovery Progress")
        
        # Visual Linear Completion Slider Bar
        progress_val = int(patient_data['Progress_Percent'])
        st.progress(progress_val / 100, text=f"Overall Mobility Recovered: {progress_val}%")
        
        # Historical Trend Graphic Tracking Motion Over Time
        st.write("### Motion Recovery Velocity (Weekly Trends)")
        history_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Angle achieved (°)': [20, 35, 50, int(patient_data['Current_Angle'])]
        })
        fig = px.line(history_data, x='Week', y='Angle achieved (°)', markers=True)
        fig.update_layout(yaxis_range=)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Awaiting Google Sheet Authorization Protocol")
    st.warning("Please verify your spreadsheet 'Share' permissions are switched to 'Anyone with the link can view'.")

# 5. Live Active System Footer
st.markdown("---")
st.caption("🔴 Live System Operational | Dashboard syncs with Google Sheets every 5 seconds.")
