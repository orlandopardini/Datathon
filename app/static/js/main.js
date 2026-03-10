// API Base URL - Uses relative URLs to work both locally and in production (Render)
const API_URL = '';

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadMetrics();
    setupPredictionForm();
    setupNavigation();
    loadDrift();
    loadProcedures();
});

// Setup navigation
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!this.getAttribute('target')) {
                e.preventDefault();
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
                const target = this.getAttribute('href');
                if (target.startsWith('#')) {
                    document.querySelector(target).scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
}

// Load model metrics
async function loadMetrics() {
    try {
        const response = await fetch(`${API_URL}/metrics`);
        const data = await response.json();
        
        // Update hero stats
        document.getElementById('totalStudents').textContent = '1160';
        document.getElementById('modelAccuracy').textContent = (data.accuracy * 100).toFixed(1) + '%';
        document.getElementById('predictions').textContent = '0';
        
        // Update metric cards
        document.getElementById('accuracy').textContent = (data.accuracy * 100).toFixed(2) + '%';
        document.getElementById('precision').textContent = (data.precision * 100).toFixed(2) + '%';
        document.getElementById('recall').textContent = (data.recall * 100).toFixed(2) + '%';
        document.getElementById('f1').textContent = (data.f1 * 100).toFixed(2) + '%';
        
        // Update confusion matrix
        const cm = data.confusion_matrix;
        document.getElementById('tn').textContent = cm[0][0];
        document.getElementById('fp').textContent = cm[0][1];
        document.getElementById('fn').textContent = cm[1][0];
        document.getElementById('tp').textContent = cm[1][1];
        
        // Create metric charts
        createGaugeChart('accuracyChart', data.accuracy, '#5ca7e8');
        createGaugeChart('precisionChart', data.precision, '#5cb85c');
        createGaugeChart('recallChart', data.recall, '#f0ad4e');
        createGaugeChart('f1Chart', data.f1, '#d9534f');
        
        // Create ROC and PR curves
        createROCChart(data.roc_auc);
        createPRChart(data.pr_auc);
        
    } catch (error) {
        console.error('Error loading metrics:', error);
    }
}
// Load procedures from API
async function loadProcedures() {
    try {
        const response = await fetch(`${API_URL}/procedures/info`);
        const data = await response.json();
        
        const grid = document.getElementById('proceduresGrid');
        grid.innerHTML = '';
        
        data.procedures.forEach(proc => {
            const card = createProcedureCard(proc);
            grid.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading procedures:', error);
    }
}

// Create procedure card
function createProcedureCard(proc) {
    const card = document.createElement('div');
    card.className = 'procedure-card';
    card.dataset.procedureId = proc.id;
    
    card.innerHTML = `
        <div class="procedure-header">
            <div class="procedure-icon">${proc.icon}</div>
            <div class="procedure-title">
                <h3>${proc.name}</h3>
                <p>${proc.file}</p>
            </div>
        </div>
        <div class="procedure-description">${proc.description}</div>
        <div class="procedure-steps" style="display: none;">
            <h4>📋 Etapas do Processo:</h4>
            <ol>
                ${proc.steps.map(step => `<li>${step}</li>`).join('')}
            </ol>
        </div>
        <div class="procedure-actions">
            <button class="btn-procedure btn-info" onclick="toggleProcedureDetails('${proc.id}')">
                📖 Ver Detalhes
            </button>
            <button class="btn-procedure btn-run" onclick="runProcedure('${proc.id}', '${proc.name}')">
                ▶️ Executar
            </button>
        </div>
        <span class="procedure-badge badge-ready">✓ Pronto para executar</span>
    `;
    
    return card;
}

// Toggle procedure details
function toggleProcedureDetails(procedureId) {
    const card = document.querySelector(`[data-procedure-id="${procedureId}"]`);
    const steps = card.querySelector('.procedure-steps');
    const btn = card.querySelector('.btn-info');
    
    if (steps.style.display === 'none') {
        steps.style.display = 'block';
        btn.textContent = '📖 Ocultar Detalhes';
        card.classList.add('expanded');
    } else {
        steps.style.display = 'none';
        btn.textContent = '📖 Ver Detalhes';
        card.classList.remove('expanded');
    }
}

// Run procedure
function runProcedure(procedureId, procedureName) {
    // Show instructions modal
    const message = `
        Para executar "${procedureName}":
        
        1. Abra um terminal PowerShell na pasta do projeto:
           C:\\Users\\orlando.gardezani\\Downloads\\datathon
        
        2. Execute o comando:
           .\\procedures\\${procedureId}.bat
        
        Ou use o menu interativo executando:
           .\\start.bat
    `;
    
    alert(message);
    
    // Optional: Copy command to clipboard
    const command = `.\\procedures\\${procedureId}.bat`;
    navigator.clipboard.writeText(command).then(() => {
        console.log('Comando copiado para a área de transferência!');
    }).catch(err => {
        console.error('Erro ao copiar comando:', err);
    });
}

// Create gauge chart
function createGaugeChart(canvasId, value, color) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value * 100, 100 - (value * 100)],
                backgroundColor: [color, '#e0e6ed'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

// Create ROC Chart
function createROCChart(rocAuc) {
    const ctx = document.getElementById('rocChart').getContext('2d');
    
    // Perfect ROC curve points (for visualization)
    const rocPoints = [];
    for (let i = 0; i <= 100; i++) {
        rocPoints.push({
            x: i / 100,
            y: i / 100
        });
    }
    
    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: `ROC Curve (AUC = ${rocAuc.toFixed(3)})`,
                data: rocPoints,
                borderColor: '#5ca7e8',
                backgroundColor: 'rgba(92, 167, 232, 0.1)',
                borderWidth: 3,
                pointRadius: 0,
                fill: true
            }, {
                label: 'Random Classifier',
                data: [{x: 0, y: 0}, {x: 1, y: 1}],
                borderColor: '#e0e6ed',
                borderWidth: 2,
                borderDash: [5, 5],
                pointRadius: 0,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'False Positive Rate'
                    },
                    min: 0,
                    max: 1
                },
                y: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'True Positive Rate'
                    },
                    min: 0,
                    max: 1
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'ROC Curve'
                },
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        }
    });
}

// Create PR Chart
function createPRChart(prAuc) {
    const ctx = document.getElementById('prChart').getContext('2d');
    
    // Perfect PR curve points (for visualization)
    const prPoints = [];
    for (let i = 0; i <= 100; i++) {
        const recall = i / 100;
        prPoints.push({
            x: recall,
            y: 1 - (recall * 0.1) // Approximate curve
        });
    }
    
    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: `PR Curve (AUC = ${prAuc.toFixed(3)})`,
                data: prPoints,
                borderColor: '#5cb85c',
                backgroundColor: 'rgba(92, 184, 92, 0.1)',
                borderWidth: 3,
                pointRadius: 0,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Recall'
                    },
                    min: 0,
                    max: 1
                },
                y: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Precision'
                    },
                    min: 0,
                    max: 1
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Precision-Recall Curve'
                },
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        }
    });
}

// Setup prediction form
function setupPredictionForm() {
    const form = document.getElementById('predictionForm');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = {};
        
        formData.forEach((value, key) => {
            // Convert numeric fields (skip empty values for optional fields)
            if (['Idade', 'Ano ingresso', 'INDE 22', 'INDE 23', 'INDE 2024', 'IAA', 'IPS', 'IPP', 'IPV', 'IAN', 'Nº Av'].includes(key)) {
                // Only add if value is not empty
                if (value !== '') {
                    data[key] = parseFloat(value);
                }
            } else {
                data[key] = value;
            }
        });
        
        // Auto-fill Turma from Fase if not provided
        if (!data['Turma']) {
            data['Turma'] = data['Fase'] || '1A';
        }
        
        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ records: [data] })
            });
            
            const result = await response.json();
            displayPredictionResult(result.predictions[0]);
            
            // Update prediction count
            const currentCount = parseInt(document.getElementById('predictions').textContent);
            document.getElementById('predictions').textContent = currentCount + 1;
            
        } catch (error) {
            console.error('Error making prediction:', error);
            alert('Erro ao realizar predição. Verifique se a API está rodando.');
        }
    });
}

// Display prediction result
function displayPredictionResult(prediction) {
    const resultDiv = document.getElementById('predictionResult');
    const statusDiv = document.getElementById('resultStatus');
    const probabilityValue = document.getElementById('probabilityValue');
    const probabilityFill = document.getElementById('probabilityFill');
    const messageDiv = document.getElementById('resultMessage');
    
    const isAtRisk = prediction.at_risk_label === 1;
    const probability = (prediction.at_risk_probability * 100).toFixed(1);
    
    // Update status
    statusDiv.className = 'result-status ' + (isAtRisk ? 'at-risk' : 'not-at-risk');
    statusDiv.textContent = isAtRisk ? '⚠️ Em Risco' : '✅ Não está em Risco';
    
    // Update probability
    probabilityValue.textContent = probability + '%';
    probabilityFill.style.width = probability + '%';
    
    // Update message
    if (isAtRisk) {
        messageDiv.textContent = 'Este estudante apresenta alto risco de desempenho acadêmico baixo (média de notas < 6.0). Recomenda-se acompanhamento pedagógico intensivo e suporte psicopedagógico.';
    } else {
        messageDiv.textContent = 'Este estudante apresenta baixo risco de desempenho acadêmico baixo. Continue o acompanhamento regular e incentive seu desenvolvimento acadêmico.';
    }
    
    // Show result
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Load drift data
async function loadDrift() {
    try {
        const response = await fetch(`${API_URL}/drift`);
        const data = await response.json();
        
        const metricsDiv = document.getElementById('driftMetrics');
        
        if (data.features && Object.keys(data.features).length > 0) {
            metricsDiv.innerHTML = '';
            
            // Display drift metrics
            Object.entries(data.features).forEach(([feature, metrics]) => {
                const card = document.createElement('div');
                card.className = 'drift-metric-card';
                
                let driftStatus = '';
                let driftColor = '#5ca7e8';
                
                if (metrics.psi !== undefined) {
                    if (metrics.psi < 0.1) {
                        driftStatus = '✓ Estável';
                        driftColor = '#5cb85c';
                    } else if (metrics.psi < 0.2) {
                        driftStatus = '⚠️ Atenção';
                        driftColor = '#f0ad4e';
                    } else {
                        driftStatus = '❌ Drift Detectado';
                        driftColor = '#d9534f';
                    }
                }
                
                card.innerHTML = `
                    <h4>${feature}</h4>
                    <div class="drift-value" style="color: ${driftColor}">
                        ${metrics.psi !== undefined ? metrics.psi.toFixed(4) : 'N/A'}
                    </div>
                    <div style="font-size: 12px; margin-top: 5px;">${driftStatus}</div>
                `;
                card.style.borderLeftColor = driftColor;
                
                metricsDiv.appendChild(card);
            });
            
            // Create drift chart
            createDriftChart(data.features);
            
        } else {
            metricsDiv.innerHTML = '<div class="loading">Nenhum dado de drift disponível. Execute algumas predições primeiro.</div>';
        }
        
    } catch (error) {
        console.error('Error loading drift:', error);
        document.getElementById('driftMetrics').innerHTML = '<div class="loading">Erro ao carregar dados de drift.</div>';
    }
}

// Create drift chart
function createDriftChart(features) {
    const ctx = document.getElementById('driftChart').getContext('2d');
    
    const labels = Object.keys(features);
    const psiValues = labels.map(key => features[key].psi || 0);
    
    const backgroundColors = psiValues.map(psi => {
        if (psi < 0.1) return 'rgba(92, 184, 92, 0.6)';
        if (psi < 0.2) return 'rgba(240, 173, 78, 0.6)';
        return 'rgba(217, 83, 79, 0.6)';
    });
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'PSI (Population Stability Index)',
                data: psiValues,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color.replace('0.6', '1')),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'PSI Value'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Features'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Drift Analysis por Feature'
                },
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        afterLabel: function(context) {
                            const psi = context.parsed.y;
                            if (psi < 0.1) return 'Status: Estável';
                            if (psi < 0.2) return 'Status: Atenção';
                            return 'Status: Drift Detectado';
                        }
                    }
                }
            }
        }
    });
}

// Make loadDrift available globally
window.loadDrift = loadDrift;
