Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const globalSelection_1 = require("app/actionCreators/globalSelection");
const modal_1 = require("app/actionCreators/modal");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
const queryString_1 = require("app/utils/queryString");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const utils_1 = require("./savedQuery/utils");
const miniGraph_1 = (0, tslib_1.__importDefault)(require("./miniGraph"));
const querycard_1 = (0, tslib_1.__importDefault)(require("./querycard"));
const utils_2 = require("./utils");
class QueryList extends React.Component {
    constructor() {
        super(...arguments);
        this.handleDeleteQuery = (eventView) => (event) => {
            event.preventDefault();
            event.stopPropagation();
            const { api, organization, onQueryChange, location, savedQueries } = this.props;
            (0, utils_1.handleDeleteQuery)(api, organization, eventView).then(() => {
                if (savedQueries.length === 1 && location.query.cursor) {
                    react_router_1.browserHistory.push({
                        pathname: location.pathname,
                        query: Object.assign(Object.assign({}, location.query), { cursor: undefined }),
                    });
                }
                else {
                    onQueryChange();
                }
            });
        };
        this.handleDuplicateQuery = (eventView, yAxis) => (event) => {
            event.preventDefault();
            event.stopPropagation();
            const { api, location, organization, onQueryChange } = this.props;
            eventView = eventView.clone();
            eventView.name = `${eventView.name} copy`;
            (0, utils_1.handleCreateQuery)(api, organization, eventView, yAxis).then(() => {
                onQueryChange();
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: {},
                });
            });
        };
        this.handleAddQueryToDashboard = (eventView, savedQuery) => (event) => {
            var _a, _b;
            const { organization } = this.props;
            event.preventDefault();
            event.stopPropagation();
            const defaultWidgetQuery = {
                name: '',
                fields: (_a = savedQuery === null || savedQuery === void 0 ? void 0 : savedQuery.yAxis) !== null && _a !== void 0 ? _a : ['count()'],
                conditions: eventView.query,
                orderby: '',
            };
            (0, trackAdvancedAnalyticsEvent_1.default)('discover_views.add_to_dashboard.modal_open', {
                organization,
                saved_query: !!savedQuery,
            });
            (0, modal_1.openAddDashboardWidgetModal)({
                organization,
                start: eventView.start,
                end: eventView.end,
                statsPeriod: eventView.statsPeriod,
                fromDiscover: true,
                defaultWidgetQuery,
                defaultTableColumns: eventView.fields.map(({ field }) => field),
                defaultTitle: (_b = savedQuery === null || savedQuery === void 0 ? void 0 : savedQuery.name) !== null && _b !== void 0 ? _b : (eventView.name !== 'All Events' ? eventView.name : undefined),
            });
        };
    }
    componentDidMount() {
        /**
         * We need to reset global selection here because the saved queries can define their own projects
         * in the query. This can lead to mismatched queries for the project
         */
        (0, globalSelection_1.resetGlobalSelection)();
    }
    renderQueries() {
        const { pageLinks, renderPrebuilt } = this.props;
        const links = (0, parseLinkHeader_1.default)(pageLinks || '');
        let cards = [];
        // If we're on the first page (no-previous page exists)
        // include the pre-built queries.
        if (renderPrebuilt && (!links.previous || links.previous.results === false)) {
            cards = cards.concat(this.renderPrebuiltQueries());
        }
        cards = cards.concat(this.renderSavedQueries());
        if (cards.filter(x => x).length === 0) {
            return (<StyledEmptyStateWarning>
          <p>{(0, locale_1.t)('No saved queries match that filter')}</p>
        </StyledEmptyStateWarning>);
        }
        return cards;
    }
    renderPrebuiltQueries() {
        const { location, organization, savedQuerySearchQuery } = this.props;
        const views = (0, utils_2.getPrebuiltQueries)(organization);
        const hasSearchQuery = typeof savedQuerySearchQuery === 'string' && savedQuerySearchQuery.length > 0;
        const needleSearch = hasSearchQuery ? savedQuerySearchQuery.toLowerCase() : '';
        const list = views.map((view, index) => {
            const eventView = eventView_1.default.fromNewQueryWithLocation(view, location);
            // if a search is performed on the list of queries, we filter
            // on the pre-built queries
            if (hasSearchQuery &&
                eventView.name &&
                !eventView.name.toLowerCase().includes(needleSearch)) {
                return null;
            }
            const recentTimeline = (0, locale_1.t)('Last ') + eventView.statsPeriod;
            const customTimeline = (0, moment_1.default)(eventView.start).format('MMM D, YYYY h:mm A') +
                ' - ' +
                (0, moment_1.default)(eventView.end).format('MMM D, YYYY h:mm A');
            const to = eventView.getResultsViewUrlTarget(organization.slug);
            return (<querycard_1.default key={`${index}-${eventView.name}`} to={to} title={eventView.name} subtitle={eventView.statsPeriod ? recentTimeline : customTimeline} queryDetail={eventView.query} createdBy={eventView.createdBy} renderGraph={() => (<miniGraph_1.default location={location} eventView={eventView} organization={organization} referrer="api.discover.homepage.prebuilt"/>)} onEventClick={() => {
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventKey: 'discover_v2.prebuilt_query_click',
                        eventName: 'Discoverv2: Click a pre-built query',
                        organization_id: parseInt(this.props.organization.id, 10),
                        query_name: eventView.name,
                    });
                }} renderContextMenu={() => (<feature_1.default organization={organization} features={['connect-discover-and-dashboards', 'dashboards-edit']}>
              {({ hasFeature }) => {
                        return (hasFeature && (<ContextMenu>
                      <StyledMenuItem data-test-id="add-query-to-dashboard" onClick={this.handleAddQueryToDashboard(eventView)}>
                        {(0, locale_1.t)('Add to Dashboard')} <featureBadge_1.default type="beta" noTooltip/>
                      </StyledMenuItem>
                    </ContextMenu>));
                    }}
            </feature_1.default>)}/>);
        });
        return list;
    }
    renderSavedQueries() {
        const { savedQueries, location, organization } = this.props;
        if (!savedQueries || !Array.isArray(savedQueries) || savedQueries.length === 0) {
            return [];
        }
        return savedQueries.map((savedQuery, index) => {
            const eventView = eventView_1.default.fromSavedQuery(savedQuery);
            const recentTimeline = (0, locale_1.t)('Last ') + eventView.statsPeriod;
            const customTimeline = (0, moment_1.default)(eventView.start).format('MMM D, YYYY h:mm A') +
                ' - ' +
                (0, moment_1.default)(eventView.end).format('MMM D, YYYY h:mm A');
            const to = eventView.getResultsViewShortUrlTarget(organization.slug);
            const dateStatus = <timeSince_1.default date={savedQuery.dateUpdated}/>;
            const referrer = `api.discover.${eventView.getDisplayMode()}-chart`;
            return (<querycard_1.default key={`${index}-${eventView.id}`} to={to} title={eventView.name} subtitle={eventView.statsPeriod ? recentTimeline : customTimeline} queryDetail={eventView.query} createdBy={eventView.createdBy} dateStatus={dateStatus} onEventClick={() => {
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventKey: 'discover_v2.saved_query_click',
                        eventName: 'Discoverv2: Click a saved query',
                        organization_id: parseInt(this.props.organization.id, 10),
                    });
                }} renderGraph={() => (<feature_1.default organization={organization} features={['connect-discover-and-dashboards']}>
              {({ hasFeature }) => (<miniGraph_1.default location={location} eventView={eventView} organization={organization} referrer={referrer} yAxis={hasFeature ? savedQuery.yAxis : undefined}/>)}
            </feature_1.default>)} renderContextMenu={() => (<ContextMenu>
              <feature_1.default organization={organization} features={['connect-discover-and-dashboards', 'dashboards-edit']}>
                {({ hasFeature }) => hasFeature && (<StyledMenuItem data-test-id="add-query-to-dashboard" onClick={this.handleAddQueryToDashboard(eventView, savedQuery)}>
                      {(0, locale_1.t)('Add to Dashboard')} <featureBadge_1.default type="beta" noTooltip/>
                    </StyledMenuItem>)}
              </feature_1.default>
              <menuItem_1.default data-test-id="delete-query" onClick={this.handleDeleteQuery(eventView)}>
                {(0, locale_1.t)('Delete Query')}
              </menuItem_1.default>
              <menuItem_1.default data-test-id="duplicate-query" onClick={this.handleDuplicateQuery(eventView, (0, queryString_1.decodeList)(savedQuery.yAxis))}>
                {(0, locale_1.t)('Duplicate Query')}
              </menuItem_1.default>
            </ContextMenu>)}/>);
        });
    }
    render() {
        const { pageLinks } = this.props;
        return (<React.Fragment>
        <QueryGrid>{this.renderQueries()}</QueryGrid>
        <PaginationRow pageLinks={pageLinks} onCursor={(cursor, path, query, direction) => {
                var _a, _b;
                const offset = Number((_b = (_a = cursor === null || cursor === void 0 ? void 0 : cursor.split(':')) === null || _a === void 0 ? void 0 : _a[1]) !== null && _b !== void 0 ? _b : 0);
                const newQuery = Object.assign(Object.assign({}, query), { cursor });
                const isPrevious = direction === -1;
                if (offset <= 0 && isPrevious) {
                    delete newQuery.cursor;
                }
                react_router_1.browserHistory.push({
                    pathname: path,
                    query: newQuery,
                });
            }}/>
      </React.Fragment>);
    }
}
const PaginationRow = (0, styled_1.default)(pagination_1.default) `
  margin-bottom: 20px;
`;
const QueryGrid = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: minmax(100px, 1fr);
  grid-gap: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: repeat(2, minmax(100px, 1fr));
  }

  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    grid-template-columns: repeat(3, minmax(100px, 1fr));
  }
`;
const ContextMenu = ({ children }) => (<dropdownMenu_1.default>
    {({ isOpen, getRootProps, getActorProps, getMenuProps }) => {
        const topLevelCx = (0, classnames_1.default)('dropdown', {
            'anchor-right': true,
            open: isOpen,
        });
        return (<MoreOptions {...getRootProps({
            className: topLevelCx,
        })}>
          <DropdownTarget {...getActorProps({
            onClick: (event) => {
                event.stopPropagation();
                event.preventDefault();
            },
        })}>
            <icons_1.IconEllipsis data-test-id="context-menu" size="md"/>
          </DropdownTarget>
          {isOpen && (<ul {...getMenuProps({})} className={(0, classnames_1.default)('dropdown-menu')}>
              {children}
            </ul>)}
        </MoreOptions>);
    }}
  </dropdownMenu_1.default>);
const MoreOptions = (0, styled_1.default)('span') `
  display: flex;
  color: ${p => p.theme.textColor};
`;
const DropdownTarget = (0, styled_1.default)('div') `
  display: flex;
`;
const StyledEmptyStateWarning = (0, styled_1.default)(emptyStateWarning_1.default) `
  grid-column: 1 / 4;
`;
const StyledMenuItem = (0, styled_1.default)(menuItem_1.default) `
  white-space: nowrap;
  span {
    align-items: baseline;
  }
`;
exports.default = (0, withApi_1.default)(QueryList);
//# sourceMappingURL=queryList.jsx.map