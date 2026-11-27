
import streamlit as st
import os
import hmac
import pandas as pd

from dotenv import load_dotenv
import database


st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

load_dotenv()
database.initialize_database()

st.title("📊 Chatbot Admin Dashboard")
st.caption("Private owner dashboard")


# --------------------------------
# Admin authentication
# --------------------------------

admin_password = os.getenv("ADMIN_PASSWORD")

if not admin_password:
    st.error("ADMIN_PASSWORD is missing from your .env file.")
    st.stop()

if not st.session_state.get("admin_authenticated", False):

    st.subheader("🔐 Admin Login")

    with st.form("admin_login"):

        entered_password = st.text_input(
            "Enter admin password",
            type="password"
        )

        submitted = st.form_submit_button("Login")

        if submitted:

            if hmac.compare_digest(
                entered_password,
                admin_password
            ):

                st.session_state.admin_authenticated = True
                st.rerun()

            else:
                st.error("Incorrect password")

    st.stop()


# --------------------------------
# Logout
# --------------------------------

if st.button("Logout"):
    st.session_state.admin_authenticated = False
    st.rerun()


# --------------------------------
# Analytics
# --------------------------------

visitors, questions, conversations, positive, negative = (
    database.get_analytics()
)

st.divider()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Visitor Sessions", visitors)
col2.metric("Questions", questions)
col3.metric("Conversations", conversations)
col4.metric("👍 Positive", positive)
col5.metric("👎 Negative", negative)


# --------------------------------
# Feedback chart
# --------------------------------

st.subheader("Feedback Overview")

if positive + negative > 0:

    feedback_data = pd.DataFrame({
        "Feedback": ["Helpful", "Not Helpful"],
        "Count": [positive, negative]
    })

    st.bar_chart(
        feedback_data.set_index("Feedback")
    )

else:
    st.info("No feedback collected yet.")


# --------------------------------
# Conversation history
# --------------------------------

st.divider()

st.subheader("💬 User Conversations")

all_chats = database.get_all_conversations()

if all_chats:

    chat_options = {
        f"{row[2]} | {row[3][:16]} | {row[1][:8]}": row[0]
        for row in all_chats
    }

    selected_label = st.selectbox(
        "Select a conversation",
        list(chat_options.keys())
    )

    selected_chat_id = chat_options[selected_label]

    conversation_messages = (
        database.get_conversation_messages(selected_chat_id)
    )

    st.markdown("### Complete Conversation")

    for role, content, created_at in conversation_messages:

        with st.chat_message(
            "user" if role == "user" else "assistant"
        ):

            st.caption(created_at)
            st.markdown(content)

else:

    st.info("No conversations available yet.")


# --------------------------------
# Popular questions
# --------------------------------

st.divider()

st.subheader("🔥 Most Asked Questions")

popular_questions = database.get_popular_questions()

if popular_questions:

    popular_df = pd.DataFrame(
        popular_questions,
        columns=["Question", "Times Asked"]
    )

    st.dataframe(
        popular_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No questions collected yet.")


st.caption("Chatbot Analytics | Private Admin Area")
