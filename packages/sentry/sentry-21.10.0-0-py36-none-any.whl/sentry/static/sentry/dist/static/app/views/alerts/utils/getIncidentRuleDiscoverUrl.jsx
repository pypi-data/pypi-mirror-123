Object.defineProperty(exports, "__esModule", { value: true });
exports.getIncidentRuleDiscoverUrl = void 0;
const tslib_1 = require("tslib");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fields_1 = require("app/utils/discover/fields");
const types_1 = require("app/views/alerts/incidentRules/types");
/**
 * Gets the URL for a discover view of the rule with the following default
 * parameters:
 *
 * - Ordered by the rule aggregate, descending
 * - yAxis maps to the aggregate
 * - The following fields are displayed:
 *   - For Error dataset alert rules: [issue, count(), count_unique(user)]
 *   - For Transaction dataset alert rules: [transaction, count()]
 * - Start and end are the period's values selected in the chart header
 */
function getIncidentRuleDiscoverUrl(opts) {
    var _a;
    const { orgSlug, projects, rule, eventType, start, end, extraQueryParams } = opts;
    const eventTypeTagFilter = eventType && (rule === null || rule === void 0 ? void 0 : rule.query) ? eventType : '';
    if (!projects || !projects.length || !rule || (!start && !end)) {
        return '';
    }
    const timeWindowString = `${rule.timeWindow}m`;
    const discoverQuery = Object.assign({ id: undefined, name: (rule && rule.name) || '', orderby: `-${(0, fields_1.getAggregateAlias)(rule.aggregate)}`, yAxis: rule.aggregate ? [rule.aggregate] : undefined, query: (_a = (eventTypeTagFilter || (rule === null || rule === void 0 ? void 0 : rule.query) || eventType)) !== null && _a !== void 0 ? _a : '', projects: projects
            .filter(({ slug }) => rule.projects.includes(slug))
            .map(({ id }) => Number(id)), version: 2, fields: rule.dataset === types_1.Dataset.ERRORS
            ? ['issue', 'count()', 'count_unique(user)']
            : ['transaction', rule.aggregate], start,
        end }, extraQueryParams);
    const discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
    const _b = discoverView.getResultsViewUrlTarget(orgSlug), { query } = _b, toObject = (0, tslib_1.__rest)(_b, ["query"]);
    return Object.assign({ query: Object.assign(Object.assign({}, query), { interval: timeWindowString }) }, toObject);
}
exports.getIncidentRuleDiscoverUrl = getIncidentRuleDiscoverUrl;
//# sourceMappingURL=getIncidentRuleDiscoverUrl.jsx.map