Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const modal_1 = require("app/actionCreators/modal");
const gridEditable_1 = (0, tslib_1.__importStar)(require("app/components/gridEditable"));
const sortLink_1 = (0, tslib_1.__importDefault)(require("app/components/gridEditable/sortLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const truncate_1 = (0, tslib_1.__importDefault)(require("app/components/truncate"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const eventView_1 = require("app/utils/discover/eventView");
const fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
const fields_1 = require("app/utils/discover/fields");
const types_1 = require("app/utils/discover/types");
const urls_1 = require("app/utils/discover/urls");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const utils_2 = require("app/views/performance/traceDetails/utils");
const utils_3 = require("app/views/performance/transactionSummary/utils");
const utils_4 = require("../utils");
const cellAction_1 = (0, tslib_1.__importStar)(require("./cellAction"));
const columnEditModal_1 = (0, tslib_1.__importStar)(require("./columnEditModal"));
const tableActions_1 = (0, tslib_1.__importDefault)(require("./tableActions"));
/**
 * The `TableView` is marked with leading _ in its method names. It consumes
 * the EventView object given in its props to generate new EventView objects
 * for actions like resizing column.

 * The entire state of the table view (or event view) is co-located within
 * the EventView object. This object is fed from the props.
 *
 * Attempting to modify the state, and therefore, modifying the given EventView
 * object given from its props, will generate new instances of EventView objects.
 *
 * In most cases, the new EventView object differs from the previous EventView
 * object. The new EventView object is pushed to the location object.
 */
class TableView extends React.Component {
    constructor() {
        super(...arguments);
        /**
         * Updates a column on resizing
         */
        this._resizeColumn = (columnIndex, nextColumn) => {
            const { location, eventView } = this.props;
            const newWidth = nextColumn.width ? Number(nextColumn.width) : gridEditable_1.COL_WIDTH_UNDEFINED;
            const nextEventView = eventView.withResizedColumn(columnIndex, newWidth);
            (0, utils_4.pushEventViewToLocation)({
                location,
                nextEventView,
                extraQuery: (0, eventView_1.pickRelevantLocationQueryStrings)(location),
            });
        };
        this._renderPrependColumns = (isHeader, dataRow, rowIndex) => {
            const { organization, eventView, tableData, location } = this.props;
            const hasAggregates = eventView.hasAggregateField();
            const hasIdField = eventView.hasIdField();
            if (isHeader) {
                if (hasAggregates) {
                    return [
                        <PrependHeader key="header-icon">
            <icons_1.IconStack size="sm"/>
          </PrependHeader>,
                    ];
                }
                else if (!hasIdField) {
                    return [
                        <PrependHeader key="header-event-id">
            <sortLink_1.default align="left" title={(0, locale_1.t)('event id')} direction={undefined} canSort={false} generateSortLink={() => undefined}/>
          </PrependHeader>,
                    ];
                }
                else {
                    return [];
                }
            }
            if (hasAggregates) {
                const nextView = (0, utils_4.getExpandedResults)(eventView, {}, dataRow);
                const target = {
                    pathname: location.pathname,
                    query: nextView.generateQueryStringObject(),
                };
                return [
                    <tooltip_1.default key={`eventlink${rowIndex}`} title={(0, locale_1.t)('Open Group')}>
          <link_1.default to={target} data-test-id="open-group" onClick={() => {
                            if (nextView.isEqualTo(eventView)) {
                                Sentry.captureException(new Error('Failed to drilldown'));
                            }
                        }}>
            <StyledIcon size="sm"/>
          </link_1.default>
        </tooltip_1.default>,
                ];
            }
            else if (!hasIdField) {
                let value = dataRow.id;
                if (tableData && tableData.meta) {
                    const fieldRenderer = (0, fieldRenderers_1.getFieldRenderer)('id', tableData.meta);
                    value = fieldRenderer(dataRow, { organization, location });
                }
                const eventSlug = (0, urls_1.generateEventSlug)(dataRow);
                const target = (0, urls_1.eventDetailsRouteWithEventView)({
                    orgSlug: organization.slug,
                    eventSlug,
                    eventView,
                });
                return [
                    <tooltip_1.default key={`eventlink${rowIndex}`} title={(0, locale_1.t)('View Event')}>
          <StyledLink data-test-id="view-event" to={target}>
            {value}
          </StyledLink>
        </tooltip_1.default>,
                ];
            }
            else {
                return [];
            }
        };
        this._renderGridHeaderCell = (column) => {
            const { eventView, location, tableData } = this.props;
            const tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
            const align = (0, fields_1.fieldAlignment)(column.name, column.type, tableMeta);
            const field = { field: column.name, width: column.width };
            function generateSortLink() {
                if (!tableMeta) {
                    return undefined;
                }
                const nextEventView = eventView.sortOnField(field, tableMeta);
                const queryStringObject = nextEventView.generateQueryStringObject();
                // Need to pull yAxis from location since eventView only stores 1 yAxis field at time
                queryStringObject.yAxis = (0, queryString_1.decodeList)(location.query.yAxis);
                return Object.assign(Object.assign({}, location), { query: queryStringObject });
            }
            const currentSort = eventView.sortForField(field, tableMeta);
            const canSort = (0, eventView_1.isFieldSortable)(field, tableMeta);
            const titleText = (0, fields_1.isEquationAlias)(column.name)
                ? eventView.getEquations()[(0, fields_1.getEquationAliasIndex)(column.name)]
                : column.name;
            const title = (<StyledTooltip title={titleText}>
        <truncate_1.default value={titleText} maxLength={60} expandable={false}/>
      </StyledTooltip>);
            return (<sortLink_1.default align={align} title={title} direction={currentSort ? currentSort.kind : undefined} canSort={canSort} generateSortLink={generateSortLink}/>);
        };
        this._renderGridBodyCell = (column, dataRow, rowIndex, columnIndex) => {
            var _a, _b;
            const { isFirstPage, eventView, location, organization, tableData } = this.props;
            if (!tableData || !tableData.meta) {
                return dataRow[column.key];
            }
            const columnKey = String(column.key);
            const fieldRenderer = (0, fieldRenderers_1.getFieldRenderer)(columnKey, tableData.meta);
            const display = eventView.getDisplayMode();
            const isTopEvents = display === types_1.DisplayModes.TOP5 || display === types_1.DisplayModes.DAILYTOP5;
            const topEvents = eventView.topEvents ? parseInt(eventView.topEvents, 10) : types_1.TOP_N;
            const count = Math.min((_b = (_a = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _a === void 0 ? void 0 : _a.length) !== null && _b !== void 0 ? _b : topEvents, topEvents);
            let cell = fieldRenderer(dataRow, { organization, location });
            if (columnKey === 'id') {
                const eventSlug = (0, urls_1.generateEventSlug)(dataRow);
                const target = (0, urls_1.eventDetailsRouteWithEventView)({
                    orgSlug: organization.slug,
                    eventSlug,
                    eventView,
                });
                cell = (<tooltip_1.default title={(0, locale_1.t)('View Event')}>
          <StyledLink data-test-id="view-event" to={target}>
            {cell}
          </StyledLink>
        </tooltip_1.default>);
            }
            else if (columnKey === 'trace') {
                const dateSelection = eventView.normalizeDateSelection(location);
                if (dataRow.trace) {
                    const target = (0, utils_2.getTraceDetailsUrl)(organization, String(dataRow.trace), dateSelection, {});
                    cell = (<tooltip_1.default title={(0, locale_1.t)('View Trace')}>
            <StyledLink data-test-id="view-trace" to={target}>
              {cell}
            </StyledLink>
          </tooltip_1.default>);
                }
            }
            const fieldName = (0, fields_1.getAggregateAlias)(columnKey);
            const value = dataRow[fieldName];
            if (tableData.meta[fieldName] === 'integer' && (0, utils_1.defined)(value) && value > 999) {
                return (<tooltip_1.default title={value.toLocaleString()} containerDisplayMode="block" position="right">
          <cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(dataRow, column)}>
            {cell}
          </cellAction_1.default>
        </tooltip_1.default>);
            }
            return (<React.Fragment>
        {isFirstPage && isTopEvents && rowIndex < topEvents && columnIndex === 0 ? (
                // Add one if we need to include Other in the series
                <TopResultsIndicator count={count} index={rowIndex}/>) : null}
        <cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(dataRow, column)}>
          {cell}
        </cellAction_1.default>
      </React.Fragment>);
        };
        this.handleEditColumns = () => {
            const { organization, eventView, tagKeys, measurementKeys, spanOperationBreakdownKeys, } = this.props;
            const hasBreakdownFeature = organization.features.includes('performance-ops-breakdown');
            (0, modal_1.openModal)(modalProps => (<columnEditModal_1.default {...modalProps} organization={organization} tagKeys={tagKeys} measurementKeys={measurementKeys} spanOperationBreakdownKeys={hasBreakdownFeature ? spanOperationBreakdownKeys : undefined} columns={eventView.getColumns().map(col => col.column)} onApply={this.handleUpdateColumns}/>), { modalCss: columnEditModal_1.modalCss, backdrop: 'static' });
        };
        this.handleCellAction = (dataRow, column) => {
            return (action, value) => {
                const { eventView, organization, projects, location } = this.props;
                const query = new tokenizeSearch_1.MutableSearch(eventView.query);
                let nextView = eventView.clone();
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'discover_v2.results.cellaction',
                    eventName: 'Discoverv2: Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action,
                });
                switch (action) {
                    case cellAction_1.Actions.TRANSACTION: {
                        const maybeProject = projects.find(project => project.slug === dataRow.project);
                        const projectID = maybeProject ? [maybeProject.id] : undefined;
                        const next = (0, utils_3.transactionSummaryRouteWithQuery)({
                            orgSlug: organization.slug,
                            transaction: String(value),
                            projectID,
                            query: nextView.getGlobalSelectionQuery(),
                        });
                        react_router_1.browserHistory.push(next);
                        return;
                    }
                    case cellAction_1.Actions.RELEASE: {
                        const maybeProject = projects.find(project => {
                            return project.slug === dataRow.project;
                        });
                        react_router_1.browserHistory.push({
                            pathname: `/organizations/${organization.slug}/releases/${encodeURIComponent(value)}/`,
                            query: Object.assign(Object.assign({}, nextView.getGlobalSelectionQuery()), { project: maybeProject ? maybeProject.id : undefined }),
                        });
                        return;
                    }
                    case cellAction_1.Actions.DRILLDOWN: {
                        // count_unique(column) drilldown
                        (0, analytics_1.trackAnalyticsEvent)({
                            eventKey: 'discover_v2.results.drilldown',
                            eventName: 'Discoverv2: Click aggregate drilldown',
                            organization_id: parseInt(organization.id, 10),
                        });
                        // Drilldown into each distinct value and get a count() for each value.
                        nextView = (0, utils_4.getExpandedResults)(nextView, {}, dataRow).withNewColumn({
                            kind: 'function',
                            function: ['count', '', undefined, undefined],
                        });
                        react_router_1.browserHistory.push(nextView.getResultsViewUrlTarget(organization.slug));
                        return;
                    }
                    default: {
                        (0, cellAction_1.updateQuery)(query, action, column, value);
                    }
                }
                nextView.query = query.formatString();
                const target = nextView.getResultsViewUrlTarget(organization.slug);
                // Get yAxis from location
                target.query.yAxis = (0, queryString_1.decodeList)(location.query.yAxis);
                react_router_1.browserHistory.push(target);
            };
        };
        this.handleUpdateColumns = (columns) => {
            const { organization, eventView, location } = this.props;
            // metrics
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.update_columns',
                eventName: 'Discoverv2: Update columns',
                organization_id: parseInt(organization.id, 10),
            });
            const nextView = eventView.withColumns(columns);
            const resultsViewUrlTarget = nextView.getResultsViewUrlTarget(organization.slug);
            // Need to pull yAxis from location since eventView only stores 1 yAxis field at time
            const previousYAxis = (0, queryString_1.decodeList)(location.query.yAxis);
            resultsViewUrlTarget.query.yAxis = previousYAxis.filter(yAxis => nextView.getYAxisOptions().find(({ value }) => value === yAxis));
            react_router_1.browserHistory.push(resultsViewUrlTarget);
        };
        this.renderHeaderButtons = () => {
            const { organization, title, eventView, isLoading, error, tableData, location, onChangeShowTags, showTags, } = this.props;
            return (<tableActions_1.default title={title} isLoading={isLoading} error={error} organization={organization} eventView={eventView} onEdit={this.handleEditColumns} tableData={tableData} location={location} onChangeShowTags={onChangeShowTags} showTags={showTags}/>);
        };
    }
    render() {
        const { isLoading, error, location, tableData, eventView } = this.props;
        const columnOrder = eventView.getColumns();
        const columnSortBy = eventView.getSorts();
        const prependColumnWidths = eventView.hasAggregateField()
            ? ['40px']
            : eventView.hasIdField()
                ? []
                : [`minmax(${gridEditable_1.COL_WIDTH_MINIMUM}px, max-content)`];
        return (<gridEditable_1.default isLoading={isLoading} error={error} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} title={(0, locale_1.t)('Results')} grid={{
                renderHeadCell: this._renderGridHeaderCell,
                renderBodyCell: this._renderGridBodyCell,
                onResizeColumn: this._resizeColumn,
                renderPrependColumns: this._renderPrependColumns,
                prependColumnWidths,
            }} headerButtons={this.renderHeaderButtons} location={location}/>);
    }
}
const PrependHeader = (0, styled_1.default)('span') `
  color: ${p => p.theme.subText};
`;
const StyledTooltip = (0, styled_1.default)(tooltip_1.default) `
  display: initial;
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  > div {
    display: inline;
  }
`;
const StyledIcon = (0, styled_1.default)(icons_1.IconStack) `
  vertical-align: middle;
`;
const TopResultsIndicator = (0, styled_1.default)('div') `
  position: absolute;
  left: -1px;
  margin-top: 4.5px;
  width: 9px;
  height: 15px;
  border-radius: 0 3px 3px 0;

  background-color: ${p => {
    // this background color needs to match the colors used in
    // app/components/charts/eventsChart so that the ordering matches
    // the color pallete contains n + 2 colors, so we subtract 2 here
    return p.theme.charts.getColorPalette(p.count - 2)[p.index];
}};
`;
exports.default = (0, withProjects_1.default)(TableView);
//# sourceMappingURL=tableView.jsx.map