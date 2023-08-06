Object.defineProperty(exports, "__esModule", { value: true });
exports.SidebarWrapper = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const queryString = (0, tslib_1.__importStar)(require("query-string"));
const preferences_1 = require("app/actionCreators/preferences");
const sidebarPanelActions_1 = (0, tslib_1.__importDefault)(require("app/actions/sidebarPanelActions"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const preferencesStore_1 = (0, tslib_1.__importDefault)(require("app/stores/preferencesStore"));
const sidebarPanelStore_1 = (0, tslib_1.__importDefault)(require("app/stores/sidebarPanelStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const urls_1 = require("app/utils/discover/urls");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const useMedia_1 = (0, tslib_1.__importDefault)(require("app/utils/useMedia"));
const broadcasts_1 = (0, tslib_1.__importDefault)(require("./broadcasts"));
const help_1 = (0, tslib_1.__importDefault)(require("./help"));
const onboardingStatus_1 = (0, tslib_1.__importDefault)(require("./onboardingStatus"));
const serviceIncidents_1 = (0, tslib_1.__importDefault)(require("./serviceIncidents"));
const sidebarDropdown_1 = (0, tslib_1.__importDefault)(require("./sidebarDropdown"));
const sidebarItem_1 = (0, tslib_1.__importDefault)(require("./sidebarItem"));
const types_1 = require("./types");
const SidebarOverride = (0, hookOrDefault_1.default)({
    hookName: 'sidebar:item-override',
    defaultComponent: ({ children }) => <react_1.Fragment>{children({})}</react_1.Fragment>,
});
function Sidebar({ location, organization }) {
    const config = (0, useLegacyStore_1.useLegacyStore)(configStore_1.default);
    const preferences = (0, useLegacyStore_1.useLegacyStore)(preferencesStore_1.default);
    const activePanel = (0, useLegacyStore_1.useLegacyStore)(sidebarPanelStore_1.default);
    const collapsed = !!preferences.collapsed;
    const horizontal = (0, useMedia_1.default)(`(max-width: ${theme_1.default.breakpoints[1]})`);
    const toggleCollapse = () => {
        const action = collapsed ? preferences_1.showSidebar : preferences_1.hideSidebar;
        action();
    };
    const togglePanel = (panel) => sidebarPanelActions_1.default.togglePanel(panel);
    const hidePanel = () => sidebarPanelActions_1.default.hidePanel();
    const bcl = document.body.classList;
    // Close panel on any navigation
    (0, react_1.useEffect)(() => void hidePanel(), [location === null || location === void 0 ? void 0 : location.pathname]);
    // Add classname to body
    (0, react_1.useEffect)(() => {
        bcl.add('body-sidebar');
        return () => bcl.remove('body-sidebar');
    }, []);
    // Add sidebar collapse classname to body
    (0, react_1.useEffect)(() => {
        if (collapsed) {
            bcl.add('collapsed');
        }
        else {
            bcl.remove('collapsed');
        }
        return () => bcl.remove('collapsed');
    }, [collapsed]);
    // Trigger panels depending on the location hash
    (0, react_1.useEffect)(() => {
        if ((location === null || location === void 0 ? void 0 : location.hash) === '#welcome') {
            togglePanel(types_1.SidebarPanelKey.OnboardingWizard);
        }
    }, [location === null || location === void 0 ? void 0 : location.hash]);
    /**
     * Navigate to a path, but keep the global selection query strings.
     */
    const navigateWithGlobalSelection = (pathname, evt) => {
        const globalSelectionRoutes = [
            'alerts',
            'alerts/rules',
            'dashboards',
            'issues',
            'releases',
            'user-feedback',
            'discover',
            'discover/results',
            'performance',
        ].map(route => `/organizations/${organization === null || organization === void 0 ? void 0 : organization.slug}/${route}/`);
        // Only keep the querystring if the current route matches one of the above
        if (globalSelectionRoutes.includes(pathname)) {
            const query = (0, utils_1.extractSelectionParameters)(location === null || location === void 0 ? void 0 : location.query);
            // Handle cmd-click (mac) and meta-click (linux)
            if (evt.metaKey) {
                const q = queryString.stringify(query);
                evt.currentTarget.href = `${evt.currentTarget.href}?${q}`;
                return;
            }
            evt.preventDefault();
            react_router_1.browserHistory.push({ pathname, query });
        }
    };
    const hasPanel = !!activePanel;
    const hasOrganization = !!organization;
    const orientation = horizontal ? 'top' : 'left';
    const sidebarItemProps = {
        orientation,
        collapsed,
        hasPanel,
    };
    const projects = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} index icon={<icons_1.IconProject size="md"/>} label={<guideAnchor_1.default target="projects">{(0, locale_1.t)('Projects')}</guideAnchor_1.default>} to={`/organizations/${organization.slug}/projects/`} id="projects"/>);
    const issues = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => navigateWithGlobalSelection(`/organizations/${organization.slug}/issues/`, evt)} icon={<icons_1.IconIssues size="md"/>} label={<guideAnchor_1.default target="issues">{(0, locale_1.t)('Issues')}</guideAnchor_1.default>} to={`/organizations/${organization.slug}/issues/`} id="issues"/>);
    const discover2 = hasOrganization && (<feature_1.default hookName="feature-disabled:discover2-sidebar-item" features={['discover-basic']} organization={organization}>
      <sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => navigateWithGlobalSelection((0, urls_1.getDiscoverLandingUrl)(organization), evt)} icon={<icons_1.IconTelescope size="md"/>} label={<guideAnchor_1.default target="discover">{(0, locale_1.t)('Discover')}</guideAnchor_1.default>} to={(0, urls_1.getDiscoverLandingUrl)(organization)} id="discover-v2"/>
    </feature_1.default>);
    const performance = hasOrganization && (<feature_1.default hookName="feature-disabled:performance-sidebar-item" features={['performance-view']} organization={organization}>
      <SidebarOverride id="performance-override">
        {(overideProps) => (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => navigateWithGlobalSelection(`/organizations/${organization.slug}/performance/`, evt)} icon={<icons_1.IconLightning size="md"/>} label={<guideAnchor_1.default target="performance">{(0, locale_1.t)('Performance')}</guideAnchor_1.default>} to={`/organizations/${organization.slug}/performance/`} id="performance" {...overideProps}/>)}
      </SidebarOverride>
    </feature_1.default>);
    const releases = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => navigateWithGlobalSelection(`/organizations/${organization.slug}/releases/`, evt)} icon={<icons_1.IconReleases size="md"/>} label={<guideAnchor_1.default target="releases">{(0, locale_1.t)('Releases')}</guideAnchor_1.default>} to={`/organizations/${organization.slug}/releases/`} id="releases"/>);
    const userFeedback = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => navigateWithGlobalSelection(`/organizations/${organization.slug}/user-feedback/`, evt)} icon={<icons_1.IconSupport size="md"/>} label={(0, locale_1.t)('User Feedback')} to={`/organizations/${organization.slug}/user-feedback/`} id="user-feedback"/>);
    const alerts = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => navigateWithGlobalSelection(`/organizations/${organization.slug}/alerts/rules/`, evt)} icon={<icons_1.IconSiren size="md"/>} label={(0, locale_1.t)('Alerts')} to={`/organizations/${organization.slug}/alerts/rules/`} id="alerts"/>);
    const monitors = hasOrganization && (<feature_1.default features={['monitors']} organization={organization}>
      <sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => navigateWithGlobalSelection(`/organizations/${organization.slug}/monitors/`, evt)} icon={<icons_1.IconLab size="md"/>} label={(0, locale_1.t)('Monitors')} to={`/organizations/${organization.slug}/monitors/`} id="monitors"/>
    </feature_1.default>);
    const dashboards = hasOrganization && (<feature_1.default hookName="feature-disabled:dashboards-sidebar-item" features={['discover', 'discover-query', 'dashboards-basic', 'dashboards-edit']} organization={organization} requireAll={false}>
      <sidebarItem_1.default {...sidebarItemProps} index onClick={(_id, evt) => navigateWithGlobalSelection(`/organizations/${organization.slug}/dashboards/`, evt)} icon={<icons_1.IconGraph size="md"/>} label={(0, locale_1.t)('Dashboards')} to={`/organizations/${organization.slug}/dashboards/`} id="customizable-dashboards" isNew/>
    </feature_1.default>);
    const activity = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} icon={<icons_1.IconActivity size="md"/>} label={(0, locale_1.t)('Activity')} to={`/organizations/${organization.slug}/activity/`} id="activity"/>);
    const stats = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} icon={<icons_1.IconStats size="md"/>} label={(0, locale_1.t)('Stats')} to={`/organizations/${organization.slug}/stats/`} id="stats"/>);
    const settings = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} icon={<icons_1.IconSettings size="md"/>} label={(0, locale_1.t)('Settings')} to={`/settings/${organization.slug}/`} id="settings"/>);
    return (<exports.SidebarWrapper collapsed={collapsed}>
      <SidebarSectionGroupPrimary>
        <SidebarSection>
          <sidebarDropdown_1.default orientation={orientation} collapsed={collapsed} org={organization} user={config.user} config={config}/>
        </SidebarSection>

        <PrimaryItems>
          {hasOrganization && (<react_1.Fragment>
              <SidebarSection>
                {projects}
                {issues}
                {performance}
                {releases}
                {userFeedback}
                {alerts}
                {discover2}
                {dashboards}
              </SidebarSection>

              <SidebarSection>{monitors}</SidebarSection>

              <SidebarSection>
                {activity}
                {stats}
              </SidebarSection>

              <SidebarSection>{settings}</SidebarSection>
            </react_1.Fragment>)}
        </PrimaryItems>
      </SidebarSectionGroupPrimary>

      {hasOrganization && (<SidebarSectionGroup>
          <SidebarSection noMargin noPadding>
            <onboardingStatus_1.default org={organization} currentPanel={activePanel} onShowPanel={() => togglePanel(types_1.SidebarPanelKey.OnboardingWizard)} hidePanel={hidePanel} {...sidebarItemProps}/>
          </SidebarSection>

          <SidebarSection>
            {hookStore_1.default.get('sidebar:bottom-items').length > 0 &&
                hookStore_1.default.get('sidebar:bottom-items')[0](Object.assign({ organization }, sidebarItemProps))}
            <help_1.default orientation={orientation} collapsed={collapsed} hidePanel={hidePanel} organization={organization}/>
            <broadcasts_1.default orientation={orientation} collapsed={collapsed} currentPanel={activePanel} onShowPanel={() => togglePanel(types_1.SidebarPanelKey.Broadcasts)} hidePanel={hidePanel} organization={organization}/>
            <serviceIncidents_1.default orientation={orientation} collapsed={collapsed} currentPanel={activePanel} onShowPanel={() => togglePanel(types_1.SidebarPanelKey.StatusUpdate)} hidePanel={hidePanel}/>
          </SidebarSection>

          {!horizontal && (<SidebarSection>
              <SidebarCollapseItem id="collapse" data-test-id="sidebar-collapse" {...sidebarItemProps} icon={<StyledIconChevron collapsed={collapsed}/>} label={collapsed ? (0, locale_1.t)('Expand') : (0, locale_1.t)('Collapse')} onClick={toggleCollapse}/>
            </SidebarSection>)}
        </SidebarSectionGroup>)}
    </exports.SidebarWrapper>);
}
exports.default = Sidebar;
const responsiveFlex = (0, react_2.css) `
  display: flex;
  flex-direction: column;

  @media (max-width: ${theme_1.default.breakpoints[1]}) {
    flex-direction: row;
  }
`;
exports.SidebarWrapper = (0, styled_1.default)('nav') `
  background: ${p => p.theme.sidebar.background};
  background: ${p => p.theme.sidebarGradient};
  color: ${p => p.theme.sidebar.color};
  line-height: 1;
  padding: 12px 0 2px; /* Allows for 32px avatars  */
  width: ${p => p.theme.sidebar.expandedWidth};
  position: fixed;
  top: ${p => (configStore_1.default.get('demoMode') ? p.theme.demo.headerSize : 0)};
  left: 0;
  bottom: 0;
  justify-content: space-between;
  z-index: ${p => p.theme.zIndex.sidebar};
  ${responsiveFlex};
  ${p => p.collapsed && `width: ${p.theme.sidebar.collapsedWidth};`};

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    top: 0;
    left: 0;
    right: 0;
    height: ${p => p.theme.sidebar.mobileHeight};
    bottom: auto;
    width: auto;
    padding: 0 ${(0, space_1.default)(1)};
    align-items: center;
  }
`;
const SidebarSectionGroup = (0, styled_1.default)('div') `
  ${responsiveFlex};
  flex-shrink: 0; /* prevents shrinking on Safari */
`;
const SidebarSectionGroupPrimary = (0, styled_1.default)('div') `
  ${responsiveFlex};
  /* necessary for child flexing on msedge and ff */
  min-height: 0;
  min-width: 0;
  flex: 1;
  /* expand to fill the entire height on mobile */
  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    height: 100%;
    align-items: center;
  }
`;
const PrimaryItems = (0, styled_1.default)('div') `
  overflow: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  -ms-overflow-style: -ms-autohiding-scrollbar;
  @media (max-height: 675px) and (min-width: ${p => p.theme.breakpoints[1]}) {
    border-bottom: 1px solid ${p => p.theme.gray400};
    padding-bottom: ${(0, space_1.default)(1)};
    box-shadow: rgba(0, 0, 0, 0.15) 0px -10px 10px inset;
    &::-webkit-scrollbar {
      background-color: transparent;
      width: 8px;
    }
    &::-webkit-scrollbar-thumb {
      background: ${p => p.theme.gray400};
      border-radius: 8px;
    }
  }
  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    overflow-y: visible;
    flex-direction: row;
    height: 100%;
    align-items: center;
    border-right: 1px solid ${p => p.theme.gray400};
    padding-right: ${(0, space_1.default)(1)};
    margin-right: ${(0, space_1.default)(0.5)};
    box-shadow: rgba(0, 0, 0, 0.15) -10px 0px 10px inset;
    ::-webkit-scrollbar {
      display: none;
    }
  }
`;
const SidebarSection = (0, styled_1.default)(SidebarSectionGroup) `
  ${p => !p.noMargin && `margin: ${(0, space_1.default)(1)} 0`};
  ${p => !p.noPadding && 'padding: 0 19px'};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    margin: 0;
    padding: 0;
  }

  &:empty {
    display: none;
  }
`;
const ExpandedIcon = (0, react_2.css) `
  transition: 0.3s transform ease;
  transform: rotate(270deg);
`;
const CollapsedIcon = (0, react_2.css) `
  transform: rotate(90deg);
`;
const StyledIconChevron = (0, styled_1.default)((_a) => {
    var { collapsed } = _a, props = (0, tslib_1.__rest)(_a, ["collapsed"]);
    return (<icons_1.IconChevron direction="left" size="md" isCircled css={[ExpandedIcon, collapsed && CollapsedIcon]} {...props}/>);
}) ``;
const SidebarCollapseItem = (0, styled_1.default)(sidebarItem_1.default) `
  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    display: none;
  }
`;
//# sourceMappingURL=index.jsx.map