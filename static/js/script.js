document.addEventListener('DOMContentLoaded', function() {
    // Format mathematical expressions for better display
    formatMathExpressions();
    
    // Initialize the toggle mark scheme functionality
    initializeMarkSchemeToggle();
    
    // Setup question regeneration via AJAX
    setupAjaxRegeneration();
});

function formatMathExpressions() {
    // This is a placeholder for potential MathJax or KaTeX integration
    // For actual implementation, you would include the appropriate library
    // and configure it to render mathematical notation
    
    // Example if using MathJax:
    // if (window.MathJax) {
    //     MathJax.typeset();
    // }
}

function initializeMarkSchemeToggle() {
    const toggleBtn = document.getElementById('toggle-mark-scheme');
    if (!toggleBtn) return;
    
    const markScheme = document.querySelector('.question-mark-scheme');
    
    // Set initial state
    markScheme.style.display = 'none';
    toggleBtn.textContent = 'Show Mark Scheme';
    
    toggleBtn.addEventListener('click', function() {
        if (markScheme.style.display === 'none') {
            markScheme.style.display = 'block';
            toggleBtn.textContent = 'Hide Mark Scheme';
        } else {
            markScheme.style.display = 'none';
            toggleBtn.textContent = 'Show Mark Scheme';
        }
    });
}

function setupAjaxRegeneration() {
    // This allows for regenerating questions without page reload
    const ajaxRegenerateButtons = document.querySelectorAll('.ajax-regenerate');
    
    ajaxRegenerateButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const questionId = this.dataset.questionId;
            const resultContainer = document.querySelector(`#regenerate-result-${questionId}`);
            
            if (!questionId || !resultContainer) return;
            
            // Show loading indicator
            resultContainer.innerHTML = '<div class="loading">Generating new variant...</div>';
            resultContainer.style.display = 'block';
            
            // Make AJAX request
            fetch(`/api/generate/${questionId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        resultContainer.innerHTML = `
                            <div class="regenerate-success">
                                <p>New variant generated successfully!</p>
                                <a href="/question/${data.question_id}" class="btn">View New Question</a>
                            </div>
                        `;
                    } else {
                        resultContainer.innerHTML = `
                            <div class="regenerate-error">
                                <p>Failed to generate new variant: ${data.error}</p>
                            </div>
                        `;
                    }
                })
                .catch(error => {
                    resultContainer.innerHTML = `
                        <div class="regenerate-error">
                            <p>An error occurred: ${error.message}</p>
                        </div>
                    `;
                });
        });
    });
}

// Function to handle LaTeX or mathematical notation
function renderMathInElement(element) {
    // This is a placeholder for KaTeX or MathJax rendering
    // You would implement this based on which library you choose
}
