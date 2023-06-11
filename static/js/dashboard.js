console.log('Helloworld');

const dashboardSlug = document.getElementById('dashboard-slug').textContent;
const submitBtn = document.getElementById('submit-btn');
const dataInput = document.getElementById('data-input');
const user = document.getElementById('user').textContent.trim();
const dataBox = document.getElementById('data-box');

const socket = new WebSocket(`ws://${window.location.host}/ws/${dashboardSlug}/`)
console.log(socket);

socket.onmessage = function (e) {
    const { sender, message } = JSON.parse(e.data);
    dataBox.innerHTML += `<p>${sender}: ${message}</p>`
    updateChart()
};

submitBtn.addEventListener('click', () => {
    const dataValue = dataInput.value;
    socket.send(JSON.stringify({
        'message': dataValue,
        'sender': user
    }))
});

const ctx = document.getElementById('myChart').getContext('2d');
let chart;

const fetchData = async () => {
    const res = await fetch(window.location.href + 'chart/')
    const data = await res.json();
    return data
}

const drawChart = async () => {
    const data = await fetchData()
    const { chartData, chartLabels } = data

    chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: '% of contribution',
                data: chartData,
                borderWidth: 1,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    })
}

const updateChart = async () => {
    if (chart) {
        chart.destroy()
    }

    await drawChart()
}

drawChart()