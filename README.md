# 🤖 Groq AI Chatbot

A conversational AI chatbot built using **Python, Streamlit, and Groq API**. It supports multiple chat sessions, streaming responses, user feedback, and a password-protected admin dashboard for viewing conversations and usage analytics.

## 🚀 Features

- AI-powered chatbot using Groq API
- Real-time streaming responses
- Multiple chat sessions
- Conversation history
- 👍 / 👎 user feedback
- Admin dashboard with password protection
- View user conversations and questions
- Usage analytics and popular questions
- SQLite database (local development)

## 🛠️ Technologies Used

- Python
- Streamlit
- Groq API
- SQLite
- Pandas
- Python-dotenv

## 📁 Project Structure

```text
mini_ai_chatbot/
│
├── app.py
├── backend.py
├── database.py
├── requirements.txt
├── .env
├── .gitignore
│
└── pages/
    └── 1_Admin_Dashboard.py
```

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/gobinath0105-lgtm/mini-ai-chatbot.git
```

### 2. Open the project folder

```bash
cd mini-ai-chatbot
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment (Windows PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project folder:

```env
GROQ_API_KEY=your_groq_api_key
ADMIN_PASSWORD=your_private_admin_password
```

Get your Groq API key from:

https://console.groq.com/keys

**Never upload your `.env` file to GitHub.**

### 7. Run the chatbot

```bash
streamlit run app.py
```

The application will open in your browser.

## ☁️ Deploy on Streamlit Community Cloud

### Step 1: Upload your project to GitHub

Push your project repository to GitHub.

### Step 2: Open Streamlit Community Cloud

https://share.streamlit.io/

Sign in using your GitHub account.

### Step 3: Create a new application

1. Click **Create app**.
2. Select your GitHub repository.
3. Select
