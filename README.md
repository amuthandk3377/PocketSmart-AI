# PocketSmart AI — Smart Budget & Recommendation Assistant

A beginner-friendly full-stack personal finance project built with Python Flask, SQLite, HTML, CSS and JavaScript.

## Features

- Dashboard with income, expenses and balance
- Add income/expense transactions
- Delete transactions
- Expense category analysis
- Visual spending chart
- Smart rule-based recommendations
- SQLite database — no separate database server required
- Responsive UI
- No API key required

## Project Structure

```text
PocketSmart-AI/
├── app.py
├── database.py
├── recommender.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Run in VS Code

### 1. Open the folder

Extract `PocketSmart-AI.zip` and open the `PocketSmart-AI` folder in VS Code.

### 2. Create a virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Run

```bash
python app.py
```

### 5. Open in browser

```text
http://127.0.0.1:5000
```

The SQLite database file `pocketsmart.db` will be created automatically.

## Notes

This is an educational budget assistant. Its recommendations are rule-based and are not financial advice. You can later connect a generative AI API for natural-language recommendations.
