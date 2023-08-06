Object.defineProperty(exports, "__esModule", { value: true });
exports.normalizeQueries = exports.mapErrors = void 0;
const tslib_1 = require("tslib");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const fields_1 = require("app/utils/discover/fields");
const utils_1 = require("../utils");
function mapErrors(data, update) {
    Object.keys(data).forEach((key) => {
        const value = data[key];
        // Recurse into nested objects.
        if (Array.isArray(value) && typeof value[0] === 'string') {
            update[key] = value[0];
            return;
        }
        else if (Array.isArray(value) && typeof value[0] === 'object') {
            update[key] = value.map(item => mapErrors(item, {}));
        }
        else {
            update[key] = mapErrors(value, {});
        }
    });
    return update;
}
exports.mapErrors = mapErrors;
function normalizeQueries(displayType, queries) {
    const isTimeseriesChart = [
        utils_1.DisplayType.LINE,
        utils_1.DisplayType.AREA,
        utils_1.DisplayType.STACKED_AREA,
        utils_1.DisplayType.BAR,
    ].includes(displayType);
    if ([utils_1.DisplayType.TABLE, utils_1.DisplayType.WORLD_MAP, utils_1.DisplayType.BIG_NUMBER].includes(displayType)) {
        // Some display types may only support at most 1 query.
        queries = queries.slice(0, 1);
    }
    else if (isTimeseriesChart) {
        // Timeseries charts supports at most 3 queries.
        queries = queries.slice(0, 3);
    }
    if (displayType === utils_1.DisplayType.TABLE) {
        return queries;
    }
    if (displayType === utils_1.DisplayType.TOP_N) {
        queries = queries.slice(0, 1);
        const aggregateFields = (0, fields_1.getAggregateFields)(queries[0].fields);
        let otherFields = queries[0].fields.filter(field => !!!aggregateFields.includes(field));
        otherFields = otherFields.length ? otherFields : ['title'];
        const fields = [
            ...otherFields,
            aggregateFields.length ? aggregateFields[0] : 'count()',
        ];
        queries = queries.map(query => (Object.assign(Object.assign({}, query), { fields })));
        return queries;
    }
    // Filter out non-aggregate fields
    queries = queries.map(query => {
        let fields = query.fields.filter(fields_1.isAggregateFieldOrEquation);
        if (isTimeseriesChart || displayType === utils_1.DisplayType.WORLD_MAP) {
            // Filter out fields that will not generate numeric output types
            fields = fields.filter(field => (0, fields_1.isLegalYAxisType)((0, fields_1.aggregateOutputType)(field)));
        }
        if (isTimeseriesChart && fields.length && fields.length > 3) {
            // Timeseries charts supports at most 3 fields.
            fields = fields.slice(0, 3);
        }
        return Object.assign(Object.assign({}, query), { fields: fields.length ? fields : ['count()'] });
    });
    if (isTimeseriesChart) {
        // For timeseries widget, all queries must share identical set of fields.
        const referenceFields = [...queries[0].fields];
        queryLoop: for (const query of queries) {
            if (referenceFields.length >= 3) {
                break;
            }
            if ((0, isEqual_1.default)(referenceFields, query.fields)) {
                continue;
            }
            for (const field of query.fields) {
                if (referenceFields.length >= 3) {
                    break queryLoop;
                }
                if (!referenceFields.includes(field)) {
                    referenceFields.push(field);
                }
            }
        }
        queries = queries.map(query => {
            return Object.assign(Object.assign({}, query), { fields: referenceFields });
        });
    }
    if ([utils_1.DisplayType.WORLD_MAP, utils_1.DisplayType.BIG_NUMBER].includes(displayType)) {
        // For world map chart, cap fields of the queries to only one field.
        queries = queries.map(query => {
            return Object.assign(Object.assign({}, query), { fields: query.fields.slice(0, 1) });
        });
    }
    return queries;
}
exports.normalizeQueries = normalizeQueries;
//# sourceMappingURL=utils.jsx.map