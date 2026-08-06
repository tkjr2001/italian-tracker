import streamlit as st
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Italian Learning Dashboard",
    page_icon="🇮🇹",
    layout="centered"
)

SCHEDULE_FILE = "italian_schedule.json"
PROGRESS_FILE = "user_progress.json"

# Helper functions to load/save data
def load_data(filename, default_data):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_data

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Load schedule & progress
schedule = load_data(SCHEDULE_FILE, {})
progress = load_data(PROGRESS_FILE, {"streak": 0, "completed_dates": []})

if not schedule:
    st.error("⚠️ 'italian_schedule.json' not found! Make sure it's in the same folder.")
    st.stop()

# Header Section
st.title("🇮🇹 Italian Learning Dashboard")
st.markdown("Your daily habit tracker and weekly curriculum layout.")

today_name = datetime.now().strftime("%A")
today_date = datetime.now().strftime("%Y-%m-%d")

# Sidebar for Metrics
st.sidebar.header("📊 Progress Stats")
st.sidebar.metric(label="Current Streak", value=f"{progress['streak']} Days 🔥")
st.sidebar.metric(label="Total Sessions Completed", value=len(progress["completed_dates"]))

if st.sidebar.button("Reset Progress"):
    progress = {"streak": 0, "completed_dates": []}
    save_data(PROGRESS_FILE, progress)
    st.sidebar.success("Progress reset!")
    st.rerun()

# Main Container: Today's Focus
st.markdown("---")
st.subheader(f"📅 Today's Focus: {today_name} ({today_date})")

if today_name in schedule:
    task_info = schedule[today_name]
    
    with st.container():
        st.info(f"**Focus Area:** {task_info['focus']}")
        st.write(f"**Task:** {task_info['task']}")
        st.write(f"⏱️ **Duration:** {task_info['duration_mins']} minutes")
        st.write(f"🛠️ **Resources:** {', '.join(task_info['resources'])}")
        
    is_completed_today = today_date in progress["completed_dates"]
    
    if is_completed_today:
        st.success("✅ You have already completed today's session! Awesome job!")
        if st.button("Undo Completion"):
            progress["completed_dates"].remove(today_date)
            progress["streak"] = max(0, progress["streak"] - 1)
            save_data(PROGRESS_FILE, progress)
            st.rerun()
    else:
        if st.button("✨ Mark Today's Session Complete", type="primary"):
            progress["completed_dates"].append(today_date)
            progress["streak"] += 1
            save_data(PROGRESS_FILE, progress)
            st.balloons()
            st.success("Progress saved! Keep up the momentum!")
            st.rerun()
else:
    st.warning("No specific task found for today.")

# Weekly Schedule Overview
st.markdown("---")
st.subheader("🗓️ Full Weekly Curriculum")

for day, details in schedule.items():
    with st.expander(f"{day} — {details['focus']} ({details['duration_mins']} mins)"):
        st.write(f"**Task:** {details['task']}")
        st.write(f"**Tools/Resources:** {', '.join(details['resources'])}")