# Profile Telegram Bot

Telegram bot for creating and managing user profiles with SQLite database.

## Features
- Create profile (name, age, city)
- Inline keyboard buttons for age selection
- Edit specific profile fields (name, age, city separately)
- Delete profile
- SQLite database — data is saved permanently
- /profile command to view profile
- /help command

## Tech Stack
- Python 3.11
- python-telegram-bot library
- SQLite3 for data storage
- ConversationHandler for multi-step dialog

## How to run
1. Install library: pip install python-telegram-bot
2. In anketa_bot.py replace token: TOKEN = "your_token_here"
3. Run: python anketa_bot.py

## Files
- anketa_bot.py — main bot file
- database.py — database functions
