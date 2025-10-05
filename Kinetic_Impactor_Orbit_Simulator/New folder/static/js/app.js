// Kinetic Impactor Simulator JavaScript
class KineticImpactorApp {
    constructor() {
        this.form = document.getElementById('impactorForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.submitText = document.getElementById('submitText');
        this.loadingSpinner = document.getElementById('loadingSpinner');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');

        this.initEventListeners();
    }

    initEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
    }

    async handleFormSubmit(event) {
        event.preventDefault();

        this.showLoading();
        this.hideResults();
        this.hideError();

        try {
            const formData = new FormData(this.form);
            const response = await fetch('/calculate', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showResults(result);
            } else {
                this.showError(result.error || 'An unknown error occurred');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        this.submitBtn.disabled = true;
        this.submitText.textContent = 'Calculating...';
        this.loadingSpinner.classList.remove('d-none');
    }

    hideLoading() {
        this.submitBtn.disabled = false;
        this.submitText.textContent = 'Calculate Impact Effects';
        this.loadingSpinner.classList.add('d-none');
    }

    showResults(data) {
        const resultsContent = document.getElementById('resultsContent');

        // Create results HTML
        resultsContent.innerHTML = `
            <div class="results-card fade-in">
                <h4>🌌 ${data.asteroid_name}</h4>

                <div class="row">
                    <div class="col-md-6">
                        <div class="metric">
                            <div class="metric-label">Diameter</div>
                            <div class="metric-value">${this.formatNumber(data.diameter)} m</div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="metric">
                            <div class="metric-label">Estimated Mass</div>
                            <div class="metric-value">${this.formatScientific(data.mass)} kg</div>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <div class="metric">
                            <div class="metric-label">Delta-V Applied</div>
                            <div class="metric-value">${this.formatVector(data.delta_v)} m/s</div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="metric">
                            <div class="metric-label">Total Maneuver Cost</div>
                            <div class="metric-value">${this.formatNumber(data.maneuver_cost, 6)} km/s</div>
                        </div>
                    </div>
                </div>

                ${this.createOrbitalChangesHTML(data.orbital_changes)}
            </div>
        `;

        // Show the plot
        this.showPlot(JSON.parse(data.plot));

        this.resultsSection.classList.remove('d-none');
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    createOrbitalChangesHTML(changes) {
        let html = `
            <div class="orbital-changes">
                <h5>📊 Orbital Changes</h5>
                <div class="row">
        `;

        const labels = {
            'semi_major_axis': 'Semi-major Axis (AU)',
            'eccentricity': 'Eccentricity',
            'inclination': 'Inclination (°)',
            'period': 'Orbital Period (days)'
        };

        for (const [key, change] of Object.entries(changes)) {
            const changeClass = this.getChangeClass(change.change);
            const changeSymbol = change.change >= 0 ? '+' : '';

            html += `
                <div class="col-md-6 mb-3">
                    <div class="metric">
                        <div class="metric-label">${labels[key]}</div>
                        <div class="metric-value">
                            ${this.formatNumber(change.original, 6)} → ${this.formatNumber(change.final, 6)}
                        </div>
                        <div class="${changeClass}">
                            ${changeSymbol}${this.formatNumber(change.change, 6)} 
                            (${changeSymbol}${this.formatNumber(change.percent_change, 2)}%)
                        </div>
                    </div>
                </div>
            `;
        }

        html += `
                </div>
            </div>
        `;

        return html;
    }

    getChangeClass(change) {
        if (Math.abs(change) < 1e-10) return 'change-neutral';
        return change > 0 ? 'change-positive' : 'change-negative';
    }

    showPlot(plotData) {
        const plotContainer = document.getElementById('plotContainer');
        Plotly.newPlot('plotContainer', plotData.data, plotData.layout, {
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d']
        });
    }

    showError(message) {
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = message;
        this.errorSection.classList.remove('d-none');
        this.errorSection.scrollIntoView({ behavior: 'smooth' });
    }

    hideResults() {
        this.resultsSection.classList.add('d-none');
    }

    hideError() {
        this.errorSection.classList.add('d-none');
    }

    formatNumber(num, decimals = 2) {
        if (typeof num === 'number') {
            return num.toFixed(decimals);
        }
        return num;
    }

    formatScientific(num) {
        if (typeof num === 'number') {
            return num.toExponential(2);
        }
        return num;
    }

    formatVector(vector) {
        if (Array.isArray(vector)) {
            return `[${vector.map(v => v.toFixed(3)).join(', ')}]`;
        }
        return vector;
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new KineticImpactorApp();
});

// Add some example asteroid SPK IDs for user convenience
const EXAMPLE_ASTEROIDS = {
    '2000433': 'Eros',
    '2001627': 'Ivar',
    '2001916': 'Boreas',
    '2002063': 'Bacchus'
};

// Add tooltip or helper text showing example asteroids
document.addEventListener('DOMContentLoaded', () => {
    const spkInput = document.getElementById('spk_id');
    const helpText = spkInput.nextElementSibling;

    let exampleText = 'Examples: ';
    for (const [id, name] of Object.entries(EXAMPLE_ASTEROIDS)) {
        exampleText += `${id} (${name}), `;
    }
    exampleText = exampleText.slice(0, -2); // Remove last comma

    helpText.innerHTML += `<br><small class="text-muted">${exampleText}</small>`;
});