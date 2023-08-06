Object.defineProperty(exports, "__esModule", { value: true });
exports.getEventTypeFilter = exports.extractEventTypeFilterFromRule = void 0;
const utils_1 = require("app/views/alerts/utils");
const constants_1 = require("../constants");
const types_1 = require("../types");
function extractEventTypeFilterFromRule(metricRule) {
    const { dataset, eventTypes } = metricRule;
    return getEventTypeFilter(dataset, eventTypes);
}
exports.extractEventTypeFilterFromRule = extractEventTypeFilterFromRule;
function getEventTypeFilter(dataset, eventTypes) {
    var _a;
    if (eventTypes) {
        return constants_1.DATASOURCE_EVENT_TYPE_FILTERS[(_a = (0, utils_1.convertDatasetEventTypesToSource)(dataset, eventTypes)) !== null && _a !== void 0 ? _a : types_1.Datasource.ERROR];
    }
    else {
        return constants_1.DATASET_EVENT_TYPE_FILTERS[dataset !== null && dataset !== void 0 ? dataset : types_1.Dataset.ERRORS];
    }
}
exports.getEventTypeFilter = getEventTypeFilter;
//# sourceMappingURL=getEventTypeFilter.jsx.map