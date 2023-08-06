Object.defineProperty(exports, "__esModule", { value: true });
exports.OwnershipRules = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const sidebarSection_1 = (0, tslib_1.__importDefault)(require("../sidebarSection"));
const OwnershipRules = ({ project, organization, issueId, codeowners, isDismissed, handleCTAClose, }) => {
    const handleOpenCreateOwnershipRule = () => {
        (0, modal_1.openCreateOwnershipRule)({ project, organization, issueId });
    };
    const showCTA = organization.features.includes('integrations-codeowners') &&
        !codeowners.length &&
        !isDismissed;
    const createRuleButton = (<access_1.default access={['project:write']}>
      <guideAnchor_1.default target="owners" position="bottom" offset={(0, space_1.default)(3)}>
        <button_1.default onClick={handleOpenCreateOwnershipRule} size="small">
          {(0, locale_1.t)('Create Ownership Rule')}
        </button_1.default>
      </guideAnchor_1.default>
    </access_1.default>);
    const codeOwnersCTA = (<Container dashedBorder>
      <HeaderContainer>
        <Header>{(0, locale_1.t)('Codeowners sync')}</Header>{' '}
        <featureBadge_1.default style={{ top: -3 }} type="new" noTooltip/>
        <DismissButton icon={<icons_1.IconClose size="xs"/>} priority="link" onClick={() => handleCTAClose()}/>
      </HeaderContainer>
      <Content>
        {(0, locale_1.t)('Import GitHub or GitLab CODEOWNERS files to automatically assign issues to the right people.')}
      </Content>
      <buttonBar_1.default gap={1}>
        <SetupButton size="small" priority="primary" href={`/settings/${organization.slug}/projects/${project.slug}/ownership/`} onClick={() => (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.code_owners_cta_setup_clicked', {
            view: 'stacktrace_issue_details',
            project_id: project.id,
            organization,
        })}>
          {(0, locale_1.t)('Set It Up')}
        </SetupButton>
        <button_1.default size="small" external href="https://docs.sentry.io/product/issues/issue-owners/#code-owners" onClick={() => (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.code_owners_cta_docs_clicked', {
            view: 'stacktrace_issue_details',
            project_id: project.id,
            organization,
        })}>
          {(0, locale_1.t)('Read Docs')}
        </button_1.default>
      </buttonBar_1.default>
    </Container>);
    return (<sidebarSection_1.default title={<react_1.Fragment>
          {(0, locale_1.t)('Ownership Rules')}
          <react_2.ClassNames>
            {({ css }) => (<hovercard_1.default body={<HelpfulBody>
                    <p>
                      {(0, locale_1.t)('Ownership rules allow you to associate file paths and URLs to specific teams or users, so alerts can be routed to the right people.')}
                    </p>
                    <button_1.default href="https://docs.sentry.io/workflow/issue-owners/" priority="primary">
                      {(0, locale_1.t)('Learn more')}
                    </button_1.default>
                  </HelpfulBody>} containerClassName={css `
                  display: flex;
                  align-items: center;
                `}>
                <StyledIconQuestion size="xs"/>
              </hovercard_1.default>)}
          </react_2.ClassNames>
        </react_1.Fragment>}>
      {showCTA ? codeOwnersCTA : createRuleButton}
    </sidebarSection_1.default>);
};
exports.OwnershipRules = OwnershipRules;
const StyledIconQuestion = (0, styled_1.default)(icons_1.IconQuestion) `
  margin-left: ${(0, space_1.default)(0.5)};
`;
const HelpfulBody = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1)};
  text-align: center;
`;
const Container = (0, styled_1.default)(panels_1.Panel) `
  background: none;
  display: flex;
  flex-direction: column;
  padding: ${(0, space_1.default)(2)};
`;
const HeaderContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content max-content 1fr;
  align-items: flex-start;
`;
const Header = (0, styled_1.default)('h6') `
  margin-bottom: ${(0, space_1.default)(1)};
  text-transform: uppercase;
  font-weight: bold;
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeExtraSmall};
`;
const Content = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray500};
  margin-bottom: ${(0, space_1.default)(2)};
`;
const SetupButton = (0, styled_1.default)(button_1.default) `
  &:focus {
    color: ${p => p.theme.white};
  }
`;
const DismissButton = (0, styled_1.default)(button_1.default) `
  justify-self: flex-end;
  color: ${p => p.theme.gray400};
`;
//# sourceMappingURL=ownershipRules.jsx.map