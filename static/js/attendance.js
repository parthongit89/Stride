// Attendance Interactivity JS for ALL Months & Years (Real-Time Indian Format)

let currentYear = new Date().getFullYear();
let currentMonth = new Date().getMonth() + 1; // 1-indexed
let selectedDateStr = `${currentYear}-${String(currentMonth).padStart(2, '0')}-${String(new Date().getDate()).padStart(2, '0')}`;
let recordsData = {};
let currentWeekNum = Math.ceil(new Date().getDate() / 7);

const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

document.addEventListener('DOMContentLoaded', () => {
    const today = new Date();
    currentYear = today.getFullYear();
    currentMonth = today.getMonth() + 1;
    selectedDateStr = `${currentYear}-${String(currentMonth).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    currentWeekNum = Math.ceil(today.getDate() / 7);

    setupEventListeners();
    loadAttendanceData();
});

function setupEventListeners() {
    const prevM = document.getElementById('btn-prev-month');
    const nextM = document.getElementById('btn-next-month');

    if (prevM) {
        prevM.addEventListener('click', () => {
            currentMonth--;
            if (currentMonth < 1) {
                currentMonth = 12;
                currentYear--;
            }
            loadAttendanceData();
        });
    }

    if (nextM) {
        nextM.addEventListener('click', () => {
            currentMonth++;
            if (currentMonth > 12) {
                currentMonth = 1;
                currentYear++;
            }
            loadAttendanceData();
        });
    }

    const prevW = document.getElementById('btn-prev-week');
    const nextW = document.getElementById('btn-next-week');

    if (prevW) {
        prevW.addEventListener('click', () => {
            currentWeekNum = Math.max(1, currentWeekNum - 1);
            document.getElementById('week-pill-label').innerText = `Week ${currentWeekNum}`;
            renderWeeklyDays();
        });
    }

    if (nextW) {
        nextW.addEventListener('click', () => {
            currentWeekNum = Math.min(5, currentWeekNum + 1);
            document.getElementById('week-pill-label').innerText = `Week ${currentWeekNum}`;
            renderWeeklyDays();
        });
    }
}

function loadAttendanceData() {
    const mName = monthNames[currentMonth - 1];
    
    // Update headers
    document.getElementById('month-badge').innerText = `${mName} ${currentYear}`;
    document.getElementById('monthly-header-title').innerText = mName;
    document.getElementById('monthly-header-year').innerText = currentYear;
    document.getElementById('week-pill-label').innerText = `Week ${currentWeekNum}`;

    fetch(`/attendance/api/records?year=${currentYear}&month=${currentMonth}`)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                recordsData = data.records;
                updateCounters(data.counters);
                renderWeeklyDays();
                renderMonthlyDaysGrid();

                // Ensure selectedDateStr is in current month
                const [sY, sM] = selectedDateStr.split('-').map(Number);
                if (sY !== currentYear || sM !== currentMonth) {
                    const today = new Date();
                    if (today.getFullYear() === currentYear && (today.getMonth() + 1) === currentMonth) {
                        selectedDateStr = `${currentYear}-${String(currentMonth).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
                    } else {
                        selectedDateStr = `${currentYear}-${String(currentMonth).padStart(2, '0')}-01`;
                    }
                }
                updateSelectedDateView(selectedDateStr);
            }
        })
        .catch(err => console.error("Failed to load attendance records:", err));
}

function updateCounters(c) {
    document.getElementById('monthly-count-present').innerText = c.present || 0;
    document.getElementById('monthly-count-absent').innerText = c.absent || 0;
    document.getElementById('monthly-count-holiday').innerText = c.holiday || 0;
    document.getElementById('monthly-count-halfday').innerText = c.half_day || 0;

    document.getElementById('week-count-present').innerText = Math.min(c.present || 0, 7);
    document.getElementById('week-count-absent').innerText = Math.min(c.absent || 0, 7);
    document.getElementById('week-count-holiday').innerText = Math.min(c.holiday || 0, 7);
    document.getElementById('week-count-halfday').innerText = Math.min(c.half_day || 0, 7);

    document.getElementById('week-streak-num').innerText = c.streak || 0;
    document.getElementById('strikes-card-num').innerText = c.streak || 0;
}

function getItemStatus(dateStr, year, month, day) {
    const record = recordsData[dateStr];
    if (record) return record.status;
    
    // Check if Sunday (0 in JS)
    const dayOfWeek = new Date(year, month - 1, day).getDay();
    if (dayOfWeek === 0) {
        return 'holiday';
    }
    return 'unrecorded';
}

function renderWeeklyDays() {
    const container = document.getElementById('weekly-days-row');
    container.innerHTML = '';

    const daysInMonth = new Date(currentYear, currentMonth, 0).getDate();
    
    // Pagination offset per week
    const startDay = (currentWeekNum - 1) * 7 + 1;
    const endDay = Math.min(daysInMonth, startDay + 6);

    for (let day = startDay; day <= endDay; day++) {
        const m = String(currentMonth).padStart(2, '0');
        const d = String(day).padStart(2, '0');
        const dateStr = `${currentYear}-${m}-${d}`;

        const status = getItemStatus(dateStr, currentYear, currentMonth, day);

        const btn = document.createElement('button');
        btn.className = `h-14 rounded-2xl font-bold text-sm flex flex-col items-center justify-center relative transition-transform hover:scale-105 ${getDayClass(status)}`;
        btn.onclick = () => selectDate(dateStr);

        btn.innerHTML = `
            <span>${day}</span>
            ${status === 'present' ? '<i class="fa-solid fa-check text-[10px] absolute bottom-1 text-emerald-800"></i>' : ''}
        `;

        container.appendChild(btn);
    }
}

function renderMonthlyDaysGrid() {
    const grid = document.getElementById('monthly-days-grid');
    grid.innerHTML = '';

    const daysInMonth = new Date(currentYear, currentMonth, 0).getDate();

    for (let day = 1; day <= daysInMonth; day++) {
        const m = String(currentMonth).padStart(2, '0');
        const d = String(day).padStart(2, '0');
        const dateStr = `${currentYear}-${m}-${d}`;

        const status = getItemStatus(dateStr, currentYear, currentMonth, day);

        const box = document.createElement('div');
        box.className = `day-box ${getDayClass(status)} ${selectedDateStr === dateStr ? 'ring-2 ring-black font-extrabold scale-105' : ''}`;
        box.innerText = day;
        box.onclick = () => selectDate(dateStr);

        grid.appendChild(box);
    }
}

function getDayClass(status) {
    switch (status) {
        case 'present': return 'day-present';
        case 'absent': return 'day-absent';
        case 'holiday': return 'day-holiday';
        case 'half_day': return 'day-halfday';
        default: return 'day-unrecorded';
    }
}

function selectDate(dateStr) {
    selectedDateStr = dateStr;
    renderMonthlyDaysGrid();
    updateSelectedDateView(dateStr);
}

function getLiveFormattedTime() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    const formattedHours = String(hours).padStart(2, '0');
    return `${formattedHours} : ${minutes} ${ampm}`;
}

function updateSelectedDateView(dateStr) {
    const parts = dateStr.split('-');
    const m = parseInt(parts[1], 10);
    const dayNum = parseInt(parts[2], 10);
    const mShort = monthNames[m - 1].substring(0, 3);
    
    // Real-Time dynamic Indian format (e.g. 31 Jul 07 : 50 PM)
    const timeStr = getLiveFormattedTime();
    document.getElementById('schedule-date-tag').innerText = `${dayNum} ${mShort} ${timeStr}`;

    const record = recordsData[dateStr];
    const noteInput = document.getElementById('schedule-input-note');
    const labelEl = document.getElementById('strikes-card-label');
    const numEl = document.getElementById('strikes-card-num');

    // Check if Sunday
    const dayOfWeek = new Date(currentYear, m - 1, dayNum).getDay();
    const isSunday = dayOfWeek === 0;

    if (record) {
        noteInput.value = record.schedule_note || '';
        labelEl.innerText = record.schedule_note ? record.schedule_note : (isSunday ? 'Sunday Holiday' : 'No Schedule added');
        numEl.innerText = dayNum;
    } else {
        noteInput.value = isSunday ? 'Sunday Holiday' : '';
        labelEl.innerText = isSunday ? 'Sunday Holiday' : 'No Schedule added';
        numEl.innerText = dayNum;
    }
}

function quickMarkStatus(status) {
    const note = document.getElementById('schedule-input-note').value.trim();

    if ((status === 'absent' || status === 'half_day') && !note) {
        alert(`Schedule note is strictly required when marking ${status === 'absent' ? 'Absent' : 'Half Day'}. Please enter a note in the schedule box.`);
        return;
    }

    fetch('/attendance/api/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            date: selectedDateStr,
            status: status,
            schedule_note: note
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            loadAttendanceData();
        } else {
            alert(data.message || 'Failed to update attendance.');
        }
    });
}

function saveScheduleNote() {
    const record = recordsData[selectedDateStr];
    const currentStatus = record ? record.status : 'present';
    quickMarkStatus(currentStatus);
}
