// Expenses JS matching Figma mockups

let isMasked = false;
let accountsList = [];
let transactionsList = [];

document.addEventListener('DOMContentLoaded', () => {
    loadExpensesData();
});

function loadExpensesData() {
    fetch('/expenses/api/data')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                accountsList = data.accounts;
                transactionsList = data.transactions;
                updateView(data.summary);
            }
        });
}

function confirmNillData() {
    if (confirm("Are you sure you want to Nill out all payment data? All transaction history will vanish and account balances will be reset to ₹0.00.")) {
        fetch('/expenses/api/nill', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                loadExpensesData();
            } else {
                alert(data.message || 'Failed to Nill payment data.');
            }
        })
        .catch(err => console.error("Nill error:", err));
    }
}

function togglePrivacy() {
    isMasked = !isMasked;
    const eyeBank = document.getElementById('eye-icon-bank');
    const eyeCash = document.getElementById('eye-icon-cash');

    if (isMasked) {
        if (eyeBank) eyeBank.className = 'fa-solid fa-eye-slash text-sm text-gray-400';
        if (eyeCash) eyeCash.className = 'fa-solid fa-eye-slash text-sm text-gray-400';
    } else {
        if (eyeBank) eyeBank.className = 'fa-solid fa-eye text-sm text-gray-700';
        if (eyeCash) eyeCash.className = 'fa-solid fa-eye text-sm text-gray-700';
    }

    loadExpensesData();
}

function updateView(summary) {
    // Top headers
    document.getElementById('header-income-val').innerText = isMasked ? '••••••' : `₹${(summary.total_income || 0).toFixed(2)}`;
    document.getElementById('header-expense-val').innerText = isMasked ? '••••••' : `₹ -${(summary.total_expense || 0).toFixed(2)}`;

    // Bank accounts list
    const accountsContainer = document.getElementById('bank-accounts-list');
    accountsContainer.innerHTML = '';

    const cashAccount = accountsList.find(a => a.is_cash);
    const bankAccounts = accountsList.filter(a => !a.is_cash);

    bankAccounts.forEach(acc => {
        const row = document.createElement('div');
        row.className = 'flex items-center justify-between text-sm font-normal';

        const valText = isMasked ? '................' : `+ ₹${acc.balance.toFixed(2)}`;

        row.innerHTML = `
            <div class="flex items-center gap-3">
                <i class="fa-regular fa-circle-plus text-sm text-gray-800"></i>
                <span class="text-gray-900">${acc.account_name}</span>
            </div>
            <span class="${isMasked ? 'text-gray-400 tracking-widest' : 'text-emerald-600 font-medium'}">${valText}</span>
        `;
        accountsContainer.appendChild(row);
    });

    // Cash Card
    const cashVal = cashAccount ? cashAccount.balance : 0;
    const cashDisplay = isMasked ? '●●●●●●●●●●●●' : `₹ ${cashVal.toFixed(2)}`;
    document.getElementById('cash-balance-val').innerText = cashDisplay;

    // Populate Account Dropdown for modal
    const sel = document.getElementById('t-account');
    if (sel) {
        sel.innerHTML = '';
        accountsList.forEach(a => {
            sel.innerHTML += `<option value="${a.id}">${a.account_name}</option>`;
        });
    }

    // Transactions list
    renderTransactionsLedger();
}

function renderTransactionsLedger() {
    const container = document.getElementById('transactions-cards-feed');
    container.innerHTML = '';

    if (transactionsList.length === 0) {
        container.innerHTML = `<div class="p-8 text-center text-gray-400 text-sm">No recorded transactions.</div>`;
        return;
    }

    transactionsList.forEach(t => {
        const card = document.createElement('div');
        card.className = 'figma-card-white p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4';

        const typeLabel = getTransactionLabel(t.type);
        const reasonText = t.reason ? (t.reason.startsWith('Reason') ? t.reason : `Reason : ${t.reason}`) : '';
        const amountDisplay = isMasked ? '••••••' : getAmountDisplay(t.type, t.amount);
        const amountColor = getAmountColor(t.type);

        card.innerHTML = `
            <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center text-gray-800 text-lg">
                    <i class="fa-regular fa-credit-card"></i>
                </div>
                <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-8">
                    <span class="font-normal text-base text-gray-900">${typeLabel}</span>
                    ${reasonText ? `<span class="text-sm text-gray-500 font-normal">${reasonText}</span>` : ''}
                </div>
            </div>

            <div class="flex items-center gap-6 self-end sm:self-center">
                <span class="text-xs text-gray-500 font-normal">${t.account_name}</span>
                <span class="font-medium text-sm ${amountColor}">${amountDisplay}</span>
            </div>
        `;

        container.appendChild(card);
    });
}

function getTransactionLabel(type) {
    switch (type) {
        case 'income': return 'Income add';
        case 'expense': return 'Expense';
        case 'withdrawal': return 'Withdrawal';
        case 'deposit': return 'Deposit';
        case 'transfer': return 'Transfer';
        default: return type;
    }
}

function getAmountDisplay(type, amount) {
    const formatted = `₹${amount.toFixed(2)}`;
    if (type === 'income' || type === 'deposit' || type === 'withdrawal' || type === 'transfer') {
        return `+ ${formatted}`;
    }
    return `- ${formatted}`;
}

function getAmountColor(type) {
    if (type === 'income' || type === 'deposit') return 'text-emerald-500';
    if (type === 'expense') return 'text-rose-500';
    if (type === 'withdrawal') return 'text-amber-500';
    return 'text-indigo-500';
}

function openAddTransactionModal() {
    document.getElementById('modal-add-transaction').classList.remove('hidden');
    document.getElementById('modal-add-transaction').classList.add('flex');
}

function closeModal(id) {
    const m = document.getElementById(id);
    m.classList.add('hidden');
    m.classList.remove('flex');
}

function handleAddTransactionSubmit(e) {
    e.preventDefault();
    const type = document.getElementById('t-type').value;
    const amount = parseFloat(document.getElementById('t-amount').value);
    const account_id = parseInt(document.getElementById('t-account').value);
    const reason = document.getElementById('t-reason').value.trim();

    fetch('/expenses/api/transactions/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ type, amount, account_id, reason })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeModal('modal-add-transaction');
            loadExpensesData();
        }
    });
}

function downloadMonthlyReport() {
    window.location.href = '/expenses/api/download-report?month=Aug2026';
}
