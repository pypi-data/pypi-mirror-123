Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const account_1 = require("app/actionCreators/account");
const demoModeGate_1 = (0, tslib_1.__importDefault)(require("app/components/acl/demoModeGate"));
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const hook_1 = (0, tslib_1.__importDefault)(require("app/components/hook"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const sidebarDropdownMenu_styled_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarDropdownMenu.styled"));
const sidebarMenuItem_1 = (0, tslib_1.__importStar)(require("app/components/sidebar/sidebarMenuItem"));
const sidebarOrgSummary_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarOrgSummary"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const divider_styled_1 = (0, tslib_1.__importDefault)(require("./divider.styled"));
const switchOrganization_1 = (0, tslib_1.__importDefault)(require("./switchOrganization"));
const SidebarDropdown = ({ api, org, projects, orientation, collapsed, config, user, hideOrgLinks, }) => {
    var _a, _b, _c;
    const handleLogout = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        yield (0, account_1.logout)(api);
        window.location.assign('/auth/login/');
    });
    const hasOrganization = !!org;
    const hasUser = !!user;
    // It's possible we do not have an org in context (e.g. RouteNotFound)
    // Otherwise, we should have the full org
    const hasOrgRead = (_a = org === null || org === void 0 ? void 0 : org.access) === null || _a === void 0 ? void 0 : _a.includes('org:read');
    const hasMemberRead = (_b = org === null || org === void 0 ? void 0 : org.access) === null || _b === void 0 ? void 0 : _b.includes('member:read');
    const hasTeamRead = (_c = org === null || org === void 0 ? void 0 : org.access) === null || _c === void 0 ? void 0 : _c.includes('team:read');
    const canCreateOrg = configStore_1.default.get('features').has('organizations:create');
    // Avatar to use: Organization --> user --> Sentry
    const avatar = hasOrganization || hasUser ? (<StyledAvatar collapsed={collapsed} organization={org} user={!org ? user : undefined} size={32} round={false}/>) : (<SentryLink to="/">
        <icons_1.IconSentry size="32px"/>
      </SentryLink>);
    return (<dropdownMenu_1.default>
      {({ isOpen, getRootProps, getActorProps, getMenuProps }) => (<SidebarDropdownRoot {...getRootProps()}>
          <SidebarDropdownActor type="button" data-test-id="sidebar-dropdown" {...getActorProps({})}>
            {avatar}
            {!collapsed && orientation !== 'top' && (<OrgAndUserWrapper>
                <OrgOrUserName>
                  {hasOrganization ? org.name : user.name}{' '}
                  <StyledIconChevron color="white" size="xs" direction="down"/>
                </OrgOrUserName>
                <UserNameOrEmail>
                  {hasOrganization ? user.name : user.email}
                </UserNameOrEmail>
              </OrgAndUserWrapper>)}
          </SidebarDropdownActor>

          {isOpen && (<OrgAndUserMenu {...getMenuProps({})}>
              {hasOrganization && (<react_1.Fragment>
                  <sidebarOrgSummary_1.default organization={org} projectCount={projects.length}/>
                  {!hideOrgLinks && (<react_1.Fragment>
                      {hasOrgRead && (<sidebarMenuItem_1.default to={`/settings/${org.slug}/`}>
                          {(0, locale_1.t)('Organization settings')}
                        </sidebarMenuItem_1.default>)}
                      {hasMemberRead && (<sidebarMenuItem_1.default to={`/settings/${org.slug}/members/`}>
                          {(0, locale_1.t)('Members')}
                        </sidebarMenuItem_1.default>)}

                      {hasTeamRead && (<sidebarMenuItem_1.default to={`/settings/${org.slug}/teams/`}>
                          {(0, locale_1.t)('Teams')}
                        </sidebarMenuItem_1.default>)}

                      <hook_1.default name="sidebar:organization-dropdown-menu" organization={org}/>
                    </react_1.Fragment>)}

                  {!config.singleOrganization && (<sidebarMenuItem_1.default>
                      <switchOrganization_1.default canCreateOrganization={canCreateOrg}/>
                    </sidebarMenuItem_1.default>)}
                </react_1.Fragment>)}

              <demoModeGate_1.default>
                {hasOrganization && user && <divider_styled_1.default />}
                {!!user && (<react_1.Fragment>
                    <UserSummary to="/settings/account/details/">
                      <UserBadgeNoOverflow user={user} avatarSize={32}/>
                    </UserSummary>

                    <div>
                      <sidebarMenuItem_1.default to="/settings/account/">
                        {(0, locale_1.t)('User settings')}
                      </sidebarMenuItem_1.default>
                      <sidebarMenuItem_1.default to="/settings/account/api/">
                        {(0, locale_1.t)('API keys')}
                      </sidebarMenuItem_1.default>
                      {hasOrganization && (<hook_1.default name="sidebar:organization-dropdown-menu-bottom" organization={org}/>)}
                      {user.isSuperuser && (<sidebarMenuItem_1.default to="/manage/">{(0, locale_1.t)('Admin')}</sidebarMenuItem_1.default>)}
                      <sidebarMenuItem_1.default data-test-id="sidebar-signout" onClick={handleLogout}>
                        {(0, locale_1.t)('Sign out')}
                      </sidebarMenuItem_1.default>
                    </div>
                  </react_1.Fragment>)}
              </demoModeGate_1.default>
            </OrgAndUserMenu>)}
        </SidebarDropdownRoot>)}
    </dropdownMenu_1.default>);
};
exports.default = (0, withApi_1.default)((0, withProjects_1.default)(SidebarDropdown));
const SentryLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.white};
  &:hover {
    color: ${p => p.theme.white};
  }
`;
const UserSummary = (0, styled_1.default)(link_1.default) `
  ${p => (0, sidebarMenuItem_1.menuItemStyles)(p)}
  padding: 10px 15px;
`;
const UserBadgeNoOverflow = (0, styled_1.default)(idBadge_1.default) `
  overflow: hidden;
`;
const SidebarDropdownRoot = (0, styled_1.default)('div') `
  position: relative;
`;
// So that long org names and user names do not overflow
const OrgAndUserWrapper = (0, styled_1.default)('div') `
  overflow: hidden;
  text-align: left;
`;
const OrgOrUserName = (0, styled_1.default)(textOverflow_1.default) `
  font-size: ${p => p.theme.fontSizeLarge};
  line-height: 1.2;
  font-weight: bold;
  color: ${p => p.theme.white};
  text-shadow: 0 0 6px rgba(255, 255, 255, 0);
  transition: 0.15s text-shadow linear;
`;
const UserNameOrEmail = (0, styled_1.default)(textOverflow_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};
  line-height: 16px;
  transition: 0.15s color linear;
`;
const SidebarDropdownActor = (0, styled_1.default)('button') `
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  border: none;
  padding: 0;
  background: none;
  width: 100%;

  &:hover {
    ${OrgOrUserName} {
      text-shadow: 0 0 6px rgba(255, 255, 255, 0.1);
    }
    ${UserNameOrEmail} {
      color: ${p => p.theme.gray200};
    }
  }
`;
const StyledAvatar = (0, styled_1.default)(avatar_1.default) `
  margin: ${(0, space_1.default)(0.25)} 0;
  margin-right: ${p => (p.collapsed ? '0' : (0, space_1.default)(1.5))};
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.08);
  border-radius: 6px; /* Fixes background bleeding on corners */
`;
const OrgAndUserMenu = (0, styled_1.default)('div') `
  ${sidebarDropdownMenu_styled_1.default};
  top: 42px;
  min-width: 180px;
  z-index: ${p => p.theme.zIndex.orgAndUserMenu};
`;
const StyledIconChevron = (0, styled_1.default)(icons_1.IconChevron) `
  margin-left: ${(0, space_1.default)(0.25)};
`;
//# sourceMappingURL=index.jsx.map