## ภาษาไทยอยู่ด่านล่าง

![BOT](https://cdn.discordapp.com/attachments/1401474726253039662/1550811035613528124/Screenshot_20260919-170708.jpg?ex=6aafb0d3&is=6aae5f53&hm=e5c42da7ece77006df2a736633aa022ef7a75c90d88185a79103ff373e896326&)
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

# 🎫 Discord Ticket Bot (Python / discord.py)

บอทระบบเปิดตั๋ว (Ticket System) สำหรับ Discord เขียนด้วยภาษา Python โดยใช้ไลบรารี `discord.py` รองรับการสร้างปุ่มอินเทอร์แอกชัน (Buttons) จัดการสิทธิ์การมองเห็นห้องอัตโนมัติ บันทึกประวัติการสนทนา (Transcript) และส่งสรุปเข้าห้องแอดมินเมื่อทำการปิดตั๋ว

---

## 🚀 ฟีเจอร์หลักของบอท

- **🎫 ระบบเปิดตั๋วแบบปุ่ม (Ticket Panels):** รองรับหลากหลายหัวข้อ (เช่น ซื้อสินค้า, ติดต่อแอดมิน)
- **🔒 ระบบจัดการสิทธิ์อัตโนมัติ:** ให้สิทธิ์เฉพาะผู้ใช้ที่เปิดตั๋วและยศแอดมินที่กำหนดเท่านั้นที่มองเห็นห้อง
- **🚫 ป้องกันการเปิดตั๋วซ้ำ:** ระบบตรวจสอบหากผู้ใช้มีตั๋วเปิดอยู่แล้วจะไม่สามารถเปิดซ้ำได้
- **📝 ระบบปิดตั๋วและบันทึกประวัติ (Transcript):** บันทึกข้อความการสนทนาพร้อมส่งสรุป (Embed) ไปยังห้องแอดมินอัตโนมัติเมื่อกดปิดตั๋ว
- **⚙️ คำสั่ง Setup ง่ายๆ:** ใช้คำสั่ง `!setup` เพื่อส่งแผงปุ่มตั๋วไปยังห้องที่ต้องการทันที

---

## 🛠️ ข้อกำหนดเบื้องต้น (Prerequisites)

- Python 3.8 หรือสูงกว่า
- ไลบรารี `discord.py`

---

## 📦 วิธีการติดตั้งและรันบอท

### 1. ติดตั้งไลบรารีที่จำเป็น
เปิด Terminal / Command Prompt แล้วพิมพ์คำสั่ง:
```bash
pip install discord.py
```

### 2. ตั้งค่าไฟล์บอท (`bot.py`)
นำโค้ดไปใส่ในไฟล์ Python (เช่น `bot.py`) แล้วทำการแก้ไขตัวแปรตั้งค่าด้านบนของโค้ดให้ตรงกับเซิร์ฟเวอร์ของคุณ:

```python
TOKEN = "YOUR_TOKEN_BOT"               # Token ของบอท Discord (จาก Discord Developer Portal)
GUILD_ID = 1419282589105000541          # ไอดีเซิร์ฟเวอร์ของคุณ
ADMIN_ROLE_ID = 1421730357991968818     # ไอดียศแอดมิน (สามารถมองเห็นห้องตั๋วได้)
ADMIN_CHANNEL_ID = 1422224061819256883 # ช่องแอดมิน (สำหรับรับแจ้งเตือนและสรุปตั๋ว)
CATEGORY_ID = 1421731612881846355       # ไอดีหมวดหมู่ (Category) ที่ต้องการสร้างห้องตั๋ว
```

### 3. เปิดใช้งาน Intent ใน Discord Developer Portal
ไปที่ [Discord Developer Portal](https://discord.com/developers/applications) เลือกแอปพลิเคชันของคุณ ไปที่เมนู **Bot** แล้วเปิดใช้งาน:
- **Server Members Intent** (เปิด)
- **Message Content Intent** (เปิด)

### 4. รันบอท
รันไฟล์ผ่าน Command Line:
```bash
python bot.py
```
หากสำเร็จ จะแสดงข้อความในคอนโซล:
```text
✅ บอทออนไลน์: ชื่อบอทของคุณ#0000
```

---

## 🕹️ วิธีใช้งาน

1. พิมพ์คำสั่ง `!setup` ในห้องที่ต้องการให้ผู้ใช้งานเข้ามาเปิดตั๋ว (ผู้ใช้ต้องมีสิทธิ์ Administrator)
2. บอทจะแสดงหน้าต่างพร้อมปุ่มเปิดตั๋ว
3. ผู้ใช้สามารถกดปุ่มเพื่อสร้างห้องตั๋วส่วนตัวได้ทันที
4. ภายในห้องตั๋วจะมีปุ่ม **"🔒 Close"** สำหรับให้แอดมินหรือผู้เกี่ยวข้องกดปิดตั๋ว บอทจะทำการส่ง Transcript Discord
