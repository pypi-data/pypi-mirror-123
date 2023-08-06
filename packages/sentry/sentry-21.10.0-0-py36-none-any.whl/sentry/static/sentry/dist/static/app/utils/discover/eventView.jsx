Object.defineProperty(exports, "__esModule", { value: true });
exports.pickRelevantLocationQueryStrings = exports.isAPIPayloadSimilar = exports.fromSorts = exports.isFieldSortable = void 0;
const tslib_1 = require("tslib");
const cloneDeep_1 = (0, tslib_1.__importDefault)(require("lodash/cloneDeep"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const isString_1 = (0, tslib_1.__importDefault)(require("lodash/isString"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const uniqBy_1 = (0, tslib_1.__importDefault)(require("lodash/uniqBy"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const gridEditable_1 = require("app/components/gridEditable");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const constants_1 = require("app/constants");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
const types_1 = require("app/utils/discover/types");
const queryString_1 = require("app/utils/queryString");
const types_2 = require("app/views/eventsV2/table/types");
const utils_1 = require("app/views/eventsV2/utils");
const dates_1 = require("../dates");
const tokenizeSearch_1 = require("../tokenizeSearch");
const fieldRenderers_1 = require("./fieldRenderers");
const DATETIME_QUERY_STRING_KEYS = ['start', 'end', 'utc', 'statsPeriod'];
const EXTERNAL_QUERY_STRING_KEYS = [
    ...DATETIME_QUERY_STRING_KEYS,
    'cursor',
];
const setSortOrder = (sort, kind) => ({
    kind,
    field: sort.field,
});
const reverseSort = (sort) => ({
    kind: sort.kind === 'desc' ? 'asc' : 'desc',
    field: sort.field,
});
const isSortEqualToField = (sort, field, tableMeta) => {
    const sortKey = getSortKeyFromField(field, tableMeta);
    return sort.field === sortKey;
};
const fieldToSort = (field, tableMeta, kind) => {
    const sortKey = getSortKeyFromField(field, tableMeta);
    if (!sortKey) {
        return void 0;
    }
    return {
        kind: kind || 'desc',
        field: sortKey,
    };
};
function getSortKeyFromField(field, tableMeta) {
    const alias = (0, fields_1.getAggregateAlias)(field.field);
    return (0, fieldRenderers_1.getSortField)(alias, tableMeta);
}
function isFieldSortable(field, tableMeta) {
    return !!getSortKeyFromField(field, tableMeta);
}
exports.isFieldSortable = isFieldSortable;
const decodeFields = (location) => {
    const { query } = location;
    if (!query || !query.field) {
        return [];
    }
    const fields = (0, queryString_1.decodeList)(query.field);
    const widths = (0, queryString_1.decodeList)(query.widths);
    const parsed = [];
    fields.forEach((field, i) => {
        const w = Number(widths[i]);
        const width = !isNaN(w) ? w : gridEditable_1.COL_WIDTH_UNDEFINED;
        parsed.push({ field, width });
    });
    return parsed;
};
const parseSort = (sort) => {
    sort = sort.trim();
    if (sort.startsWith('-')) {
        return {
            kind: 'desc',
            field: sort.substring(1),
        };
    }
    return {
        kind: 'asc',
        field: sort,
    };
};
const fromSorts = (sorts) => {
    if (sorts === undefined) {
        return [];
    }
    sorts = (0, isString_1.default)(sorts) ? [sorts] : sorts;
    // NOTE: sets are iterated in insertion order
    const uniqueSorts = [...new Set(sorts)];
    return uniqueSorts.reduce((acc, sort) => {
        acc.push(parseSort(sort));
        return acc;
    }, []);
};
exports.fromSorts = fromSorts;
const decodeSorts = (location) => {
    const { query } = location;
    if (!query || !query.sort) {
        return [];
    }
    const sorts = (0, queryString_1.decodeList)(query.sort);
    return (0, exports.fromSorts)(sorts);
};
const encodeSort = (sort) => {
    switch (sort.kind) {
        case 'desc': {
            return `-${sort.field}`;
        }
        case 'asc': {
            return String(sort.field);
        }
        default: {
            throw new Error('Unexpected sort type');
        }
    }
};
const encodeSorts = (sorts) => sorts.map(encodeSort);
const collectQueryStringByKey = (query, key) => {
    const needle = query[key];
    const collection = (0, queryString_1.decodeList)(needle);
    return collection.reduce((acc, item) => {
        item = item.trim();
        if (item.length > 0) {
            acc.push(item);
        }
        return acc;
    }, []);
};
const decodeQuery = (location) => {
    if (!location.query || !location.query.query) {
        return '';
    }
    const queryParameter = location.query.query;
    return (0, queryString_1.decodeScalar)(queryParameter, '').trim();
};
const decodeTeam = (value) => {
    if (value === 'myteams') {
        return value;
    }
    return parseInt(value, 10);
};
const decodeTeams = (location) => {
    if (!location.query || !location.query.team) {
        return [];
    }
    const value = location.query.team;
    return Array.isArray(value) ? value.map(decodeTeam) : [decodeTeam(value)];
};
const decodeProjects = (location) => {
    if (!location.query || !location.query.project) {
        return [];
    }
    const value = location.query.project;
    return Array.isArray(value) ? value.map(i => parseInt(i, 10)) : [parseInt(value, 10)];
};
const queryStringFromSavedQuery = (saved) => {
    if (saved.query) {
        return saved.query || '';
    }
    return '';
};
function validateTableMeta(tableMeta) {
    return tableMeta && Object.keys(tableMeta).length > 0 ? tableMeta : undefined;
}
class EventView {
    constructor(props) {
        const fields = Array.isArray(props.fields) ? props.fields : [];
        let sorts = Array.isArray(props.sorts) ? props.sorts : [];
        const team = Array.isArray(props.team) ? props.team : [];
        const project = Array.isArray(props.project) ? props.project : [];
        const environment = Array.isArray(props.environment) ? props.environment : [];
        // only include sort keys that are included in the fields
        let equations = 0;
        const sortKeys = fields
            .map(field => {
            if (field.field && (0, fields_1.isEquation)(field.field)) {
                const sortKey = getSortKeyFromField({ field: `equation[${equations}]` }, undefined);
                equations += 1;
                return sortKey;
            }
            return getSortKeyFromField(field, undefined);
        })
            .filter((sortKey) => !!sortKey);
        const sort = sorts.find(currentSort => sortKeys.includes(currentSort.field));
        sorts = sort ? [sort] : [];
        const id = props.id !== null && props.id !== void 0 ? String(props.id) : void 0;
        this.id = id;
        this.name = props.name;
        this.fields = fields;
        this.sorts = sorts;
        this.query = typeof props.query === 'string' ? props.query : '';
        this.team = team;
        this.project = project;
        this.start = props.start;
        this.end = props.end;
        this.statsPeriod = props.statsPeriod;
        this.environment = environment;
        this.yAxis = props.yAxis;
        this.display = props.display;
        this.topEvents = props.topEvents;
        this.interval = props.interval;
        this.createdBy = props.createdBy;
        this.expired = props.expired;
        this.additionalConditions = props.additionalConditions
            ? props.additionalConditions.copy()
            : new tokenizeSearch_1.MutableSearch([]);
    }
    static fromLocation(location) {
        const { start, end, statsPeriod } = (0, getParams_1.getParams)(location.query);
        return new EventView({
            id: (0, queryString_1.decodeScalar)(location.query.id),
            name: (0, queryString_1.decodeScalar)(location.query.name),
            fields: decodeFields(location),
            sorts: decodeSorts(location),
            query: decodeQuery(location),
            team: decodeTeams(location),
            project: decodeProjects(location),
            start: (0, queryString_1.decodeScalar)(start),
            end: (0, queryString_1.decodeScalar)(end),
            statsPeriod: (0, queryString_1.decodeScalar)(statsPeriod),
            environment: collectQueryStringByKey(location.query, 'environment'),
            yAxis: (0, queryString_1.decodeScalar)(location.query.yAxis),
            display: (0, queryString_1.decodeScalar)(location.query.display),
            topEvents: (0, queryString_1.decodeScalar)(location.query.topEvents),
            interval: (0, queryString_1.decodeScalar)(location.query.interval),
            createdBy: undefined,
            additionalConditions: new tokenizeSearch_1.MutableSearch([]),
        });
    }
    static fromNewQueryWithLocation(newQuery, location) {
        const query = location.query;
        // apply global selection header values from location whenever possible
        const environment = Array.isArray(newQuery.environment) && newQuery.environment.length > 0
            ? newQuery.environment
            : collectQueryStringByKey(query, 'environment');
        const project = Array.isArray(newQuery.projects) && newQuery.projects.length > 0
            ? newQuery.projects
            : decodeProjects(location);
        const saved = Object.assign(Object.assign({}, newQuery), { environment, projects: project, 
            // datetime selection
            start: newQuery.start || (0, queryString_1.decodeScalar)(query.start), end: newQuery.end || (0, queryString_1.decodeScalar)(query.end), range: newQuery.range || (0, queryString_1.decodeScalar)(query.statsPeriod) });
        return EventView.fromSavedQuery(saved);
    }
    static getFields(saved) {
        return saved.fields.map((field, i) => {
            const width = saved.widths && saved.widths[i] ? Number(saved.widths[i]) : gridEditable_1.COL_WIDTH_UNDEFINED;
            return { field, width };
        });
    }
    static fromSavedQuery(saved) {
        var _a;
        const fields = EventView.getFields(saved);
        // normalize datetime selection
        const { start, end, statsPeriod } = (0, getParams_1.getParams)({
            start: saved.start,
            end: saved.end,
            statsPeriod: saved.range,
        });
        return new EventView({
            id: saved.id,
            name: saved.name,
            fields,
            query: queryStringFromSavedQuery(saved),
            team: (_a = saved.teams) !== null && _a !== void 0 ? _a : [],
            project: saved.projects,
            start: (0, queryString_1.decodeScalar)(start),
            end: (0, queryString_1.decodeScalar)(end),
            statsPeriod: (0, queryString_1.decodeScalar)(statsPeriod),
            sorts: (0, exports.fromSorts)(saved.orderby),
            environment: collectQueryStringByKey({
                environment: saved.environment,
            }, 'environment'),
            // Workaround to only use the first yAxis since eventView yAxis doesn't accept string[]
            yAxis: Array.isArray(saved.yAxis) ? saved.yAxis[0] : saved.yAxis,
            display: saved.display,
            topEvents: saved.topEvents ? saved.topEvents.toString() : undefined,
            createdBy: saved.createdBy,
            expired: saved.expired,
            additionalConditions: new tokenizeSearch_1.MutableSearch([]),
        });
    }
    static fromSavedQueryOrLocation(saved, location) {
        let fields = decodeFields(location);
        const { start, end, statsPeriod } = (0, getParams_1.getParams)(location.query);
        const id = (0, queryString_1.decodeScalar)(location.query.id);
        const teams = decodeTeams(location);
        const projects = decodeProjects(location);
        const sorts = decodeSorts(location);
        const environments = collectQueryStringByKey(location.query, 'environment');
        if (saved) {
            if (fields.length === 0) {
                fields = EventView.getFields(saved);
            }
            return new EventView({
                id: id || saved.id,
                name: (0, queryString_1.decodeScalar)(location.query.name) || saved.name,
                fields,
                query: 'query' in location.query
                    ? decodeQuery(location)
                    : queryStringFromSavedQuery(saved),
                sorts: sorts.length === 0 ? (0, exports.fromSorts)(saved.orderby) : sorts,
                yAxis: (0, queryString_1.decodeScalar)(location.query.yAxis) ||
                    // Workaround to only use the first yAxis since eventView yAxis doesn't accept string[]
                    (Array.isArray(saved.yAxis) ? saved.yAxis[0] : saved.yAxis),
                display: (0, queryString_1.decodeScalar)(location.query.display) || saved.display,
                topEvents: ((0, queryString_1.decodeScalar)(location.query.topEvents) ||
                    saved.topEvents ||
                    types_1.TOP_N).toString(),
                interval: (0, queryString_1.decodeScalar)(location.query.interval),
                createdBy: saved.createdBy,
                expired: saved.expired,
                additionalConditions: new tokenizeSearch_1.MutableSearch([]),
                // Always read team from location since they can be set by other parts
                // of the UI
                team: teams,
                // Always read project and environment from location since they can
                // be set by the GlobalSelectionHeaders.
                project: projects,
                environment: environments,
                start: (0, queryString_1.decodeScalar)(start),
                end: (0, queryString_1.decodeScalar)(end),
                statsPeriod: (0, queryString_1.decodeScalar)(statsPeriod),
            });
        }
        return EventView.fromLocation(location);
    }
    isEqualTo(other) {
        var _a, _b;
        const keys = [
            'id',
            'name',
            'query',
            'statsPeriod',
            'fields',
            'sorts',
            'project',
            'environment',
            'display',
            'topEvents',
        ];
        for (const key of keys) {
            const currentValue = this[key];
            const otherValue = other[key];
            if (!(0, isEqual_1.default)(currentValue, otherValue)) {
                return false;
            }
        }
        // compare datetime selections using moment
        const dateTimeKeys = ['start', 'end'];
        for (const key of dateTimeKeys) {
            const currentValue = this[key];
            const otherValue = other[key];
            if (currentValue && otherValue) {
                const currentDateTime = moment_1.default.utc(currentValue);
                const othereDateTime = moment_1.default.utc(otherValue);
                if (!currentDateTime.isSame(othereDateTime)) {
                    return false;
                }
            }
        }
        // compare yAxis selections
        // undefined yAxis values default to count()
        const currentYAxisValue = (_a = this.yAxis) !== null && _a !== void 0 ? _a : 'count()';
        const otherYAxisValue = (_b = other.yAxis) !== null && _b !== void 0 ? _b : 'count()';
        if (!(0, isEqual_1.default)(currentYAxisValue, otherYAxisValue)) {
            return false;
        }
        return true;
    }
    toNewQuery() {
        const orderby = this.sorts.length > 0 ? encodeSorts(this.sorts)[0] : undefined;
        const newQuery = {
            version: 2,
            id: this.id,
            name: this.name || '',
            fields: this.getFields(),
            widths: this.getWidths().map(w => String(w)),
            orderby,
            query: this.query || '',
            projects: this.project,
            start: this.start,
            end: this.end,
            range: this.statsPeriod,
            environment: this.environment,
            yAxis: this.yAxis ? [this.yAxis] : undefined,
            display: this.display,
            topEvents: this.topEvents,
        };
        if (!newQuery.query) {
            // if query is an empty string, then it cannot be saved, so we omit it
            // from the payload
            delete newQuery.query;
        }
        return newQuery;
    }
    getGlobalSelection() {
        var _a, _b, _c;
        return {
            projects: this.project,
            environments: this.environment,
            datetime: {
                start: (_a = this.start) !== null && _a !== void 0 ? _a : null,
                end: (_b = this.end) !== null && _b !== void 0 ? _b : null,
                period: (_c = this.statsPeriod) !== null && _c !== void 0 ? _c : '',
                // TODO(tony) Add support for the Use UTC option from
                // the global headers, currently, that option is not
                // supported and all times are assumed to be UTC
                utc: true,
            },
        };
    }
    getGlobalSelectionQuery() {
        const { environments: environment, projects, datetime: { start, end, period, utc }, } = this.getGlobalSelection();
        return {
            project: projects.map(proj => proj.toString()),
            environment,
            utc: utc ? 'true' : 'false',
            // since these values are from `getGlobalSelection`
            // we know they have type `string | null`
            start: (start !== null && start !== void 0 ? start : undefined),
            end: (end !== null && end !== void 0 ? end : undefined),
            // we can't use the ?? operator here as we want to
            // convert the empty string to undefined
            statsPeriod: period ? period : undefined,
        };
    }
    generateBlankQueryStringObject() {
        const output = {
            id: undefined,
            name: undefined,
            field: undefined,
            widths: undefined,
            sort: undefined,
            tag: undefined,
            query: undefined,
            yAxis: undefined,
            display: undefined,
            topEvents: undefined,
            interval: undefined,
        };
        for (const field of EXTERNAL_QUERY_STRING_KEYS) {
            output[field] = undefined;
        }
        return output;
    }
    generateQueryStringObject() {
        const output = {
            id: this.id,
            name: this.name,
            field: this.getFields(),
            widths: this.getWidths(),
            sort: encodeSorts(this.sorts),
            environment: this.environment,
            project: this.project,
            query: this.query,
            yAxis: this.yAxis || this.getYAxis(),
            display: this.display,
            topEvents: this.topEvents,
            interval: this.interval,
        };
        for (const field of EXTERNAL_QUERY_STRING_KEYS) {
            if (this[field] && this[field].length) {
                output[field] = this[field];
            }
        }
        return (0, cloneDeep_1.default)(output);
    }
    isValid() {
        return this.fields.length > 0;
    }
    getWidths() {
        const result = this.fields.map(field => field.width ? field.width : gridEditable_1.COL_WIDTH_UNDEFINED);
        while (result.length > 0) {
            const width = result[result.length - 1];
            if (width === gridEditable_1.COL_WIDTH_UNDEFINED) {
                result.pop();
                continue;
            }
            break;
        }
        return result;
    }
    getFields() {
        return this.fields.map(field => field.field);
    }
    getEquations() {
        return this.fields
            .filter(field => (0, fields_1.isEquation)(field.field))
            .map(field => (0, fields_1.getEquation)(field.field));
    }
    getAggregateFields() {
        return this.fields.filter(field => (0, fields_1.isAggregateField)(field.field) || (0, fields_1.isAggregateEquation)(field.field));
    }
    hasAggregateField() {
        return this.fields.some(field => (0, fields_1.isAggregateField)(field.field));
    }
    hasIdField() {
        return this.fields.some(field => field.field === 'id');
    }
    numOfColumns() {
        return this.fields.length;
    }
    getColumns() {
        return (0, utils_1.decodeColumnOrder)(this.fields);
    }
    getDays() {
        const statsPeriod = (0, queryString_1.decodeScalar)(this.statsPeriod);
        return (0, dates_1.statsPeriodToDays)(statsPeriod, this.start, this.end);
    }
    clone() {
        // NOTE: We rely on usage of Readonly from TypeScript to ensure we do not mutate
        //       the attributes of EventView directly. This enables us to quickly
        //       clone new instances of EventView.
        return new EventView({
            id: this.id,
            name: this.name,
            fields: this.fields,
            sorts: this.sorts,
            query: this.query,
            team: this.team,
            project: this.project,
            start: this.start,
            end: this.end,
            statsPeriod: this.statsPeriod,
            environment: this.environment,
            yAxis: this.yAxis,
            display: this.display,
            topEvents: this.topEvents,
            interval: this.interval,
            expired: this.expired,
            createdBy: this.createdBy,
            additionalConditions: this.additionalConditions.copy(),
        });
    }
    withSorts(sorts) {
        const newEventView = this.clone();
        const fields = newEventView.fields.map(field => (0, fields_1.getAggregateAlias)(field.field));
        newEventView.sorts = sorts.filter(sort => fields.includes(sort.field));
        return newEventView;
    }
    withColumns(columns) {
        const newEventView = this.clone();
        const fields = columns
            .filter(col => ((col.kind === 'field' || col.kind === types_2.FieldValueKind.EQUATION) && col.field) ||
            (col.kind === 'function' && col.function[0]))
            .map(col => (0, fields_1.generateFieldAsString)(col))
            .map((field, i) => {
            // newly added field
            if (!newEventView.fields[i]) {
                return { field, width: gridEditable_1.COL_WIDTH_UNDEFINED };
            }
            // Existing columns that were not re ordered should retain
            // their old widths.
            const existing = newEventView.fields[i];
            const width = existing.field === field && existing.width !== undefined
                ? existing.width
                : gridEditable_1.COL_WIDTH_UNDEFINED;
            return { field, width };
        });
        newEventView.fields = fields;
        // Update sorts as sorted fields may have been removed.
        if (newEventView.sorts) {
            // Filter the sort fields down to those that are still selected.
            const sortKeys = fields.map(field => { var _a; return (_a = fieldToSort(field, undefined)) === null || _a === void 0 ? void 0 : _a.field; });
            const newSort = newEventView.sorts.filter(sort => sort && sortKeys.includes(sort.field));
            // If the sort field was removed, try and find a new sortable column.
            if (newSort.length === 0) {
                const sortField = fields.find(field => isFieldSortable(field, undefined));
                if (sortField) {
                    newSort.push({ field: sortField.field, kind: 'desc' });
                }
            }
            newEventView.sorts = newSort;
        }
        newEventView.yAxis = newEventView.getYAxis();
        return newEventView;
    }
    withNewColumn(newColumn) {
        const fieldAsString = (0, fields_1.generateFieldAsString)(newColumn);
        const newField = {
            field: fieldAsString,
            width: gridEditable_1.COL_WIDTH_UNDEFINED,
        };
        const newEventView = this.clone();
        newEventView.fields = [...newEventView.fields, newField];
        return newEventView;
    }
    withResizedColumn(columnIndex, newWidth) {
        const field = this.fields[columnIndex];
        const newEventView = this.clone();
        if (!field) {
            return newEventView;
        }
        const updateWidth = field.width !== newWidth;
        if (updateWidth) {
            const fields = [...newEventView.fields];
            fields[columnIndex] = Object.assign(Object.assign({}, field), { width: newWidth });
            newEventView.fields = fields;
        }
        return newEventView;
    }
    withUpdatedColumn(columnIndex, updatedColumn, tableMeta) {
        const columnToBeUpdated = this.fields[columnIndex];
        const fieldAsString = (0, fields_1.generateFieldAsString)(updatedColumn);
        const updateField = columnToBeUpdated.field !== fieldAsString;
        if (!updateField) {
            return this;
        }
        // ensure tableMeta is non-empty
        tableMeta = validateTableMeta(tableMeta);
        const newEventView = this.clone();
        const updatedField = {
            field: fieldAsString,
            width: gridEditable_1.COL_WIDTH_UNDEFINED,
        };
        const fields = [...newEventView.fields];
        fields[columnIndex] = updatedField;
        newEventView.fields = fields;
        // if the updated column is one of the sorted columns, we may need to remove
        // it from the list of sorts
        const needleSortIndex = this.sorts.findIndex(sort => isSortEqualToField(sort, columnToBeUpdated, tableMeta));
        if (needleSortIndex >= 0) {
            const needleSort = this.sorts[needleSortIndex];
            const numOfColumns = this.fields.reduce((sum, currentField) => {
                if (isSortEqualToField(needleSort, currentField, tableMeta)) {
                    return sum + 1;
                }
                return sum;
            }, 0);
            // do not bother deleting the sort key if there are more than one columns
            // of it in the table.
            if (numOfColumns <= 1) {
                if (isFieldSortable(updatedField, tableMeta)) {
                    // use the current updated field as the sort key
                    const sort = fieldToSort(updatedField, tableMeta);
                    // preserve the sort kind
                    sort.kind = needleSort.kind;
                    const sorts = [...newEventView.sorts];
                    sorts[needleSortIndex] = sort;
                    newEventView.sorts = sorts;
                }
                else {
                    const sorts = [...newEventView.sorts];
                    sorts.splice(needleSortIndex, 1);
                    newEventView.sorts = [...new Set(sorts)];
                }
            }
            if (newEventView.sorts.length <= 0 && newEventView.fields.length > 0) {
                // establish a default sort by finding the first sortable field
                if (isFieldSortable(updatedField, tableMeta)) {
                    // use the current updated field as the sort key
                    const sort = fieldToSort(updatedField, tableMeta);
                    // preserve the sort kind
                    sort.kind = needleSort.kind;
                    newEventView.sorts = [sort];
                }
                else {
                    const sortableFieldIndex = newEventView.fields.findIndex(currentField => isFieldSortable(currentField, tableMeta));
                    if (sortableFieldIndex >= 0) {
                        const fieldToBeSorted = newEventView.fields[sortableFieldIndex];
                        const sort = fieldToSort(fieldToBeSorted, tableMeta);
                        newEventView.sorts = [sort];
                    }
                }
            }
        }
        newEventView.yAxis = newEventView.getYAxis();
        return newEventView;
    }
    withDeletedColumn(columnIndex, tableMeta) {
        // Disallow removal of the orphan column, and check for out-of-bounds
        if (this.fields.length <= 1 || this.fields.length <= columnIndex || columnIndex < 0) {
            return this;
        }
        // ensure tableMeta is non-empty
        tableMeta = validateTableMeta(tableMeta);
        // delete the column
        const newEventView = this.clone();
        const fields = [...newEventView.fields];
        fields.splice(columnIndex, 1);
        newEventView.fields = fields;
        // Ensure there is at least one auto width column
        // To ensure a well formed table results.
        const hasAutoIndex = fields.find(field => field.width === gridEditable_1.COL_WIDTH_UNDEFINED);
        if (!hasAutoIndex) {
            newEventView.fields[0].width = gridEditable_1.COL_WIDTH_UNDEFINED;
        }
        // if the deleted column is one of the sorted columns, we need to remove
        // it from the list of sorts
        const columnToBeDeleted = this.fields[columnIndex];
        const needleSortIndex = this.sorts.findIndex(sort => isSortEqualToField(sort, columnToBeDeleted, tableMeta));
        if (needleSortIndex >= 0) {
            const needleSort = this.sorts[needleSortIndex];
            const numOfColumns = this.fields.reduce((sum, field) => {
                if (isSortEqualToField(needleSort, field, tableMeta)) {
                    return sum + 1;
                }
                return sum;
            }, 0);
            // do not bother deleting the sort key if there are more than one columns
            // of it in the table.
            if (numOfColumns <= 1) {
                const sorts = [...newEventView.sorts];
                sorts.splice(needleSortIndex, 1);
                newEventView.sorts = [...new Set(sorts)];
                if (newEventView.sorts.length <= 0 && newEventView.fields.length > 0) {
                    // establish a default sort by finding the first sortable field
                    const sortableFieldIndex = newEventView.fields.findIndex(field => isFieldSortable(field, tableMeta));
                    if (sortableFieldIndex >= 0) {
                        const fieldToBeSorted = newEventView.fields[sortableFieldIndex];
                        const sort = fieldToSort(fieldToBeSorted, tableMeta);
                        newEventView.sorts = [sort];
                    }
                }
            }
        }
        newEventView.yAxis = newEventView.getYAxis();
        return newEventView;
    }
    withTeams(teams) {
        const newEventView = this.clone();
        newEventView.team = teams;
        return newEventView;
    }
    getSorts() {
        return this.sorts.map(sort => ({
            key: sort.field,
            order: sort.kind,
        }));
    }
    // returns query input for the search
    getQuery(inputQuery) {
        const queryParts = [];
        if (this.query) {
            if (this.additionalConditions) {
                queryParts.push(this.getQueryWithAdditionalConditions());
            }
            else {
                queryParts.push(this.query);
            }
        }
        if (inputQuery) {
            // there may be duplicate query in the query string
            // e.g. query=hello&query=world
            if (Array.isArray(inputQuery)) {
                inputQuery.forEach(query => {
                    if (typeof query === 'string' && !queryParts.includes(query)) {
                        queryParts.push(query);
                    }
                });
            }
            if (typeof inputQuery === 'string' && !queryParts.includes(inputQuery)) {
                queryParts.push(inputQuery);
            }
        }
        return queryParts.join(' ');
    }
    getFacetsAPIPayload(location) {
        const payload = this.getEventsAPIPayload(location);
        const remove = [
            'id',
            'name',
            'per_page',
            'sort',
            'cursor',
            'field',
            'equation',
            'interval',
        ];
        for (const key of remove) {
            delete payload[key];
        }
        return payload;
    }
    normalizeDateSelection(location) {
        const query = (location && location.query) || {};
        // pick only the query strings that we care about
        const picked = pickRelevantLocationQueryStrings(location);
        const hasDateSelection = this.statsPeriod || (this.start && this.end);
        // an eventview's date selection has higher precedence than the date selection in the query string
        const dateSelection = hasDateSelection
            ? {
                start: this.start,
                end: this.end,
                statsPeriod: this.statsPeriod,
            }
            : {
                start: picked.start,
                end: picked.end,
                period: (0, queryString_1.decodeScalar)(query.period),
                statsPeriod: picked.statsPeriod,
            };
        // normalize datetime selection
        return (0, getParams_1.getParams)(Object.assign(Object.assign({}, dateSelection), { utc: (0, queryString_1.decodeScalar)(query.utc) }));
    }
    // Takes an EventView instance and converts it into the format required for the events API
    getEventsAPIPayload(location) {
        // pick only the query strings that we care about
        const picked = pickRelevantLocationQueryStrings(location);
        // normalize datetime selection
        const normalizedTimeWindowParams = this.normalizeDateSelection(location);
        const sort = this.sorts.length <= 0
            ? undefined
            : this.sorts.length > 1
                ? encodeSorts(this.sorts)
                : encodeSort(this.sorts[0]);
        const fields = this.getFields();
        const team = this.team.map(proj => String(proj));
        const project = this.project.map(proj => String(proj));
        const environment = this.environment;
        // generate event query
        const eventQuery = Object.assign((0, omit_1.default)(picked, DATETIME_QUERY_STRING_KEYS), normalizedTimeWindowParams, {
            team,
            project,
            environment,
            field: [...new Set(fields)],
            sort,
            per_page: constants_1.DEFAULT_PER_PAGE,
            query: this.getQueryWithAdditionalConditions(),
        });
        if (eventQuery.team && !eventQuery.team.length) {
            delete eventQuery.team;
        }
        if (!eventQuery.sort) {
            delete eventQuery.sort;
        }
        return eventQuery;
    }
    getResultsViewUrlTarget(slug) {
        return {
            pathname: `/organizations/${slug}/discover/results/`,
            query: this.generateQueryStringObject(),
        };
    }
    getResultsViewShortUrlTarget(slug) {
        const output = { id: this.id };
        for (const field of [...Object.values(globalSelectionHeader_1.URL_PARAM), 'cursor']) {
            if (this[field] && this[field].length) {
                output[field] = this[field];
            }
        }
        return {
            pathname: `/organizations/${slug}/discover/results/`,
            query: (0, cloneDeep_1.default)(output),
        };
    }
    getPerformanceTransactionEventsViewUrlTarget(slug, options) {
        const { showTransactions, breakdown, webVital } = options;
        const output = {
            sort: encodeSorts(this.sorts),
            project: this.project,
            query: this.query,
            transaction: this.name,
            showTransactions,
            breakdown,
            webVital,
        };
        for (const field of EXTERNAL_QUERY_STRING_KEYS) {
            if (this[field] && this[field].length) {
                output[field] = this[field];
            }
        }
        const query = (0, cloneDeep_1.default)(output);
        return {
            pathname: `/organizations/${slug}/performance/summary/events/`,
            query,
        };
    }
    sortForField(field, tableMeta) {
        if (!tableMeta) {
            return undefined;
        }
        return this.sorts.find(sort => isSortEqualToField(sort, field, tableMeta));
    }
    sortOnField(field, tableMeta, kind) {
        // check if field can be sorted
        if (!isFieldSortable(field, tableMeta)) {
            return this;
        }
        const needleIndex = this.sorts.findIndex(sort => isSortEqualToField(sort, field, tableMeta));
        if (needleIndex >= 0) {
            const newEventView = this.clone();
            const currentSort = this.sorts[needleIndex];
            const sorts = [...newEventView.sorts];
            sorts[needleIndex] = kind
                ? setSortOrder(currentSort, kind)
                : reverseSort(currentSort);
            newEventView.sorts = sorts;
            return newEventView;
        }
        // field is currently not sorted; so, we sort on it
        const newEventView = this.clone();
        // invariant: this is not falsey, since sortKey exists
        const sort = fieldToSort(field, tableMeta, kind);
        newEventView.sorts = [sort];
        return newEventView;
    }
    getYAxisOptions() {
        // Make option set and add the default options in.
        return (0, uniqBy_1.default)(this.getAggregateFields()
            // Only include aggregates that make sense to be graphable (eg. not string or date)
            .filter((field) => (0, fields_1.isLegalYAxisType)((0, fields_1.aggregateOutputType)(field.field)) ||
            (0, fields_1.isAggregateEquation)(field.field))
            .map((field) => ({
            label: (0, fields_1.isEquation)(field.field) ? (0, fields_1.getEquation)(field.field) : field.field,
            value: field.field,
        }))
            .concat(types_1.CHART_AXIS_OPTIONS), 'value');
    }
    getYAxis() {
        const yAxisOptions = this.getYAxisOptions();
        const yAxis = this.yAxis;
        const defaultOption = yAxisOptions[0].value;
        if (!yAxis) {
            return defaultOption;
        }
        // ensure current selected yAxis is one of the items in yAxisOptions
        const result = yAxisOptions.findIndex((option) => option.value === yAxis);
        if (result >= 0) {
            return yAxis;
        }
        return defaultOption;
    }
    getDisplayOptions() {
        return types_1.DISPLAY_MODE_OPTIONS.map(item => {
            if (item.value === types_1.DisplayModes.PREVIOUS) {
                if (this.start || this.end) {
                    return Object.assign(Object.assign({}, item), { disabled: true });
                }
            }
            if (item.value === types_1.DisplayModes.TOP5 || item.value === types_1.DisplayModes.DAILYTOP5) {
                if (this.getAggregateFields().length === 0) {
                    return Object.assign(Object.assign({}, item), { disabled: true, tooltip: (0, locale_1.t)('Add a function that groups events to use this view.') });
                }
            }
            if (item.value === types_1.DisplayModes.DAILY || item.value === types_1.DisplayModes.DAILYTOP5) {
                if (this.getDays() < 1) {
                    return Object.assign(Object.assign({}, item), { disabled: true, tooltip: (0, locale_1.t)('Change the date rage to at least 1 day to use this view.') });
                }
            }
            return item;
        });
    }
    getDisplayMode() {
        var _a;
        const mode = (_a = this.display) !== null && _a !== void 0 ? _a : types_1.DisplayModes.DEFAULT;
        const displayOptions = this.getDisplayOptions();
        let display = Object.values(types_1.DisplayModes).includes(mode)
            ? mode
            : types_1.DisplayModes.DEFAULT;
        const cond = option => option.value === display;
        // Just in case we define a fallback chain that results in an infinite loop.
        // The number 5 isn't anything special, its just larger than the longest fallback
        // chain that exists and isn't too big.
        for (let i = 0; i < 5; i++) {
            const selectedOption = displayOptions.find(cond);
            if (selectedOption && !selectedOption.disabled) {
                return display;
            }
            display = types_1.DISPLAY_MODE_FALLBACK_OPTIONS[display];
        }
        // after trying to find an enabled display mode and failing to find one,
        // we just use the default display mode
        return types_1.DisplayModes.DEFAULT;
    }
    getQueryWithAdditionalConditions() {
        const { query } = this;
        if (this.additionalConditions.isEmpty()) {
            return query;
        }
        const conditions = new tokenizeSearch_1.MutableSearch(query);
        Object.entries(this.additionalConditions.filters).forEach(([tag, tagValues]) => {
            const existingTagValues = conditions.getFilterValues(tag);
            const newTagValues = tagValues.filter(tagValue => !existingTagValues.includes(tagValue));
            if (newTagValues.length) {
                conditions.addFilterValues(tag, newTagValues);
            }
        });
        return conditions.formatString();
    }
}
const isFieldsSimilar = (currentValue, otherValue) => {
    // For equation's their order matters because we alias them based on index
    const currentEquations = currentValue.filter(fields_1.isEquation);
    const otherEquations = otherValue.filter(fields_1.isEquation);
    // Field orders don't matter, so using a set for comparison
    const currentFields = new Set(currentValue.filter(value => !(0, fields_1.isEquation)(value)));
    const otherFields = new Set(otherValue.filter(value => !(0, fields_1.isEquation)(value)));
    if (!(0, isEqual_1.default)(currentEquations, otherEquations)) {
        return false;
    }
    else if (!(0, isEqual_1.default)(currentFields, otherFields)) {
        return false;
    }
    return true;
};
const isAPIPayloadSimilar = (current, other) => {
    const currentKeys = new Set(Object.keys(current));
    const otherKeys = new Set(Object.keys(other));
    if (!(0, isEqual_1.default)(currentKeys, otherKeys)) {
        return false;
    }
    for (const key of currentKeys) {
        const currentValue = current[key];
        const otherValue = other[key];
        if (key === 'field') {
            if (!isFieldsSimilar(currentValue, otherValue)) {
                return false;
            }
        }
        else {
            const currentTarget = Array.isArray(currentValue)
                ? new Set(currentValue)
                : currentValue;
            const otherTarget = Array.isArray(otherValue) ? new Set(otherValue) : otherValue;
            if (!(0, isEqual_1.default)(currentTarget, otherTarget)) {
                return false;
            }
        }
    }
    return true;
};
exports.isAPIPayloadSimilar = isAPIPayloadSimilar;
function pickRelevantLocationQueryStrings(location) {
    const query = location.query || {};
    const picked = (0, pick_1.default)(query || {}, EXTERNAL_QUERY_STRING_KEYS);
    return picked;
}
exports.pickRelevantLocationQueryStrings = pickRelevantLocationQueryStrings;
exports.default = EventView;
//# sourceMappingURL=eventView.jsx.map