# Library Management System

## Features
- Book and Member Management (CRUD)
- Issue and Return transactions with fees
- Book Import from Frappe API
- Debt limit enforcement (₹500 max)

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:FLASK_APP = run.py
flask db init
flask db migrate -m "initial"
flask db upgrade
python run.py
```

## Usage
- `/books` to manage books
- `/members` to manage members
- `/transactions/issue` to issue books
- `/transactions/return` to return books
- `/import-books` to import from Frappe API

## Screenshots

<img width="1677" height="300" alt="Screenshot 2025-07-17 100545" src="https://github.com/user-attachments/assets/25bdaa23-00d9-44ec-9c89-a9a460e25a28" />

1. "/books"

   <img width="1897" height="997" alt="Screenshot 2025-07-17 100639" src="https://github.com/user-attachments/assets/1aabe1ba-e3bc-499a-a482-1532ee578f23" />
   <img width="770" height="1010" alt="Screenshot 2025-07-17 100703" src="https://github.com/user-attachments/assets/63654c7b-0e17-42b2-97ae-17d33101356e" />
   <img width="541" height="1000" alt="Screenshot 2025-07-17 100737" src="https://github.com/user-attachments/assets/5e313baf-96ad-45c8-9f97-2f600540fd3f" />

2. "/members"

   <img width="1532" height="453" alt="Screenshot 2025-07-17 100836" src="https://github.com/user-attachments/assets/90066186-18cd-4798-aa91-f3c8bcb5066b" />
   <img width="633" height="608" alt="Screenshot 2025-07-17 100850" src="https://github.com/user-attachments/assets/a18680e9-8605-4b20-abf0-4cd457fa0d76" />

3. "/transactions/issue"

   <img width="1053" height="627" alt="Screenshot 2025-07-17 101820" src="https://github.com/user-attachments/assets/c7b5685b-17ce-459e-bc0b-0e204a0d0400" />

4. "/transactions/return"

   <img width="1064" height="475" alt="Screenshot 2025-07-17 101928" src="https://github.com/user-attachments/assets/45c08ec9-a68c-4de5-926d-ba7148a29386" />

5. "/import-books"

   <img width="1088" height="661" alt="Screenshot 2025-07-17 102022" src="https://github.com/user-attachments/assets/f8ba3160-4f9c-4295-9f05-397a1046bef4" />
