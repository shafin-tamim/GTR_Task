# Algorithmic Trading & Samsung Phone Advisor

This repository contains two independent projects implemented using Python.

## Task 1: Algorithmic Trading Adventure

### Overview

A Python-based algorithmic trading system that:
- Downloads stock data using yfinance
- Computes 50-day and 200-day moving averages
- Buys on Golden Cross
- Sells on Death Cross
- Uses a fixed $5000 budget
- Calculates final profit or loss

### How to Run

1. Go to `task1_trading` folder
2. Run: `python trading_strategy.py`

### Output

- BUY / SELL trade history
- Initial capital
- Final capital
- Profit or Loss

## Task 2: Samsung Phone Advisor

### Overview

A smart assistant system that:
- Scrapes Samsung phone data from GSMArena using BeautifulSoup
- Stores data in PostgreSQL
- Uses RAG for factual answers
- Uses Multi-Agent system for comparison and recommendation
- Exposes a single FastAPI endpoint `/ask`

## Technologies Used

- Python 3.10
- yfinance
- pandas
- numpy
- FastAPI
- PostgreSQL
- psycopg2
- BeautifulSoup4
- requests
- Conda Environment

## Project Structure

```
.
├── task1_trading/
│   └── trading_strategy.py
├── task2_samsung_phone_advisor/
│   ├── scrape_gsmarena.py
│   ├── database.py
│   ├── agents.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Setup

### Conda Environment

```bash
conda create -n samsung_ai python=3.10 -y
conda activate samsung_ai 
pip install -r requirements.txt
```

### Task 2 Database Setup

```sql
CREATE TABLE samsung_phones (
    id SERIAL PRIMARY KEY,
    model TEXT UNIQUE,
    display TEXT,
    battery INTEGER,
    camera TEXT,
    ram INTEGER,
    storage INTEGER,
    price INTEGER
);
```

## Running Task 2

1. Go to `task2_samsung_phone_advisor` folder
2. Run scraping once: `python scrape_gsmarena.py`
3. Start API server: `uvicorn main:app --reload`
4. Open browser: http://127.0.0.1:8000/docs

## API Usage

**Endpoint:** `POST /ask`

**Input Example:**
```json
{
  "question": "Compare Samsung Galaxy S23 Ultra and S22 Ultra"
}
```

**Output Example:**
```json
{
  "answer": "Samsung Galaxy S23 Ultra has better camera performance and battery life than S22 Ultra."
}
```

## System Architecture (Task 2)

```
User Query
   ↓
FastAPI (/ask)
   ↓
RAG (PostgreSQL)
   ↓
Multi-Agent System
   ↓
Unified Response
```

## Demo

A short demo video showing both tasks running is provided via 
Google Drive: https://drive.google.com/file/d/1rMzLXU4edcTUWD3T1oqYCKAI1t8lnrko/view?usp=drive_link

