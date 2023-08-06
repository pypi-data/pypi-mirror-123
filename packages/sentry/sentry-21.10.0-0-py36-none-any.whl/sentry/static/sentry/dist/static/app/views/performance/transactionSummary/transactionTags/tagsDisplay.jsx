Object.defineProperty(exports, "__esModule", { value: true });
exports.TAGS_TABLE_COLUMN_ORDER = void 0;
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const react_router_1 = require("react-router");
const eventView_1 = require("app/utils/discover/eventView");
const segmentExplorerQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/segmentExplorer/segmentExplorerQuery"));
const tagKeyHistogramQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/segmentExplorer/tagKeyHistogramQuery"));
const queryString_1 = require("app/utils/queryString");
const filter_1 = require("../filter");
const tagExplorer_1 = require("../transactionOverview/tagExplorer");
const tagsHeatMap_1 = (0, tslib_1.__importDefault)(require("./tagsHeatMap"));
const tagValueTable_1 = require("./tagValueTable");
const utils_1 = require("./utils");
const HISTOGRAM_TAG_KEY_LIMIT = 8;
const HISTOGRAM_BUCKET_LIMIT = 40;
const TAG_PAGE_TABLE_CURSOR = 'tableCursor';
exports.TAGS_TABLE_COLUMN_ORDER = [
    {
        key: 'tagValue',
        field: 'tagValue',
        name: 'Tag Values',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'frequency',
        field: 'frequency',
        name: 'Frequency',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'count',
        field: 'count',
        name: 'Events',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'aggregate',
        field: 'aggregate',
        name: 'Avg Duration',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'action',
        field: 'action',
        name: '',
        width: -1,
        column: {
            kind: 'field',
        },
    },
];
const TagsDisplay = (props) => {
    var _a;
    const { eventView: _eventView, location, organization, projects, tagKey } = props;
    const eventView = _eventView.clone();
    const aggregateColumn = (0, tagExplorer_1.getTransactionField)(filter_1.SpanOperationBreakdownFilter.None, projects, eventView);
    const handleCursor = (cursor, pathname, query) => react_router_1.browserHistory.push({
        pathname,
        query: Object.assign(Object.assign({}, query), { [TAG_PAGE_TABLE_CURSOR]: cursor }),
    });
    const cursor = (0, queryString_1.decodeScalar)((_a = location.query) === null || _a === void 0 ? void 0 : _a[TAG_PAGE_TABLE_CURSOR]);
    const tagSort = (0, utils_1.getTagSortForTagsPage)(location);
    const tagSorts = (0, eventView_1.fromSorts)(tagSort);
    eventView.fields = exports.TAGS_TABLE_COLUMN_ORDER;
    const sortedEventView = eventView.withSorts(tagSorts.length
        ? tagSorts
        : [
            {
                field: 'frequency',
                kind: 'desc',
            },
        ]);
    return (<react_1.default.Fragment>
      {tagKey ? (<react_1.default.Fragment>
          <tagKeyHistogramQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} numBucketsPerKey={HISTOGRAM_BUCKET_LIMIT} tagKey={tagKey} limit={HISTOGRAM_TAG_KEY_LIMIT} cursor={cursor} sort={tagSort !== null && tagSort !== void 0 ? tagSort : '-sumdelta'}>
            {({ isLoading, tableData }) => {
                return (<tagsHeatMap_1.default {...props} tagKey={tagKey} aggregateColumn={aggregateColumn} tableData={tableData} isLoading={isLoading}/>);
            }}
          </tagKeyHistogramQuery_1.default>
          <segmentExplorerQuery_1.default eventView={sortedEventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} tagKey={tagKey} limit={HISTOGRAM_TAG_KEY_LIMIT} cursor={cursor} sort={tagSort} allTagKeys>
            {({ isLoading, tableData, pageLinks }) => {
                return (<tagValueTable_1.TagValueTable {...props} eventView={sortedEventView} tagKey={tagKey} aggregateColumn={aggregateColumn} pageLinks={pageLinks} tableData={tableData} isLoading={isLoading} onCursor={handleCursor}/>);
            }}
          </segmentExplorerQuery_1.default>
        </react_1.default.Fragment>) : (<react_1.default.Fragment>
          <tagsHeatMap_1.default {...props} aggregateColumn={aggregateColumn} tableData={null} isLoading={false}/>
          <tagValueTable_1.TagValueTable {...props} pageLinks={null} aggregateColumn={aggregateColumn} tableData={null} isLoading={false}/>
        </react_1.default.Fragment>)}
    </react_1.default.Fragment>);
};
exports.default = TagsDisplay;
//# sourceMappingURL=tagsDisplay.jsx.map