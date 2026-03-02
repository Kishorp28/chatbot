import os
import mimetypes
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------------------------------------------------
# Configuration & Setup
# -------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found. Please set it in your environment or .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------------------------------------------
# Streamlit UI Configuration
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Glassmorphism look)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e1e2f 0%, #25293e 100%);
        color: white;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #ff4b2b, #ff416c);
        color: white;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# Sidebar - App Info & Capabilities
# -------------------------------------------------------------------
with st.sidebar:
    st.title("🤖 AI Assistant")
    st.info("Experience the power of Gemini 1.5 Flash")
    
    st.subheader("🚀 Features")
    st.markdown("""
    - **💬 Instant Chat**: Real-time AI conversations.
    - **📂 File Analysis**: Upload PDF, Images, or Docs.
    - **⚡ Fast Response**: Powered by Flash model.
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# -------------------------------------------------------------------
# Chat Interface
# -------------------------------------------------------------------
st.title("💬 Smart AI Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask me anything..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {e}")

# -------------------------------------------------------------------
# File Upload Section (Sticky at bottom or in sidebar - here we use bottom)
# -------------------------------------------------------------------
st.divider()
st.subheader("📂 Analyze Documents or Images")

uploaded_file = st.file_uploader(
    "Upload a file for AI breakdown", 
    type=["jpg", "jpeg", "png", "gif", "webp", "pdf", "doc", "docx"],
    help="Limit 200MB"
)

if uploaded_file:
    # Save file temporarily
    temp_filename = f"temp_{uploaded_file.name}"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    mime_type, _ = mimetypes.guess_type(temp_filename)
    mime_type = mime_type or "application/octet-stream"

    if st.button("🔍 Analyze File"):
        with st.spinner("Processing file with Gemini..."):
            try:
                # Upload to Gemini
                gemini_file = genai.upload_file(temp_filename, mime_type=mime_type)
                
                # Chat with file
                chat = model.start_chat()
                response = chat.send_message([gemini_file, "Summarize this file and extract key details."])
                
                st.success("✅ Analysis Complete!")
                st.write(response.text)
                
                # Add to history
                st.session_state.messages.append({"role": "assistant", "content": f"📎 **Analyzed File: {uploaded_file.name}**\n\n{response.text}"})

            except Exception as e:
                st.error(f"Analysis failed: {e}")
            finally:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
