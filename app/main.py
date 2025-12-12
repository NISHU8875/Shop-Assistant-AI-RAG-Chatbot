import streamlit as st
import time
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from chitchat import chitchat_chain
from pathlib import Path
from router import router

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="E-commerce Assistant",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize Database
faqs_path = Path(__file__).parent / "resources/faq_data.csv"
if "db_init" not in st.session_state:
    with st.spinner("Waking up the database..."):
        ingest_faq_data(faqs_path)
    st.session_state["db_init"] = True

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! I am your shopping assistant. Ask me about products, policies, or just say hi! 👋"}
    ]

# --- 2. CSS FOR "LIVELY" BACKGROUND & FIXES ---
st.markdown("""
<style>
    /* 1. ANIMATED BACKGROUND */
    .stApp {
        background: linear-gradient(to left, #8f94fb, #4e54c8);
        background-attachment: fixed;
    }
    
    /* 2. CHAT MESSAGE STYLING (Fixed Overflow) */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid transparent;
        transition: all 0.3s ease;
        position: relative;
        z-index: 1;
        
        /* CRITICAL FIX: Prevents text from spilling out */
        word-wrap: break-word;
        word-break: break-word;
        overflow-wrap: break-word;
    }
    
    /* 2. CHAT MESSAGE STYLING (Fixed Overflow) */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        
        /* ADD THIS LINE HERE: */
        font-size: 40px;  /* Change 18px to whatever size you want */
        
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid transparent;
        transition: all 0.3s ease;
        position: relative;
        z-index: 1;
        
        /* CRITICAL FIX: Prevents text from spilling out */
        word-wrap: break-word;
        word-break: break-word;
        overflow-wrap: break-word;
    }

    /* Force links to wrap inside the box */
    .stChatMessage a {
        word-break: break-all; 
    }

    /* Hover Effect */
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        border-left: 5px solid #4e54c8;
    }

    /* 3. INPUT BOX STYLING (In-Flow) */
    /* Remove default styling to make it look cleaner */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.5);
        padding: 10px 15px;
        color: #333;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* 3. INPUT BOX STYLING (In-Flow) */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        
        /* ADD THIS LINE HERE: */
        font-size: 18px; 
        
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.5);
        padding: 10px 15px;
        color: #333;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
            
    /* Focus state for input */
    .stTextInput > div > div > input:focus {
        border-color: #fff;
        box-shadow: 0 0 15px rgba(255,255,255,0.3);
    }

    /* Hide Header and Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Background Animation Circles */
    .area {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
    }
    .circles {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }
    .circles li {
        position: absolute;
        display: block;
        list-style: none;
        width: 20px;
        height: 20px;
        background: rgba(255, 255, 255, 0.2);
        animation: animate 25s linear infinite;
        bottom: -150px;
        border-radius: 50%;
    }
    /* Randomizing bubbles */
    .circles li:nth-child(1){ left: 25%; width: 80px; height: 80px; animation-delay: 0s; }
    .circles li:nth-child(2){ left: 10%; width: 20px; height: 20px; animation-delay: 2s; animation-duration: 12s; }
    .circles li:nth-child(3){ left: 70%; width: 20px; height: 20px; animation-delay: 4s; }
    .circles li:nth-child(4){ left: 40%; width: 60px; height: 60px; animation-delay: 0s; animation-duration: 18s; }
    .circles li:nth-child(5){ left: 65%; width: 20px; height: 20px; animation-delay: 0s; }
    
    @keyframes animate {
        0%{ transform: translateY(0) rotate(0deg); opacity: 1; border-radius: 0; }
        100%{ transform: translateY(-1000px) rotate(720deg); opacity: 0; border-radius: 50%; }
    }
</style>

<div class="area" >
    <ul class="circles">
        <li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li>
    </ul>
</div >
""", unsafe_allow_html=True)

# --- 3. LOGIC ---
def ask(query):
    """Route the query to appropriate handler"""
    try:
        route = router(query)
        if route is None or route.name is None:
            return chitchat_chain(query)
        
        route_name = route.name
        if route_name == 'faq':
            return faq_chain(query)
        elif route_name == 'sql':
            return sql_chain(query)
        elif route_name == 'chitchat':
            return chitchat_chain(query)
        else:
            return chitchat_chain(query)
    except Exception as e:
        return f"I encountered a slight hiccup: {str(e)}"

# --- 4. UI RENDER ---

st.title("🛍️ ShopAssist")

# Display Chat History
for message in st.session_state.messages:
    avatar = "👤" if message['role'] == "user" else "🦄"
    with st.chat_message(message['role'], avatar=avatar):
        st.markdown(message['content'])

# --- 5. THE NEW "IN-FLOW" INPUT BOX ---
# We use st.text_input instead of chat_input so it sits here, at the bottom of the list
def submit_query():
    user_input = st.session_state.query_input
    if user_input:
        # 1. Append User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 2. Append Placeholder for Assistant
        st.session_state.messages.append({"role": "assistant", "content": "..."})
        
        # 3. Clear Input
        st.session_state.query_input = ""

# Input Field
st.text_input(
    label="Ask me anything...", 
    placeholder="Type your question here...", 
    key="query_input", 
    label_visibility="collapsed",
    on_change=submit_query
)

# Process Response (If the last message is "...")
if st.session_state.messages and st.session_state.messages[-1]["content"] == "...":
    # Get the actual query from the user (second to last message)
    last_query = st.session_state.messages[-2]["content"]
    
    # Generate Answer
    response = ask(last_query)
    
    # Update the "..." placeholder with the real response
    st.session_state.messages[-1]["content"] = response
    
    # Rerun to show the final result
    st.rerun()