1# 4. `rules.md`

```markdown
# Antigravity Development Rules & Guidelines

## 1. Code Style & Architecture Constraints
* **Flask Best Practices**: Use Flask Blueprints to organize application modules (`attendance_bp`, `expenses_bp`, `assignments_bp`, `progress_bp`).
* **Database Operations**: Never execute raw SQL strings; always use SQLAlchemy ORM queries inside Flask backend routes.
* **Frontend Architecture**: 
  * HTML templates must extend a shared `base.html` template.
  * Keep CSS clean, modular, and organized inside `static/css(taliwandcss inbuild in html)/`.
  * Modularize JavaScript functions per page inside `static/js/`.

## 2. Environment & Credential Management
* **Zero Hardcoded Secrets**: Secrets, access tokens, DB credentials, and private keys MUST be stored exclusively inside `.env`.
* **Git Hygiene**: Always include `.env` and `__pycache__/` in `.gitignore` before committing code to GitHub.

## 3. UI/UX Consistency Rules
* fonts : <link rel="preconnect" href="https://fonts.googleapis.com">
          <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
          <link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:opsz,wght@6..144,1..1000&family=Pacifico&display=swap" rel="stylesheet">
* Color Palette Compliance:
  * Present / Income Positive: Green (`#A8E6CF` / `#2ECC71`)
  * Absent / Expense Negative: Red / Coral (`#FF8B94` / `#E74C3C`)
  * Holidays / Transfers: Light Purple (`#B19CD9`)
  * Half Day: Tan / Warm Beige (`#D7C4B7`)
* Maintain rounded container corners (`border-radius: 12px` to `20px`) and light grey backgrounds (`#F4F4F6`) as pictured in the design mockups.






