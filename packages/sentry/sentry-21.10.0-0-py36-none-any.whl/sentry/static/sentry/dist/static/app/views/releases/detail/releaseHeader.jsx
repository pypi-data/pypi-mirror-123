Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const badge_1 = (0, tslib_1.__importDefault)(require("app/components/badge"));
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const listLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/listLink"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
const releaseActions_1 = (0, tslib_1.__importDefault)(require("./releaseActions"));
const ReleaseHeader = ({ location, organization, release, project, releaseMeta, refetchData, }) => {
    const { version, url } = release;
    const { commitCount, commitFilesChanged } = releaseMeta;
    const releasePath = `/organizations/${organization.slug}/releases/${encodeURIComponent(version)}/`;
    const tabs = [
        { title: (0, locale_1.t)('Overview'), to: '' },
        {
            title: (<react_1.Fragment>
          {(0, locale_1.t)('Commits')} <NavTabsBadge text={(0, formatters_1.formatAbbreviatedNumber)(commitCount)}/>
        </react_1.Fragment>),
            to: `commits/`,
        },
        {
            title: (<react_1.Fragment>
          {(0, locale_1.t)('Files Changed')}
          <NavTabsBadge text={(0, formatters_1.formatAbbreviatedNumber)(commitFilesChanged)}/>
        </react_1.Fragment>),
            to: `files-changed/`,
        },
    ];
    const getTabUrl = (path) => ({
        pathname: releasePath + path,
        query: (0, pick_1.default)(location.query, Object.values(globalSelectionHeader_1.URL_PARAM)),
    });
    const getActiveTabTo = () => {
        // We are not doing strict version check because there would be a tiny page shift when switching between releases with paginator
        const activeTab = tabs
            .filter(tab => tab.to.length) // remove home 'Overview' from consideration
            .find(tab => location.pathname.endsWith(tab.to));
        if (activeTab) {
            return activeTab.to;
        }
        return tabs[0].to; // default to 'Overview'
    };
    return (<Layout.Header>
      <Layout.HeaderContent>
        <breadcrumbs_1.default crumbs={[
            {
                to: `/organizations/${organization.slug}/releases/`,
                label: (0, locale_1.t)('Releases'),
                preserveGlobalSelection: true,
            },
            { label: (0, locale_1.t)('Release Details') },
        ]}/>
        <Layout.Title>
          <ReleaseName>
            <idBadge_1.default project={project} avatarSize={28} hideName/>
            <StyledVersion version={version} anchor={false} truncate/>
            <IconWrapper>
              <clipboard_1.default value={version}>
                <tooltip_1.default title={version} containerDisplayMode="flex">
                  <icons_1.IconCopy />
                </tooltip_1.default>
              </clipboard_1.default>
            </IconWrapper>
            {!!url && (<IconWrapper>
                <tooltip_1.default title={url}>
                  <externalLink_1.default href={url}>
                    <icons_1.IconOpen />
                  </externalLink_1.default>
                </tooltip_1.default>
              </IconWrapper>)}
          </ReleaseName>
        </Layout.Title>
      </Layout.HeaderContent>

      <Layout.HeaderActions>
        <releaseActions_1.default organization={organization} projectSlug={project.slug} release={release} releaseMeta={releaseMeta} refetchData={refetchData} location={location}/>
      </Layout.HeaderActions>

      <react_1.Fragment>
        <StyledNavTabs>
          {tabs.map(tab => (<listLink_1.default key={tab.to} to={getTabUrl(tab.to)} isActive={() => getActiveTabTo() === tab.to}>
              {tab.title}
            </listLink_1.default>))}
        </StyledNavTabs>
      </react_1.Fragment>
    </Layout.Header>);
};
const ReleaseName = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const StyledVersion = (0, styled_1.default)(version_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
const IconWrapper = (0, styled_1.default)('span') `
  transition: color 0.3s ease-in-out;
  margin-left: ${(0, space_1.default)(1)};

  &,
  a {
    color: ${p => p.theme.gray300};
    display: flex;
    &:hover {
      cursor: pointer;
      color: ${p => p.theme.textColor};
    }
  }
`;
const StyledNavTabs = (0, styled_1.default)(navTabs_1.default) `
  margin-bottom: 0;
  /* Makes sure the tabs are pushed into another row */
  width: 100%;
`;
const NavTabsBadge = (0, styled_1.default)(badge_1.default) `
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: none;
  }
`;
exports.default = ReleaseHeader;
//# sourceMappingURL=releaseHeader.jsx.map