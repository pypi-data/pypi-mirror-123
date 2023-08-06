Object.defineProperty(exports, "__esModule", { value: true });
exports.getProjectID = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const gridEditable_1 = (0, tslib_1.__importStar)(require("app/components/gridEditable"));
const sortLink_1 = (0, tslib_1.__importDefault)(require("app/components/gridEditable/sortLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const eventView_1 = require("app/utils/discover/eventView");
const fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
const fields_1 = require("app/utils/discover/fields");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const cellAction_1 = (0, tslib_1.__importStar)(require("app/views/eventsV2/table/cellAction"));
const transactionThresholdModal_1 = (0, tslib_1.__importStar)(require("./transactionSummary/transactionThresholdModal"));
const utils_2 = require("./transactionSummary/utils");
const data_1 = require("./data");
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
class _Table extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            widths: [],
            transaction: undefined,
            transactionThreshold: undefined,
            transactionThresholdMetric: undefined,
        };
        this.handleCellAction = (column, dataRow) => {
            return (action, value) => {
                const { eventView, location, organization, projects } = this.props;
                (0, trackAdvancedAnalyticsEvent_1.default)('performance_views.overview.cellaction', {
                    organization,
                    action,
                });
                if (action === cellAction_1.Actions.EDIT_THRESHOLD) {
                    const project_threshold = dataRow.project_threshold_config;
                    const transactionName = dataRow.transaction;
                    const projectID = getProjectID(dataRow, projects);
                    (0, modal_1.openModal)(modalProps => (<transactionThresholdModal_1.default {...modalProps} organization={organization} transactionName={transactionName} eventView={eventView} project={projectID} transactionThreshold={project_threshold[1]} transactionThresholdMetric={project_threshold[0]} onApply={(threshold, metric) => {
                            if (threshold !== project_threshold[1] ||
                                metric !== project_threshold[0]) {
                                this.setState({
                                    transaction: transactionName,
                                    transactionThreshold: threshold,
                                    transactionThresholdMetric: metric,
                                });
                            }
                            (0, indicator_1.addSuccessMessage)((0, locale_1.tct)('[transactionName] updated successfully', {
                                transactionName,
                            }));
                        }}/>), { modalCss: transactionThresholdModal_1.modalCss, backdrop: 'static' });
                    return;
                }
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
        this.renderPrependCellWithData = (tableData) => {
            const { eventView } = this.props;
            const teamKeyTransactionColumn = eventView
                .getColumns()
                .find((col) => col.name === 'team_key_transaction');
            return (isHeader, dataRow) => {
                if (teamKeyTransactionColumn) {
                    if (isHeader) {
                        const star = (<guideAnchor_1.default target="team_key_transaction_header" position="top">
              <icons_1.IconStar key="keyTransaction" color="yellow300" isSolid data-test-id="team-key-transaction-header"/>
            </guideAnchor_1.default>);
                        return [this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta, teamKeyTransactionColumn, star)];
                    }
                    else {
                        return [this.renderBodyCell(tableData, teamKeyTransactionColumn, dataRow)];
                    }
                }
                return [];
            };
        };
        this.handleSummaryClick = () => {
            const { organization } = this.props;
            (0, trackAdvancedAnalyticsEvent_1.default)('performance_views.overview.navigate.summary', {
                organization,
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
    renderBodyCell(tableData, column, dataRow) {
        const { eventView, organization, projects, location } = this.props;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        const tableMeta = tableData.meta;
        const field = String(column.key);
        const fieldRenderer = (0, fieldRenderers_1.getFieldRenderer)(field, tableMeta);
        const rendered = fieldRenderer(dataRow, { organization, location });
        const allowActions = [
            cellAction_1.Actions.ADD,
            cellAction_1.Actions.EXCLUDE,
            cellAction_1.Actions.SHOW_GREATER_THAN,
            cellAction_1.Actions.SHOW_LESS_THAN,
            cellAction_1.Actions.EDIT_THRESHOLD,
        ];
        if (field === 'transaction') {
            const projectID = getProjectID(dataRow, projects);
            const summaryView = eventView.clone();
            if (dataRow['http.method']) {
                summaryView.additionalConditions.setFilterValues('http.method', [
                    dataRow['http.method'],
                ]);
            }
            summaryView.query = summaryView.getQueryWithAdditionalConditions();
            const target = (0, utils_2.transactionSummaryRouteWithQuery)({
                orgSlug: organization.slug,
                transaction: String(dataRow.transaction) || '',
                query: summaryView.generateQueryStringObject(),
                projectID,
            });
            return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column, dataRow)} allowActions={allowActions}>
          <link_1.default to={target} onClick={this.handleSummaryClick}>
            {rendered}
          </link_1.default>
        </cellAction_1.default>);
        }
        if (field.startsWith('team_key_transaction')) {
            // don't display per cell actions for team_key_transaction
            return rendered;
        }
        const fieldName = (0, fields_1.getAggregateAlias)(field);
        const value = dataRow[fieldName];
        if (tableMeta[fieldName] === 'integer' && (0, utils_1.defined)(value) && value > 999) {
            return (<tooltip_1.default title={value.toLocaleString()} containerDisplayMode="block" position="right">
          <cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column, dataRow)} allowActions={allowActions}>
            {rendered}
          </cellAction_1.default>
        </tooltip_1.default>);
        }
        return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column, dataRow)} allowActions={allowActions}>
        {rendered}
      </cellAction_1.default>);
    }
    onSortClick(currentSortKind, currentSortField) {
        const { organization } = this.props;
        (0, trackAdvancedAnalyticsEvent_1.default)('performance_views.landingv2.transactions.sort', {
            organization,
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
        const canSort = (0, eventView_1.isFieldSortable)(field, tableMeta);
        const currentSortKind = currentSort ? currentSort.kind : undefined;
        const currentSortField = currentSort ? currentSort.field : undefined;
        const sortLink = (<sortLink_1.default align={align} title={title || field.field} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={() => this.onSortClick(currentSortKind, currentSortField)}/>);
        if (field.field.startsWith('user_misery')) {
            return (<guideAnchor_1.default target="project_transaction_threshold" position="top">
          {sortLink}
        </guideAnchor_1.default>);
        }
        return sortLink;
    }
    getSortedEventView() {
        const { eventView } = this.props;
        return eventView.withSorts([
            {
                field: 'team_key_transaction',
                kind: 'desc',
            },
            ...eventView.sorts,
        ]);
    }
    render() {
        const { eventView, organization, location, setError } = this.props;
        const { widths, transaction, transactionThreshold, transactionThresholdMetric } = this.state;
        const columnOrder = eventView
            .getColumns()
            // remove team_key_transactions from the column order as we'll be rendering it
            // via a prepended column
            .filter((col) => col.name !== 'team_key_transaction' &&
            !col.name.startsWith('count_miserable') &&
            col.name !== 'project_threshold_config')
            .map((col, i) => {
            if (typeof widths[i] === 'number') {
                return Object.assign(Object.assign({}, col), { width: widths[i] });
            }
            return col;
        });
        const sortedEventView = this.getSortedEventView();
        const columnSortBy = sortedEventView.getSorts();
        const prependColumnWidths = ['max-content'];
        return (<div>
        <discoverQuery_1.default eventView={sortedEventView} orgSlug={organization.slug} location={location} setError={setError} referrer="api.performance.landing-table" transactionName={transaction} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric}>
          {({ pageLinks, isLoading, tableData }) => (<React.Fragment>
              <gridEditable_1.default isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                    onResizeColumn: this.handleResizeColumn,
                    renderHeadCell: this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                    renderBodyCell: this.renderBodyCellWithData(tableData),
                    renderPrependColumns: this.renderPrependCellWithData(tableData),
                    prependColumnWidths,
                }} location={location}/>
              <pagination_1.default pageLinks={pageLinks}/>
            </React.Fragment>)}
        </discoverQuery_1.default>
      </div>);
    }
}
function Table(props) {
    var _a;
    const summaryConditions = (_a = props.summaryConditions) !== null && _a !== void 0 ? _a : props.eventView.getQueryWithAdditionalConditions();
    return <_Table {...props} summaryConditions={summaryConditions}/>;
}
exports.default = Table;
//# sourceMappingURL=table.jsx.map