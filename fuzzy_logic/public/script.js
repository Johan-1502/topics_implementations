// Referencias DOM
const currentTempSlider = document.getElementById('currentTemp');
const targetTempSlider = document.getElementById('targetTemp');
const rateChangeSlider = document.getElementById('rateOfChange');
const valCurrent = document.getElementById('val-current');
const valTarget = document.getElementById('val-target');
const valDelta = document.getElementById('val-delta');
const valError = document.getElementById('val-error');
const fanSpeedDisplay = document.getElementById('fanSpeedResult');
const visualFan = document.getElementById('visualFan');

// --- GRÁFICO 1: Temperatura (Horizontal) ---
const ctxTemp = document.getElementById('tempChart').getContext('2d');
const tempChart = new Chart(ctxTemp, {
    type: 'bar',
    data: {
        labels: ['❄️ Frío', '😌 Ideal', '🔥 Caliente'],
        datasets: [{
            label: 'Membresía',
            data: [0, 0, 0],
            backgroundColor: ['#3b82f6', '#10b981', '#f43f5e'], 
            borderRadius: 4,
            barPercentage: 0.7
        }]
    },
    options: {
        indexAxis: 'y', // Barras horizontales
        responsive: true,
        maintainAspectRatio: false,
        scales: { x: { beginAtZero: true, max: 1, display: false }, y: { grid: { display: false }, ticks: { color: '#e2e8f0' } } },
        plugins: { legend: { display: false } }
    }
});

// --- GRÁFICO 2: Tendencia (Vertical) ---
const ctxTrend = document.getElementById('trendChart').getContext('2d');
const trendChart = new Chart(ctxTrend, {
    type: 'bar',
    data: {
        labels: ['Baja Rápido', 'Estable', 'Sube Rápido'],
        datasets: [{
            label: 'Certeza',
            data: [0, 0, 0],
            backgroundColor: ['#3b82f6', '#94a3b8', '#f43f5e'], 
            borderRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: true, max: 1, display: false }, x: { grid: { display: false }, ticks: { color: '#e2e8f0', font: {size: 10} } } },
        plugins: { legend: { display: false } }
    }
});

// --- LÓGICA DE ACTUALIZACIÓN ---
async function updateSimulation() {
    const current = parseFloat(currentTempSlider.value);
    const target = parseFloat(targetTempSlider.value);
    const rate = parseFloat(rateChangeSlider.value);

    // UI Updates
    valCurrent.innerText = current;
    valTarget.innerText = target;
    valDelta.innerText = rate > 0 ? `+${rate}` : rate;

    try {
        const response = await fetch('/api/fuzzy/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ currentTemp: current, targetTemp: target, rateOfChange: rate })
        });

        const result = await response.json();
        
        if (result.success) {
            const { inputs, fuzzyAnalysis, output } = result.data;

            valError.innerText = inputs.error.toFixed(1);

            // Actualizar Gráfico Temperatura
            tempChart.data.datasets[0].data = [
                fuzzyAnalysis.errorSets.frio,
                fuzzyAnalysis.errorSets.ideal,
                fuzzyAnalysis.errorSets.caliente
            ];
            tempChart.update();

            // Actualizar Gráfico Tendencia
            trendChart.data.datasets[0].data = [
                fuzzyAnalysis.deltaSets.enfriando,
                fuzzyAnalysis.deltaSets.estable,
                fuzzyAnalysis.deltaSets.calentando
            ];
            trendChart.update();

            // Actualizar Ventilador
            const speed = output.fanSpeed;
            fanSpeedDisplay.innerText = speed;
            visualFan.style.color = speed > 0 ? '#38bdf8' : '#475569';
            
            if (speed > 0) {
                const duration = 2000 / (speed + 1);
                visualFan.style.animation = `spin ${duration}s linear infinite`;
            } else {
                visualFan.style.animation = 'none';
            }
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// Inyectar keyframes
const styleSheet = document.createElement("style");
styleSheet.innerText = `@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`;
document.head.appendChild(styleSheet);

// Listeners
currentTempSlider.addEventListener('input', updateSimulation);
targetTempSlider.addEventListener('input', updateSimulation);
rateChangeSlider.addEventListener('input', updateSimulation);

// Inicializar
updateSimulation();