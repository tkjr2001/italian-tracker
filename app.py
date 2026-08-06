from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st

# Local timezone setting (matches local time)
LOCAL_TZ = ZoneInfo("America/Chicago")


def initialize_session_state():
    """Initializes default schedule and user progress in Streamlit session state

    so each user gets an independent isolated session.
    """
    if "schedule" not in st.session_state:
        st.session_state.schedule = {
            "Monday": {
                "focus": "Listening & Pronunciation",
                "task": "Listen to a 10-minute Italian podcast (e.g., 'Coffee Break Italian') and shadow the dialogue.",
                "duration_mins": 15,
            },
            "Tuesday": {
                "focus": "Vocabulary & Reading",
                "task": "Learn 10 new words and read a short news article on News in Slow Italian.",
                "duration_mins": 20,
            },
            "Wednesday": {
                "focus": "Grammar & Structure",
                "task": "Review present tense regular verbs (-are, -ere, -ire) and complete 5 practice sentences.",
                "duration_mins": 20,
            },
            "Thursday": {
                "focus": "Speaking & Output",
                "task": "Record a 1-minute voice note describing your day out loud in Italian.",
                "duration_mins": 15,
            },
            "Friday": {
                "focus": "Cultural Immersion",
                "task": "Watch a short YouTube video or music clip in Italian with Italian subtitles.",
                "duration_mins": 25,
            },
            "Saturday": {
                "focus": "Review & Practice",
                "task": "Review flashcards of the week's vocabulary and chat with a language partner or AI.",
                "duration_mins": 30,
            },
            "Sunday": {
                "focus": "Rest & Reflection",
                "task": "Light review or take a break. Write down 3 things you are grateful for in Italian.",
                "duration_mins": 10,
            },
        }

    if "progress" not in st.session_state:
        st.session_state.progress = {"completed_dates": [], "streak": 0}


def main():
    st.set_page_config(
        page_title="Italian Learning Dashboard", page_icon="🇮🇹", layout="centered"
    )

    initialize_session_state()

    schedule = st.session_state.schedule
    progress = st.session_state.progress

    # Get local current date and day name using ZoneInfo
    now_local = datetime.now(LOCAL_TZ)
    today_str = now_local.strftime("%Y-%m-%d")
    today_name = now_local.strftime("%A")

    # App Header
    st.title("🇮🇹 Italian Learning Routine")
    st.markdown(
        "Welcome! Build your daily consistency with bite-sized language tasks."
    )

    # Sidebar for Stats & Navigation
    st.sidebar.header("📊 Progress Tracker")
    completed_dates = progress.get("completed_dates", [])
    streak = progress.get("streak", 0)

    st.sidebar.metric(label="Current Streak", value=f"{streak} days 🔥")
    st.sidebar.metric(
        label="Total Days Completed", value=len(completed_dates)
    )

    # Main Dashboard Tabs
    tab1, tab2, tab3 = st.tabs(
        ["📅 Today's Task", "🗓️ Full 7-Day Curriculum", "⚙️ Manage Schedule"]
    )

    # --- TAB 1: TODAY'S TASK ---
    with tab1:
        st.header(f"Today is {today_name}")
        st.caption(f"Date: {now_local.strftime('%B %d, %Y')}")

        if today_name in schedule:
            todays_plan = schedule[today_name]

            st.info(f"**Focus Area:** {todays_plan['focus']}")
            st.write(f"**Task:** {todays_plan['task']}")
            st.write(f"⏱️ **Target Duration:** {todays_plan['duration_mins']} mins")

            is_completed_today = today_str in completed_dates

            if not is_completed_today:
                if st.button("✅ Mark Today's Task as Complete"):
                    completed_dates.append(today_str)
                    progress["streak"] = streak + 1
                    progress["completed_dates"] = completed_dates
                    st.session_state.progress = progress
                    st.success("Great job! Streak updated.")
                    st.rerun()
            else:
                st.success("🎉 You have already completed today's task!")
                if st.button("🔄 Undo Completion"):
                    completed_dates.remove(today_str)
                    progress["streak"] = max(0, streak - 1)
                    progress["completed_dates"] = completed_dates
                    st.session_state.progress = progress
                    st.rerun()
        else:
            st.warning("No curriculum found for today.")

    # --- TAB 2: FULL CURRICULUM ---
    with tab2:
        st.header("Your 7-Day Curriculum")
        st.markdown(
            "Here is the complete weekly breakdown designed to build well-rounded fluency."
        )

        for day, details in schedule.items():
            with st.expander(f"{day}: {details['focus']}"):
                st.write(f"**Task:** {details['task']}")
                st.write(f"⏱️ **Duration:** {details['duration_mins']} mins")

    # --- TAB 3: CUSTOMIZE SCHEDULE ---
    with tab3:
        st.header("Customize Routine")
        st.markdown("Modify daily tasks to fit your preferences.")

        selected_day = st.selectbox("Select day to edit", list(schedule.keys()))

        current_focus = schedule[selected_day]["focus"]
        current_task = schedule[selected_day]["task"]
        current_duration = schedule[selected_day]["duration_mins"]

        with st.form("edit_form"):
            new_focus = st.text_input("Focus Area", value=current_focus)
            new_task = st.text_area("Task Description", value=current_task)
            new_duration = st.number_input(
                "Duration (minutes)",
                min_value=5,
                max_value=120,
                value=current_duration,
                step=5,
            )

            submitted = st.form_submit_button("Save Changes")
            if submitted:
                schedule[selected_day] = {
                    "focus": new_focus,
                    "task": new_task,
                    "duration_mins": int(new_duration),
                }
                st.session_state.schedule = schedule
                st.success(f"Successfully updated {selected_day}!")
                st.rerun()


if __name__ == "__main__":
    main()
