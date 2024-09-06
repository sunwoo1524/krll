# Krll
Krll, a privacy-friendly open source URL shortener

https://krll.me

## Run
1. Copy `.env.example` to `.env` and edit it
- `NAME`: Krll server's name(ex: Krll)
- `HOST`: Krll server's host(ex: https://krll.me)
- `CONTACT`: Server operator's contact info
- `POSTGRES_...`: PostgreSQL setting(If you'll run postgresql with docker compose, you should edit just `POSTGRES_PASSWORD`, if not, you should edit `POSTGRES_HOST` to your postgresql's host.)

2. RUN
```bash
# with docker compose
cp docker-compose.example.yml docker-compose.yml
docker compose up -d

# without docker compose
python -m venv venv
source ./venv/bin/activate/ # ./venv/Scripts/activate
pip install -r requirements.txt
fastapi dev main.py
```