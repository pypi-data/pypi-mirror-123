Object.defineProperty(exports, "__esModule", { value: true });
exports.constructWidgetFromQuery = exports.eventViewFromWidget = exports.cloneDashboard = void 0;
const tslib_1 = require("tslib");
const cloneDeep_1 = (0, tslib_1.__importDefault)(require("lodash/cloneDeep"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const dates_1 = require("app/utils/dates");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const types_1 = require("./types");
function cloneDashboard(dashboard) {
    return (0, cloneDeep_1.default)(dashboard);
}
exports.cloneDashboard = cloneDashboard;
function eventViewFromWidget(title, query, selection, widgetType) {
    const { start, end, period: statsPeriod } = selection.datetime;
    const { projects, environments } = selection;
    // World Map requires an additional column (geo.country_code) to display in discover when navigating from the widget
    const fields = widgetType === types_1.DisplayType.WORLD_MAP
        ? ['geo.country_code', ...query.fields]
        : query.fields;
    const conditions = widgetType === types_1.DisplayType.WORLD_MAP
        ? `${query.conditions} has:geo.country_code`
        : query.conditions;
    return eventView_1.default.fromSavedQuery({
        id: undefined,
        name: title,
        version: 2,
        fields,
        query: conditions,
        orderby: query.orderby,
        projects,
        range: statsPeriod,
        start: start ? (0, dates_1.getUtcDateString)(start) : undefined,
        end: end ? (0, dates_1.getUtcDateString)(end) : undefined,
        environment: environments,
    });
}
exports.eventViewFromWidget = eventViewFromWidget;
function coerceStringToArray(value) {
    return typeof value === 'string' ? [value] : value;
}
function constructWidgetFromQuery(query) {
    if (query) {
        const queryNames = coerceStringToArray(query.queryNames);
        const queryConditions = coerceStringToArray(query.queryConditions);
        const queryFields = coerceStringToArray(query.queryFields);
        const queries = [];
        if (queryConditions &&
            queryNames &&
            queryFields &&
            typeof query.queryOrderby === 'string')
            queryConditions.forEach((condition, index) => {
                queries.push({
                    name: queryNames[index],
                    conditions: condition,
                    fields: queryFields,
                    orderby: query.queryOrderby,
                });
            });
        if (query.title && query.displayType && query.interval && queries.length > 0) {
            const newWidget = Object.assign(Object.assign({}, (0, pick_1.default)(query, ['title', 'displayType', 'interval'])), { queries });
            return newWidget;
        }
    }
    return undefined;
}
exports.constructWidgetFromQuery = constructWidgetFromQuery;
//# sourceMappingURL=utils.jsx.map