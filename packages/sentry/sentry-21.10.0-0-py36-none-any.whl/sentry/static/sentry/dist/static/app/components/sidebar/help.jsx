Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const hook_1 = (0, tslib_1.__importDefault)(require("app/components/hook"));
const sidebarItem_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarItem"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const sidebarDropdownMenu_styled_1 = (0, tslib_1.__importDefault)(require("./sidebarDropdownMenu.styled"));
const sidebarMenuItem_1 = (0, tslib_1.__importDefault)(require("./sidebarMenuItem"));
const SidebarHelp = ({ orientation, collapsed, hidePanel, organization }) => (<dropdownMenu_1.default>
    {({ isOpen, getActorProps, getMenuProps }) => (<HelpRoot>
        <HelpActor {...getActorProps({ onClick: hidePanel })}>
          <sidebarItem_1.default data-test-id="help-sidebar" orientation={orientation} collapsed={collapsed} hasPanel={false} icon={<icons_1.IconQuestion size="md"/>} label={(0, locale_1.t)('Help')} id="help"/>
        </HelpActor>

        {isOpen && (<HelpMenu {...getMenuProps({})}>
            <sidebarMenuItem_1.default data-test-id="search-docs-and-faqs" onClick={() => (0, modal_1.openHelpSearchModal)({ organization })}>
              {(0, locale_1.t)('Search Support, Docs and More')}
            </sidebarMenuItem_1.default>
            <sidebarMenuItem_1.default href="https://help.sentry.io/">
              {(0, locale_1.t)('Visit Help Center')}
            </sidebarMenuItem_1.default>
            <hook_1.default name="sidebar:help-menu" organization={organization}/>
          </HelpMenu>)}
      </HelpRoot>)}
  </dropdownMenu_1.default>);
exports.default = SidebarHelp;
const HelpRoot = (0, styled_1.default)('div') `
  position: relative;
`;
// This exists to provide a styled actor for the dropdown. Making the actor a regular,
// non-styled react component causes some issues with toggling correctly because of
// how refs are handled.
const HelpActor = (0, styled_1.default)('div') ``;
const HelpMenu = (0, styled_1.default)('div') `
  ${sidebarDropdownMenu_styled_1.default};
  bottom: 100%;
`;
//# sourceMappingURL=help.jsx.map