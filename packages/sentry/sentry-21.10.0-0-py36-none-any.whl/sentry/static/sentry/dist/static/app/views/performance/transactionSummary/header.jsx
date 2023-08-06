Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const guideAnchor_1 = require("app/components/assistant/guideAnchor");
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const createAlertButton_1 = require("app/components/createAlertButton");
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const listLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/listLink"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const hasMeasurementsQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/vitals/hasMeasurementsQuery"));
const queryString_1 = require("app/utils/queryString");
const breadcrumb_1 = (0, tslib_1.__importDefault)(require("app/views/performance/breadcrumb"));
const utils_1 = require("../landing/utils");
const utils_2 = require("./transactionEvents/utils");
const utils_3 = require("./transactionSpans/utils");
const utils_4 = require("./transactionTags/utils");
const utils_5 = require("./transactionVitals/utils");
const tabs_1 = (0, tslib_1.__importDefault)(require("./tabs"));
const teamKeyTransactionButton_1 = (0, tslib_1.__importDefault)(require("./teamKeyTransactionButton"));
const transactionThresholdButton_1 = (0, tslib_1.__importDefault)(require("./transactionThresholdButton"));
const utils_6 = require("./utils");
const TAB_ANALYTICS = {
    [tabs_1.default.WebVitals]: {
        eventKey: 'performance_views.vitals.vitals_tab_clicked',
        eventName: 'Performance Views: Vitals tab clicked',
    },
    [tabs_1.default.Tags]: {
        eventKey: 'performance_views.tags.tags_tab_clicked',
        eventName: 'Performance Views: Tags tab clicked',
    },
    [tabs_1.default.Events]: {
        eventKey: 'performance_views.events.events_tab_clicked',
        eventName: 'Performance Views: Events tab clicked',
    },
    [tabs_1.default.Spans]: {
        eventKey: 'performance_views.spans.spans_tab_clicked',
        eventName: 'Performance Views: Spans tab clicked',
    },
};
class TransactionHeader extends React.Component {
    constructor() {
        super(...arguments);
        this.trackTabClick = (tab) => () => {
            const analyticKeys = TAB_ANALYTICS[tab];
            if (!analyticKeys) {
                return;
            }
            (0, analytics_1.trackAnalyticsEvent)(Object.assign(Object.assign({}, analyticKeys), { organization_id: this.props.organization.id }));
        };
        this.handleIncompatibleQuery = (incompatibleAlertNoticeFn, errors) => {
            var _a, _b;
            this.trackAlertClick(errors);
            (_b = (_a = this.props).handleIncompatibleQuery) === null || _b === void 0 ? void 0 : _b.call(_a, incompatibleAlertNoticeFn, errors);
        };
        this.handleCreateAlertSuccess = () => {
            this.trackAlertClick();
        };
    }
    trackAlertClick(errors) {
        const { organization } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance_views.summary.create_alert_clicked',
            eventName: 'Performance Views: Create alert clicked',
            organization_id: organization.id,
            status: errors ? 'error' : 'success',
            errors,
            url: window.location.href,
        });
    }
    renderCreateAlertButton() {
        const { eventView, organization, projects } = this.props;
        return (<createAlertButton_1.CreateAlertFromViewButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={this.handleIncompatibleQuery} onSuccess={this.handleCreateAlertSuccess} referrer="performance"/>);
    }
    renderKeyTransactionButton() {
        const { eventView, organization, transactionName } = this.props;
        return (<teamKeyTransactionButton_1.default transactionName={transactionName} eventView={eventView} organization={organization}/>);
    }
    renderSettingsButton() {
        const { organization, transactionName, eventView, onChangeThreshold } = this.props;
        return (<guideAnchor_1.GuideAnchor target="project_transaction_threshold_override" position="bottom">
        <transactionThresholdButton_1.default organization={organization} transactionName={transactionName} eventView={eventView} onChangeThreshold={onChangeThreshold}/>
      </guideAnchor_1.GuideAnchor>);
    }
    renderWebVitalsTab() {
        const { organization, eventView, location, projects, transactionName, currentTab, hasWebVitals, } = this.props;
        const vitalsTarget = (0, utils_5.vitalsRouteWithQuery)({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: (0, queryString_1.decodeScalar)(location.query.project),
            query: location.query,
        });
        const tab = (<listLink_1.default data-test-id="web-vitals-tab" to={vitalsTarget} isActive={() => currentTab === tabs_1.default.WebVitals} onClick={this.trackTabClick(tabs_1.default.WebVitals)}>
        {(0, locale_1.t)('Web Vitals')}
      </listLink_1.default>);
        switch (hasWebVitals) {
            case 'maybe':
                // need to check if the web vitals tab should be shown
                // frontend projects should always show the web vitals tab
                if ((0, utils_1.getCurrentLandingDisplay)(location, projects, eventView).field ===
                    utils_1.LandingDisplayField.FRONTEND_PAGELOAD) {
                    return tab;
                }
                // if it is not a frontend project, then we check to see if there
                // are any web vitals associated with the transaction recently
                return (<hasMeasurementsQuery_1.default location={location} orgSlug={organization.slug} eventView={eventView} transaction={transactionName} type="web">
            {({ hasMeasurements }) => (hasMeasurements ? tab : null)}
          </hasMeasurementsQuery_1.default>);
            case 'yes':
                // always show the web vitals tab
                return tab;
            case 'no':
            default:
                // never show the web vitals tab
                return null;
        }
    }
    render() {
        const { organization, location, projectId, transactionName, currentTab } = this.props;
        const routeQuery = {
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: projectId,
            query: location.query,
        };
        const summaryTarget = (0, utils_6.transactionSummaryRouteWithQuery)(routeQuery);
        const tagsTarget = (0, utils_4.tagsRouteWithQuery)(routeQuery);
        const eventsTarget = (0, utils_2.eventsRouteWithQuery)(routeQuery);
        const spansTarget = (0, utils_3.spansRouteWithQuery)(routeQuery);
        return (<Layout.Header>
        <Layout.HeaderContent>
          <breadcrumb_1.default organization={organization} location={location} transaction={{
                project: projectId,
                name: transactionName,
            }} tab={currentTab}/>
          <Layout.Title>{transactionName}</Layout.Title>
        </Layout.HeaderContent>
        <Layout.HeaderActions>
          <buttonBar_1.default gap={1}>
            <feature_1.default organization={organization} features={['incidents']}>
              {({ hasFeature }) => hasFeature && this.renderCreateAlertButton()}
            </feature_1.default>
            {this.renderKeyTransactionButton()}
            {this.renderSettingsButton()}
          </buttonBar_1.default>
        </Layout.HeaderActions>
        <React.Fragment>
          <StyledNavTabs>
            <listLink_1.default to={summaryTarget} isActive={() => currentTab === tabs_1.default.TransactionSummary}>
              {(0, locale_1.t)('Overview')}
            </listLink_1.default>
            {this.renderWebVitalsTab()}
            <feature_1.default features={['organizations:performance-tag-page']}>
              <listLink_1.default to={tagsTarget} isActive={() => currentTab === tabs_1.default.Tags} onClick={this.trackTabClick(tabs_1.default.Tags)}>
                {(0, locale_1.t)('Tags')}
                <featureBadge_1.default type="new" noTooltip/>
              </listLink_1.default>
            </feature_1.default>
            <feature_1.default features={['organizations:performance-events-page']}>
              <listLink_1.default to={eventsTarget} isActive={() => currentTab === tabs_1.default.Events} onClick={this.trackTabClick(tabs_1.default.Events)}>
                {(0, locale_1.t)('All Events')}
              </listLink_1.default>
            </feature_1.default>
            <feature_1.default organization={organization} features={['organizations:performance-suspect-spans-view']}>
              <listLink_1.default data-test-id="spans-tab" to={spansTarget} isActive={() => currentTab === tabs_1.default.Spans} onClick={this.trackTabClick(tabs_1.default.Spans)}>
                {(0, locale_1.t)('Spans')}
              </listLink_1.default>
            </feature_1.default>
          </StyledNavTabs>
        </React.Fragment>
      </Layout.Header>);
    }
}
const StyledNavTabs = (0, styled_1.default)(navTabs_1.default) `
  margin-bottom: 0;
  /* Makes sure the tabs are pushed into another row */
  width: 100%;
`;
exports.default = TransactionHeader;
//# sourceMappingURL=header.jsx.map