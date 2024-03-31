# Krll
Krll, a privacy-friendly URL shortener

https://krll.me

## Dev
Copy `.env.example` to `.env` and edit it
```
python -m venv venv
source ./venv/bin/activate/
pip install -r requirements.txt
uvicorn main:app --reload
```