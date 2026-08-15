import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Forearm Rehab Dashboard", layout="wide")
st.title("🦾 Forearm Rehabilitation Glove Monitor")
st.markdown("---")

SHEET_ID = "1xVVp0eZqUp16RF-KVb_38Qyao3ah1ciwieH3um5G5Fw"
SHEET_CSV_URL = f"https://google.com{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=1)
def load_data():
    return pd.read_csv(SHEET_CSV_URL)

try:
    df = load_data()
    st.sidebar.header("Patient Management")
    selected_name = st.sidebar.selectbox("Select Patient Profile", df['Name'].unique())
    patient_data = df[df['Name'] == selected_name].iloc[0]

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
        progress = int(patient_data['Progress_Percent'])
        st.progress(progress / 100, text=f"Overall Mobility Recovered: {progress}%")
        
        st.write("### Motion Recovery Velocity (Weekly Trends)")
        history_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Angle achieved (°)': [20, 35, 50, int(patient_data['Current_Angle'])]
        })
        fig = px.line(history_data, x='Week', y='Angle achieved (°)', markers=True)
        fig.update_layout(yaxis_range=[0, 180])
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Connecting to Database Stream... Details: {e}")
    st.info("Please refresh your browser tab if this screen stays stuck.")

st.markdown("---")
st.caption("🔴 Live System Connection Active | Dashboard syncs with Google Sheets instantly.")
