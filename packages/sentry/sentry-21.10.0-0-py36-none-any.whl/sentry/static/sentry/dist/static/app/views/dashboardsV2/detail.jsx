Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const dashboards_1 = require("app/actionCreators/dashboards");
const indicator_1 = require("app/actionCreators/indicator");
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const controls_1 = (0, tslib_1.__importDefault)(require("./controls"));
const dashboard_1 = (0, tslib_1.__importDefault)(require("./dashboard"));
const data_1 = require("./data");
const title_1 = (0, tslib_1.__importDefault)(require("./title"));
const types_1 = require("./types");
const utils_1 = require("./utils");
const UNSAVED_MESSAGE = (0, locale_1.t)('You have unsaved changes, are you sure you want to leave?');
const HookHeader = (0, hookOrDefault_1.default)({ hookName: 'component:dashboards-header' });
class DashboardDetail extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            dashboardState: this.props.initialState,
            modifiedDashboard: this.updateModifiedDashboard(this.props.initialState),
        };
        this.onEdit = () => {
            const { dashboard } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'dashboards2.edit.start',
                eventName: 'Dashboards2: Edit start',
                organization_id: parseInt(this.props.organization.id, 10),
            });
            this.setState({
                dashboardState: types_1.DashboardState.EDIT,
                modifiedDashboard: (0, utils_1.cloneDashboard)(dashboard),
            });
        };
        this.onRouteLeave = () => {
            if (![types_1.DashboardState.VIEW, types_1.DashboardState.PENDING_DELETE].includes(this.state.dashboardState)) {
                return UNSAVED_MESSAGE;
            }
            return undefined;
        };
        this.onUnload = (event) => {
            if ([types_1.DashboardState.VIEW, types_1.DashboardState.PENDING_DELETE].includes(this.state.dashboardState)) {
                return;
            }
            event.preventDefault();
            event.returnValue = UNSAVED_MESSAGE;
        };
        this.onDelete = (dashboard) => () => {
            const { api, organization, location } = this.props;
            if (!(dashboard === null || dashboard === void 0 ? void 0 : dashboard.id)) {
                return;
            }
            const previousDashboardState = this.state.dashboardState;
            this.setState({ dashboardState: types_1.DashboardState.PENDING_DELETE }, () => {
                (0, dashboards_1.deleteDashboard)(api, organization.slug, dashboard.id)
                    .then(() => {
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Dashboard deleted'));
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventKey: 'dashboards2.delete',
                        eventName: 'Dashboards2: Delete',
                        organization_id: parseInt(this.props.organization.id, 10),
                    });
                    react_router_1.browserHistory.replace({
                        pathname: `/organizations/${organization.slug}/dashboards/`,
                        query: location.query,
                    });
                })
                    .catch(() => {
                    this.setState({
                        dashboardState: previousDashboardState,
                    });
                });
            });
        };
        this.onCancel = () => {
            const { organization, location, params } = this.props;
            if (params.dashboardId) {
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'dashboards2.edit.cancel',
                    eventName: 'Dashboards2: Edit cancel',
                    organization_id: parseInt(this.props.organization.id, 10),
                });
                this.setState({
                    dashboardState: types_1.DashboardState.VIEW,
                    modifiedDashboard: null,
                });
                return;
            }
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'dashboards2.create.cancel',
                eventName: 'Dashboards2: Create cancel',
                organization_id: parseInt(this.props.organization.id, 10),
            });
            react_router_1.browserHistory.replace({
                pathname: `/organizations/${organization.slug}/dashboards/`,
                query: location.query,
            });
        };
        this.onCommit = () => {
            const { api, organization, location, dashboard, reloadData } = this.props;
            const { modifiedDashboard, dashboardState } = this.state;
            switch (dashboardState) {
                case types_1.DashboardState.CREATE: {
                    if (modifiedDashboard) {
                        (0, dashboards_1.createDashboard)(api, organization.slug, modifiedDashboard).then((newDashboard) => {
                            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Dashboard created'));
                            (0, analytics_1.trackAnalyticsEvent)({
                                eventKey: 'dashboards2.create.complete',
                                eventName: 'Dashboards2: Create complete',
                                organization_id: parseInt(organization.id, 10),
                            });
                            this.setState({
                                dashboardState: types_1.DashboardState.VIEW,
                                modifiedDashboard: null,
                            });
                            // redirect to new dashboard
                            react_router_1.browserHistory.replace({
                                pathname: `/organizations/${organization.slug}/dashboard/${newDashboard.id}/`,
                                query: Object.assign({}, location.query),
                            });
                        }, () => undefined);
                    }
                    break;
                }
                case types_1.DashboardState.EDIT: {
                    // only update the dashboard if there are changes
                    if (modifiedDashboard) {
                        if ((0, isEqual_1.default)(dashboard, modifiedDashboard)) {
                            this.setState({
                                dashboardState: types_1.DashboardState.VIEW,
                                modifiedDashboard: null,
                            });
                            return;
                        }
                        (0, dashboards_1.updateDashboard)(api, organization.slug, modifiedDashboard).then((newDashboard) => {
                            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Dashboard updated'));
                            (0, analytics_1.trackAnalyticsEvent)({
                                eventKey: 'dashboards2.edit.complete',
                                eventName: 'Dashboards2: Edit complete',
                                organization_id: parseInt(organization.id, 10),
                            });
                            this.setState({
                                dashboardState: types_1.DashboardState.VIEW,
                                modifiedDashboard: null,
                            });
                            if (reloadData) {
                                reloadData();
                            }
                            if (dashboard && newDashboard.id !== dashboard.id) {
                                react_router_1.browserHistory.replace({
                                    pathname: `/organizations/${organization.slug}/dashboard/${newDashboard.id}/`,
                                    query: Object.assign({}, location.query),
                                });
                                return;
                            }
                        }, () => undefined);
                        return;
                    }
                    this.setState({
                        dashboardState: types_1.DashboardState.VIEW,
                        modifiedDashboard: null,
                    });
                    break;
                }
                case types_1.DashboardState.VIEW:
                default: {
                    this.setState({
                        dashboardState: types_1.DashboardState.VIEW,
                        modifiedDashboard: null,
                    });
                    break;
                }
            }
        };
        this.setModifiedDashboard = (dashboard) => {
            this.setState({
                modifiedDashboard: dashboard,
            });
        };
        this.onSetWidgetToBeUpdated = (widget) => {
            this.setState({ widgetToBeUpdated: widget });
        };
        this.onUpdateWidget = (widgets) => {
            const { modifiedDashboard } = this.state;
            if (modifiedDashboard === null) {
                return;
            }
            this.setState((state) => (Object.assign(Object.assign({}, state), { widgetToBeUpdated: undefined, modifiedDashboard: Object.assign(Object.assign({}, state.modifiedDashboard), { widgets }) })), this.updateRouteAfterSavingWidget);
        };
    }
    componentDidMount() {
        const { route, router } = this.props;
        this.checkStateRoute();
        router.setRouteLeaveHook(route, this.onRouteLeave);
        window.addEventListener('beforeunload', this.onUnload);
    }
    componentDidUpdate(prevProps) {
        if (prevProps.location.pathname !== this.props.location.pathname) {
            this.checkStateRoute();
        }
    }
    componentWillUnmount() {
        window.removeEventListener('beforeunload', this.onUnload);
    }
    checkStateRoute() {
        const { router, organization, params } = this.props;
        const { dashboardId } = params;
        const dashboardDetailsRoute = `/organizations/${organization.slug}/dashboard/${dashboardId}/`;
        if (this.isWidgetBuilderRouter && !this.isEditing) {
            router.replace(dashboardDetailsRoute);
        }
        if (location.pathname === dashboardDetailsRoute && !!this.state.widgetToBeUpdated) {
            this.onSetWidgetToBeUpdated(undefined);
        }
    }
    updateRouteAfterSavingWidget() {
        if (this.isWidgetBuilderRouter) {
            const { router, organization, params } = this.props;
            const { dashboardId } = params;
            if (dashboardId) {
                router.replace(`/organizations/${organization.slug}/dashboard/${dashboardId}/`);
                return;
            }
            router.replace(`/organizations/${organization.slug}/dashboards/new/`);
        }
    }
    updateModifiedDashboard(dashboardState) {
        const { dashboard } = this.props;
        switch (dashboardState) {
            case types_1.DashboardState.CREATE:
                return (0, utils_1.cloneDashboard)(data_1.EMPTY_DASHBOARD);
            case types_1.DashboardState.EDIT:
                return (0, utils_1.cloneDashboard)(dashboard);
            default: {
                return null;
            }
        }
    }
    get isEditing() {
        const { dashboardState } = this.state;
        return [
            types_1.DashboardState.EDIT,
            types_1.DashboardState.CREATE,
            types_1.DashboardState.PENDING_DELETE,
        ].includes(dashboardState);
    }
    get isWidgetBuilderRouter() {
        const { location, params, organization } = this.props;
        const { dashboardId } = params;
        const newWidgetRoutes = [
            `/organizations/${organization.slug}/dashboards/new/widget/new/`,
            `/organizations/${organization.slug}/dashboard/${dashboardId}/widget/new/`,
        ];
        return newWidgetRoutes.includes(location.pathname) || this.isWidgetBuilderEditRouter;
    }
    get isWidgetBuilderEditRouter() {
        const { location, params, organization } = this.props;
        const { dashboardId, widgetId } = params;
        const widgetEditRoutes = [
            `/organizations/${organization.slug}/dashboards/new/widget/${widgetId}/edit/`,
            `/organizations/${organization.slug}/dashboard/${dashboardId}/widget/${widgetId}/edit/`,
        ];
        return widgetEditRoutes.includes(location.pathname);
    }
    get dashboardTitle() {
        const { dashboard } = this.props;
        const { modifiedDashboard } = this.state;
        return modifiedDashboard ? modifiedDashboard.title : dashboard.title;
    }
    renderWidgetBuilder(dashboard) {
        const { children } = this.props;
        const { modifiedDashboard, widgetToBeUpdated } = this.state;
        return (0, react_1.isValidElement)(children)
            ? (0, react_1.cloneElement)(children, {
                dashboard: modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard,
                onSave: this.onUpdateWidget,
                widget: widgetToBeUpdated,
            })
            : children;
    }
    renderDefaultDashboardDetail() {
        const { organization, dashboard, dashboards, params, router, location } = this.props;
        const { modifiedDashboard, dashboardState } = this.state;
        const { dashboardId } = params;
        return (<globalSelectionHeader_1.default skipLoadLastUsed={organization.features.includes('global-views')} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: data_1.DEFAULT_STATS_PERIOD,
                },
            }}>
        <organization_1.PageContent>
          <noProjectMessage_1.default organization={organization}>
            <StyledPageHeader>
              <title_1.default dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} onUpdate={this.setModifiedDashboard} isEditing={this.isEditing}/>
              <controls_1.default organization={organization} dashboards={dashboards} onEdit={this.onEdit} onCancel={this.onCancel} onCommit={this.onCommit} onDelete={this.onDelete(dashboard)} dashboardState={dashboardState}/>
            </StyledPageHeader>
            <HookHeader organization={organization}/>
            <dashboard_1.default paramDashboardId={dashboardId} dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} organization={organization} isEditing={this.isEditing} onUpdate={this.onUpdateWidget} onSetWidgetToBeUpdated={this.onSetWidgetToBeUpdated} router={router} location={location}/>
          </noProjectMessage_1.default>
        </organization_1.PageContent>
      </globalSelectionHeader_1.default>);
    }
    renderDashboardDetail() {
        const { organization, dashboard, dashboards, params, router, location, newWidget } = this.props;
        const { modifiedDashboard, dashboardState } = this.state;
        const { dashboardId } = params;
        return (<globalSelectionHeader_1.default skipLoadLastUsed={organization.features.includes('global-views')} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: data_1.DEFAULT_STATS_PERIOD,
                },
            }}>
        <noProjectMessage_1.default organization={organization}>
          <Layout.Header>
            <Layout.HeaderContent>
              <breadcrumbs_1.default crumbs={[
                {
                    label: (0, locale_1.t)('Dashboards'),
                    to: `/organizations/${organization.slug}/dashboards/`,
                },
                {
                    label: dashboardState === types_1.DashboardState.CREATE
                        ? (0, locale_1.t)('Create Dashboard')
                        : organization.features.includes('dashboards-edit') &&
                            dashboard.id === 'default-overview'
                            ? 'Default Dashboard'
                            : this.dashboardTitle,
                },
            ]}/>
              <Layout.Title>
                <title_1.default dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} onUpdate={this.setModifiedDashboard} isEditing={this.isEditing}/>
              </Layout.Title>
            </Layout.HeaderContent>
            <Layout.HeaderActions>
              <controls_1.default organization={organization} dashboards={dashboards} onEdit={this.onEdit} onCancel={this.onCancel} onCommit={this.onCommit} onDelete={this.onDelete(dashboard)} dashboardState={dashboardState}/>
            </Layout.HeaderActions>
          </Layout.Header>
          <Layout.Body>
            <Layout.Main fullWidth>
              <dashboard_1.default paramDashboardId={dashboardId} dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} organization={organization} isEditing={this.isEditing} onUpdate={this.onUpdateWidget} onSetWidgetToBeUpdated={this.onSetWidgetToBeUpdated} router={router} location={location} newWidget={newWidget}/>
            </Layout.Main>
          </Layout.Body>
        </noProjectMessage_1.default>
      </globalSelectionHeader_1.default>);
    }
    render() {
        const { organization, dashboard } = this.props;
        if (this.isEditing && this.isWidgetBuilderRouter) {
            return this.renderWidgetBuilder(dashboard);
        }
        if (organization.features.includes('dashboards-edit')) {
            return this.renderDashboardDetail();
        }
        return this.renderDefaultDashboardDetail();
    }
}
const StyledPageHeader = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  grid-row-gap: ${(0, space_1.default)(2)};
  align-items: center;
  font-size: ${p => p.theme.headerFontSize};
  color: ${p => p.theme.textColor};
  margin-bottom: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: minmax(0, 1fr) max-content;
    grid-column-gap: ${(0, space_1.default)(2)};
    height: 40px;
  }
`;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(DashboardDetail));
//# sourceMappingURL=detail.jsx.map