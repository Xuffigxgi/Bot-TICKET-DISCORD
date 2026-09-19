# 🎫 Discord Ticket Bot (Python / discord.py)

A clean and efficient Discord Ticket System bot built with Python using `discord.py`. It features interactive buttons, automatic channel permission management, chat history transcripts, and automated logging to an admin channel when a ticket is closed.

---

## 🚀 Key Features

- **🎫 Interactive Ticket Panels:** Supports multiple customizable topics (e.g., buying products, contacting administration).
- **🔒 Automatic Permission Management:** Automatically restricts channel visibility to the ticket creator and designated admin roles only.
- **🚫 Duplicate Prevention:** Prevents users from opening multiple tickets simultaneously.
- **📝 Transcript & Close System:** Automatically captures chat history, builds an embed summary, sends it to the admin channel, and safely deletes the ticket channel when closed.
- **⚙️ Simple Setup Command:** Easily deploy the ticket panel anywhere using the `!setup` command.

---

## 🛠️ Prerequisites

- Python 3.8 or higher
- `discord.py` library

---

## 📦 Installation & Setup

### 1. Install Dependencies
Open your Terminal or Command Prompt and run:
```bash
pip install discord.py
```

### 2. Configure Your Bot (`bot.py`)
Paste your code into a Python file (e.g., `bot.py`) and update the configuration variables at the top to match your server details:

```python
TOKEN = "YOUR_TOKEN_BOT"               # Your Discord Bot Token from the Developer Portal
GUILD_ID = 1419282589105000541          # Your Discord Server ID
ADMIN_ROLE_ID = 1421730357991968818     # Admin Role ID (allowed to view tickets)
ADMIN_CHANNEL_ID = 1422224061819256883 # Admin Channel ID (for alerts and ticket logs)
CATEGORY_ID = 1421731612881846355       # Category ID where new tickets will be created
```

### 3. Enable Intents in Discord Developer Portal
Go to the [Discord Developer Portal](https://discord.com/developers/applications), select your application, navigate to the **Bot** tab, and enable:
- **Server Members Intent** (Enabled)
- **Message Content Intent** (Enabled)

### 4. Run the Bot
Execute the script via Command Line:
```bash
python bot.py
```
If successful, you will see the following message in your console:
```text
✅ Bot is online: YourBotName#0000
```

---

## 🕹️ Usage

1. Type the `!setup` command in the channel where you want the ticket panel to appear (requires Administrator permissions).
2. The bot will send an embed message with interactive buttons.
3. Users can click any button to instantly generate a private ticket channel.
4. Inside the ticket channel, click the **"🔒 Close"** button to archive the conversation, send a transcript to the admin channel, and delete the ticket channel automatically.
