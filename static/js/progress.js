// Progress JS - 100% Real-Time Data Rendering

let chartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    loadProgressData();
});

function loadProgressData() {
    fetch('/progress/api/stats')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                updateMetrics(data.metrics);
                renderChart(data.chart_data);
            }
        })
        .catch(err => console.error("Failed to load progress stats:", err));
}

function updateMetrics(m) {
    document.getElementById('metric-present').innerText = `${m.present_pct}%`;
    document.getElementById('metric-absent').innerText = `${m.absent_pct}%`;
    document.getElementById('metric-halfday').innerText = `${m.half_day_pct}%`;
    document.getElementById('metric-overall').innerText = `${m.overall_performance}%`;
}

function renderChart(chartData) {
    const ctx = document.getElementById('progressChart').getContext('2d');

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels, // Real-time dynamic month labels
            datasets: [
                {
                    label: 'Absent',
                    data: chartData.absent, // Real-time absent counts
                    backgroundColor: '#FFA2A6',
                    borderRadius: 6,
                    barThickness: 44
                },
                {
                    label: 'Present',
                    data: chartData.present, // Real-time present counts
                    backgroundColor: '#90E8B2',
                    borderRadius: 6,
                    barThickness: 44
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    align: 'end',
                    labels: {
                        usePointStyle: true,
                        boxWidth: 10,
                        font: { family: 'Google Sans Flex', size: 12 }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    stacked: true,
                    grid: { display: false },
                    ticks: { font: { family: 'Google Sans Flex', size: 12, weight: '500' } }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        precision: 0,
                        font: { family: 'Google Sans Flex', size: 12 }
                    },
                    grid: { color: '#F0F0F0' }
                }
            }
        }
    });
}
