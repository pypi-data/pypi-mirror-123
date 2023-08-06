Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const createAlertButton_1 = (0, tslib_1.__importDefault)(require("app/components/createAlertButton"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const panels_1 = require("app/components/panels");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const builderBreadCrumbs_1 = (0, tslib_1.__importDefault)(require("app/views/alerts/builder/builderBreadCrumbs"));
const types_1 = require("app/views/alerts/incidentRules/types");
const options_1 = require("./options");
const radioPanelGroup_1 = (0, tslib_1.__importDefault)(require("./radioPanelGroup"));
const DEFAULT_ALERT_OPTION = 'issues';
class AlertWizard extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            alertOption: DEFAULT_ALERT_OPTION,
        };
        this.handleChangeAlertOption = (alertOption) => {
            const { organization } = this.props;
            this.setState({ alertOption });
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'alert_wizard.option_viewed',
                eventName: 'Alert Wizard: Option Viewed',
                organization_id: organization.id,
                alert_type: alertOption,
            });
        };
    }
    componentDidMount() {
        // capture landing on the alert wizard page and viewing the issue alert by default
        const { organization } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'alert_wizard.option_viewed',
            eventName: 'Alert Wizard: Option Viewed',
            organization_id: organization.id,
            alert_type: DEFAULT_ALERT_OPTION,
        });
    }
    renderCreateAlertButton() {
        var _a;
        const { organization, location, params: { projectId }, } = this.props;
        const { alertOption } = this.state;
        const metricRuleTemplate = options_1.AlertWizardRuleTemplates[alertOption];
        const isMetricAlert = !!metricRuleTemplate;
        const isTransactionDataset = (metricRuleTemplate === null || metricRuleTemplate === void 0 ? void 0 : metricRuleTemplate.dataset) === types_1.Dataset.TRANSACTIONS;
        const to = {
            pathname: `/organizations/${organization.slug}/alerts/${projectId}/new/`,
            query: Object.assign(Object.assign({}, (metricRuleTemplate && metricRuleTemplate)), { createFromWizard: true, referrer: (_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.referrer }),
        };
        const noFeatureMessage = (0, locale_1.t)('Requires incidents feature.');
        const renderNoAccess = p => (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
        {p.children(p)}
      </hovercard_1.default>);
        return (<feature_1.default features={isTransactionDataset
                ? ['incidents', 'performance-view']
                : isMetricAlert
                    ? ['incidents']
                    : []} requireAll organization={organization} hookName="feature-disabled:alert-wizard-performance" renderDisabled={renderNoAccess}>
        {({ hasFeature }) => (<WizardButtonContainer onClick={() => (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'alert_wizard.option_selected',
                    eventName: 'Alert Wizard: Option Selected',
                    organization_id: organization.id,
                    alert_type: alertOption,
                })}>
            <createAlertButton_1.default organization={organization} projectSlug={projectId} disabled={!hasFeature} priority="primary" to={to} hideIcon>
              {(0, locale_1.t)('Set Conditions')}
            </createAlertButton_1.default>
          </WizardButtonContainer>)}
      </feature_1.default>);
    }
    render() {
        const { organization, params: { projectId }, routes, location, } = this.props;
        const { alertOption } = this.state;
        const title = (0, locale_1.t)('Alert Creation Wizard');
        const panelContent = options_1.AlertWizardPanelContent[alertOption];
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} projectSlug={projectId}/>

        <Layout.Header>
          <StyledHeaderContent>
            <builderBreadCrumbs_1.default orgSlug={organization.slug} projectSlug={projectId} title={(0, locale_1.t)('Select Alert')} routes={routes} location={location} canChangeProject/>
            <Layout.Title>{(0, locale_1.t)('Select Alert')}</Layout.Title>
          </StyledHeaderContent>
        </Layout.Header>
        <StyledLayoutBody>
          <Layout.Main fullWidth>
            <WizardBody>
              <WizardOptions>
                <CategoryTitle>{(0, locale_1.t)('Errors')}</CategoryTitle>
                {(0, options_1.getAlertWizardCategories)(organization).map(({ categoryHeading, options }, i) => (<OptionsWrapper key={categoryHeading}>
                      {i > 0 && <CategoryTitle>{categoryHeading}</CategoryTitle>}
                      <radioPanelGroup_1.default choices={options.map(alertType => {
                    return [alertType, options_1.AlertWizardAlertNames[alertType]];
                })} onChange={this.handleChangeAlertOption} value={alertOption} label="alert-option"/>
                    </OptionsWrapper>))}
              </WizardOptions>
              <WizardPanel visible={!!panelContent && !!alertOption}>
                <WizardPanelBody>
                  <div>
                    <panels_1.PanelHeader>{options_1.AlertWizardAlertNames[alertOption]}</panels_1.PanelHeader>
                    <panels_1.PanelBody withPadding>
                      <PanelDescription>
                        {panelContent.description}{' '}
                        {panelContent.docsLink && (<externalLink_1.default href={panelContent.docsLink}>
                            {(0, locale_1.t)('Learn more')}
                          </externalLink_1.default>)}
                      </PanelDescription>
                      <WizardImage src={panelContent.illustration}/>
                      <ExampleHeader>{(0, locale_1.t)('Examples')}</ExampleHeader>
                      <ExampleList symbol="bullet">
                        {panelContent.examples.map((example, i) => (<ExampleItem key={i}>{example}</ExampleItem>))}
                      </ExampleList>
                    </panels_1.PanelBody>
                  </div>
                  <WizardFooter>{this.renderCreateAlertButton()}</WizardFooter>
                </WizardPanelBody>
              </WizardPanel>
            </WizardBody>
          </Layout.Main>
        </StyledLayoutBody>
      </react_1.Fragment>);
    }
}
const StyledLayoutBody = (0, styled_1.default)(Layout.Body) `
  margin-bottom: -${(0, space_1.default)(3)};
`;
const StyledHeaderContent = (0, styled_1.default)(Layout.HeaderContent) `
  overflow: visible;
`;
const CategoryTitle = (0, styled_1.default)('h2') `
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeExtraLarge};
  margin-bottom: ${(0, space_1.default)(1)} !important;
`;
const WizardBody = (0, styled_1.default)('div') `
  display: flex;
  padding-top: ${(0, space_1.default)(1)};
`;
const WizardOptions = (0, styled_1.default)('div') `
  flex: 3;
  margin-right: ${(0, space_1.default)(3)};
  padding-right: ${(0, space_1.default)(3)};
  max-width: 300px;
`;
const WizardImage = (0, styled_1.default)('img') `
  max-height: 300px;
`;
const WizardPanel = (0, styled_1.default)(panels_1.Panel) `
  max-width: 700px;
  position: sticky;
  top: 20px;
  flex: 5;
  display: flex;
  ${p => !p.visible && 'visibility: hidden'};
  flex-direction: column;
  align-items: start;
  align-self: flex-start;
  ${p => p.visible && 'animation: 0.6s pop ease forwards'};

  @keyframes pop {
    0% {
      transform: translateY(30px);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }
`;
const ExampleList = (0, styled_1.default)(list_1.default) `
  margin-bottom: ${(0, space_1.default)(2)} !important;
`;
const WizardPanelBody = (0, styled_1.default)(panels_1.PanelBody) `
  flex: 1;
  min-width: 100%;
`;
const PanelDescription = (0, styled_1.default)('p') `
  margin-bottom: ${(0, space_1.default)(2)};
`;
const ExampleHeader = (0, styled_1.default)('div') `
  margin: 0 0 ${(0, space_1.default)(1)} 0;
  font-size: ${p => p.theme.fontSizeLarge};
`;
const ExampleItem = (0, styled_1.default)(listItem_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};
`;
const OptionsWrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(4)};

  &:last-child {
    margin-bottom: 0;
  }
`;
const WizardFooter = (0, styled_1.default)('div') `
  border-top: 1px solid ${p => p.theme.border};
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(1.5)} ${(0, space_1.default)(1.5)} ${(0, space_1.default)(1.5)};
`;
const WizardButtonContainer = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
`;
exports.default = AlertWizard;
//# sourceMappingURL=index.jsx.map