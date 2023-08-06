Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const mobx_1 = require("mobx");
const api_1 = require("app/api");
const createFuzzySearch_1 = require("app/utils/createFuzzySearch");
const filter_1 = require("./filter");
const spanTreeModel_1 = (0, tslib_1.__importDefault)(require("./spanTreeModel"));
const utils_1 = require("./utils");
class WaterfallModel {
    constructor(event) {
        this.api = new api_1.Client();
        this.fuse = undefined;
        // readable/writable state
        this.operationNameFilters = filter_1.noFilter;
        this.filterSpans = undefined;
        this.searchQuery = undefined;
        this.toggleOperationNameFilter = (operationName) => {
            this.operationNameFilters = (0, filter_1.toggleFilter)(this.operationNameFilters, operationName);
        };
        this.toggleAllOperationNameFilters = () => {
            const operationNames = Array.from(this.operationNameCounts.keys());
            this.operationNameFilters = (0, filter_1.toggleAllFilters)(this.operationNameFilters, operationNames);
        };
        this.toggleSpanGroup = (spanID) => {
            if (this.hiddenSpanGroups.has(spanID)) {
                this.hiddenSpanGroups.delete(spanID);
                return;
            }
            this.hiddenSpanGroups.add(spanID);
        };
        this.addTraceBounds = (traceBound) => {
            this.traceBounds.push(traceBound);
            this.parsedTrace = Object.assign(Object.assign({}, this.parsedTrace), this.getTraceBounds());
        };
        this.removeTraceBounds = (spanId) => {
            this.traceBounds = this.traceBounds.filter(bound => bound.spanId !== spanId);
            // traceBounds must always be non-empty
            if (this.traceBounds.length === 0) {
                this.traceBounds = [this.rootSpan.generateTraceBounds()];
            }
            this.parsedTrace = Object.assign(Object.assign({}, this.parsedTrace), this.getTraceBounds());
        };
        this.getTraceBounds = () => {
            // traceBounds must always be non-empty
            if (this.traceBounds.length === 0) {
                this.traceBounds = [this.rootSpan.generateTraceBounds()];
            }
            return this.traceBounds.reduce((acc, bounds) => {
                return {
                    traceStartTimestamp: Math.min(acc.traceStartTimestamp, bounds.traceStartTimestamp),
                    traceEndTimestamp: Math.max(acc.traceEndTimestamp, bounds.traceEndTimestamp),
                };
            }, {
                traceStartTimestamp: this.traceBounds[0].traceStartTimestamp,
                traceEndTimestamp: this.traceBounds[0].traceEndTimestamp,
            });
        };
        this.generateBounds = ({ viewStart, viewEnd, }) => {
            return (0, utils_1.boundsGenerator)(Object.assign(Object.assign({}, this.getTraceBounds()), { viewStart,
                viewEnd }));
        };
        this.getWaterfall = ({ viewStart, viewEnd, }) => {
            const generateBounds = this.generateBounds({
                viewStart,
                viewEnd,
            });
            return this.rootSpan.getSpansList({
                operationNameFilters: this.operationNameFilters,
                generateBounds,
                treeDepth: 0,
                isLastSibling: true,
                continuingTreeDepths: [],
                hiddenSpanGroups: this.hiddenSpanGroups,
                spanGroups: new Set(),
                filterSpans: this.filterSpans,
                previousSiblingEndTimestamp: undefined,
                event: this.event,
                isOnlySibling: true,
                spanGrouping: undefined,
                toggleSpanGroup: undefined,
                showSpanGroup: false,
                addTraceBounds: this.addTraceBounds,
                removeTraceBounds: this.removeTraceBounds,
            });
        };
        this.event = event;
        this.parsedTrace = (0, utils_1.parseTrace)(event);
        const rootSpan = (0, utils_1.generateRootSpan)(this.parsedTrace);
        this.rootSpan = new spanTreeModel_1.default(rootSpan, this.parsedTrace.childSpans, this.api, true);
        // Track the trace bounds of the current transaction and the trace bounds of
        // any embedded transactions
        this.traceBounds = [this.rootSpan.generateTraceBounds()];
        this.indexSearch(this.parsedTrace, rootSpan);
        // Set of span IDs whose sub-trees should be hidden. This is used for the
        // span tree toggling product feature.
        this.hiddenSpanGroups = new Set();
        (0, mobx_1.makeObservable)(this, {
            parsedTrace: mobx_1.observable,
            rootSpan: mobx_1.observable,
            // operation names filtering
            operationNameFilters: mobx_1.observable,
            toggleOperationNameFilter: mobx_1.action,
            toggleAllOperationNameFilters: mobx_1.action,
            operationNameCounts: mobx_1.computed.struct,
            // span search
            filterSpans: mobx_1.observable,
            searchQuery: mobx_1.observable,
            querySpanSearch: mobx_1.action,
            // span group toggling
            hiddenSpanGroups: mobx_1.observable,
            toggleSpanGroup: mobx_1.action,
            // trace bounds
            traceBounds: mobx_1.observable,
            addTraceBounds: mobx_1.action,
            removeTraceBounds: mobx_1.action,
        });
    }
    isEvent(otherEvent) {
        return (0, isEqual_1.default)(this.event, otherEvent);
    }
    get operationNameCounts() {
        return this.rootSpan.operationNameCounts;
    }
    indexSearch(parsedTrace, rootSpan) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.filterSpans = undefined;
            this.searchQuery = undefined;
            const { spans } = parsedTrace;
            const transformed = [rootSpan, ...spans].map((span) => {
                var _a;
                const indexed = [];
                // basic properties
                const pickedSpan = (0, pick_1.default)(span, [
                    // TODO: do we want this?
                    // 'trace_id',
                    'span_id',
                    'start_timestamp',
                    'timestamp',
                    'op',
                    'description',
                ]);
                const basicValues = Object.values(pickedSpan)
                    .filter(value => !!value)
                    .map(value => String(value));
                indexed.push(...basicValues);
                // tags
                let tagKeys = [];
                let tagValues = [];
                const tags = span === null || span === void 0 ? void 0 : span.tags;
                if (tags) {
                    tagKeys = Object.keys(tags);
                    tagValues = Object.values(tags);
                }
                const data = (_a = span === null || span === void 0 ? void 0 : span.data) !== null && _a !== void 0 ? _a : {};
                let dataKeys = [];
                let dataValues = [];
                if (data) {
                    dataKeys = Object.keys(data);
                    dataValues = Object.values(data).map(value => JSON.stringify(value, null, 4) || '');
                }
                return {
                    span,
                    indexed,
                    tagKeys,
                    tagValues,
                    dataKeys,
                    dataValues,
                };
            });
            this.fuse = yield (0, createFuzzySearch_1.createFuzzySearch)(transformed, {
                keys: ['indexed', 'tagKeys', 'tagValues', 'dataKeys', 'dataValues'],
                includeMatches: false,
                threshold: 0.6,
                location: 0,
                distance: 100,
                maxPatternLength: 32,
            });
        });
    }
    querySpanSearch(searchQuery) {
        if (!searchQuery) {
            // reset
            if (this.filterSpans !== undefined) {
                this.filterSpans = undefined;
                this.searchQuery = undefined;
            }
            return;
        }
        if (!this.fuse) {
            return;
        }
        const results = this.fuse.search(searchQuery);
        const spanIDs = results.reduce((setOfSpanIDs, result) => {
            const spanID = (0, utils_1.getSpanID)(result.item.span);
            if (spanID) {
                setOfSpanIDs.add(spanID);
            }
            return setOfSpanIDs;
        }, new Set());
        this.searchQuery = searchQuery;
        this.filterSpans = {
            results,
            spanIDs,
        };
    }
}
exports.default = WaterfallModel;
//# sourceMappingURL=waterfallModel.jsx.map