Object.defineProperty(exports, "__esModule", { value: true });
exports.TagExplorer = exports.TagValue = exports.getTransactionField = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const guideAnchor_1 = require("app/components/assistant/guideAnchor");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const styles_1 = require("app/components/charts/styles");
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const gridEditable_1 = (0, tslib_1.__importStar)(require("app/components/gridEditable"));
const sortLink_1 = (0, tslib_1.__importDefault)(require("app/components/gridEditable/sortLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const eventView_1 = require("app/utils/discover/eventView");
const fields_1 = require("app/utils/discover/fields");
const formatters_1 = require("app/utils/formatters");
const segmentExplorerQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/segmentExplorer/segmentExplorerQuery"));
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const cellAction_1 = (0, tslib_1.__importStar)(require("app/views/eventsV2/table/cellAction"));
const utils_1 = require("../../utils");
const filter_1 = require("../filter");
const utils_2 = require("../transactionTags/utils");
const TAGS_CURSOR_NAME = 'tags_cursor';
const COLUMN_ORDER = [
    {
        key: 'key',
        field: 'key',
        name: 'Tag Key',
        width: -1,
        column: {
            kind: 'field',
        },
    },
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
        key: 'comparison',
        field: 'comparison',
        name: 'Compared To Avg',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'sumdelta',
        field: 'sumdelta',
        name: 'Total Time Lost',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
];
const filterToField = {
    [filter_1.SpanOperationBreakdownFilter.Browser]: 'spans.browser',
    [filter_1.SpanOperationBreakdownFilter.Http]: 'spans.http',
    [filter_1.SpanOperationBreakdownFilter.Db]: 'spans.db',
    [filter_1.SpanOperationBreakdownFilter.Resource]: 'spans.resource',
};
const getTransactionField = (currentFilter, projects, eventView) => {
    const fieldFromFilter = filterToField[currentFilter];
    if (fieldFromFilter) {
        return fieldFromFilter;
    }
    const performanceType = (0, utils_1.platformAndConditionsToPerformanceType)(projects, eventView);
    if (performanceType === utils_1.PROJECT_PERFORMANCE_TYPE.FRONTEND) {
        return 'measurements.lcp';
    }
    return 'transaction.duration';
};
exports.getTransactionField = getTransactionField;
const getColumnsWithReplacedDuration = (currentFilter, projects, eventView) => {
    const columns = COLUMN_ORDER.map(c => (Object.assign({}, c)));
    const durationColumn = columns.find(c => c.key === 'aggregate');
    if (!durationColumn) {
        return columns;
    }
    const fieldFromFilter = filterToField[currentFilter];
    if (fieldFromFilter) {
        durationColumn.name = 'Avg Span Duration';
        return columns;
    }
    const performanceType = (0, utils_1.platformAndConditionsToPerformanceType)(projects, eventView);
    if (performanceType === utils_1.PROJECT_PERFORMANCE_TYPE.FRONTEND) {
        durationColumn.name = 'Avg LCP';
        return columns;
    }
    return columns;
};
function TagValue(props) {
    return <div className="truncate">{props.row.tags_value}</div>;
}
exports.TagValue = TagValue;
class _TagExplorer extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            widths: [],
        };
        this.handleResizeColumn = (columnIndex, nextColumn) => {
            const widths = [...this.state.widths];
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : gridEditable_1.COL_WIDTH_UNDEFINED;
            this.setState({ widths });
        };
        this.getColumnOrder = (columns) => {
            const { widths } = this.state;
            return columns.map((col, i) => {
                if (typeof widths[i] === 'number') {
                    return Object.assign(Object.assign({}, col), { width: widths[i] });
                }
                return col;
            });
        };
        this.renderHeadCellWithMeta = (sortedEventView, tableMeta, columns) => {
            return (column, index) => this.renderHeadCell(sortedEventView, tableMeta, column, columns[index]);
        };
        this.handleTagValueClick = (location, tagKey, tagValue) => {
            const { organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.summary.tag_explorer.tag_value',
                eventName: 'Performance Views: Tag Explorer Value Clicked',
                organization_id: parseInt(organization.id, 10),
            });
            const queryString = (0, queryString_1.decodeScalar)(location.query.query);
            const conditions = new tokenizeSearch_1.MutableSearch(queryString !== null && queryString !== void 0 ? queryString : '');
            conditions.addFilterValues(tagKey, [tagValue]);
            const query = conditions.formatString();
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { query: String(query).trim() }),
            });
        };
        this.handleCellAction = (column, tagValue, actionRow) => {
            return (action) => {
                const { eventView, location, organization } = this.props;
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'performance_views.summary.tag_explorer.cell_action',
                    eventName: 'Performance Views: Tag Explorer Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                });
                const searchConditions = new tokenizeSearch_1.MutableSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeFilter('event.type');
                (0, cellAction_1.updateQuery)(searchConditions, action, Object.assign(Object.assign({}, column), { name: actionRow.id }), tagValue);
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: Object.assign(Object.assign({}, location.query), { [TAGS_CURSOR_NAME]: undefined, query: searchConditions.formatString() }),
                });
            };
        };
        this.renderBodyCell = (parentProps, column, dataRow) => {
            const value = dataRow[column.key];
            const { location, organization, transactionName } = parentProps;
            if (column.key === 'key') {
                const target = (0, utils_2.tagsRouteWithQuery)({
                    orgSlug: organization.slug,
                    transaction: transactionName,
                    projectID: (0, queryString_1.decodeScalar)(location.query.project),
                    query: Object.assign(Object.assign({}, location.query), { tagKey: dataRow.tags_key }),
                });
                return (<feature_1.default features={['performance-tag-page']} organization={organization}>
          {({ hasFeature }) => {
                        if (hasFeature) {
                            return (<link_1.default to={target} onClick={() => this.onTagKeyClick()}>
                  {dataRow.tags_key}
                </link_1.default>);
                        }
                        return dataRow.tags_key;
                    }}
        </feature_1.default>);
            }
            const allowActions = [cellAction_1.Actions.ADD, cellAction_1.Actions.EXCLUDE];
            if (column.key === 'tagValue') {
                const actionRow = Object.assign(Object.assign({}, dataRow), { id: dataRow.tags_key });
                return (<cellAction_1.default column={column} dataRow={actionRow} handleCellAction={this.handleCellAction(column, dataRow.tags_value, actionRow)} allowActions={allowActions}>
          <feature_1.default features={['performance-tag-page']} organization={organization}>
            {({ hasFeature }) => {
                        if (hasFeature) {
                            return <div className="truncate">{dataRow.tags_value}</div>;
                        }
                        return (<link_1.default to="" onClick={() => this.handleTagValueClick(location, dataRow.tags_key, dataRow.tags_value)}>
                  <TagValue row={dataRow}/>
                </link_1.default>);
                    }}
          </feature_1.default>
        </cellAction_1.default>);
            }
            if (column.key === 'frequency') {
                return <AlignRight>{(0, formatters_1.formatPercentage)(dataRow.frequency, 0)}</AlignRight>;
            }
            if (column.key === 'comparison') {
                const localValue = dataRow.comparison;
                const pct = (0, formatters_1.formatPercentage)(localValue - 1, 0);
                return (<AlignRight>
          {localValue > 1 ? (0, locale_1.t)('+%s slower', pct) : (0, locale_1.t)('%s faster', pct)}
        </AlignRight>);
            }
            if (column.key === 'aggregate') {
                return (<AlignRight>
          <utils_1.PerformanceDuration abbreviation milliseconds={dataRow.aggregate}/>
        </AlignRight>);
            }
            if (column.key === 'sumdelta') {
                return (<AlignRight>
          <utils_1.PerformanceDuration abbreviation milliseconds={dataRow.sumdelta}/>
        </AlignRight>);
            }
            return value;
        };
        this.renderBodyCellWithData = (parentProps) => {
            return (column, dataRow) => this.renderBodyCell(parentProps, column, dataRow);
        };
    }
    onSortClick(currentSortKind, currentSortField) {
        const { organization } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance_views.summary.tag_explorer.sort',
            eventName: 'Performance Views: Tag Explorer Sorted',
            organization_id: parseInt(organization.id, 10),
            field: currentSortField,
            direction: currentSortKind,
        });
    }
    renderHeadCell(sortedEventView, tableMeta, column, columnInfo) {
        const { location } = this.props;
        const align = (0, fields_1.fieldAlignment)(column.key, column.type, tableMeta);
        const field = { field: column.key, width: column.width };
        function generateSortLink() {
            if (!tableMeta) {
                return undefined;
            }
            const nextEventView = sortedEventView.sortOnField(field, tableMeta);
            const { sort } = nextEventView.generateQueryStringObject();
            return Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { [TAGS_CURSOR_NAME]: undefined, tagSort: sort }) });
        }
        const currentSort = sortedEventView.sortForField(field, tableMeta);
        const canSort = (0, eventView_1.isFieldSortable)(field, tableMeta);
        const currentSortKind = currentSort ? currentSort.kind : undefined;
        const currentSortField = currentSort ? currentSort.field : undefined;
        return (<sortLink_1.default align={align} title={columnInfo.name} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={() => this.onSortClick(currentSortKind, currentSortField)}/>);
    }
    onTagKeyClick() {
        const { organization } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance_views.summary.tag_explorer.visit_tag_key',
            eventName: 'Performance Views: Tag Explorer - Visit Tag Key',
            organization_id: parseInt(organization.id, 10),
        });
    }
    render() {
        var _a, _b;
        const { eventView, organization, location, currentFilter, projects, transactionName } = this.props;
        const tagSort = (0, queryString_1.decodeScalar)((_a = location.query) === null || _a === void 0 ? void 0 : _a.tagSort);
        const cursor = (0, queryString_1.decodeScalar)((_b = location.query) === null || _b === void 0 ? void 0 : _b[TAGS_CURSOR_NAME]);
        const tagEventView = eventView.clone();
        tagEventView.fields = COLUMN_ORDER;
        const tagSorts = (0, eventView_1.fromSorts)(tagSort);
        const sortedEventView = tagEventView.withSorts(tagSorts.length
            ? tagSorts
            : [
                {
                    field: 'sumdelta',
                    kind: 'desc',
                },
            ]);
        const aggregateColumn = (0, exports.getTransactionField)(currentFilter, projects, sortedEventView);
        const adjustedColumns = getColumnsWithReplacedDuration(currentFilter, projects, sortedEventView);
        const columns = this.getColumnOrder(adjustedColumns);
        const columnSortBy = sortedEventView.getSorts();
        return (<segmentExplorerQuery_1.default eventView={sortedEventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} limit={5} cursor={cursor}>
        {({ isLoading, tableData, pageLinks }) => {
                return (<React.Fragment>
              <guideAnchor_1.GuideAnchor target="tag_explorer">
                <TagsHeader transactionName={transactionName} location={location} organization={organization} pageLinks={pageLinks}/>
              </guideAnchor_1.GuideAnchor>
              <gridEditable_1.default isLoading={isLoading} data={tableData && tableData.data ? tableData.data : []} columnOrder={columns} columnSortBy={columnSortBy} grid={{
                        renderHeadCell: this.renderHeadCellWithMeta(sortedEventView, (tableData === null || tableData === void 0 ? void 0 : tableData.meta) || {}, adjustedColumns),
                        renderBodyCell: this.renderBodyCellWithData(this.props),
                        onResizeColumn: this.handleResizeColumn,
                    }} location={location}/>
            </React.Fragment>);
            }}
      </segmentExplorerQuery_1.default>);
    }
}
function TagsHeader(props) {
    const { pageLinks, organization, location, transactionName } = props;
    const handleCursor = (cursor, pathname, query) => {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance_views.summary.tag_explorer.change_page',
            eventName: 'Performance Views: Tag Explorer Change Page',
            organization_id: parseInt(organization.id, 10),
        });
        react_router_1.browserHistory.push({
            pathname,
            query: Object.assign(Object.assign({}, query), { [TAGS_CURSOR_NAME]: cursor }),
        });
    };
    const handleViewAllTagsClick = () => {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance_views.summary.tag_explorer.change_page',
            eventName: 'Performance Views: Tag Explorer Change Page',
            organization_id: parseInt(organization.id, 10),
        });
    };
    const viewAllTarget = (0, utils_2.tagsRouteWithQuery)({
        orgSlug: organization.slug,
        transaction: transactionName,
        projectID: (0, queryString_1.decodeScalar)(location.query.project),
        query: Object.assign({}, location.query),
    });
    return (<Header>
      <div>
        <styles_1.SectionHeading>{(0, locale_1.t)('Suspect Tags')}</styles_1.SectionHeading>
        <featureBadge_1.default type="new"/>
      </div>
      <feature_1.default features={['performance-tag-page']} organization={organization}>
        <button_1.default onClick={handleViewAllTagsClick} to={viewAllTarget} size="small" data-test-id="tags-explorer-open-tags">
          {(0, locale_1.t)('View All Tags')}
        </button_1.default>
      </feature_1.default>
      <StyledPagination pageLinks={pageLinks} onCursor={handleCursor} size="small"/>
    </Header>);
}
const AlignRight = (0, styled_1.default)('div') `
  text-align: right;
  font-variant-numeric: tabular-nums;
`;
const Header = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr auto auto;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const StyledPagination = (0, styled_1.default)(pagination_1.default) `
  margin: 0 0 0 ${(0, space_1.default)(1)};
`;
exports.TagExplorer = _TagExplorer;
//# sourceMappingURL=tagExplorer.jsx.map