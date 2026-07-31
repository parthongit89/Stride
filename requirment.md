# Technical Requirements - Stride

## 1. Environment & Dependencies
```txt
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.0
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
Gunicorn>=21.2.0

2. Functional Requirements
FR-01: User Authentication & Sessions
The system shall maintain persistent session storage for logged-in users.

FR-02: Attendance Management
System must allow users to toggle day status between Present, Absent, Holiday, and Half Day.

Monthly streaks and totals must dynamically recalculate on every update.

FR-03: Expense & Account Privacy
System must calculate total income vs total expenses dynamically.

Users must be able to toggle the eye icon to obscure sensitivity amounts in the UI using local state.

FR-04: Assignments Workflow
Users must be able to create new assignment cards with title and target dates.

Clicking the completion circle must mark assignments as complete/incomplete.

FR-05: Dynamic Analytics
Progress tab must render dynamic monthly attendance bar graphs using backend data payload.

3. Non-Functional Requirements
Performance: Page loads must complete under 1.5 seconds.

Responsive Layout: Designed explicitly for clean desktop layouts matching the UI mockups.

Security: Passwords hashed using bcrypt or pbkdf2:sha256. Database credentials handled via .env.