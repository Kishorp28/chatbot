# AI-Powered Gemini Chatbot

An intelligent web-based chatbot powered by **Google Gemini (Generative AI)**.  
Built using **Streamlit** for the frontend and deployed on **Streamlit Cloud**.

🔗 **Live Application:**  
https://kishorp28-chatbot-gemniapp-iipy31.streamlit.app/

---

## 📌 Project Overview

This project is a real-time AI chatbot that leverages Google’s **Gemini 1.5 Flash** model to generate human-like responses.

The application provides:

- Text-based conversational AI
- File upload support (images, PDFs, documents)
- Instant AI-generated summaries and responses
- Clean and interactive Streamlit interface

This project demonstrates API integration, environment management, secure deployment, and cloud hosting.

---

## 🚀 Features

- 💬 Real-time conversational chatbot
- 📄 File upload and AI-based file analysis
- ⚡ Fast responses using Gemini 1.5 Flash
- 🔐 Secure API key handling using environment variables
- 🌐 Cloud deployment via Streamlit

---

## 🛠 Tech Stack

### Frontend
- Streamlit

### Backend / AI Integration
- Python
- Google Generative AI (Gemini API)

### File Handling
- Streamlit file uploader
- Secure temporary storage

### Deployment
- Streamlit Community Cloud

---

## ⚙️ Installation (Run Locally)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Kishorp28/chatbot.git
cd chatbot
```

(Replace with your actual repo link if different.)

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Environment Variable

Create a `.env` file in the root folder:

```
GOOGLE_API_KEY=your_api_key_here
```

Or export manually:

**Mac/Linux**
```bash
export GOOGLE_API_KEY=your_api_key_here
```

**Windows**
```bash
set GOOGLE_API_KEY=your_api_key_here
```

---

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

Open the local URL shown in your terminal.

---

## 🔐 Streamlit Cloud Deployment

When deploying to Streamlit Cloud:

1. Push project to GitHub
2. Connect repository to Streamlit Cloud
3. Set `app.py` as the entry file
4. Add secret in **App Settings → Secrets**

Example:

```
GOOGLE_API_KEY = "your_api_key_here"
```

Then access in code using:

```python
import streamlit as st
api_key = st.secrets["GOOGLE_API_KEY"]
```

Do NOT upload `.env` to GitHub.

---

## 🧠 How It Works

1. User enters a message or uploads a file.
2. The app sends the input to Gemini API.
3. Gemini processes the request.
4. The AI-generated response is displayed instantly.

For file uploads:
- File is processed
- Content is sent to Gemini
- Summary or analysis is generated
- Temporary file is removed after processing

---

## 📊 Use Cases

- AI-powered Q&A assistant
- Document summarization
- Quick PDF insights
- Educational AI tool
- Productivity assistant

---

## 🔮 Future Improvements

- Conversation memory across sessions
- Multi-file comparison
- Advanced prompt customization
- Chat history export
- Authentication system
- Rate limiting & logging

---

## 👨‍💻 Author

Kishore  
Built using Streamlit + Google Gemini API

---

## 📄 License

This project is licensed under the MIT License.
