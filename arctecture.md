# Architectural Specification - Stride

## 1. Technology Stack
* **Frontend**: HTML5, Semantic CSS3 (Flexbox/Grid), Vanilla JavaScript (ES6+), Chart.js (for Progress analytics)
* **Backend**: Python 3.x, Flask Web Framework, Flask-SQLAlchemy (ORM), Jinja2 Templating
* **Database**: PostgreSQL 
* **Deployment / Version Control**: Git, GitHub

## 2. System Architecture Diagram

[ Browser / Client ]
│
▼ (HTTP/HTTPS)
┌─────────────────────────────────────────┐
│ Flask Web Framework (Backend App)       │
│  ├── Routes & Controllers               │
│  │    ├── /attendance                   │
│  │    ├── /expenses                     │
│  │    ├── /assignments                  │
│  │    └── /progress                     │
│  └── Taliwand css (must in build css on html ) + Static Assets   │
└────────────────────┬────────────────────┘
│
▼ (SQLAlchemy ORM)
┌─────────────────────────────────────────┐
│ PostgreSQL Database                     │
│  ├── users                              │
│  ├── attendance_records                 │
│  ├── expense_transactions               │
│  ├── bank_accounts                      │
│  └── assignments                        │
└─────────────────────────────────────────


## 3. Database Schema Design (PostgreSQL)

### 3.1 `users`
* `id`: SERIAL PRIMARY KEY
* `username`: VARCHAR(50) UNIQUE NOT NULL
* `email`: VARCHAR(120) UNIQUE NOT NULL
* `password_hash`: VARCHAR(255) NOT NULL

### 3.2 `attendance_records`
* `id`: SERIAL PRIMARY KEY
* `user_id`: INT REFERENCES users(id)
* `date`: DATE NOT NULL
* `status`: VARCHAR(20) CHECK (status IN ('present', 'absent', 'holiday', 'half_day'))
* `schedule_note`: TEXT

### 3.3 `bank_accounts`
* `id`: SERIAL PRIMARY KEY
* `user_id`: INT REFERENCES users(id)
* `account_name`: VARCHAR(100) NOT NULL
* `balance`: NUMERIC(12, 2) DEFAULT 0.00
* `is_cash`: BOOLEAN DEFAULT FALSE

### 3.4 `expense_transactions`
* `id`: SERIAL PRIMARY KEY
* `user_id`: INT REFERENCES users(id)
* `type`: VARCHAR(20) CHECK (type IN ('income', 'expense', 'withdrawal', 'deposit', 'transfer'))
* `amount`: NUMERIC(12, 2) NOT NULL
* `reason`: VARCHAR(255)
* `account_id`: INT REFERENCES bank_accounts(id)
* `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### 3.5 `assignments`
* `id`: SERIAL PRIMARY KEY
* `user_id`: INT REFERENCES users(id)
* `title`: VARCHAR(255) NOT NULL
* `status`: VARCHAR(20) DEFAULT 'pending'
* `due_date`: DATE

---