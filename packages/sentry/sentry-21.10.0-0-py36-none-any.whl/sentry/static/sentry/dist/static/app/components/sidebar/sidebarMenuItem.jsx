Object.defineProperty(exports, "__esModule", { value: true });
exports.menuItemStyles = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const sidebarMenuItemLink_1 = (0, tslib_1.__importDefault)(require("./sidebarMenuItemLink"));
const sidebarOrgSummary_1 = require("./sidebarOrgSummary");
const SidebarMenuItem = (_a) => {
    var { to, children, href } = _a, props = (0, tslib_1.__rest)(_a, ["to", "children", "href"]);
    const hasMenu = !to && !href;
    return (<StyledSidebarMenuItemLink to={to} href={href} {...props}>
      <MenuItemLabel hasMenu={hasMenu}>{children}</MenuItemLabel>
    </StyledSidebarMenuItemLink>);
};
const menuItemStyles = (p) => (0, react_1.css) `
  color: ${p.theme.textColor};
  cursor: pointer;
  display: flex;
  font-size: ${p.theme.fontSizeMedium};
  line-height: 32px;
  padding: 0 ${p.theme.sidebar.menuSpacing};
  position: relative;
  transition: 0.1s all linear;
  ${(!!p.to || !!p.href) && 'overflow: hidden'};

  &:hover,
  &:active,
  &.focus-visible {
    background: ${p.theme.backgroundSecondary};
    color: ${p.theme.textColor};
    outline: none;
  }

  ${sidebarOrgSummary_1.OrgSummary} {
    padding-left: 0;
    padding-right: 0;
  }
`;
exports.menuItemStyles = menuItemStyles;
const MenuItemLabel = (0, styled_1.default)('span') `
  flex: 1;
  ${p => p.hasMenu
    ? (0, react_1.css) `
          margin: 0 -${p.theme.sidebar.menuSpacing};
          padding: 0 ${p.theme.sidebar.menuSpacing};
        `
    : (0, react_1.css) `
          overflow: hidden;
        `};
`;
const StyledSidebarMenuItemLink = (0, styled_1.default)(sidebarMenuItemLink_1.default) `
  ${menuItemStyles}
`;
exports.default = SidebarMenuItem;
//# sourceMappingURL=sidebarMenuItem.jsx.map