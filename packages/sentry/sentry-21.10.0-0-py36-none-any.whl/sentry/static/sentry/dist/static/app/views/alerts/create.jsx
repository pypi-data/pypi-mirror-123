Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const guid_1 = require("app/utils/guid");
const builderBreadCrumbs_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/builder/builderBreadCrumbs"));
const create_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/create"));
const issueRuleEditor_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/issueRuleEditor"));
const options_1 = require("app/views/alerts/wizard/options");
const utils_1 = require("app/views/alerts/wizard/utils");
class Create extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        /** Used to track analytics within one visit to the creation page */
        this.sessionId = (0, guid_1.uniqueId)();
    }
    getInitialState() {
        var _a;
        const { organization, location, project } = this.props;
        const { createFromDiscover, createFromWizard, aggregate, dataset, eventTypes } = (_a = location === null || location === void 0 ? void 0 : location.query) !== null && _a !== void 0 ? _a : {};
        let alertType = 'issue';
        // Alerts can only be created via create from discover or alert wizard
        if (createFromDiscover) {
            alertType = 'metric';
        }
        else if (createFromWizard) {
            if (aggregate && dataset && eventTypes) {
                alertType = 'metric';
            }
            else {
                // Just to be explicit
                alertType = 'issue';
            }
        }
        else {
            react_router_1.browserHistory.replace(`/organizations/${organization.slug}/alerts/${project.slug}/wizard`);
        }
        return { alertType };
    }
    componentDidMount() {
        const { organization, project } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'new_alert_rule.viewed',
            eventName: 'New Alert Rule: Viewed',
            organization_id: organization.id,
            project_id: project.id,
            session_id: this.sessionId,
            alert_type: this.state.alertType,
        });
    }
    render() {
        var _a;
        const { hasMetricAlerts, organization, project, params: { projectId }, location, routes, } = this.props;
        const { alertType } = this.state;
        const { aggregate, dataset, eventTypes, createFromWizard, createFromDiscover } = (_a = location === null || location === void 0 ? void 0 : location.query) !== null && _a !== void 0 ? _a : {};
        const wizardTemplate = { aggregate, dataset, eventTypes };
        const eventView = createFromDiscover ? eventView_1.default.fromLocation(location) : undefined;
        let wizardAlertType;
        if (createFromWizard && alertType === 'metric') {
            wizardAlertType = wizardTemplate
                ? (0, utils_1.getAlertTypeFromAggregateDataset)(wizardTemplate)
                : 'issues';
        }
        const title = (0, locale_1.t)('New Alert Rule');
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} projectSlug={projectId}/>

        <Layout.Header>
          <StyledHeaderContent>
            <builderBreadCrumbs_1.default orgSlug={organization.slug} alertName={(0, locale_1.t)('Set Conditions')} title={wizardAlertType ? (0, locale_1.t)('Select Alert') : title} projectSlug={projectId} routes={routes} location={location} canChangeProject/>
            <Layout.Title>
              {wizardAlertType
                ? `${(0, locale_1.t)('Set Conditions for')} ${options_1.AlertWizardAlertNames[wizardAlertType]}`
                : title}
            </Layout.Title>
          </StyledHeaderContent>
        </Layout.Header>
        <AlertConditionsBody>
          <StyledLayoutMain fullWidth>
            {(!hasMetricAlerts || alertType === 'issue') && (<issueRuleEditor_1.default {...this.props} project={project}/>)}

            {hasMetricAlerts && alertType === 'metric' && (<create_1.default {...this.props} eventView={eventView} wizardTemplate={wizardTemplate} sessionId={this.sessionId} project={project} isCustomMetric={wizardAlertType === 'custom'}/>)}
          </StyledLayoutMain>
        </AlertConditionsBody>
      </react_1.Fragment>);
    }
}
const AlertConditionsBody = (0, styled_1.default)(Layout.Body) `
  margin-bottom: -${(0, space_1.default)(3)};
`;
const StyledLayoutMain = (0, styled_1.default)(Layout.Main) `
  max-width: 1000px;
`;
const StyledHeaderContent = (0, styled_1.default)(Layout.HeaderContent) `
  overflow: visible;
`;
exports.default = Create;
//# sourceMappingURL=create.jsx.map