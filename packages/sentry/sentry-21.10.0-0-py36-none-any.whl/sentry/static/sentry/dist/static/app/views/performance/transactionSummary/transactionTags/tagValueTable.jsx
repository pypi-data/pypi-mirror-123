Object.defineProperty(exports, "__esModule", { value: true });
exports.TagValueTable = void 0;
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const gridEditable_1 = (0, tslib_1.__importStar)(require("app/components/gridEditable"));
const sortLink_1 = (0, tslib_1.__importDefault)(require("app/components/gridEditable/sortLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const iconAdd_1 = require("app/icons/iconAdd");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fields_1 = require("app/utils/discover/fields");
const formatters_1 = require("app/utils/formatters");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const cellAction_1 = (0, tslib_1.__importStar)(require("app/views/eventsV2/table/cellAction"));
const utils_1 = require("../../utils");
const tagExplorer_1 = require("../transactionOverview/tagExplorer");
const tagsDisplay_1 = require("./tagsDisplay");
const utils_2 = require("./utils");
const TAGS_CURSOR_NAME = 'tags_cursor';
class TagValueTable extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            widths: [],
        };
        this.renderHeadCellWithMeta = (sortedEventView, tableMeta, columns) => {
            return (column, index) => this.renderHeadCell(sortedEventView, tableMeta, column, columns[index]);
        };
        this.handleTagValueClick = (location, tagKey, tagValue) => {
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
                (0, utils_2.trackTagPageInteraction)(organization);
                const searchConditions = new tokenizeSearch_1.MutableSearch(eventView.query);
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
            const { location, eventView, organization } = parentProps;
            if (column.key === 'key') {
                return dataRow.tags_key;
            }
            const allowActions = [cellAction_1.Actions.ADD, cellAction_1.Actions.EXCLUDE];
            if (column.key === 'tagValue') {
                const actionRow = Object.assign(Object.assign({}, dataRow), { id: dataRow.tags_key });
                return (<cellAction_1.default column={column} dataRow={actionRow} handleCellAction={this.handleCellAction(column, dataRow.tags_value, actionRow)} allowActions={allowActions}>
          <tagExplorer_1.TagValue row={dataRow}/>
        </cellAction_1.default>);
            }
            if (column.key === 'frequency') {
                return <AlignRight>{(0, formatters_1.formatPercentage)(dataRow.frequency, 0)}</AlignRight>;
            }
            if (column.key === 'action') {
                const searchConditions = new tokenizeSearch_1.MutableSearch(eventView.query);
                const disabled = searchConditions.hasFilter(dataRow.tags_key);
                return (<link_1.default disabled={disabled} to="" onClick={() => {
                        (0, utils_2.trackTagPageInteraction)(organization);
                        this.handleTagValueClick(location, dataRow.tags_key, dataRow.tags_value);
                    }}>
          <LinkContainer>
            <iconAdd_1.IconAdd isCircled/>
            {(0, locale_1.t)('Add to filter')}
          </LinkContainer>
        </link_1.default>);
            }
            if (column.key === 'comparison') {
                const localValue = dataRow.comparison;
                const pct = (0, formatters_1.formatPercentage)(localValue - 1, 0);
                return localValue > 1 ? (0, locale_1.t)('+%s slower', pct) : (0, locale_1.t)('%s faster', pct);
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
            if (column.key === 'count') {
                return <AlignRight>{value}</AlignRight>;
            }
            return value;
        };
        this.renderBodyCellWithData = (parentProps) => {
            return (column, dataRow) => this.renderBodyCell(parentProps, column, dataRow);
        };
        this.handleResizeColumn = (columnIndex, nextColumn) => {
            const widths = [...this.state.widths];
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : gridEditable_1.COL_WIDTH_UNDEFINED;
            this.setState({ widths });
        };
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
        const currentSortKind = currentSort ? currentSort.kind : undefined;
        return (<sortLink_1.default align={align} title={columnInfo.name} direction={currentSortKind} canSort generateSortLink={generateSortLink}/>);
    }
    render() {
        const { eventView, tagKey, location, isLoading, tableData, aggregateColumn, pageLinks, onCursor, } = this.props;
        const newColumns = [...tagsDisplay_1.TAGS_TABLE_COLUMN_ORDER].map(c => {
            const newColumn = Object.assign({}, c);
            if (c.key === 'tagValue' && tagKey) {
                newColumn.name = tagKey;
            }
            if (c.key === 'aggregate') {
                if (aggregateColumn === 'measurements.lcp') {
                    newColumn.name = 'Avg LCP';
                }
            }
            return newColumn;
        });
        return (<StyledPanelTable>
        <gridEditable_1.default isLoading={isLoading} data={tableData && tableData.data ? tableData.data : []} columnOrder={newColumns} columnSortBy={[]} grid={{
                renderHeadCell: this.renderHeadCellWithMeta(eventView, tableData ? tableData.meta : {}, newColumns),
                renderBodyCell: this.renderBodyCellWithData(this.props),
                onResizeColumn: this.handleResizeColumn,
            }} location={location}/>

        <pagination_1.default pageLinks={pageLinks} onCursor={onCursor} size="small"/>
      </StyledPanelTable>);
    }
}
exports.TagValueTable = TagValueTable;
const StyledPanelTable = (0, styled_1.default)('div') `
  > div {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }
`;
const AlignRight = (0, styled_1.default)('div') `
  text-align: right;
`;
const LinkContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(0.5)};
  justify-content: flex-end;
  align-items: center;
`;
exports.default = TagValueTable;
//# sourceMappingURL=tagValueTable.jsx.map