from datetime import datetime
import json
import os
from zoneinfo import ZoneInfo
import streamlit as st

# File paths for data persistence
SCHEDULE_FILE = "italian_schedule.json"
PROGRESS_FILE = "user_progress.json"

# Local timezone setting (matches local time for your friend)
LOCAL_TZ = ZoneInfo("America/Chicago")


def initialize_files():
    """Ensures default JSON files exist with baseline data."""
    if not os.path.exists(SCHEDULE_FILE):
        default_schedule = {
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
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(default_schedule, f, indent=4)

    if not os.path.exists(PROGRESS_FILE):
        default_progress = {
            "completed_dates": [],
            "streak": 0,
            "daily_notes": {},
        }
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_progress, f, indent=4)


def load_data():
    """Loads schedule and user progress data from JSON files."""
    initialize_files()
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        schedule = json.load(f)
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        progress = json.load(f)

    if "daily_notes" not in progress:
        progress["daily_notes"] = {}

    return schedule, progress


def save_progress(progress):
    """Saves user progress data back to JSON."""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=4)


def main():
    st.set_page_config(
        page_title="Italian Learning Dashboard", page_icon="🇮🇹", layout="centered"
    )

    schedule, progress = load_data()

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
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📅 Today's Task",
            "📓 Daily Notes",
            "🗓️ Full 7-Day Curriculum",
            "⚙️ Manage Schedule",
        ]
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
                    save_progress(progress)
                    st.success("Great job! Streak updated.")
                    st.rerun()
            else:
                st.success("🎉 You have already completed today's task!")
                if st.button("🔄 Undo Completion"):
                    completed_dates.remove(today_str)
                    progress["streak"] = max(0, streak - 1)
                    progress["completed_dates"] = completed_dates
                    save_progress(progress)
                    st.rerun()
        else:
            st.warning("No curriculum found for today.")

    # --- TAB 2: DAILY NOTES ---
    with tab2:
        st.header("📓 Daily Learning Notes")
        st.markdown(
            "Jot down new words, grammar rules, or reflections from your practice."
        )

        daily_notes = progress.get("daily_notes", {})

        selected_date = st.date_input(
            "Select Date", value=now_local.date()
        ).strftime("%Y-%m-%d")

        current_note_content = daily_notes.get(selected_date, "")

        with st.form("notes_form"):
            note_input = st.text_area(
                f"Notes for {selected_date}",
                value=current_note_content,
                placeholder="Write new vocabulary, sentences, or thoughts here...",
                height=150,
            )
            submitted_note = st.form_submit_button("Save Note")

            if submitted_note:
                daily_notes[selected_date] = note_input
                progress["daily_notes"] = daily_notes
                save_progress(progress)
                st.success(f"Notes for {selected_date} saved successfully!")
                st.rerun()

        # Delete option for the currently selected date if a note exists
        if current_note_content.strip():
            if st.button(f"🗑️ Delete Note for {selected_date}"):
                if selected_date in daily_notes:
                    del daily_notes[selected_date]
                    progress["daily_notes"] = daily_notes
                    save_progress(progress)
                    st.success(f"Note for {selected_date} deleted!")
                    st.rerun()

        st.markdown("---")
        st.subheader("📚 Past Notes Archive")
        if daily_notes:
            sorted_dates = sorted(daily_notes.keys(), reverse=True)
            for d in sorted_dates:
                if daily_notes[d].strip():
                    with st.expander(f"📝 {d}"):
                        st.write(daily_notes[d])
                        if st.button(
                            "🗑️ Delete this note", key=f"del_note_{d}"
                        ):
                            del daily_notes[d]
                            progress["daily_notes"] = daily_notes
                            save_progress(progress)
                            st.success(f"Deleted note for {d}")
                            st.rerun()
        else:
            st.info("No saved notes yet. Start writing above!")

    # --- TAB 3: FULL CURRICULUM ---
    with tab3:
        st.header("Your 7-Day Curriculum")
        st.markdown(
            "Here is the complete weekly breakdown designed to build well-rounded fluency."
        )

        for day, details in schedule.items():
            with st.expander(f"{day}: {details['focus']}"):
                st.write(f"**Task:** {details['task']}")
                st.write(f"⏱️ **Duration:** {details['duration_mins']} mins")

    # --- TAB 4: CUSTOMIZE SCHEDULE ---
    with tab4:
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
                with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
                    json.dump(schedule, f, indent=4)
                st.success(f"Successfully updated {selected_day}!")
                st.rerun()


if __name__ == "__main__":
    main()
