# 🤖 Omni-Channel ERP Assistant

Welcome to the Omni-Channel ERP Assistant! This project connects a live WhatsApp phone number directly to a Zoho Inventory database using an advanced Artificial Intelligence brain. 

Instead of navigating complex software, you can simply send a text message or a voice note to your WhatsApp bot, and it will autonomously check stock levels, deduct inventory, and reply to you in plain English.

---

## ✨ Features
* **Conversational AI:** Talk to your database like you are talking to a human manager.
* **Voice Note Support:** Send an audio message on WhatsApp, and the system will transcribe it and execute the command.
* **Live ERP Sync:** Instantly reads and updates your Zoho Inventory stock levels.
* **100% Free Tier Architecture:** Built using open-source tools and free developer tiers.

---

## 🛠️ Prerequisites
Before you start, you will need to have these accounts set up:
1. **Meta Developer Account:** For the WhatsApp Business Cloud API.
2. **Zoho Developer Account:** To access your Zoho Inventory.
3. **Groq Account:** To power the AI brain (Llama 3.3).
4. **Ngrok Account:** To connect your local computer to the internet securely.

---

## 🚀 Setup Instructions

### Step 1: Prepare Your Environment
Open your computer's terminal (If on Windows, open your **WSL/Ubuntu** terminal) and navigate to the project folder. 

Create a secure virtual environment and activate it:
```bash
# Create the environment
python -m venv venv

# Activate it (Linux/Mac/WSL)
source venv/bin/activate