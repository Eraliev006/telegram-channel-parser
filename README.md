![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![asyncio](https://img.shields.io/badge/asyncio-powered-orange)

# 🔍 Telegram Channel Parser

Async parser for public Telegram channels.  
Collects channel metadata and last posts, stores everything in PostgreSQL.

---

## 🛠 Tech Stack

- Python 3.10+
- Telethon — Telegram API client
- asyncpg — async PostgreSQL driver
- PostgreSQL — main database
- Docker & docker-compose — local environment

---

## 📁 Project Structure
```
telegram-channel-parser/
├── config.py        # loads env variables
├── db.py            # database connection and queries
├── parser.py        # main script
├── channels.txt     # list of telegram channels
├── docs/
│   ├── architecture.md
│   └── usage.md
├── .env.example
├── docker-compose.yml
├── requirements.txt
└── README.md
```
---

## 🗄 Database Schema

Two tables: `channels` and `posts`.  
See full schema → [docs/architecture.md](docs/architecture.md)

---

## ⚙️ Installation
```
git clone https://github.com/yourusername/telegram-channel-parser
cd telegram-channel-parser

# with uv (recommended)
uv sync

# or with pip
pip install -r requirements.txt

cp .env.example .env
```
---

## 🔧 Configuration

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|----------|-------------|
| TG_API_ID | Telegram API ID from my.telegram.org |
| TG_API_HASH | Telegram API Hash |
| DB_HOST | PostgreSQL host |
| DB_PORT | PostgreSQL port |
| DB_NAME | Database name |
| DB_USER | Database user |
| DB_PASSWORD | Database password |

---

## 🚀 Usage

# Run with Docker
docker-compose up

# Or run manually
python parser.py

# Options
python parser.py --channels 500 --posts 10

---

## 📚 Documentation

- [Architecture & Database Schema](docs/architecture.md)
- [Usage Guide](docs/usage.md)

---

## 📄 License

MIT