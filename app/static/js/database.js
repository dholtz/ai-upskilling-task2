// Database viewer JavaScript

let currentTable = null;

// Load tables on page load
document.addEventListener('DOMContentLoaded', function() {
    loadTables();
});

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
            } else if (typeof value === 'object') {
                value = JSON.stringify(value);
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

