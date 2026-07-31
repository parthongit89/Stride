// Assignments JS matching Figma specs

let assignmentsList = [];

document.addEventListener('DOMContentLoaded', () => {
    loadAssignmentsData();
});

function loadAssignmentsData() {
    fetch('/assignments/api/list')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                assignmentsList = data.assignments;
                renderAssignmentsFeed();
            }
        });
}

function renderAssignmentsFeed() {
    const container = document.getElementById('assignments-feed');
    container.innerHTML = '';

    if (assignmentsList.length === 0) {
        container.innerHTML = `
            <div class="figma-card-white p-8 text-center text-gray-400 text-sm">
                No active assignments. Click '+' below to add your first assignment.
            </div>
        `;
        return;
    }

    assignmentsList.forEach(a => {
        const card = document.createElement('div');
        card.className = 'figma-card-white p-6 flex items-center justify-between gap-4 transition-all hover:shadow-md';

        const isCompleted = a.status === 'completed';

        card.innerHTML = `
            <div class="flex items-center gap-4">
                <i class="fa-solid fa-rectangle-list text-gray-800 text-lg"></i>
                <span class="font-normal text-base text-gray-900 ${isCompleted ? 'line-through text-gray-400' : ''}">
                    ${a.title}
                </span>
            </div>

            <button onclick="toggleAssignmentStatus(${a.id})" class="text-gray-800 hover:text-black p-1 transition-colors">
                <i class="fa-${isCompleted ? 'solid fa-circle-check text-emerald-600' : 'regular fa-circle'} text-xl"></i>
            </button>
        `;

        container.appendChild(card);
    });
}

function toggleAssignmentStatus(aId) {
    fetch(`/assignments/api/toggle/${aId}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                loadAssignmentsData();
            }
        });
}

function openAddAssignmentModal() {
    document.getElementById('modal-add-assignment').classList.remove('hidden');
    document.getElementById('modal-add-assignment').classList.add('flex');
}

function closeModal(id) {
    const m = document.getElementById(id);
    m.classList.add('hidden');
    m.classList.remove('flex');
}

function handleAddAssignmentSubmit(e) {
    e.preventDefault();
    const title = document.getElementById('ass-title').value.trim();
    const due_date = document.getElementById('ass-date').value;

    fetch('/assignments/api/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title, due_date, status: 'pending' })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeModal('modal-add-assignment');
            loadAssignmentsData();
        }
    });
}
