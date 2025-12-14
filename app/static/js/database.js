// Database viewer JavaScript

let currentTable = null;

// Load tables on page load
document.addEventListener('DOMContentLoaded', function() {
    loadTables();
    setupUploadForm();
    loadFiles();
});

function setupUploadForm() {
    const form = document.getElementById('upload-form');
    if (!form) return;
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('pptx-file');
        const statusDiv = document.getElementById('upload-status');
        
        if (!fileInput.files || fileInput.files.length === 0) {
            statusDiv.innerHTML = '<div class="error">Please select at least one file</div>';
            return;
        }
        
        statusDiv.innerHTML = `<div class="loading">Uploading and parsing ${fileInput.files.length} file(s)...</div>`;
        
        // Upload files sequentially
        let successCount = 0;
        let errorCount = 0;
        const errors = [];
        
        for (let i = 0; i < fileInput.files.length; i++) {
            const file = fileInput.files[i];
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch('/db/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    successCount++;
                } else {
                    errorCount++;
                    errors.push(`${file.name}: ${data.error}`);
                }
            } catch (error) {
                errorCount++;
                errors.push(`${file.name}: ${error.message}`);
            }
        }
        
        // Show results
        let resultHtml = '';
        if (successCount > 0) {
            resultHtml += `<div style="background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin-top: 10px;">
                <strong>✓ ${successCount} file(s) uploaded successfully!</strong>
            </div>`;
        }
        if (errorCount > 0) {
            resultHtml += `<div class="error" style="margin-top: 10px;">
                <strong>✗ ${errorCount} file(s) failed:</strong><br>
                ${errors.join('<br>')}
            </div>`;
        }
        
        statusDiv.innerHTML = resultHtml;
        
        // Reload tables and files to show new data
        loadTables();
        loadFiles();
        // Reset form
        form.reset();
    });
}

async function loadFiles() {
    const filesListDiv = document.getElementById('files-list');
    if (!filesListDiv) return;
    
    try {
        const response = await fetch('/db/files');
        const data = await response.json();
        
        if (data.files && data.files.length > 0) {
            filesListDiv.innerHTML = `
                <table class="records-table" style="margin-top: 10px;">
                    <thead>
                        <tr>
                            <th>Filename</th>
                            <th>Uploaded</th>
                            <th>Slides</th>
                            <th>URLs</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.files.map(file => `
                            <tr>
                                <td>${file.original_filename}</td>
                                <td>${new Date(file.uploaded_at).toLocaleString()}</td>
                                <td>${file.slide_count}</td>
                                <td>${file.url_count}</td>
                                <td>
                                    <button onclick="deleteFile(${file.id}, '${file.original_filename}')" 
                                            class="btn btn-secondary" 
                                            style="padding: 5px 10px; font-size: 12px;">
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } else {
            filesListDiv.innerHTML = '<div class="empty">No files uploaded yet</div>';
        }
    } catch (error) {
        console.error('Error loading files:', error);
        filesListDiv.innerHTML = '<div class="error">Error loading files</div>';
    }
}

async function deleteFile(fileId, filename) {
    if (!confirm(`Are you sure you want to delete all data from "${filename}"? This cannot be undone.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/db/files/${fileId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert(`File "${filename}" deleted successfully!\n${data.slides_deleted} slides and ${data.url_count} URLs removed.`);
            // Reload tables and files
            loadTables();
            loadFiles();
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function loadTables() {
    try {
        const response = await fetch('/db/tables');
        const data = await response.json();
        displayTables(data.tables);
    } catch (error) {
        console.error('Error loading tables:', error);
        document.getElementById('tables-list').innerHTML = 
            '<div class="error">Error loading tables. Make sure the database is connected.</div>';
    }
}

function displayTables(tables) {
    const container = document.getElementById('tables-list');
    
    if (tables.length === 0) {
        container.innerHTML = '<div class="empty">No tables found in database.</div>';
        return;
    }
    
    container.innerHTML = tables.map(table => `
        <div class="table-card" onclick="loadTableRecords('${table.name}')">
            <h3>${table.display_name}</h3>
            <div class="count">${table.count} records</div>
        </div>
    `).join('');
}

async function loadTableRecords(tableName) {
    currentTable = tableName;
    
    // Show loading
    document.getElementById('records-section').style.display = 'block';
    document.getElementById('records-container').innerHTML = '<div class="loading">Loading records...</div>';
    document.getElementById('table-title').textContent = `Table: ${tableName}`;
    
    // Scroll to records section
    document.getElementById('records-section').scrollIntoView({ behavior: 'smooth' });
    
    try {
        const response = await fetch(`/db/table/${tableName}`);
        const data = await response.json();
        
        if (data.error) {
            document.getElementById('records-container').innerHTML = 
                `<div class="error">Error: ${data.error}</div>`;
            return;
        }
        
        displayRecords(data.records, data.table);
    } catch (error) {
        console.error('Error loading records:', error);
        document.getElementById('records-container').innerHTML = 
            '<div class="error">Error loading records. Please try again.</div>';
    }
}

function displayRecords(records, tableName) {
    const container = document.getElementById('records-container');
    
    if (records.length === 0) {
        container.innerHTML = '<div class="empty">No records found in this table.</div>';
        return;
    }
    
    // Get column names from first record
    const columns = Object.keys(records[0]);
    
    // Create table
    let html = '<table class="records-table"><thead><tr>';
    columns.forEach(col => {
        html += `<th>${col.charAt(0).toUpperCase() + col.slice(1).replace(/_/g, ' ')}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    records.forEach(record => {
        html += '<tr>';
        columns.forEach(col => {
            let value = record[col];
            if (value === null || value === undefined) {
                value = '<em>null</em>';
            } else if (Array.isArray(value)) {
                // Handle arrays (like URLs)
                if (value.length === 0) {
                    value = '<em>none</em>';
                } else if (col === 'urls' && value.length > 0) {
                    // Special formatting for URLs
                    value = value.map(url => {
                        if (typeof url === 'object' && url.url) {
                            return `<a href="${url.url}" target="_blank">${url.link_text || url.url}</a>`;
                        }
                        return `<a href="${url}" target="_blank">${url}</a>`;
                    }).join('<br>');
                } else {
                    value = value.map(v => typeof v === 'object' ? JSON.stringify(v) : v).join('<br>');
                }
            } else if (typeof value === 'object') {
                value = JSON.stringify(value);
            } else {
                // Check if this column contains URLs and make them clickable
                const colLower = col.toLowerCase();
                const valueStr = String(value);
                
                // Check if it's a URL column or contains a URL pattern
                if (colLower === 'url' || colLower === 'urls') {
                    // If it's a URL column and contains a valid URL
                    if (valueStr.startsWith('http://') || valueStr.startsWith('https://') || valueStr.startsWith('mailto:')) {
                        // Use link_text if available, otherwise use the URL itself
                        const displayText = record['link_text'] || record['text'] || valueStr;
                        value = `<a href="${valueStr}" target="_blank" rel="noopener noreferrer">${displayText}</a>`;
                    }
                } else if (colLower === 'link_text' && record['url']) {
                    // If we have link_text and a url, make the link_text clickable
                    const url = record['url'];
                    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('mailto:')) {
                        value = `<a href="${url}" target="_blank" rel="noopener noreferrer">${valueStr}</a>`;
                    }
                }
            }
            html += `<td>${value}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    html += `<div style="margin-top: 15px; color: #666;">Total: ${records.length} records</div>`;
    
    container.innerHTML = html;
}

function closeRecords() {
    document.getElementById('records-section').style.display = 'none';
    currentTable = null;
    document.getElementById('records-container').innerHTML = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function clearDatabase() {
    const statusDiv = document.getElementById('clear-status');
    const clearBtn = document.getElementById('clear-btn');
    
    // Confirm before clearing
    if (!confirm('Are you sure you want to clear all presentation data? This cannot be undone.')) {
        return;
    }
    
    clearBtn.disabled = true;
    clearBtn.textContent = 'Clearing...';
    statusDiv.innerHTML = '<div class="loading">Clearing database...</div>';
    
    try {
        const response = await fetch('/db/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            statusDiv.innerHTML = `
                <div style="background: #d4edda; color: #155724; padding: 15px; border-radius: 5px;">
                    <strong>✓ Database cleared!</strong><br>
                    ${data.files_deleted || 0} files, ${data.slides_deleted} slides and ${data.urls_deleted} URLs removed
                </div>
            `;
            // Reload tables and files to show empty state
            loadTables();
            loadFiles();
        } else {
            statusDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    } finally {
        clearBtn.disabled = false;
        clearBtn.textContent = 'Clear Database';
    }
}

