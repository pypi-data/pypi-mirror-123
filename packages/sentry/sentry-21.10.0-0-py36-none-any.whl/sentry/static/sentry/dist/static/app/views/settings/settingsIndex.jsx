Object.defineProperty(exports, "__esModule", { value: true });
exports.SettingsIndex = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const organizations_1 = require("app/actionCreators/organizations");
const demoModeGate_1 = (0, tslib_1.__importDefault)(require("app/components/acl/demoModeGate"));
const organizationAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/organizationAvatar"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const withLatestContext_1 = (0, tslib_1.__importDefault)(require("app/utils/withLatestContext"));
const settingsLayout_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsLayout"));
const LINKS = {
    DOCUMENTATION: 'https://docs.sentry.io/',
    DOCUMENTATION_PLATFORMS: 'https://docs.sentry.io/clients/',
    DOCUMENTATION_QUICKSTART: 'https://docs.sentry.io/platform-redirect/?next=/',
    DOCUMENTATION_CLI: 'https://docs.sentry.io/product/cli/',
    DOCUMENTATION_API: 'https://docs.sentry.io/api/',
    API: '/settings/account/api/',
    MANAGE: '/manage/',
    FORUM: 'https://forum.sentry.io/',
    GITHUB_ISSUES: 'https://github.com/getsentry/sentry/issues',
    SERVICE_STATUS: 'https://status.sentry.io/',
};
const HOME_ICON_SIZE = 56;
const flexCenter = (0, react_1.css) `
  display: flex;
  flex-direction: column;
  align-items: center;
`;
class SettingsIndex extends React.Component {
    componentDidUpdate(prevProps) {
        const { organization } = this.props;
        if (prevProps.organization === organization) {
            return;
        }
        // if there is no org in context, SidebarDropdown uses an org from `withLatestContext`
        // (which queries the org index endpoint instead of org details)
        // and does not have `access` info
        if (organization && typeof organization.access === 'undefined') {
            (0, organizations_1.fetchOrganizationDetails)(organization.slug, {
                setActive: true,
                loadProjects: true,
            });
        }
    }
    render() {
        const { organization } = this.props;
        const user = configStore_1.default.get('user');
        const isOnPremise = configStore_1.default.get('isOnPremise');
        const organizationSettingsUrl = (organization && `/settings/${organization.slug}/`) || '';
        const supportLinkProps = {
            isOnPremise,
            href: LINKS.FORUM,
            to: `${organizationSettingsUrl}support`,
        };
        const supportText = isOnPremise ? (0, locale_1.t)('Community Forums') : (0, locale_1.t)('Contact Support');
        return (<react_document_title_1.default title={organization ? `${organization.slug} Settings` : 'Settings'}>
        <settingsLayout_1.default {...this.props}>
          <GridLayout>
            <demoModeGate_1.default>
              <GridPanel>
                <HomePanelHeader>
                  <HomeLinkIcon to="/settings/account/">
                    <AvatarContainer>
                      <userAvatar_1.default user={user} size={HOME_ICON_SIZE}/>
                    </AvatarContainer>
                    {(0, locale_1.t)('My Account')}
                  </HomeLinkIcon>
                </HomePanelHeader>

                <HomePanelBody>
                  <h3>{(0, locale_1.t)('Quick links')}:</h3>
                  <ul>
                    <li>
                      <HomeLink to="/settings/account/security/">
                        {(0, locale_1.t)('Change my password')}
                      </HomeLink>
                    </li>
                    <li>
                      <HomeLink to="/settings/account/notifications/">
                        {(0, locale_1.t)('Notification Preferences')}
                      </HomeLink>
                    </li>
                    <li>
                      <HomeLink to="/settings/account/">{(0, locale_1.t)('Change my avatar')}</HomeLink>
                    </li>
                  </ul>
                </HomePanelBody>
              </GridPanel>
            </demoModeGate_1.default>

            {/* if admin */}
            <GridPanel>
              {!organization && <loadingIndicator_1.default overlay hideSpinner/>}
              <HomePanelHeader>
                <HomeLinkIcon to={organizationSettingsUrl}>
                  {organization ? (<AvatarContainer>
                      <organizationAvatar_1.default organization={organization} size={HOME_ICON_SIZE}/>
                    </AvatarContainer>) : (<HomeIcon color="green300">
                      <icons_1.IconStack size="lg"/>
                    </HomeIcon>)}
                  <OrganizationName>
                    {organization ? organization.slug : (0, locale_1.t)('No Organization')}
                  </OrganizationName>
                </HomeLinkIcon>
              </HomePanelHeader>
              <HomePanelBody>
                <h3>{(0, locale_1.t)('Quick links')}:</h3>
                <ul>
                  <li>
                    <HomeLink to={`${organizationSettingsUrl}projects/`}>
                      {(0, locale_1.t)('Projects')}
                    </HomeLink>
                  </li>
                  <li>
                    <HomeLink to={`${organizationSettingsUrl}teams/`}>
                      {(0, locale_1.t)('Teams')}
                    </HomeLink>
                  </li>
                  <li>
                    <HomeLink to={`${organizationSettingsUrl}members/`}>
                      {(0, locale_1.t)('Members')}
                    </HomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            <GridPanel>
              <HomePanelHeader>
                <ExternalHomeLink isCentered href={LINKS.DOCUMENTATION}>
                  <HomeIcon color="orange400">
                    <icons_1.IconDocs size="lg"/>
                  </HomeIcon>
                </ExternalHomeLink>
                <ExternalHomeLink href={LINKS.DOCUMENTATION}>
                  {(0, locale_1.t)('Documentation')}
                </ExternalHomeLink>
              </HomePanelHeader>

              <HomePanelBody>
                <h3>{(0, locale_1.t)('Quick links')}:</h3>
                <ul>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENTATION_QUICKSTART}>
                      {(0, locale_1.t)('Quickstart Guide')}
                    </ExternalHomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENTATION_PLATFORMS}>
                      {(0, locale_1.t)('Platforms & Frameworks')}
                    </ExternalHomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENTATION_CLI}>
                      {(0, locale_1.t)('Sentry CLI')}
                    </ExternalHomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            <GridPanel>
              <HomePanelHeader>
                <SupportLinkComponent isCentered {...supportLinkProps}>
                  <HomeIcon color="purple300">
                    <icons_1.IconSupport size="lg"/>
                  </HomeIcon>
                  {(0, locale_1.t)('Support')}
                </SupportLinkComponent>
              </HomePanelHeader>

              <HomePanelBody>
                <h3>{(0, locale_1.t)('Quick links')}:</h3>
                <ul>
                  <li>
                    <SupportLinkComponent {...supportLinkProps}>
                      {supportText}
                    </SupportLinkComponent>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.GITHUB_ISSUES}>
                      {(0, locale_1.t)('Sentry on GitHub')}
                    </ExternalHomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.SERVICE_STATUS}>
                      {(0, locale_1.t)('Service Status')}
                    </ExternalHomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            <demoModeGate_1.default>
              <GridPanel>
                <HomePanelHeader>
                  <HomeLinkIcon to={LINKS.API}>
                    <HomeIcon>
                      <icons_1.IconLock size="lg"/>
                    </HomeIcon>
                    {(0, locale_1.t)('API Keys')}
                  </HomeLinkIcon>
                </HomePanelHeader>

                <HomePanelBody>
                  <h3>{(0, locale_1.t)('Quick links')}:</h3>
                  <ul>
                    <li>
                      <HomeLink to={LINKS.API}>{(0, locale_1.t)('Auth Tokens')}</HomeLink>
                    </li>
                    <li>
                      <HomeLink to={`${organizationSettingsUrl}developer-settings/`}>
                        {(0, locale_1.t)('Your Integrations')}
                      </HomeLink>
                    </li>
                    <li>
                      <ExternalHomeLink href={LINKS.DOCUMENTATION_API}>
                        {(0, locale_1.t)('Documentation')}
                      </ExternalHomeLink>
                    </li>
                  </ul>
                </HomePanelBody>
              </GridPanel>
            </demoModeGate_1.default>
          </GridLayout>
        </settingsLayout_1.default>
      </react_document_title_1.default>);
    }
}
exports.SettingsIndex = SettingsIndex;
exports.default = (0, withLatestContext_1.default)(SettingsIndex);
const HomePanelHeader = (0, styled_1.default)(panels_1.PanelHeader) `
  background: ${p => p.theme.background};
  flex-direction: column;
  text-align: center;
  justify-content: center;
  font-size: 18px;
  text-transform: unset;
  padding: 35px 30px;
`;
const HomePanelBody = (0, styled_1.default)(panels_1.PanelBody) `
  padding: 30px;

  h3 {
    font-size: 14px;
  }

  ul {
    margin: 0;
    li {
      line-height: 1.6;
      /* Bullet color */
      color: ${p => p.theme.gray200};
    }
  }
`;
const HomeIcon = (0, styled_1.default)('div') `
  background: ${p => p.theme[p.color || 'gray300']};
  color: ${p => p.theme.white};
  width: ${HOME_ICON_SIZE}px;
  height: ${HOME_ICON_SIZE}px;
  border-radius: ${HOME_ICON_SIZE}px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
`;
const HomeLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.purple300};

  &:hover {
    color: ${p => p.theme.purple300};
  }
`;
const HomeLinkIcon = (0, styled_1.default)(HomeLink) `
  overflow: hidden;
  width: 100%;
  ${flexCenter};
`;
const ExternalHomeLink = (0, styled_1.default)((props) => (<externalLink_1.default {...(0, omit_1.default)(props, 'isCentered')}/>)) `
  color: ${p => p.theme.purple300};

  &:hover {
    color: ${p => p.theme.purple300};
  }

  ${p => p.isCentered && flexCenter};
`;
const SupportLinkComponent = (_a) => {
    var { isCentered, isOnPremise, href, to } = _a, props = (0, tslib_1.__rest)(_a, ["isCentered", "isOnPremise", "href", "to"]);
    return isOnPremise ? (<ExternalHomeLink isCentered={isCentered} href={href} {...props}/>) : (<HomeLink to={to} {...props}/>);
};
const AvatarContainer = (0, styled_1.default)('div') `
  margin-bottom: 20px;
`;
const OrganizationName = (0, styled_1.default)('div') `
  line-height: 1.1em;

  ${overflowEllipsis_1.default};
`;
const GridLayout = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-gap: 16px;
`;
const GridPanel = (0, styled_1.default)(panels_1.Panel) `
  margin-bottom: 0;
`;
//# sourceMappingURL=settingsIndex.jsx.map