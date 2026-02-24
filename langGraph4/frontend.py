import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from backend import g, generate_thread_id, list_threads, get_thread_messages

# if there is a set named threads in session state, use it, otherwise initialize it using list_threads() from backend 
if "threads" not in st.session_state:
    st.session_state["threads"] = list_threads()

def create_new_thread():
    new_thread_id = generate_thread_id()
    st.session_state["threads"].add(new_thread_id)
    st.session_state["current_thread"] = new_thread_id
    st.session_state["chat_history"] = [] 


# if current thread is not in session state, initialize it using generate_thread_id() from backend
if "current_thread" not in st.session_state:
   create_new_thread()

# New chat button
if st.sidebar.button("New Chat", key="new_chat_btn"):
    create_new_thread()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = get_thread_messages(st.session_state["current_thread"])

# Show thread buttons
for tid in st.session_state["threads"]:
    if st.sidebar.button(f"Thread {tid[:8]}", key=f"thread_{tid}"):
        st.session_state["current_thread"] = tid
        st.session_state["chat_history"] = get_thread_messages(tid)

st.title("Chatbot")

# Show chat history for the current thread
for msg in st.session_state["chat_history"]:
    if msg.get("role") == "human":
        with st.chat_message("user"):
            st.write(msg['content'])
    elif msg.get("role") == "ai":
        with st.chat_message("assistant"):
            st.write(msg['content'])

# User input block
if prompt := st.chat_input("Type your message..."):
    # Add the user's message to the chat history
    st.session_state["chat_history"].append({"role": "human", "content": prompt})
    response = g.invoke({"messages": [HumanMessage(prompt)]}, config={"configurable": {"thread_id": st.session_state["current_thread"]}})['messages'][-1].content
    st.session_state["chat_history"].append({"role": "ai", "content": response})
    st.rerun()  # Rerun the app to update the chat history with the new messages
    # Here you can add code to process the input and generate a response
