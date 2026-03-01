# Krll
Krll, a privacy-friendly open source URL shortener

https://krll.me

## Installation
1. Copy `.env.example` to `.env` and edit it
- `NAME`: Krll server's name(ex: Krll)
- `HOST`: Krll server's host(ex: https://krll.me)
- `CONTACT`: Server operator's contact info
- `POSTGRES_...`: PostgreSQL setting(If you'll run postgresql with docker compose, you should edit just `POSTGRES_PASSWORD`, if not, you should edit `POSTGRES_HOST` to your postgresql's host.)

2. Run
```bash
# with docker compose
cp docker-compose.example.yml docker-compose.yml
docker compose up -d

# without docker compose
# You need an external PostgreSQL server 
python -m venv venv
source ./venv/bin/activate/ # ./venv/Scripts/activate
pip install -r requirements.txt
fastapi dev main.py
```

3. Create an admin account
```bash
# with docker compose
docker exec -it krll-web-1 python main.py create_admin

# without docker compose
source ./venv/bin/activate/ # ./venv/Scripts/activate
python main.py create_admin
```
Go to `https://<your krll instance address>/admin` to use the admin dashboard.