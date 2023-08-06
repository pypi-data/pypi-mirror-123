Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const builderBreadCrumbs_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/builder/builderBreadCrumbs"));
const details_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/incidentRules/details"));
const issueRuleEditor_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/issueRuleEditor"));
class ProjectAlertsEditor extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            ruleName: '',
        };
        this.handleChangeTitle = (ruleName) => {
            this.setState({ ruleName });
        };
    }
    componentDidMount() {
        const { organization, project } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'edit_alert_rule.viewed',
            eventName: 'Edit Alert Rule: Viewed',
            organization_id: organization.id,
            project_id: project.id,
            alert_type: this.getAlertType(),
        });
    }
    getTitle() {
        const { ruleName } = this.state;
        return `${ruleName}`;
    }
    getAlertType() {
        return location.pathname.includes('/alerts/metric-rules/') ? 'metric' : 'issue';
    }
    render() {
        const { hasMetricAlerts, location, organization, project, routes } = this.props;
        const alertType = this.getAlertType();
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={this.getTitle()} orgSlug={organization.slug} projectSlug={project.slug}/>
        <Layout.Header>
          <Layout.HeaderContent>
            <builderBreadCrumbs_1.default orgSlug={organization.slug} title={(0, locale_1.t)('Edit Alert Rule')} projectSlug={project.slug} routes={routes} location={location}/>
            <Layout.Title>{this.getTitle()}</Layout.Title>
          </Layout.HeaderContent>
        </Layout.Header>
        <EditConditionsBody>
          <Layout.Main fullWidth>
            {(!hasMetricAlerts || alertType === 'issue') && (<issueRuleEditor_1.default {...this.props} project={project} onChangeTitle={this.handleChangeTitle}/>)}
            {hasMetricAlerts && alertType === 'metric' && (<details_1.default {...this.props} project={project} onChangeTitle={this.handleChangeTitle}/>)}
          </Layout.Main>
        </EditConditionsBody>
      </react_1.Fragment>);
    }
}
const EditConditionsBody = (0, styled_1.default)(Layout.Body) `
  margin-bottom: -${(0, space_1.default)(3)};

  *:not(img) {
    max-width: 1000px;
  }
`;
exports.default = ProjectAlertsEditor;
//# sourceMappingURL=edit.jsx.map