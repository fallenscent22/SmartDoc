document.addEventListener('DOMContentLoaded', () => {
    // Initialize application
    initFileUpload();
});

function initFileUpload() {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('document-input');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorMessage.style.display = 'none';
        
        // Validate file input
        if (!fileInput.files || fileInput.files.length === 0) {
            showError('Please select a file first');
            return;
        }

        loading.style.display = 'block';
        
        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                body: new FormData(uploadForm)
            });
            
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Processing failed');
            }
            showResults(data);
        } catch (error) {
            showError(error.message);
        } finally {
            loading.style.display = 'none';
        }
    });
}

function showError(message) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

// Update showResults to format the output better
function showResults(data) {
    const resultsSection = document.getElementById('results-section');
    let entitiesHtml = '';
    if (data.entities) {
        entitiesHtml = `<h3>Extracted Entities</h3><pre>${JSON.stringify(data.entities, null, 2)}</pre>`;
    }
    let summaryHtml = '';
    if (data.summary) {
        summaryHtml = `<h3>Summary</h3><pre>${data.summary}</pre>`;
    }
    let docTypeHtml = '';
    if (data.doc_type) {
        docTypeHtml = `<h3>Document Type</h3><pre>${data.doc_type}</pre>`;
    }
    resultsSection.innerHTML = `
        <h3>Processing Results</h3>
        <div class="results-content">
            <p><strong>Filename:</strong> ${data.filename}</p>
            <p><strong>Status:</strong> ${data.status}</p>
            ${docTypeHtml}
            ${summaryHtml}
            ${entitiesHtml}
            <h3>Extracted Text</h3>
            <pre>${data.content}</pre>
        </div>
    `;
}

async function processFile() {
    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            body: new FormData(uploadForm)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            // Get the actual error message from the server
            const errorMsg = data.error || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        showResults(data);
    } catch (error) {
        showError(error.message);
    }
}