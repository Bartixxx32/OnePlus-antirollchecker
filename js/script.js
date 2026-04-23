/**
 * Toggle visibility of version history row.
 */
function toggleHistory(id, btn) {
    const row = document.getElementById(id);
    if (row.classList.contains('active')) {
        row.classList.remove('active');
        btn.classList.remove('active');
    } else {
        row.classList.add('active');
        btn.classList.add('active');
    }
}

/**
 * Filter device cards based on search input.
 */
function filterDevices() {
    const filter = document.getElementById('search-input').value.toLowerCase();
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const name = card.getAttribute('data-name') || '';
        card.style.display = name.includes(filter) ? '' : 'none';
    });
}

/**
 * Extract numeric parts from version string for correct ordering.
 * Note: Keep this in sync with version_sort_key() in hardcode_rules.py.
 */
const versionSortKey = (v) => {
    if (!v) return [0];
    const parts = v.match(/\d+/g);
    return parts ? parts.map(Number) : [0];
};

/**
 * Compare two version strings.
 */
const compareVersions = (a, b) => {
    const ka = versionSortKey(a);
    const kb = versionSortKey(b);
    for (let i = 0; i < Math.max(ka.length, kb.length); i++) {
        const na = ka[i] || 0;
        const nb = kb[i] || 0;
        if (na !== nb) return na - nb;
    }
    return 0;
};

/**
 * Map compact region codes to human-readable labels for display.
 * Uses the globally defined `regionMap`.
 */
const getRegionName = (code) => {
    return (typeof regionMap !== 'undefined' && regionMap[code]) ? regionMap[code] : code;
};

/**
 * Render status badge based on ARB value.
 */
const renderBadge = (v) => {
    if (v.is_hardcoded) return `<span class="badge badge-hardcode" title="Anti-rollback is present but undetectable by standard tools"><span class="badge-dot"></span>Undetectable ARB</span>`;
    if (v.arb === 0) return `<span class="badge badge-safe"><span class="badge-dot"></span>Safe</span>`;
    if (typeof v.arb === 'number' && v.arb > 0) return `<span class="badge badge-danger"><span class="badge-dot"></span>Protected</span>`;
    return `<span class="badge badge-warning"><span class="badge-dot"></span>Unknown</span>`;
};

/**
 * Render the HTML for the device list.
 */
const renderHTML = (devices) => {
    return devices.map(device => {
        let rows = '';
        if (device.variants.length === 0) {
            rows = `<tr><td colspan="4" style="text-align:center; padding:20px; color: var(--text-dim);">No data available</td></tr>`;
        } else {
            device.variants.forEach(variant => {
                const regionFull = getRegionName(variant.region_name);
                const regionShort = variant.region_name;

                const hasHistory = variant.history && variant.history.length > 0;
                const histId = `history-${device.id}-${variant.region_name.replace(/\s+/g, '-')}`;

                rows += `
                <tr>
                    <td class="col-region">
                        <span class="region-full">${regionFull}</span>
                        <span class="region-short">${regionShort}</span>
                        <div class="region-model-sub">${variant.model || ''}</div>
                    </td>
                    <td>
                        <div class="firmware-title-wrap">
                            <div class="firmware-title">${variant.version || 'Unknown'}</div>
                        </div>
                        <div class="firmware-oem">Major: ${variant.major != null ? variant.major : '?'}, Minor: ${variant.minor != null ? variant.minor : '?'}</div>
                        ${variant.md5 ? `<details class="md5-details"><summary>Show MD5</summary><code>${variant.md5}</code></details>` : ''}
                    </td>
                    <td>
                        ${renderBadge(variant)}
                        <span class="arb-sub">ARB: ${variant.is_hardcoded ? '?' : (variant.arb != null ? variant.arb : '?')}</span>
                        <div class="last-checked-sub">${variant.last_checked || variant.first_seen || 'Unknown'}</div>
                    </td>
                    <td>
                        ${hasHistory ? `<button class="btn-history" onclick="toggleHistory('${histId}', this)">History <span class="btn-history-arrow">›</span></button>` : ''}
                    </td>
                </tr>
                `;

                if (hasHistory) {
                    let histRows = variant.history.map(entry => `
                        <tr>
                            <td>
                                <div class="firmware-title-wrap">
                                    <div class="firmware-title" style="font-size:0.75rem;">${entry.version}</div>
                                </div>
                                ${entry.md5 ? `<details class="md5-details"><summary>Show MD5</summary><code>${entry.md5}</code></details>` : ''}
                            </td>
                            <td>
                                ${renderBadge(entry)}
                                <span class="arb-sub">ARB: ${entry.is_hardcoded ? '?' : (entry.arb != null ? entry.arb : '?')}</span>
                            </td>
                            <td>Major: ${entry.major != null ? entry.major : '?'}, Minor: ${entry.minor != null ? entry.minor : '?'}</td>
                            <td>${entry.last_checked || entry.first_seen || 'Unknown'}</td>
                        </tr>
                    `).join('');

                    rows += `
                    <tr id="${histId}" class="history-row">
                        <td colspan="4" style="padding:0; overflow: visible;">
                            <div class="history-container">
                                <div class="history-title">📜 Version History — ${variant.region_name}</div>
                                <table class="history-table">
                                    <thead><tr><th>Firmware Version</th><th>Status</th><th>OEM Version</th><th>Last Seen</th></tr></thead>
                                    <tbody>${histRows}</tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                    `;
                }
            });
        }

        return `
        <div class="card" data-name="${device.name.toLowerCase()} ${device.models.join(' ').toLowerCase()}">
            <div class="card-header">
                <h2>
                    ${device.name}
                    <span class="device-models">${device.models.join(' / ')}</span>
                </h2>
            </div>
            <div class="card-body">
                <table>
                    <thead>
                        <tr>
                            <th class="col-region">Region</th>
                            <th class="col-firmware">Firmware</th>
                            <th class="col-status">Status</th>
                            <th class="col-actions">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rows}
                    </tbody>
                </table>
            </div>
        </div>
        `;
    }).join('');
};

/**
 * Main data loading function.
 */
async function loadData() {
    const grid = document.getElementById('devices-grid');
    let db;

    try {
        // Try local first
        const res = await fetch('./database.json');
        if (!res.ok) throw new Error();
        db = await res.json();
    } catch (e1) {
        try {
            // Fallback to prod URL
            const res = await fetch('https://oparb.pages.dev/database.json');
            db = await res.json();
        } catch (e2) {
            grid.innerHTML = '<div style="color:var(--danger); text-align:center; padding: 40px; grid-column: 1/-1;">Failed to load database.json. Ensure you are not blocking CORS or check your network.</div>';
            return;
        }
    }

    // Process db into devices array
    const byDevice = {};
    let latestScan = '';

    const regionScores = { "GLO": 1, "EU": 2, "IN": 3, "NA": 4, "CN": 5 };

    for (const modelKey of Object.keys(db)) {
        const d = db[modelKey];
        const devName = d.device_name;
        if (!byDevice[devName]) {
            byDevice[devName] = {
                name: devName,
                id: devName.replace(/\s+/g, '-'),
                order: d.device_order ?? 999,
                variantsMap: {},
                models: [] 
            };
        }
        if (!byDevice[devName].models.includes(modelKey)) {
            byDevice[devName].models.push(modelKey);
        }

        for (const [versionStr, v] of Object.entries(d.versions)) {
            const vWithKey = { ...v, version: versionStr };
            if (vWithKey.last_checked && vWithKey.last_checked > latestScan) latestScan = vWithKey.last_checked;

            for (const r of vWithKey.regions || []) {
                if (!byDevice[devName].variantsMap[r]) {
                    byDevice[devName].variantsMap[r] = { region_name: r, model: modelKey, history: [], regions: [] };
                }
                if (!byDevice[devName].variantsMap[r].model) byDevice[devName].variantsMap[r].model = modelKey;
                const vr = byDevice[devName].variantsMap[r];

                if (!vr.regions.includes(r)) {
                    vr.regions.push(r);
                }

                if (vWithKey.status === 'current' || !vr.version) {
                    vr.version = vWithKey.version;
                    vr.arb = vWithKey.arb;
                    vr.md5 = vWithKey.md5;
                    vr.major = vWithKey.major;
                    vr.minor = vWithKey.minor;
                    vr.is_hardcoded = vWithKey.is_hardcoded;
                    vr.last_checked = vWithKey.last_checked;
                    vr.first_seen = vWithKey.first_seen;
                    if (vWithKey.status !== 'current') {
                        vr.history.push(vWithKey);
                    }
                } else {
                    vr.history.push(vWithKey);
                }
            }
        }
    }

    document.getElementById('last-scan').innerText = 'Last scan: ' + (latestScan || new Date().toISOString().split('T')[0]);

    const sortedDevices = Object.values(byDevice).sort((a, b) => a.order - b.order);
    for (const dev of sortedDevices) {
        dev.variants = Object.values(dev.variantsMap).sort((a, b) => (regionScores[a.region_name] || 99) - (regionScores[b.region_name] || 99));
        for (const v of dev.variants) {
            v.history.sort((a, b) => compareVersions(b.version, a.version));
        }
    }

    grid.innerHTML = renderHTML(sortedDevices);
}

// Cursor Glow Logic
document.addEventListener('DOMContentLoaded', () => {
    const glow = document.getElementById('cursor-glow');
    if (glow) {
        const updateGlow = (x, y) => {
            requestAnimationFrame(() => {
                glow.style.setProperty('--x', `${x}px`);
                glow.style.setProperty('--y', `${y}px`);
                glow.style.opacity = '1';
            });
        };

        document.addEventListener('mousemove', (e) => updateGlow(e.clientX, e.clientY));
        document.addEventListener('touchmove', (e) => {
            if (e.touches.length > 0) {
                updateGlow(e.touches[0].clientX, e.touches[0].clientY);
            }
        });
        document.addEventListener('touchend', () => {
            glow.style.opacity = '0';
        });
    }
    
    // Initial data load
    loadData();
});
