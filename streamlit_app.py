import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Forearm Rehab Dashboard", layout="wide")
st.title("🦾 Forearm Rehabilitation Glove Monitor")
st.markdown("---")

# 2. Connect to Free Google Sheets Database
# REPLACE THIS LINK with your actual "Publish to Web" CSV link from Step 1
SHEET_CSV_URL = "https://google.com"

@st.cache_data(ttl=10) # Refreshes data every 10 seconds
def load_data():
    try:
        return pd.read_csv(SHEET_CSV_URL)
    except:
        # Fallback dummy data if sheet link is missing/wrong
        return pd.DataFrame({
            'Patient_ID': ['P001', 'P002'],
            'Name': ['Alex Smith', 'Emma Watson'],
            'Age':,
            'Injury': ['Wrist Fracture', 'Stroke Hemiparesis'],
            'Target_Angle':,
            'Current_Angle':,
            'Progress_Percent': [50, 77]
        })

df = load_data()

# 3. Patient Selection Sidebar
st.sidebar.header("Patient Management")
selected_name = st.sidebar.selectbox("Select Patient Profile", df['Name'].unique())

# Filter data for selected patient
patient_data = df[df['Name'] == selected_name].iloc[0]

# 4. Display Layout Layout
col1, col2 = st.columns([1, 2])

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
    
    # Progress Percentage Visual Gauge
    progress = int(patient_data['Progress_Percent'])
    st.progress(progress / 100, text=f"Overall Mobility Recovered: {progress}%")
    
    # Mock Historical Graph for Demo (Can be hooked to a second sheet tab later)
    st.write("### Motion Recovery Velocity (Weekly Trends)")
    history_data = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Angle achieved (°)': [20, 35, 50, int(patient_data['Current_Angle'])]
    })
    fig = px.line(history_data, x='Week', y='Angle achieved (°)', markers=True)
    fig.update_layout(yaxis_range=[0,120])
    st.plotly_chart(fig, use_container_width=True)

# 5. Live System Status Footer
st.markdown("---")
st.caption("🔴 Live System Standby | Data auto-refreshes every 10 seconds.")
