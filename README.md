# 💰 BudgetWise — Personal Budget & Savings App

A clean Flask web app to track income, expenses, and savings goals with charts.

## Features
- ✅ Add income & expense transactions
- ✅ Category breakdown
- ✅ Monthly bar chart (income vs expenses)
- ✅ Expense pie chart
- ✅ Savings goals with progress bars
- ✅ Data stored locally in `data.json`

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://localhost:5000
```

## Project Structure
```
budget_app/
├── app.py              # Flask backend
├── requirements.txt    # Dependencies
├── data.json           # Auto-created on first run
└── templates/
    └── index.html      # Frontend UI
```
