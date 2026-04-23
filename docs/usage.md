# Usage Guide

## Prerequisites
- Python 3.10+
- Docker & docker-compose
- Telegram account + API credentials from my.telegram.org

## Installation
```
git clone https://github.com/username/telegram-channel-parser
cd telegram-channel-parser
uv sync
cp .env.example .env
# fill in your credentials
```

## Running with Docker
```
docker-compose up -d
python main.py
```

## Running manually

# Start PostgreSQL first, then:
```
python main.py
```

## CLI options
```
python main.py --channels 500 --posts 5
```
## Viewing data
Open ```http://localhost:5050``` (pgAdmin)
- login: admin@admin.com
- password: admin
