# Product Requirement Document (PRD) - Stride

## 1. Project Overview
**Stride** is a full-stack web application designed for personal tracking across academic and daily management pillars: **Attendance**, **Expenses**, **Assignments**, and **Progress Analysis**.

## 2. Core Modules & Features

### 2.1 Navigation & Global UI
* Clean, minimalistic light-theme interface with high accessibility contrast as per template of figma png on template folder.
* Top Navbar displaying Stride logo, main navigation tabs (**Attendance**, **Expenses**, **Assignments**, **Progress**), and user profile avatar as per user first letter word ex. (`J`).

### 2.2 Module 1: Attendance Tracker
* **Weekly View**: Carousel navigation displaying 7 days with quick status pills (Present, Absent, Holiday, Half Day) spc. color patterns
* **Monthly Calendar Grid**: Full-month view with color-coded status badges:
  * Green: Present
  * Red: Absent
  * Purple: Holidays
  * Brown: Half days
  * Light Grey: Unrecorded / Future
* **Status Counters**: Real-time aggregation of Total Present, Absent, Holidays, Half Days, and Monthly Streak Count.
* **Date Action Controls**: Interactive controls to set schedule, mark present/absent/half days, and record notes per date. for leave aand half days must be required the record note (must)
* **Hover Navigation** : interactive toolips navigations as per template toolips for unknown/unspecfiled icon only
* **Transitions on buttons** 

### 2.3 Module 2: Expense Tracker
* **Summary Header**: Overview metrics displaying Total Income (`₹`), Total Expenses (`₹`), and Quick Add action (`+`).
* **Bank & Cash Balance Cards**: Categorized views for linked accounts (e.g., Union Bank of India, Indian Post Bank, FamPay, Maharashtra Bank) and physical Cash this is only reprsentational record purpose only not actual added bank account.
* **Balance Visibility Toggle**: Interactive eye icon to hide/mask or show numerical account balances (`••••••` vs `₹0.00`).
* **Transaction History Ledger**: Structured list showing Income Additions, Expense Deductions, Cash Withdrawals, Cash Deposits, and Bank Transfers with color-coded amounts.(must be mutable in notes and reason for transaction unless the amount also the delete transaction with reason )
* **add transcation/account (Quick Add action)** : Trasaction category (options) , note , amount entering having another section add account with initial balaance with `0.00₹`
* **Trancation report(auto-download) in browser download** : after month is complete then the auto download the transactions in browser as "Stride-repport-trans-Aug2026"

### 2.4 Module 3: Assignment Manager
* **Assignment Feed**: Clean card list of pending, in-progress, and completed academic assignments (e.g., Physics Assignment).
* **Floating Action Button (FAB)**: Centralized bottom `+` button to quickly trigger modal forms for adding new assignments.

### 2.5 Module 4: Progress Analytics
* **Attendance Bar Chart**: Visual monthly comparison (June, July, August) showing breakdown percentages of attendance over time.
* **Performance Overview Cards**: Percentage breakdown for Present %, Absent %, Half Days %, and Overall Performance Metric.



---