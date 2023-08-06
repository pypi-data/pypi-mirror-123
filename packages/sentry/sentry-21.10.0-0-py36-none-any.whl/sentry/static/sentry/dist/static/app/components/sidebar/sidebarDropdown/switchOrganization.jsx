Object.defineProperty(exports, "__esModule", { value: true });
exports.SwitchOrganization = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const sidebarDropdownMenu_styled_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarDropdownMenu.styled"));
const sidebarMenuItem_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarMenuItem"));
const sidebarOrgSummary_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarOrgSummary"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganizations_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganizations"));
const divider_styled_1 = (0, tslib_1.__importDefault)(require("./divider.styled"));
/**
 * Switch Organization Menu Label + Sub Menu
 */
const SwitchOrganization = ({ organizations, canCreateOrganization }) => (<dropdownMenu_1.default isNestedDropdown>
    {({ isOpen, getMenuProps, getActorProps }) => (<react_1.Fragment>
        <SwitchOrganizationMenuActor data-test-id="sidebar-switch-org" {...getActorProps({})} onClick={e => {
            // This overwrites `DropdownMenu.getActorProps.onClick` which normally handles clicks on actor
            // to toggle visibility of menu. Instead, do nothing because it is nested and we only want it
            // to appear when hovered on. Will also stop menu from closing when clicked on (which seems to be common
            // behavior);
            // Stop propagation so that dropdown menu doesn't close here
            e.stopPropagation();
        }}>
          {(0, locale_1.t)('Switch organization')}

          <SubMenuCaret>
            <icons_1.IconChevron size="xs" direction="right"/>
          </SubMenuCaret>
        </SwitchOrganizationMenuActor>

        {isOpen && (<SwitchOrganizationMenu data-test-id="sidebar-switch-org-menu" {...getMenuProps({})}>
            <OrganizationList>
              {organizations.map(organization => {
                const url = `/organizations/${organization.slug}/`;
                return (<sidebarMenuItem_1.default key={organization.slug} to={url}>
                    <sidebarOrgSummary_1.default organization={organization}/>
                  </sidebarMenuItem_1.default>);
            })}
            </OrganizationList>
            {organizations && !!organizations.length && canCreateOrganization && (<divider_styled_1.default css={{ marginTop: 0 }}/>)}
            {canCreateOrganization && (<sidebarMenuItem_1.default data-test-id="sidebar-create-org" to="/organizations/new/" style={{ alignItems: 'center' }}>
                <MenuItemLabelWithIcon>
                  <StyledIconAdd />
                  <span>{(0, locale_1.t)('Create a new organization')}</span>
                </MenuItemLabelWithIcon>
              </sidebarMenuItem_1.default>)}
          </SwitchOrganizationMenu>)}
      </react_1.Fragment>)}
  </dropdownMenu_1.default>);
exports.SwitchOrganization = SwitchOrganization;
const SwitchOrganizationContainer = (0, withOrganizations_1.default)(SwitchOrganization);
exports.default = SwitchOrganizationContainer;
const StyledIconAdd = (0, styled_1.default)(icons_1.IconAdd) `
  margin-right: ${(0, space_1.default)(1)};
  color: ${p => p.theme.gray300};
`;
const MenuItemLabelWithIcon = (0, styled_1.default)('span') `
  line-height: 1;
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(1)} 0;
`;
const SubMenuCaret = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray300};
  transition: 0.1s color linear;

  &:hover,
  &:active {
    color: ${p => p.theme.subText};
  }
`;
// Menu Item in dropdown to "Switch organization"
const SwitchOrganizationMenuActor = (0, styled_1.default)('span') `
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0 -${p => p.theme.sidebar.menuSpacing};
  padding: 0 ${p => p.theme.sidebar.menuSpacing};
`;
const SwitchOrganizationMenu = (0, styled_1.default)('div') `
  ${sidebarDropdownMenu_styled_1.default};
  top: 0;
  left: 256px;
`;
const OrganizationList = (0, styled_1.default)('div') `
  max-height: 350px;
  overflow-y: auto;
`;
//# sourceMappingURL=switchOrganization.jsx.map