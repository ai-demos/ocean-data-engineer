from typing import List

import streamlit as st
from phi.conversation import Conversation

from app.openai_key import get_openai_key
from app.password import check_password
from app.reload import reload_button
from app.user_name import get_user_name
from llm.conversations.oceangpt import get_oceangpt_conversation
from utils.log import logger


st.title(":snowman: Ocean Data Engineer")
st.markdown('<a href="https://github.com/phidatahq/phidata"><h4>by phidata</h4></a>', unsafe_allow_html=True)


def restart_conversation():
    st.session_state["ocean_conversation"] = None
    st.session_state["ocean_conversation_id"] = None
    st.rerun()


def main() -> None:
    # Get users OpenAI API key
    get_openai_key()

    # Get user name
    user_name = get_user_name()
    if user_name:
        st.sidebar.info(f":technologist: User: {user_name}")
    else:
        st.write(":technologist: Please enter a username")
        return

    # Get the conversation
    ocean_conversation: Conversation
    if "ocean_conversation" not in st.session_state or st.session_state["ocean_conversation"] is None:
        logger.info("---*--- Creating OceanGPT Conversation ---*---")
        ocean_conversation = get_oceangpt_conversation(
            user_name=user_name,
            debug_mode=True,
        )
        st.session_state["ocean_conversation"] = ocean_conversation
    else:
        ocean_conversation = st.session_state["ocean_conversation"]

    # Start conversation and save conversation id in session state
    st.session_state["ocean_conversation_id"] = ocean_conversation.start()

    # Load messages for existing conversation
    user_chat_history = ocean_conversation.memory.get_chat_history()
    if len(user_chat_history) > 0:
        logger.debug("Loading chat history")
        st.session_state["messages"] = user_chat_history
    else:
        logger.debug("No chat history found")
        st.session_state["messages"] = [{"role": "assistant", "content": "Ask me anything..."}]

    # Prompt for user input
    if prompt := st.chat_input():
        st.session_state["messages"].append({"role": "user", "content": prompt})

    # Display existing chat messages
    for message in st.session_state["messages"]:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is from a user, generate a new response
    last_message = st.session_state["messages"][-1]
    if last_message.get("role") == "user":
        question = last_message["content"]
        with st.chat_message("assistant"):
            response = ""
            resp_container = st.empty()
            for delta in ocean_conversation.chat(question):
                response += delta
                resp_container.markdown(response)

            st.session_state["messages"].append({"role": "assistant", "content": response})

    if st.sidebar.button("New Conversation"):
        restart_conversation()

    # if st.sidebar.button("Load All Tables"):
    #     alert = st.sidebar.info("Loading data...", icon="ℹ️")
    #     load_ocean_tables(duckdb_agent=duckdb_ocean_agent)
    #     st.sidebar.success("Tables loaded")
    #     alert.empty()

    if st.sidebar.button("Auto Rename"):
        ocean_conversation.auto_rename()

    if ocean_conversation.storage:
        all_pdf_conversation_ids: List[str] = ocean_conversation.storage.get_all_conversation_ids(
            user_name=user_name
        )
        new_pdf_conversation_id = st.sidebar.selectbox("Conversation ID", options=all_pdf_conversation_ids)
        if st.session_state["ocean_conversation_id"] != new_pdf_conversation_id:
            logger.debug(f"Loading conversation {new_pdf_conversation_id}")
            logger.info("---*--- Loading OceanGPT Conversation ---*---")
            st.session_state["ocean_conversation"] = get_oceangpt_conversation(
                user_name=user_name,
                conversation_id=new_pdf_conversation_id,
                debug_mode=True,
            )
            st.rerun()

    ocean_conversation_name = ocean_conversation.name
    if ocean_conversation_name:
        st.sidebar.write(f":thread: {ocean_conversation_name}")

    # Show reload button
    reload_button()


if check_password():
    main()
