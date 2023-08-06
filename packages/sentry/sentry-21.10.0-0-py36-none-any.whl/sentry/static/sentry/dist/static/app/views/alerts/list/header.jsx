Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const navigation_1 = require("app/actionCreators/navigation");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const createAlertButton_1 = (0, tslib_1.__importDefault)(require("app/components/createAlertButton"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const AlertHeader = ({ router, organization, activeTab }) => {
    /**
     * Incidents list is currently at the organization level, but the link needs to
     * go down to a specific project scope.
     */
    const handleNavigateToSettings = (e) => {
        e.preventDefault();
        (0, navigation_1.navigateTo)(`/settings/${organization.slug}/projects/:projectId/alerts/`, router);
    };
    const alertRulesLink = (<li className={activeTab === 'rules' ? 'active' : ''}>
      <globalSelectionLink_1.default to={`/organizations/${organization.slug}/alerts/rules/`}>
        {(0, locale_1.t)('Alert Rules')}
      </globalSelectionLink_1.default>
    </li>);
    return (<React.Fragment>
      <BorderlessHeader>
        <StyledLayoutHeaderContent>
          <StyledLayoutTitle>{(0, locale_1.t)('Alerts')}</StyledLayoutTitle>
        </StyledLayoutHeaderContent>
        <Layout.HeaderActions>
          <Actions gap={1}>
            <createAlertButton_1.default organization={organization} iconProps={{ size: 'sm' }} priority="primary" referrer="alert_stream" showPermissionGuide>
              {(0, locale_1.t)('Create Alert Rule')}
            </createAlertButton_1.default>
            <button_1.default onClick={handleNavigateToSettings} href="#" icon={<icons_1.IconSettings size="sm"/>} aria-label="Settings"/>
          </Actions>
        </Layout.HeaderActions>
      </BorderlessHeader>
      <TabLayoutHeader>
        <Layout.HeaderNavTabs underlined>
          {alertRulesLink}
          <li className={activeTab === 'stream' ? 'active' : ''}>
            <globalSelectionLink_1.default to={`/organizations/${organization.slug}/alerts/`}>
              {(0, locale_1.t)('History')}
            </globalSelectionLink_1.default>
          </li>
        </Layout.HeaderNavTabs>
      </TabLayoutHeader>
    </React.Fragment>);
};
exports.default = AlertHeader;
const BorderlessHeader = (0, styled_1.default)(Layout.Header) `
  border-bottom: 0;

  /* Not enough buttons to change direction for tablet view */
  grid-template-columns: 1fr auto;
`;
const StyledLayoutHeaderContent = (0, styled_1.default)(Layout.HeaderContent) `
  margin-bottom: 0;
  margin-right: ${(0, space_1.default)(2)};
`;
const StyledLayoutTitle = (0, styled_1.default)(Layout.Title) `
  margin-top: ${(0, space_1.default)(0.5)};
`;
const TabLayoutHeader = (0, styled_1.default)(Layout.Header) `
  padding-top: ${(0, space_1.default)(1)};

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    padding-top: ${(0, space_1.default)(1)};
  }
`;
const Actions = (0, styled_1.default)(buttonBar_1.default) `
  height: 32px;
`;
//# sourceMappingURL=header.jsx.map