Object.defineProperty(exports, "__esModule", { value: true });
exports.getIncidentDiscoverUrl = void 0;
const tslib_1 = require("tslib");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fields_1 = require("app/utils/discover/fields");
const types_1 = require("app/views/alerts/incidentRules/types");
const utils_1 = require("app/views/alerts/utils");
/**
 * Gets the URL for a discover view of the incident with the following default
 * parameters:
 *
 * - Ordered by the incident aggregate, descending
 * - yAxis maps to the aggregate
 * - The following fields are displayed:
 *   - For Error dataset alerts: [issue, count(), count_unique(user)]
 *   - For Transaction dataset alerts: [transaction, count()]
 * - Start and end are scoped to the same period as the alert rule
 */
function getIncidentDiscoverUrl(opts) {
    var _a;
    const { orgSlug, projects, incident, stats, extraQueryParams } = opts;
    if (!projects || !projects.length || !incident || !stats) {
        return '';
    }
    const timeWindowString = `${incident.alertRule.timeWindow}m`;
    const { start, end } = (0, utils_1.getStartEndFromStats)(stats);
    const discoverQuery = Object.assign({ id: undefined, name: (incident && incident.title) || '', orderby: `-${(0, fields_1.getAggregateAlias)(incident.alertRule.aggregate)}`, yAxis: incident.alertRule.aggregate ? [incident.alertRule.aggregate] : undefined, query: (_a = incident === null || incident === void 0 ? void 0 : incident.discoverQuery) !== null && _a !== void 0 ? _a : '', projects: projects
            .filter(({ slug }) => incident.projects.includes(slug))
            .map(({ id }) => Number(id)), version: 2, fields: incident.alertRule.dataset === types_1.Dataset.ERRORS
            ? ['issue', 'count()', 'count_unique(user)']
            : ['transaction', incident.alertRule.aggregate], start,
        end }, extraQueryParams);
    const discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
    const _b = discoverView.getResultsViewUrlTarget(orgSlug), { query } = _b, toObject = (0, tslib_1.__rest)(_b, ["query"]);
    return Object.assign({ query: Object.assign(Object.assign({}, query), { interval: timeWindowString }) }, toObject);
}
exports.getIncidentDiscoverUrl = getIncidentDiscoverUrl;
//# sourceMappingURL=getIncidentDiscoverUrl.jsx.map