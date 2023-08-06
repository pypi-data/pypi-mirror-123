Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const widget_area_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/dashboard/widget-area.svg"));
const widget_bar_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/dashboard/widget-bar.svg"));
const widget_big_number_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/dashboard/widget-big-number.svg"));
const widget_line_1_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/dashboard/widget-line-1.svg"));
const widget_table_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/dashboard/widget-table.svg"));
const widget_world_map_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/dashboard/widget-world-map.svg"));
const dashboards_1 = require("app/actionCreators/dashboards");
const indicator_1 = require("app/actionCreators/indicator");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const types_1 = require("app/views/dashboardsV2/types");
const contextMenu_1 = (0, tslib_1.__importDefault)(require("../contextMenu"));
const utils_1 = require("../utils");
const dashboardCard_1 = (0, tslib_1.__importDefault)(require("./dashboardCard"));
function DashboardList({ api, organization, location, dashboards, pageLinks, onDashboardsChange, }) {
    function miniWidget(displayType) {
        switch (displayType) {
            case types_1.DisplayType.BAR:
                return widget_bar_svg_1.default;
            case types_1.DisplayType.AREA:
            case types_1.DisplayType.TOP_N:
                return widget_area_svg_1.default;
            case types_1.DisplayType.BIG_NUMBER:
                return widget_big_number_svg_1.default;
            case types_1.DisplayType.TABLE:
                return widget_table_svg_1.default;
            case types_1.DisplayType.WORLD_MAP:
                return widget_world_map_svg_1.default;
            case types_1.DisplayType.LINE:
            default:
                return widget_line_1_svg_1.default;
        }
    }
    function handleDelete(dashboard) {
        (0, dashboards_1.deleteDashboard)(api, organization.slug, dashboard.id)
            .then(() => {
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'dashboards_manage.delete',
                eventName: 'Dashboards Manager: Dashboard Deleted',
                organization_id: parseInt(organization.id, 10),
                dashboard_id: parseInt(dashboard.id, 10),
            });
            onDashboardsChange();
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Dashboard deleted'));
        })
            .catch(() => {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error deleting Dashboard'));
        });
    }
    function handleDuplicate(dashboard) {
        (0, dashboards_1.fetchDashboard)(api, organization.slug, dashboard.id)
            .then(dashboardDetail => {
            const newDashboard = (0, utils_1.cloneDashboard)(dashboardDetail);
            newDashboard.widgets.map(widget => (widget.id = undefined));
            (0, dashboards_1.createDashboard)(api, organization.slug, newDashboard, true).then(() => {
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'dashboards_manage.duplicate',
                    eventName: 'Dashboards Manager: Dashboard Duplicated',
                    organization_id: parseInt(organization.id, 10),
                    dashboard_id: parseInt(dashboard.id, 10),
                });
                onDashboardsChange();
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Dashboard duplicated'));
            });
        })
            .catch(() => (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error duplicating Dashboard')));
    }
    function renderMiniDashboards() {
        return dashboards === null || dashboards === void 0 ? void 0 : dashboards.map((dashboard, index) => {
            return (<dashboardCard_1.default key={`${index}-${dashboard.id}`} title={dashboard.id === 'default-overview' ? 'Default Dashboard' : dashboard.title} to={{
                    pathname: `/organizations/${organization.slug}/dashboard/${dashboard.id}/`,
                    query: Object.assign({}, location.query),
                }} detail={(0, locale_1.tn)('%s widget', '%s widgets', dashboard.widgetDisplay.length)} dateStatus={dashboard.dateCreated ? <timeSince_1.default date={dashboard.dateCreated}/> : undefined} createdBy={dashboard.createdBy} renderWidgets={() => (<WidgetGrid>
              {dashboard.widgetDisplay.map((displayType, i) => {
                        return displayType === types_1.DisplayType.BIG_NUMBER ? (<BigNumberWidgetWrapper key={`${i}-${displayType}`}>
                    <WidgetImage src={miniWidget(displayType)}/>
                  </BigNumberWidgetWrapper>) : (<MiniWidgetWrapper key={`${i}-${displayType}`}>
                    <WidgetImage src={miniWidget(displayType)}/>
                  </MiniWidgetWrapper>);
                    })}
            </WidgetGrid>)} renderContextMenu={() => (<contextMenu_1.default>
              <menuItem_1.default data-test-id="dashboard-delete" onClick={event => {
                        event.preventDefault();
                        handleDelete(dashboard);
                    }} disabled={dashboards.length <= 1}>
                {(0, locale_1.t)('Delete')}
              </menuItem_1.default>
              <menuItem_1.default data-test-id="dashboard-duplicate" onClick={event => {
                        event.preventDefault();
                        handleDuplicate(dashboard);
                    }}>
                {(0, locale_1.t)('Duplicate')}
              </menuItem_1.default>
            </contextMenu_1.default>)}/>);
        });
    }
    function renderDashboardGrid() {
        if (!(dashboards === null || dashboards === void 0 ? void 0 : dashboards.length)) {
            return (<emptyStateWarning_1.default>
          <p>{(0, locale_1.t)('Sorry, no Dashboards match your filters.')}</p>
        </emptyStateWarning_1.default>);
        }
        return <DashboardGrid>{renderMiniDashboards()}</DashboardGrid>;
    }
    return (<react_1.Fragment>
      {renderDashboardGrid()}
      <PaginationRow pageLinks={pageLinks} onCursor={(cursor, path, query, direction) => {
            var _a, _b, _c;
            const offset = Number((_c = (_b = (_a = cursor === null || cursor === void 0 ? void 0 : cursor.split) === null || _a === void 0 ? void 0 : _a.call(cursor, ':')) === null || _b === void 0 ? void 0 : _b[1]) !== null && _c !== void 0 ? _c : 0);
            const newQuery = Object.assign(Object.assign({}, query), { cursor });
            const isPrevious = direction === -1;
            if (offset <= 0 && isPrevious) {
                delete newQuery.cursor;
            }
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'dashboards_manage.paginate',
                eventName: 'Dashboards Manager: Paginate',
                organization_id: parseInt(organization.id, 10),
            });
            react_router_1.browserHistory.push({
                pathname: path,
                query: newQuery,
            });
        }}/>
    </react_1.Fragment>);
}
const DashboardGrid = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: minmax(100px, 1fr);
  grid-template-rows: repeat(3, max-content);
  grid-gap: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: repeat(2, minmax(100px, 1fr));
  }

  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    grid-template-columns: repeat(3, minmax(100px, 1fr));
  }
`;
const WidgetGrid = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-auto-flow: row dense;
  grid-gap: ${(0, space_1.default)(0.25)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    grid-template-columns: repeat(6, minmax(0, 1fr));
  }

  @media (min-width: ${p => p.theme.breakpoints[4]}) {
    grid-template-columns: repeat(8, minmax(0, 1fr));
  }
`;
const BigNumberWidgetWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: flex-start;
  width: 100%;
  height: 100%;

  /* 2 cols */
  grid-area: span 1 / span 2;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    /* 4 cols */
    grid-area: span 1 / span 1;
  }

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    /* 6 and 8 cols */
    grid-area: span 1 / span 2;
  }
`;
const MiniWidgetWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: flex-start;
  width: 100%;
  height: 100%;
  grid-area: span 2 / span 2;
`;
const WidgetImage = (0, styled_1.default)('img') `
  width: 100%;
  height: 100%;
`;
const PaginationRow = (0, styled_1.default)(pagination_1.default) `
  margin-bottom: ${(0, space_1.default)(3)};
`;
exports.default = (0, withApi_1.default)(DashboardList);
//# sourceMappingURL=dashboardList.jsx.map