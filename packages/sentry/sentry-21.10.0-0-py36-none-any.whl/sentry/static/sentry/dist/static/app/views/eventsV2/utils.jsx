Object.defineProperty(exports, "__esModule", { value: true });
exports.setRenderPrebuilt = exports.shouldRenderPrebuilt = exports.generateFieldOptions = exports.getExpandedResults = exports.downloadAsCsv = exports.getPrebuiltQueries = exports.generateTitle = exports.pushEventViewToLocation = exports.decodeColumnOrder = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const papaparse_1 = (0, tslib_1.__importDefault)(require("papaparse"));
const gridEditable_1 = require("app/components/gridEditable");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const dates_1 = require("app/utils/dates");
const fields_1 = require("app/utils/discover/fields");
const events_1 = require("app/utils/events");
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const types_1 = require("./table/types");
const data_1 = require("./data");
const TEMPLATE_TABLE_COLUMN = {
    key: '',
    name: '',
    type: 'never',
    isSortable: false,
    column: Object.freeze({ kind: 'field', field: '' }),
    width: gridEditable_1.COL_WIDTH_UNDEFINED,
};
// TODO(mark) these types are coupled to the gridEditable component types and
// I'd prefer the types to be more general purpose but that will require a second pass.
function decodeColumnOrder(fields) {
    let equations = 0;
    return fields.map((f) => {
        const column = Object.assign({}, TEMPLATE_TABLE_COLUMN);
        const col = (0, fields_1.explodeFieldString)(f.field);
        let columnName = f.field;
        if ((0, fields_1.isEquation)(f.field)) {
            columnName = `equation[${equations}]`;
            equations += 1;
        }
        column.key = columnName;
        column.name = columnName;
        column.width = f.width || gridEditable_1.COL_WIDTH_UNDEFINED;
        if (col.kind === 'function') {
            // Aggregations can have a strict outputType or they can inherit from their field.
            // Otherwise use the FIELDS data to infer types.
            const outputType = (0, fields_1.aggregateFunctionOutputType)(col.function[0], col.function[1]);
            if (outputType !== null) {
                column.type = outputType;
            }
            const aggregate = fields_1.AGGREGATIONS[col.function[0]];
            column.isSortable = aggregate && aggregate.isSortable;
        }
        else if (col.kind === 'field') {
            if (fields_1.FIELDS.hasOwnProperty(col.field)) {
                column.type = fields_1.FIELDS[col.field];
            }
            else if ((0, fields_1.isMeasurement)(col.field)) {
                column.type = (0, fields_1.measurementType)(col.field);
            }
            else if ((0, fields_1.isSpanOperationBreakdownField)(col.field)) {
                column.type = 'duration';
            }
        }
        column.column = col;
        return column;
    });
}
exports.decodeColumnOrder = decodeColumnOrder;
function pushEventViewToLocation(props) {
    const { location, nextEventView } = props;
    const extraQuery = props.extraQuery || {};
    const queryStringObject = nextEventView.generateQueryStringObject();
    react_router_1.browserHistory.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, extraQuery), queryStringObject) }));
}
exports.pushEventViewToLocation = pushEventViewToLocation;
function generateTitle({ eventView, event, organization, }) {
    const titles = [(0, locale_1.t)('Discover')];
    const eventViewName = eventView.name;
    if (typeof eventViewName === 'string' && String(eventViewName).trim().length > 0) {
        titles.push(String(eventViewName).trim());
    }
    const eventTitle = event ? (0, events_1.getTitle)(event, organization === null || organization === void 0 ? void 0 : organization.features).title : undefined;
    if (eventTitle) {
        titles.push(eventTitle);
    }
    titles.reverse();
    return titles.join(' - ');
}
exports.generateTitle = generateTitle;
function getPrebuiltQueries(organization) {
    const views = [...data_1.ALL_VIEWS];
    if (organization.features.includes('performance-view')) {
        // insert transactions queries at index 2
        views.splice(2, 0, ...data_1.TRANSACTION_VIEWS);
        views.push(...data_1.WEB_VITALS_VIEWS);
    }
    return views;
}
exports.getPrebuiltQueries = getPrebuiltQueries;
function disableMacros(value) {
    const unsafeCharacterRegex = /^[\=\+\-\@]/;
    if (typeof value === 'string' && `${value}`.match(unsafeCharacterRegex)) {
        return `'${value}`;
    }
    return value;
}
function downloadAsCsv(tableData, columnOrder, filename) {
    const { data } = tableData;
    const headings = columnOrder.map(column => column.name);
    const csvContent = papaparse_1.default.unparse({
        fields: headings,
        data: data.map(row => headings.map(col => {
            col = (0, fields_1.getAggregateAlias)(col);
            return disableMacros(row[col]);
        })),
    });
    // Need to also manually replace # since encodeURI skips them
    const encodedDataUrl = `data:text/csv;charset=utf8,${encodeURIComponent(csvContent)}`;
    // Create a download link then click it, this is so we can get a filename
    const link = document.createElement('a');
    const now = new Date();
    link.setAttribute('href', encodedDataUrl);
    link.setAttribute('download', `${filename} ${(0, dates_1.getUtcDateString)(now)}.csv`);
    link.click();
    link.remove();
    // Make testing easier
    return encodedDataUrl;
}
exports.downloadAsCsv = downloadAsCsv;
const ALIASED_AGGREGATES_COLUMN = {
    last_seen: 'timestamp',
    failure_count: 'transaction.status',
};
/**
 * Convert an aggregate into the resulting column from a drilldown action.
 * The result is null if the drilldown results in the aggregate being removed.
 */
function drilldownAggregate(func) {
    var _a;
    const key = func.function[0];
    const aggregation = fields_1.AGGREGATIONS[key];
    let column = func.function[1];
    if (ALIASED_AGGREGATES_COLUMN.hasOwnProperty(key)) {
        // Some aggregates are just shortcuts to other aggregates with
        // predefined arguments so we can directly map them to the result.
        column = ALIASED_AGGREGATES_COLUMN[key];
    }
    else if ((_a = aggregation === null || aggregation === void 0 ? void 0 : aggregation.parameters) === null || _a === void 0 ? void 0 : _a[0]) {
        const parameter = aggregation.parameters[0];
        if (parameter.kind !== 'column') {
            // The aggregation does not accept a column as a parameter,
            // so we clear the column.
            column = '';
        }
        else if (!column && parameter.required === false) {
            // The parameter was not given for a non-required parameter,
            // so we fall back to the default.
            column = parameter.defaultValue;
        }
    }
    else {
        // The aggregation does not exist or does not have any parameters,
        // so we clear the column.
        column = '';
    }
    return column ? { kind: 'field', field: column } : null;
}
/**
 * Convert an aggregated query into one that does not have aggregates.
 * Will also apply additions conditions defined in `additionalConditions`
 * and generate conditions based on the `dataRow` parameter and the current fields
 * in the `eventView`.
 */
function getExpandedResults(eventView, additionalConditions, dataRow) {
    const fieldSet = new Set();
    // Expand any functions in the resulting column, and dedupe the result.
    // Mark any column as null to remove it.
    const expandedColumns = eventView.fields.map((field) => {
        const exploded = (0, fields_1.explodeFieldString)(field.field);
        const column = exploded.kind === 'function' ? drilldownAggregate(exploded) : exploded;
        if (
        // if expanding the function failed
        column === null ||
            // the new column is already present
            fieldSet.has(column.field) ||
            // Skip aggregate equations, their functions will already be added so we just want to remove it
            (0, fields_1.isAggregateEquation)(field.field)) {
            return null;
        }
        fieldSet.add(column.field);
        return column;
    });
    // id should be default column when expanded results in no columns; but only if
    // the Discover query's columns is non-empty.
    // This typically occurs in Discover drilldowns.
    if (fieldSet.size === 0 && expandedColumns.length) {
        expandedColumns[0] = { kind: 'field', field: 'id' };
    }
    // update the columns according the the expansion above
    const nextView = expandedColumns.reduceRight((newView, column, index) => column === null
        ? newView.withDeletedColumn(index, undefined)
        : newView.withUpdatedColumn(index, column, undefined), eventView.clone());
    nextView.query = generateExpandedConditions(nextView, additionalConditions, dataRow);
    return nextView;
}
exports.getExpandedResults = getExpandedResults;
/**
 * Create additional conditions based on the fields in an EventView
 * and a datarow/event
 */
function generateAdditionalConditions(eventView, dataRow) {
    const specialKeys = Object.values(globalSelectionHeader_1.URL_PARAM);
    const conditions = {};
    if (!dataRow) {
        return conditions;
    }
    eventView.fields.forEach((field) => {
        const column = (0, fields_1.explodeFieldString)(field.field);
        // Skip aggregate fields
        if (column.kind === 'function') {
            return;
        }
        const dataKey = (0, fields_1.getAggregateAlias)(field.field);
        // Append the current field as a condition if it exists in the dataRow
        // Or is a simple key in the event. More complex deeply nested fields are
        // more challenging to get at as their location in the structure does not
        // match their name.
        if (dataRow.hasOwnProperty(dataKey)) {
            let value = dataRow[dataKey];
            if (Array.isArray(value)) {
                if (value.length > 1) {
                    conditions[column.field] = value;
                    return;
                }
                else {
                    // An array with only one value is equivalent to the value itself.
                    value = value[0];
                }
            }
            // if the value will be quoted, then do not trim it as the whitespaces
            // may be important to the query and should not be trimmed
            const shouldQuote = value === null || value === undefined
                ? false
                : /[\s\(\)\\"]/g.test(String(value).trim());
            const nextValue = value === null || value === undefined
                ? ''
                : shouldQuote
                    ? String(value)
                    : String(value).trim();
            if ((0, fields_1.isMeasurement)(column.field) && !nextValue) {
                // Do not add measurement conditions if nextValue is falsey.
                // It's expected that nextValue is a numeric value.
                return;
            }
            switch (column.field) {
                case 'timestamp':
                    // normalize the "timestamp" field to ensure the payload works
                    conditions[column.field] = (0, dates_1.getUtcDateString)(nextValue);
                    break;
                default:
                    conditions[column.field] = nextValue;
            }
        }
        // If we have an event, check tags as well.
        if (dataRow.tags && Array.isArray(dataRow.tags)) {
            const tagIndex = dataRow.tags.findIndex(item => item.key === dataKey);
            if (tagIndex > -1) {
                const key = specialKeys.includes(column.field)
                    ? `tags[${column.field}]`
                    : column.field;
                const tagValue = dataRow.tags[tagIndex].value;
                conditions[key] = tagValue;
            }
        }
    });
    return conditions;
}
function generateExpandedConditions(eventView, additionalConditions, dataRow) {
    const parsedQuery = new tokenizeSearch_1.MutableSearch(eventView.query);
    // Remove any aggregates from the search conditions.
    // otherwise, it'll lead to an invalid query result.
    for (const key in parsedQuery.filters) {
        const column = (0, fields_1.explodeFieldString)(key);
        if (column.kind === 'function') {
            parsedQuery.removeFilter(key);
        }
    }
    const conditions = Object.assign({}, additionalConditions, generateAdditionalConditions(eventView, dataRow));
    // Add additional conditions provided and generated.
    for (const key in conditions) {
        const value = conditions[key];
        if (Array.isArray(value)) {
            parsedQuery.setFilterValues(key, value);
            continue;
        }
        if (key === 'project.id') {
            eventView.project = [...eventView.project, parseInt(value, 10)];
            continue;
        }
        if (key === 'environment') {
            if (!eventView.environment.includes(value)) {
                eventView.environment = [...eventView.environment, value];
            }
            continue;
        }
        const column = (0, fields_1.explodeFieldString)(key);
        // Skip aggregates as they will be invalid.
        if (column.kind === 'function') {
            continue;
        }
        parsedQuery.setFilterValues(key, [value]);
    }
    return parsedQuery.formatString();
}
function generateFieldOptions({ organization, tagKeys, measurementKeys, spanOperationBreakdownKeys, aggregations = fields_1.AGGREGATIONS, fields = fields_1.FIELDS, }) {
    let fieldKeys = Object.keys(fields).sort();
    let functions = Object.keys(aggregations);
    // Strip tracing features if the org doesn't have access.
    if (!organization.features.includes('performance-view')) {
        fieldKeys = fieldKeys.filter(item => !fields_1.TRACING_FIELDS.includes(item));
        functions = functions.filter(item => !fields_1.TRACING_FIELDS.includes(item));
    }
    const fieldOptions = {};
    // Index items by prefixed keys as custom tags can overlap both fields and
    // function names. Having a mapping makes finding the value objects easier
    // later as well.
    functions.forEach(func => {
        const ellipsis = aggregations[func].parameters.length ? '\u2026' : '';
        const parameters = aggregations[func].parameters.map(param => {
            const overrides = fields_1.AGGREGATIONS[func].getFieldOverrides;
            if (typeof overrides === 'undefined') {
                return param;
            }
            return Object.assign(Object.assign({}, param), overrides({ parameter: param, organization }));
        });
        fieldOptions[`function:${func}`] = {
            label: `${func}(${ellipsis})`,
            value: {
                kind: types_1.FieldValueKind.FUNCTION,
                meta: {
                    name: func,
                    parameters,
                },
            },
        };
    });
    fieldKeys.forEach(field => {
        fieldOptions[`field:${field}`] = {
            label: field,
            value: {
                kind: types_1.FieldValueKind.FIELD,
                meta: {
                    name: field,
                    dataType: fields[field],
                },
            },
        };
    });
    if (tagKeys !== undefined && tagKeys !== null) {
        tagKeys.sort();
        tagKeys.forEach(tag => {
            const tagValue = fields.hasOwnProperty(tag) || fields_1.AGGREGATIONS.hasOwnProperty(tag)
                ? `tags[${tag}]`
                : tag;
            fieldOptions[`tag:${tag}`] = {
                label: tag,
                value: {
                    kind: types_1.FieldValueKind.TAG,
                    meta: { name: tagValue, dataType: 'string' },
                },
            };
        });
    }
    if (measurementKeys !== undefined && measurementKeys !== null) {
        measurementKeys.sort();
        measurementKeys.forEach(measurement => {
            fieldOptions[`measurement:${measurement}`] = {
                label: measurement,
                value: {
                    kind: types_1.FieldValueKind.MEASUREMENT,
                    meta: { name: measurement, dataType: (0, fields_1.measurementType)(measurement) },
                },
            };
        });
    }
    if (Array.isArray(spanOperationBreakdownKeys)) {
        spanOperationBreakdownKeys.sort();
        spanOperationBreakdownKeys.forEach(breakdownField => {
            fieldOptions[`span_op_breakdown:${breakdownField}`] = {
                label: breakdownField,
                value: {
                    kind: types_1.FieldValueKind.BREAKDOWN,
                    meta: { name: breakdownField, dataType: 'duration' },
                },
            };
        });
    }
    return fieldOptions;
}
exports.generateFieldOptions = generateFieldOptions;
const RENDER_PREBUILT_KEY = 'discover-render-prebuilt';
function shouldRenderPrebuilt() {
    const shouldRender = localStorage_1.default.getItem(RENDER_PREBUILT_KEY);
    return shouldRender === 'true' || shouldRender === null;
}
exports.shouldRenderPrebuilt = shouldRenderPrebuilt;
function setRenderPrebuilt(value) {
    localStorage_1.default.setItem(RENDER_PREBUILT_KEY, value ? 'true' : 'false');
}
exports.setRenderPrebuilt = setRenderPrebuilt;
//# sourceMappingURL=utils.jsx.map