# Stride - Student Attendance, Expenses, Assignments & Progress Tracking

**Stride** is a modern, full-stack student productivity web application built with **Flask**, **PostgreSQL**, **Tailwind CSS**, and **Chart.js**, featuring pixel-perfect design alignment inspired by modern Figma design mockups.

---

## 🌟 Key Features

### 1. 📅 Attendance Tracking
- **Weekly & Monthly View**: Carousel day cards and 31-day interactive monthly calendar grid.
- **Dynamic Status Marking**: Mark Present (`✓`), Absent (`⦸`), Holiday, or Half Day (`⊟`).
- **Strict Note Validation**: Mandatory reason notes required for Absent and Half Day records.
- **Real-Time Streak Counter**: Calculates consecutive present day streaks dynamically.
- **Indian Standard Time (IST) Support**: Live time formatting and date selection.

### 2. 💳 Expenses & Account Ledger
- **Multi-Account Support**: Bank accounts (Union Bank of India, Indian Post Bank, Fam pay, Maharastra Bank) and Cash.
- **Privacy Masking Toggle**: Single-click eye icon toggle to hide/show sensitive balances (`••••••••••••`).
- **Transaction Types**: Income, Expense, Withdrawal, Deposit, Transfer.
- **CSV Report Export**: Instant downloadable transaction ledger reports (e.g., `Stride-report-trans-Aug2026.csv`).

### 3. 📝 Assignments Feed
- Clean interactive task cards with radio completion toggles.
- Modal dialog for adding new assignments with target due dates.

### 4. 📊 Progress Analytics
- **Dynamic Stacked Bar Chart**: Chart.js integration showing Present vs. Absent trends over historical months.
- **Real-Time Metric Cards**: Present %, Absent %, Half Days %, and Overall Performance Score.

---

## 🚀 Technology Stack

- **Backend**: Python 3.14, Flask, SQLAlchemy ORM
- **Database**: PostgreSQL (with SQLite fallback)
- **Frontend**: HTML5, Tailwind CSS, Vanilla JS, Font Awesome Icons, Chart.js
- **Design System**: Plus Jakarta Sans, Google Sans Flex, Figma-inspired color tokens

---

## 🛠️ Setup & Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/parthongit89/Stride.git
   cd Stride
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables (`.env`)**:
   ```env
   SECRET_KEY=your_super_secret_key
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/stride
   ```

4. **Initialize PostgreSQL Database**:
   ```bash
   python test_pg.py
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

---

## 🔒 Security Hygiene
- Secret keys and `.env` files are excluded via `.gitignore`.
- Database credentials and tokens are strictly protected.

---

## 📜 License
Developed with ❤️ by [parthongit89](https://github.com/parthongit89).
