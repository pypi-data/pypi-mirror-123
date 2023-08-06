Object.defineProperty(exports, "__esModule", { value: true });
exports.getProjectID = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const gridEditable_1 = (0, tslib_1.__importStar)(require("app/components/gridEditable"));
const sortLink_1 = (0, tslib_1.__importDefault)(require("app/components/gridEditable/sortLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const eventView_1 = require("app/utils/discover/eventView");
const fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
const fields_1 = require("app/utils/discover/fields");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const cellAction_1 = (0, tslib_1.__importStar)(require("app/views/eventsV2/table/cellAction"));
const data_1 = require("../../data");
const utils_2 = require("../utils");
const operationSort_1 = (0, tslib_1.__importDefault)(require("./operationSort"));
function getProjectID(eventData, projects) {
    const projectSlug = (eventData === null || eventData === void 0 ? void 0 : eventData.project) || undefined;
    if (typeof projectSlug === undefined) {
        return undefined;
    }
    const project = projects.find(currentProject => currentProject.slug === projectSlug);
    if (!project) {
        return undefined;
    }
    return project.id;
}
exports.getProjectID = getProjectID;
class OperationTitle extends React.Component {
    render() {
        const { onClick } = this.props;
        return (<div onClick={onClick}>
        <span>{(0, locale_1.t)('operation duration')}</span>
        <StyledIconQuestion size="xs" position="top" title={(0, locale_1.t)(`Span durations are summed over the course of an entire transaction. Any overlapping spans are only counted once.`)}/>
      </div>);
    }
}
class EventsTable extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            widths: [],
        };
        this.handleCellAction = (column) => {
            return (action, value) => {
                const { eventView, location, organization } = this.props;
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'performance_views.transactionEvents.cellaction',
                    eventName: 'Performance Views: Transaction Events Tab Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action,
                });
                const searchConditions = new tokenizeSearch_1.MutableSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeFilter('event.type');
                (0, cellAction_1.updateQuery)(searchConditions, action, column, value);
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: Object.assign(Object.assign({}, location.query), { cursor: undefined, query: searchConditions.formatString() }),
                });
            };
        };
        this.renderBodyCellWithData = (tableData) => {
            return (column, dataRow) => this.renderBodyCell(tableData, column, dataRow);
        };
        this.renderHeadCellWithMeta = (tableMeta) => {
            var _a;
            const columnTitles = (_a = this.props.columnTitles) !== null && _a !== void 0 ? _a : data_1.COLUMN_TITLES;
            return (column, index) => this.renderHeadCell(tableMeta, column, columnTitles[index]);
        };
        this.handleResizeColumn = (columnIndex, nextColumn) => {
            const widths = [...this.state.widths];
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : gridEditable_1.COL_WIDTH_UNDEFINED;
            this.setState({ widths });
        };
    }
    renderBodyCell(tableData, column, dataRow) {
        const { eventView, organization, location, transactionName } = this.props;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        const tableMeta = tableData.meta;
        const field = String(column.key);
        const fieldRenderer = (0, fieldRenderers_1.getFieldRenderer)(field, tableMeta);
        const rendered = fieldRenderer(dataRow, { organization, location, eventView });
        const allowActions = [
            cellAction_1.Actions.ADD,
            cellAction_1.Actions.EXCLUDE,
            cellAction_1.Actions.SHOW_GREATER_THAN,
            cellAction_1.Actions.SHOW_LESS_THAN,
        ];
        if (field === 'id' || field === 'trace') {
            const generateLink = field === 'id' ? utils_2.generateTransactionLink : utils_2.generateTraceLink;
            const target = generateLink(transactionName)(organization, dataRow, location.query);
            return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
          <link_1.default to={target}>{rendered}</link_1.default>
        </cellAction_1.default>);
        }
        const fieldName = (0, fields_1.getAggregateAlias)(field);
        const value = dataRow[fieldName];
        if (tableMeta[fieldName] === 'integer' && (0, utils_1.defined)(value) && value > 999) {
            return (<tooltip_1.default title={value.toLocaleString()} containerDisplayMode="block" position="right">
          <cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
            {rendered}
          </cellAction_1.default>
        </tooltip_1.default>);
        }
        return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
        {rendered}
      </cellAction_1.default>);
    }
    onSortClick(currentSortKind, currentSortField) {
        const { organization } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance_views.transactionEvents.sort',
            eventName: 'Performance Views: Transaction Events Tab Sorted',
            organization_id: parseInt(organization.id, 10),
            field: currentSortField,
            direction: currentSortKind,
        });
    }
    renderHeadCell(tableMeta, column, title) {
        const { eventView, location } = this.props;
        const align = (0, fields_1.fieldAlignment)(column.name, column.type, tableMeta);
        const field = { field: column.name, width: column.width };
        function generateSortLink() {
            if (!tableMeta) {
                return undefined;
            }
            const nextEventView = eventView.sortOnField(field, tableMeta);
            const queryStringObject = nextEventView.generateQueryStringObject();
            return Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { sort: queryStringObject.sort }) });
        }
        const currentSort = eventView.sortForField(field, tableMeta);
        // Event id and Trace id are technically sortable but we don't want to sort them here since sorting by a uuid value doesn't make sense
        const canSort = field.field !== 'id' &&
            field.field !== 'trace' &&
            field.field !== fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD &&
            (0, eventView_1.isFieldSortable)(field, tableMeta);
        const currentSortKind = currentSort ? currentSort.kind : undefined;
        const currentSortField = currentSort ? currentSort.field : undefined;
        if (field.field === fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD) {
            title = (<operationSort_1.default title={OperationTitle} eventView={eventView} tableMeta={tableMeta} location={location}/>);
        }
        const sortLink = (<sortLink_1.default align={align} title={title || field.field} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={() => this.onSortClick(currentSortKind, currentSortField)}/>);
        return sortLink;
    }
    render() {
        const { eventView, organization, location, setError } = this.props;
        const { widths } = this.state;
        const containsSpanOpsBreakdown = eventView
            .getColumns()
            .find((col) => col.name === fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD);
        const columnOrder = eventView
            .getColumns()
            .filter((col) => !containsSpanOpsBreakdown || !(0, fields_1.isSpanOperationBreakdownField)(col.name))
            .map((col, i) => {
            if (typeof widths[i] === 'number') {
                return Object.assign(Object.assign({}, col), { width: widths[i] });
            }
            return col;
        });
        return (<div>
        <discoverQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} setError={setError} referrer="api.performance.transaction-events">
          {({ pageLinks, isLoading, tableData }) => {
                return (<React.Fragment>
                <gridEditable_1.default isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={eventView.getSorts()} grid={{
                        onResizeColumn: this.handleResizeColumn,
                        renderHeadCell: this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                        renderBodyCell: this.renderBodyCellWithData(tableData),
                    }} location={location}/>
                <pagination_1.default pageLinks={pageLinks}/>
              </React.Fragment>);
            }}
        </discoverQuery_1.default>
      </div>);
    }
}
const StyledIconQuestion = (0, styled_1.default)(questionTooltip_1.default) `
  position: relative;
  top: 1px;
  left: 4px;
`;
exports.default = EventsTable;
//# sourceMappingURL=eventsTable.jsx.map