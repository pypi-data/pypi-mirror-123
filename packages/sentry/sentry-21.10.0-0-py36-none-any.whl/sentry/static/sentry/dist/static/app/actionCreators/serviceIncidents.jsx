Object.defineProperty(exports, "__esModule", { value: true });
exports.loadIncidents = void 0;
const tslib_1 = require("tslib");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
function getIncidentsFromIncidentResponse(statuspageIncidents) {
    if (statuspageIncidents === null || statuspageIncidents.length === 0) {
        return { incidents: [], indicator: 'none' };
    }
    let isMajor = false;
    const incidents = [];
    statuspageIncidents.forEach(item => {
        if (!isMajor && item.impact === 'major') {
            isMajor = true;
        }
        incidents.push({
            id: item.id,
            name: item.name,
            updates: item.incident_updates.map(update => update.body),
            url: item.shortlink,
            status: item.status,
        });
    });
    return { incidents, indicator: isMajor ? 'major' : 'minor' };
}
function loadIncidents() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const cfg = configStore_1.default.get('statuspage');
        if (!cfg || !cfg.id) {
            return null;
        }
        const response = yield fetch(`https://${cfg.id}.${cfg.api_host}/api/v2/incidents/unresolved.json`);
        if (!response.ok) {
            return null;
        }
        const data = yield response.json();
        const { incidents, indicator } = getIncidentsFromIncidentResponse(data.incidents);
        return {
            incidents,
            indicator,
            url: data.page.url,
        };
    });
}
exports.loadIncidents = loadIncidents;
//# sourceMappingURL=serviceIncidents.jsx.map