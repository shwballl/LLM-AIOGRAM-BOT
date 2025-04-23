
# 🤖 LLM-AIOGRAM-BOT

A Telegram bot powered by the [Aiogram](https://aiogram.dev) library with AI integration.

## ✨ Features

- AI-enhanced responses
- Structured command handlers
- Clean modular architecture
- Logging support

## 📁 Structure

```
LLM-AIOGRAM-BOT/
├── app/                # Main bot logic and handlers
├── logs/               # Logging directory
├── utils/              # Utility functions and services
├── logger_config.py    # Logging configuration
├── requirements.txt    # Python dependencies
├── run.py              # Entry point for the bot
└── .env                # Environment config (not tracked)
```

## ⚙️ Installation

```bash
git clone https://github.com/shwballl/LLM-AIOGRAM-BOT.git
cd LLM-AIOGRAM-BOT
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## 🔐 Configuration

Create a `.env` file:

```
BOT_TOKEN=your_telegram_token
GITHUB_API_KEY=your_github_api_key
```

## 🚀 Run the Bot

```bash
python run.py
```

## 🧠 AI Usage

Bot responses can include AI-powered completions depending on your logic in the `app` and `utils`.

## 🛠 Tech Stack

- Python 3.10+
- Aiogram
- OpenAI/GitHub APIs

## 📄 License

MIT License


