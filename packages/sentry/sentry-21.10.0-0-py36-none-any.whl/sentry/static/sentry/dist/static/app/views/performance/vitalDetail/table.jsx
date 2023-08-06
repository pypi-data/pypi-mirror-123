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
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const eventView_1 = require("app/utils/discover/eventView");
const fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
const fields_1 = require("app/utils/discover/fields");
const vitalsDetailsTableQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/vitals/vitalsDetailsTableQuery"));
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const cellAction_1 = (0, tslib_1.__importStar)(require("app/views/eventsV2/table/cellAction"));
const charts_1 = require("../transactionSummary/transactionOverview/charts");
const utils_1 = require("../transactionSummary/utils");
const utils_2 = require("./utils");
const COLUMN_TITLES = ['Transaction', 'Project', 'Unique Users', 'Count'];
const getTableColumnTitle = (index, vitalName) => {
    const abbrev = utils_2.vitalAbbreviations[vitalName];
    const titles = [
        ...COLUMN_TITLES,
        `p50(${abbrev})`,
        `p75(${abbrev})`,
        `p95(${abbrev})`,
        `Status`,
    ];
    return titles[index];
};
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
class Table extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            widths: [],
        };
        this.handleCellAction = (column) => {
            return (action, value) => {
                const { eventView, location, organization } = this.props;
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'performance_views.overview.cellaction',
                    eventName: 'Performance Views: Cell Action Clicked',
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
        this.renderBodyCellWithData = (tableData, vitalName) => {
            return (column, dataRow) => this.renderBodyCell(tableData, column, dataRow, vitalName);
        };
        this.renderHeadCellWithMeta = (tableMeta, vitalName) => {
            return (column, index) => this.renderHeadCell(tableMeta, column, getTableColumnTitle(index, vitalName));
        };
        this.renderPrependCellWithData = (tableData, vitalName) => {
            const { eventView } = this.props;
            const teamKeyTransactionColumn = eventView
                .getColumns()
                .find((col) => col.name === 'team_key_transaction');
            return (isHeader, dataRow) => {
                if (teamKeyTransactionColumn) {
                    if (isHeader) {
                        const star = (<icons_1.IconStar key="keyTransaction" color="yellow300" isSolid data-test-id="key-transaction-header"/>);
                        return [this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta, teamKeyTransactionColumn, star)];
                    }
                    else {
                        return [
                            this.renderBodyCell(tableData, teamKeyTransactionColumn, dataRow, vitalName),
                        ];
                    }
                }
                return [];
            };
        };
        this.handleSummaryClick = () => {
            const { organization } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.overview.navigate.summary',
                eventName: 'Performance Views: Overview view summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        this.handleResizeColumn = (columnIndex, nextColumn) => {
            const widths = [...this.state.widths];
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : gridEditable_1.COL_WIDTH_UNDEFINED;
            this.setState({ widths });
        };
    }
    renderBodyCell(tableData, column, dataRow, vitalName) {
        const { eventView, organization, projects, location, summaryConditions } = this.props;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        const tableMeta = tableData.meta;
        const field = String(column.key);
        if (field === (0, utils_2.getVitalDetailTablePoorStatusFunction)(vitalName)) {
            if (dataRow[(0, fields_1.getAggregateAlias)(field)]) {
                return (<UniqueTagCell>
            <PoorTag>{(0, locale_1.t)('Poor')}</PoorTag>
          </UniqueTagCell>);
            }
            else if (dataRow[(0, fields_1.getAggregateAlias)((0, utils_2.getVitalDetailTableMehStatusFunction)(vitalName))]) {
                return (<UniqueTagCell>
            <MehTag>{(0, locale_1.t)('Meh')}</MehTag>
          </UniqueTagCell>);
            }
            else {
                return (<UniqueTagCell>
            <GoodTag>{(0, locale_1.t)('Good')}</GoodTag>
          </UniqueTagCell>);
            }
        }
        const fieldRenderer = (0, fieldRenderers_1.getFieldRenderer)(field, tableMeta);
        const rendered = fieldRenderer(dataRow, { organization, location });
        const allowActions = [
            cellAction_1.Actions.ADD,
            cellAction_1.Actions.EXCLUDE,
            cellAction_1.Actions.SHOW_GREATER_THAN,
            cellAction_1.Actions.SHOW_LESS_THAN,
        ];
        if (field === 'transaction') {
            const projectID = getProjectID(dataRow, projects);
            const summaryView = eventView.clone();
            const conditions = new tokenizeSearch_1.MutableSearch(summaryConditions);
            conditions.addFilterValues('has', [`${vitalName}`]);
            summaryView.query = conditions.formatString();
            const target = (0, utils_1.transactionSummaryRouteWithQuery)({
                orgSlug: organization.slug,
                transaction: String(dataRow.transaction) || '',
                query: summaryView.generateQueryStringObject(),
                projectID,
                showTransactions: utils_1.TransactionFilterOptions.RECENT,
                display: charts_1.DisplayModes.VITALS,
            });
            return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
          <link_1.default to={target} onClick={this.handleSummaryClick}>
            {rendered}
          </link_1.default>
        </cellAction_1.default>);
        }
        if (field.startsWith('team_key_transaction')) {
            return rendered;
        }
        return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
        {rendered}
      </cellAction_1.default>);
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
        const canSort = (0, eventView_1.isFieldSortable)(field, tableMeta);
        return (<sortLink_1.default align={align} title={title || field.field} direction={currentSort ? currentSort.kind : undefined} canSort={canSort} generateSortLink={generateSortLink}/>);
    }
    getSortedEventView(vitalName) {
        const { eventView } = this.props;
        const aggregateFieldPoor = (0, fields_1.getAggregateAlias)((0, utils_2.getVitalDetailTablePoorStatusFunction)(vitalName));
        const aggregateFieldMeh = (0, fields_1.getAggregateAlias)((0, utils_2.getVitalDetailTableMehStatusFunction)(vitalName));
        const isSortingByStatus = eventView.sorts.some(sort => sort.field.includes(aggregateFieldPoor) || sort.field.includes(aggregateFieldMeh));
        const additionalSorts = isSortingByStatus
            ? []
            : [
                {
                    field: 'team_key_transaction',
                    kind: 'desc',
                },
                {
                    field: aggregateFieldPoor,
                    kind: 'desc',
                },
                {
                    field: aggregateFieldMeh,
                    kind: 'desc',
                },
            ];
        return eventView.withSorts([...additionalSorts, ...eventView.sorts]);
    }
    render() {
        const { eventView, organization, location } = this.props;
        const { widths } = this.state;
        const fakeColumnView = eventView.clone();
        fakeColumnView.fields = [...eventView.fields];
        const columnOrder = fakeColumnView
            .getColumns()
            // remove key_transactions from the column order as we'll be rendering it
            // via a prepended column
            .filter((col) => col.name !== 'team_key_transaction')
            .slice(0, -1)
            .map((col, i) => {
            if (typeof widths[i] === 'number') {
                return Object.assign(Object.assign({}, col), { width: widths[i] });
            }
            return col;
        });
        const vitalName = (0, utils_2.vitalNameFromLocation)(location);
        const sortedEventView = this.getSortedEventView(vitalName);
        const columnSortBy = sortedEventView.getSorts();
        return (<div>
        <vitalsDetailsTableQuery_1.default eventView={sortedEventView} orgSlug={organization.slug} location={location} limit={10} referrer="api.performance.vital-detail">
          {({ pageLinks, isLoading, tableData }) => (<React.Fragment>
              <gridEditable_1.default isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                    onResizeColumn: this.handleResizeColumn,
                    renderHeadCell: this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta, vitalName),
                    renderBodyCell: this.renderBodyCellWithData(tableData, vitalName),
                    renderPrependColumns: this.renderPrependCellWithData(tableData, vitalName),
                    prependColumnWidths: ['max-content'],
                }} location={location}/>
              <pagination_1.default pageLinks={pageLinks}/>
            </React.Fragment>)}
        </vitalsDetailsTableQuery_1.default>
      </div>);
    }
}
const UniqueTagCell = (0, styled_1.default)('div') `
  text-align: right;
`;
const GoodTag = (0, styled_1.default)(tag_1.default) `
  div {
    background-color: ${p => p.theme[utils_2.vitalStateColors[utils_2.VitalState.GOOD]]};
  }
  span {
    color: ${p => p.theme.white};
  }
`;
const MehTag = (0, styled_1.default)(tag_1.default) `
  div {
    background-color: ${p => p.theme[utils_2.vitalStateColors[utils_2.VitalState.MEH]]};
  }
  span {
    color: ${p => p.theme.white};
  }
`;
const PoorTag = (0, styled_1.default)(tag_1.default) `
  div {
    background-color: ${p => p.theme[utils_2.vitalStateColors[utils_2.VitalState.POOR]]};
  }
  span {
    color: ${p => p.theme.white};
  }
`;
exports.default = Table;
//# sourceMappingURL=table.jsx.map