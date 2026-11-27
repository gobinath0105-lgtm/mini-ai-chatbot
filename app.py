
import streamlit as st
import uuid

from backend import get_ai_response
import database


st.set_page_config(
    page_title="Mini AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

database.initialize_database()


# Initialize visitor
if "visitor_id" not in st.session_state:
    st.session_state.visitor_id = str(uuid.uuid4())

visitor_id = st.session_state.visitor_id

database.register_visitor(visitor_id)


# Create new chat
def create_new_chat():

    chat_id = str(uuid.uuid4())

    system_message = {
        "role": "system",
        "content": "You are a helpful AI assistant. Give clear and accurate answers."
    }

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": [system_message],
        "feedback": {}
    }

    database.create_conversation(
        chat_id,
        visitor_id,
        "New Chat"
    )

    st.session_state.active_chat_id = chat_id


# Initialize chats
if "chats" not in st.session_state:
    st.session_state.chats = {}
    create_new_chat()

if "active_chat_id" not in st.session_state:
    create_new_chat()


# Sidebar
with st.sidebar:

    st.title("💬 Conversations")

    if st.button("➕ New Chat", use_container_width=True):
        create_new_chat()
        st.rerun()

    st.divider()

    for chat_id, chat in list(st.session_state.chats.items()):

        col1, col2 = st.columns([5, 1])

        with col1:
            if st.button(
                chat["title"],
                key=f"select_{chat_id}",
                use_container_width=True
            ):
                st.session_state.active_chat_id = chat_id
                st.rerun()

        with col2:
            if st.button("🗑️", key=f"delete_{chat_id}"):

                with database.get_connection() as conn:
                    conn.execute(
                        "DELETE FROM feedback WHERE chat_id=?",
                        (chat_id,)
                    )
                    conn.execute(
                        "DELETE FROM messages WHERE chat_id=?",
                        (chat_id,)
                    )
                    conn.execute(
                        "DELETE FROM conversations WHERE chat_id=?",
                        (chat_id,)
                    )

                del st.session_state.chats[chat_id]

                if chat_id == st.session_state.active_chat_id:
                    if st.session_state.chats:
                        st.session_state.active_chat_id = next(
                            iter(st.session_state.chats)
                        )
                    else:
                        create_new_chat()

                st.rerun()


# Active chat
chat_id = st.session_state.active_chat_id
active_chat = st.session_state.chats[chat_id]

messages = active_chat["messages"]
feedback = active_chat["feedback"]


st.title("🤖 Mini AI Chatbot")
st.caption("Powered by Groq LLM")
st.divider()


# Feedback buttons
def show_feedback(message_id):

    st.caption("Was this response helpful?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Helpful", key=f"like_{message_id}"):
            feedback[message_id] = "positive"

            database.save_feedback(
                message_id, chat_id, "positive"
            )
            st.rerun()

    with col2:
        if st.button("👎 Not helpful", key=f"dislike_{message_id}"):
            feedback[message_id] = "negative"

            database.save_feedback(
                message_id, chat_id, "negative"
            )
            st.rerun()

    if feedback.get(message_id) == "positive":
        st.success("Thanks for your feedback!")

    elif feedback.get(message_id) == "negative":
        st.info("Thanks! We'll work to improve.")


# Display messages
for index, message in enumerate(messages):

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":
            show_feedback(
                message.get("id", f"old_{index}")
            )


# User input
user_input = st.chat_input("Ask me anything...")


if user_input:

    user_message_id = str(uuid.uuid4())

    messages.append({
        "role": "user",
        "content": user_input,
        "id": user_message_id
    })

    database.save_message(
        user_message_id,
        chat_id,
        "user",
        user_input
    )

    if active_chat["title"] == "New Chat":

        active_chat["title"] = user_input[:30]

        database.update_title(
            chat_id,
            active_chat["title"]
        )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        try:

            with st.spinner("AI is thinking..."):

                answer = st.write_stream(
                    get_ai_response(messages)
                )

            message_id = str(uuid.uuid4())

            messages.append({
                "role": "assistant",
                "content": answer,
                "id": message_id
            })

            database.save_message(
                message_id,
                chat_id,
                "assistant",
                answer
            )

            show_feedback(message_id)

        except Exception as error:

            st.error(f"Something went wrong: {error}")

            messages.pop()

            with database.get_connection() as conn:
                conn.execute(
                    "DELETE FROM messages WHERE message_id=?",
                    (user_message_id,)
                )


st.divider()

st.caption(
    "💬 If you don't mind, please use this chatbot "
    "and share your feedback. Thank you! ❤️"
)
