# app.py — Polished Mental Health & Wellness App (no deprecations, stable reruns)
import os
import time
import random
import datetime as dt

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Wellness Companion", page_icon="🧠", layout="wide")

DATA_DIR = "data"
MOOD_CSV = os.path.join(DATA_DIR, "moods.csv")
JOURNAL_CSV = os.path.join(DATA_DIR, "journal.csv")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(MOOD_CSV):
    pd.DataFrame(columns=["date", "mood_score"]).to_csv(MOOD_CSV, index=False)
if not os.path.exists(JOURNAL_CSV):
    pd.DataFrame(columns=["timestamp", "title", "text"]).to_csv(JOURNAL_CSV, index=False)

MOOD_LABELS = {"😊 Happy": 5, "🙂 Okay": 4, "😐 Neutral": 3, "☹️ Sad": 2, "😭 Very Low": 1}
INV_MOOD = {v: k for k, v in MOOD_LABELS.items()}

QUOTES = [
    "This too shall pass 🌤️",
    "You are stronger than you think 💪",
    "Small steps every day lead to big changes 🌱",
    "Keep going — one breath at a time 🌿",
    "Your story is still being written ✨",
]

RESOURCES = [
    ("India — KIRAN Helpline", "1800-599-0019"),
    ("Vandrevala Foundation", "9152987821"),
    ("Befrienders Worldwide", "https://www.befrienders.org/"),
    ("WHO Mental Health", "https://www.who.int/health-topics/mental-health"),
]

# -------------------------
# UTILS
# -------------------------
def load_moods() -> pd.DataFrame:
    try:
        df = pd.read_csv(MOOD_CSV)
        if not {"date", "mood_score"}.issubset(df.columns):
            return pd.DataFrame(columns=["date", "mood_score"])
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        return df.sort_values("date")
    except Exception:
        return pd.DataFrame(columns=["date", "mood_score"])


def save_mood(date_str: str, score: int) -> None:
    df = load_moods()
    if not df.empty and "date" in df:
        df = df[df["date"].dt.strftime("%Y-%m-%d") != date_str]
    new_row = pd.DataFrame([{"date": pd.to_datetime(date_str), "mood_score": score}])
    df = pd.concat([df, new_row], ignore_index=True).sort_values("date")
    df.to_csv(MOOD_CSV, index=False)


def load_journal() -> pd.DataFrame:
    try:
        return pd.read_csv(JOURNAL_CSV)
    except Exception:
        return pd.DataFrame(columns=["timestamp", "title", "text"])


def save_journal(title: str, text: str) -> None:
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = load_journal()
    new_row = pd.DataFrame([{"timestamp": ts, "title": title, "text": text}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(JOURNAL_CSV, index=False)


def dummy_risk_score(text: str) -> float:
    """Keyword-based probability 0..100 (simple demo)."""
    negatives = [
        "sad",
        "depressed",
        "alone",
        "hopeless",
        "tired",
        "anxious",
        "worthless",
        "suicide",
        "cry",
    ]
    hits = sum(1 for w in negatives if w in text.lower())
    base = min(90, hits * 20)  # each hit adds ~20 up to 90
    jitter = random.uniform(-5, 5)
    return max(0, min(100, round(base + jitter, 1)))


def gauge_figure(percent: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=percent,
            title={"text": "Depression Risk (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {
                    "color": "crimson" if percent >= 60 else ("orange" if percent >= 35 else "green")
                },
                "steps": [
                    {"range": [0, 35], "color": "#d4edda"},
                    {"range": [35, 60], "color": "#fff3cd"},
                    {"range": [60, 100], "color": "#f8d7da"},
                ],
            },
        )
    )
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
    return fig


def mood_trend_figure(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    fig = px.line(df, x="date", y="mood_score", markers=True, title="Mood Trend")
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), template="plotly_white", title_x=0.5)
    fig.update_yaxes(range=[0.5, 5.5], dtick=1)
    return fig


def summary_text() -> str:
    moods = load_moods()
    journal = load_journal()
    avg7 = moods.tail(7)["mood_score"].mean() if not moods.empty else float("nan")
    avg30 = moods.tail(30)["mood_score"].mean() if not moods.empty else float("nan")

    # streak
    streak = 0
    if not moods.empty:
        dates = set(moods["date"].dt.date.tolist())
        d = dt.date.today()
        while d in dates:
            streak += 1
            d -= dt.timedelta(days=1)

    lines = [
        f"Report generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"7-day avg mood (1-5): {avg7:.2f}" if pd.notna(avg7) else "7-day avg mood (1-5): —",
        f"30-day avg mood (1-5): {avg30:.2f}" if pd.notna(avg30) else "30-day avg mood (1-5): —",
        f"Current logging streak: {streak} day(s)",
        f"Journal entries: {len(journal)}",
    ]
    return "\n".join(lines)


st.markdown(
    "<h1 style='text-align: center; color: white;'>🌐 Social Media Wellness Analyzer</h1>",
    unsafe_allow_html=True
)


# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
with st.sidebar:
    st.markdown("---")
    st.title("Wellness Companion")
    user_name = st.text_input("Display name", value=st.session_state.get("display_name", "Friend"))
    st.session_state.display_name = user_name
    page = st.radio("Navigate", ["Home", "Analyze", "Mood Tracker", "Journal", "Wellness", "Export"])

st.sidebar.markdown("---")
st.sidebar.markdown(
    "If you are in crisis, contact local emergency services or a helpline immediately."
)
for label, link in RESOURCES:
    if str(link).startswith("http"):
        st.sidebar.markdown(f"- [{label}]({link})")
    else:
        st.sidebar.markdown(f"- **{label}:** {link}")

# -------------------------
# PAGE: HOME
# -------------------------
if page == "Home":
    st.title(f"Welcome , {st.session_state.display_name} 🌿")
    st.caption("A calm space for reflection — this is awareness & self-care, not a medical diagnosis.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("⚡ Scan Your Thoughts")
        quick_text = st.text_area(
            "Paste a short post or your journal thought here (private):",
            height=120,
            placeholder="e.g. I haven't been sleeping well lately...",
        )
        if st.button("Scan", key="scan_quick"):
            if not quick_text.strip():
                st.warning("Please enter something to scan.")
            else:
                risk = dummy_risk_score(quick_text)
                st.plotly_chart(gauge_figure(risk), use_container_width=True)
                if risk >= 60:
                    st.error(
                        f"High risk detected — {risk}%. Consider reaching out to someone you trust or a professional."
                    )
                    st.info(random.choice(QUOTES))
                elif risk >= 35:
                    st.warning(f"Moderate indicators — {risk}%. Try a calming activity or journaling.")
                else:
                    st.success(f"Low indicators — {risk}%. Keep leaning into positive routines!")
    with col2:
        st.subheader("Today at a glance")
        moods = load_moods()
        avg7 = moods.tail(7)["mood_score"].mean() if not moods.empty else float("nan")
        avg30 = moods.tail(30)["mood_score"].mean() if not moods.empty else float("nan")
        # streak
        streak = 0
        if not moods.empty:
            dates = set(moods["date"].dt.date.tolist())
            d = dt.date.today()
            while d in dates:
                streak += 1
                d -= dt.timedelta(days=1)
        st.metric("7-day avg", f"{avg7:.2f}" if pd.notna(avg7) else "—")
        st.metric("30-day avg", f"{avg30:.2f}" if pd.notna(avg30) else "—")
        st.metric("Logging streak", f"{streak} day(s)")
        st.markdown("### A small encouragement")
        st.info(random.choice(QUOTES))

# -------------------------
# PAGE: ANALYZE (detailed)
# -------------------------
elif page == "Analyze":
    st.title("Analyze a Post or Journal Entry")
    text = st.text_area(
        "Paste text to analyze (longer text gives a clearer signal):", height=180, placeholder="Write or paste here..."
    )

    # state holders for analysis results
    if "analyze_score" not in st.session_state:
        st.session_state.analyze_score = None
        st.session_state.analyze_suggested = None

    analyze_col1, analyze_col2 = st.columns([1, 1])
    with analyze_col1:
        if st.button("Analyze Text", key="analyze_text"):
            if not text.strip():
                st.warning("Please write or paste something to analyze.")
            else:
                score = dummy_risk_score(text)
                st.session_state.analyze_score = score
                st.session_state.analyze_suggested = "☹️ Sad" if score >= 60 else ("😐 Neutral" if score >= 35 else "😊 Happy")

        # Show last results (if any)
        if st.session_state.analyze_score is not None:
            st.plotly_chart(gauge_figure(st.session_state.analyze_score), use_container_width=True)
            st.write(f"**Suggested mood:** {st.session_state.analyze_suggested} ({st.session_state.analyze_score}%)")
            if st.button("Save suggested mood", key="save_suggested"):
                today = dt.date.today().strftime("%Y-%m-%d")
                suggested = st.session_state.analyze_suggested
                score_map = {"😊 Happy": 5, "😐 Neutral": 3, "☹️ Sad": 2}
                save_mood(today, score_map.get(suggested, 3))
                st.success("Suggested mood saved.")

    with analyze_col2:
        if st.button("Analyze & Save as Journal", key="analyze_save_journal"):
            if not text.strip():
                st.warning("Please write something first.")
            else:
                score = dummy_risk_score(text)
                st.plotly_chart(gauge_figure(score), use_container_width=True)
                save_journal("Quick Entry", text)
                st.success("Saved as journal entry.")

# -------------------------
# PAGE: MOOD TRACKER
# -------------------------
elif page == "Mood Tracker":
    st.title("Mood Tracker")
    st.subheader("Log how you feel today")
    selected = st.selectbox("Pick your mood for today", list(MOOD_LABELS.keys()), index=2)
    if st.button("Save Mood", key="save_mood"):
        today = dt.date.today().strftime("%Y-%m-%d")
        save_mood(today, MOOD_LABELS[selected])
        st.success("Mood saved ✅")

    df = load_moods()
    if df.empty:
        st.info("No moods logged yet. Use the form above to add today's mood.")
    else:
        st.subheader("Mood Trend")
        fig = mood_trend_figure(df)
        st.plotly_chart(fig, use_container_width=True)
        avg7 = df.tail(7)["mood_score"].mean() if not df.empty else float("nan")
        st.markdown(f"**7-day average mood:** {avg7:.2f}" if pd.notna(avg7) else "**7-day average mood:** —")
        if st.button("Clear mood history", key="clear_moods"):
            pd.DataFrame(columns=["date", "mood_score"]).to_csv(MOOD_CSV, index=False)
            st.success("Cleared mood history")

# -------------------------
# PAGE: JOURNAL
# -------------------------
elif page == "Journal":
    st.title("Journal — Write & Reflect")
    jtitle = st.text_input("Title (optional)")
    jtext = st.text_area("Write about your day, thoughts, or paste a post to save:", height=200)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Save Journal Entry", key="save_journal"):
            if not jtext.strip():
                st.warning("Write something before saving.")
            else:
                save_journal(jtitle if jtitle else "Untitled", jtext)
                st.success("Journal saved.")
    with c2:
        if st.button("Analyze Journal Text", key="analyze_journal_text"):
            if not jtext.strip():
                st.warning("Write something to analyze.")
            else:
                score = dummy_risk_score(jtext)
                st.plotly_chart(gauge_figure(score), use_container_width=True)
                if score >= 60:
                    st.warning("High likelihood of depressive language. Consider reaching out.")
                elif score >= 35:
                    st.info("Moderate indicators — self-care recommended.")
                else:
                    st.success("Low indicators.")

    st.markdown("### Your Journal History")
    jdf = load_journal()
    if jdf.empty:
        st.info("No journal entries yet.")
    else:
        view = jdf.sort_values("timestamp", ascending=False).reset_index(drop=True)
        st.dataframe(view, use_container_width=True, height=250)
        q = st.text_input("Search journal by keyword (optional)")
        if q.strip():
            filtered = view[
                view["title"].str.contains(q, case=False, na=False)
                | view["text"].str.contains(q, case=False, na=False)
            ]
            st.dataframe(filtered, use_container_width=True, height=250)

# -------------------------
# PAGE: WELLNESS
# -------------------------
elif page == "Wellness":
    st.title("Wellness Tools")
    st.subheader("Motivational Thought")
    st.info(random.choice(QUOTES))
    st.subheader("Quick Stress Tip")
    st.success(
        random.choice(
            [
                "Take a 3-minute breathing break (4-4-4).",
                "Step outside and get 5 minutes of sunlight.",
                "Write down one small win today.",
            ]
        )
    )

    st.markdown("#### 5-minute breathing coach")
    if "breath_end" not in st.session_state:
        st.session_state.breath_end = None
        st.session_state.breath_running = False

    minutes = st.slider("Minutes", 1, 10, 3)
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("Start", key="breath_start"):
            st.session_state.breath_end = time.time() + minutes * 60
            st.session_state.breath_running = True
    with cols[1]:
        if st.button("Stop", key="breath_stop"):
            st.session_state.breath_running = False
            st.session_state.breath_end = None
    with cols[2]:
        if st.button("Skip", key="breath_skip"):
            st.session_state.breath_running = False
            st.session_state.breath_end = None

    if st.session_state.get("breath_running") and st.session_state.breath_end:
        remaining = int(st.session_state.breath_end - time.time())
        if remaining <= 0:
            st.session_state.breath_running = False
            st.session_state.breath_end = None
            st.success("Breathing session complete 🎉")
        else:
            phase = (remaining // 4) % 2
            st.info("Inhale..." if phase == 0 else "Exhale...")
            st.markdown(f"**Time left:** {remaining}s")
            # Smooth 1-second tick without deprecated APIs
            time.sleep(1)
            st.rerun()

# -------------------------
# PAGE: EXPORT
# -------------------------
elif page == "Export":
    st.title("Export Data & Summary")
    moods = load_moods()
    journal = load_journal()

    st.subheader("Download CSV")
    st.download_button("Download moods.csv", moods.to_csv(index=False).encode("utf-8"), file_name="moods.csv")
    st.download_button("Download journal.csv", journal.to_csv(index=False).encode("utf-8"), file_name="journal.csv")

    st.subheader("Summary report (TXT)")
    txt = summary_text()
    st.text_area("Summary preview", txt, height=200)
    st.download_button("Download summary.txt", txt.encode("utf-8"), file_name="summary.txt")

# Footer
st.markdown("---")
st.caption(
    "This app is an awareness & self-care tool only — not a medical device. If you are in crisis, contact local emergency services or a helpline immediately."
)
