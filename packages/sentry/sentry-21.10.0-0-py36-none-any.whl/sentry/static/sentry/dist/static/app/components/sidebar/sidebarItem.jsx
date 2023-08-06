Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const LabelHook = (0, hookOrDefault_1.default)({
    hookName: 'sidebar:item-label',
    defaultComponent: ({ children }) => <React.Fragment>{children}</React.Fragment>,
});
const SidebarItem = (_a) => {
    var _b, _c;
    var { router, id, href, to, icon, label, badge, active, hasPanel, isNew, isBeta, collapsed, className, orientation, isNewSeenKeySuffix, onClick } = _a, props = (0, tslib_1.__rest)(_a, ["router", "id", "href", "to", "icon", "label", "badge", "active", "hasPanel", "isNew", "isBeta", "collapsed", "className", "orientation", "isNewSeenKeySuffix", "onClick"]);
    // label might be wrapped in a guideAnchor
    let labelString = label;
    if (React.isValidElement(label)) {
        labelString = (_c = (_b = label === null || label === void 0 ? void 0 : label.props) === null || _b === void 0 ? void 0 : _b.children) !== null && _c !== void 0 ? _c : label;
    }
    // If there is no active panel open and if path is active according to react-router
    const isActiveRouter = (!hasPanel && router && to && location.pathname.startsWith(to)) ||
        (labelString === 'Discover' && location.pathname.includes('/discover/')) ||
        (labelString === 'Dashboards' &&
            (location.pathname.includes('/dashboards/') ||
                location.pathname.includes('/dashboard/'))) ||
        // TODO: this won't be necessary once we remove settingsHome
        (labelString === 'Settings' && location.pathname.startsWith('/settings/')) ||
        (labelString === 'Alerts' &&
            location.pathname.includes('/alerts/') &&
            !location.pathname.startsWith('/settings/'));
    const isActive = active || isActiveRouter;
    const isTop = orientation === 'top';
    const placement = isTop ? 'bottom' : 'right';
    const seenSuffix = isNewSeenKeySuffix !== null && isNewSeenKeySuffix !== void 0 ? isNewSeenKeySuffix : '';
    const isNewSeenKey = `sidebar-new-seen:${id}${seenSuffix}`;
    const showIsNew = isNew && !localStorage_1.default.getItem(isNewSeenKey);
    return (<tooltip_1.default disabled={!collapsed} title={label} position={placement}>
      <StyledSidebarItem data-test-id={props['data-test-id']} id={`sidebar-item-${id}`} active={isActive ? 'true' : undefined} to={(to ? to : href) || '#'} className={className} onClick={(event) => {
            !(to || href) && event.preventDefault();
            onClick === null || onClick === void 0 ? void 0 : onClick(id, event);
            showIsNew && localStorage_1.default.setItem(isNewSeenKey, 'true');
        }}>
        <SidebarItemWrapper>
          <SidebarItemIcon>{icon}</SidebarItemIcon>
          {!collapsed && !isTop && (<SidebarItemLabel>
              <LabelHook id={id}>
                <textOverflow_1.default>{label}</textOverflow_1.default>
                {showIsNew && <featureBadge_1.default type="new" noTooltip/>}
                {isBeta && <featureBadge_1.default type="beta" noTooltip/>}
              </LabelHook>
            </SidebarItemLabel>)}
          {collapsed && showIsNew && <CollapsedFeatureBadge type="new"/>}
          {collapsed && isBeta && <CollapsedFeatureBadge type="beta"/>}
          {badge !== undefined && badge > 0 && (<SidebarItemBadge collapsed={collapsed}>{badge}</SidebarItemBadge>)}
        </SidebarItemWrapper>
      </StyledSidebarItem>
    </tooltip_1.default>);
};
exports.default = (0, react_router_1.withRouter)(SidebarItem);
const getActiveStyle = ({ active, theme }) => {
    if (!active) {
        return '';
    }
    return (0, react_1.css) `
    color: ${theme === null || theme === void 0 ? void 0 : theme.white};

    &:active,
    &:focus,
    &:hover {
      color: ${theme === null || theme === void 0 ? void 0 : theme.white};
    }

    &:before {
      background-color: ${theme === null || theme === void 0 ? void 0 : theme.active};
    }
  `;
};
const StyledSidebarItem = (0, styled_1.default)(link_1.default) `
  display: flex;
  color: inherit;
  position: relative;
  cursor: pointer;
  font-size: 15px;
  line-height: 32px;
  height: 34px;
  flex-shrink: 0;

  transition: 0.15s color linear;

  &:before {
    display: block;
    content: '';
    position: absolute;
    top: 4px;
    left: -20px;
    bottom: 6px;
    width: 5px;
    border-radius: 0 3px 3px 0;
    background-color: transparent;
    transition: 0.15s background-color linear;
  }

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    margin: 0 4px;

    &:before {
      top: auto;
      left: 5px;
      bottom: -10px;
      height: 5px;
      width: auto;
      right: 5px;
      border-radius: 3px 3px 0 0;
    }
  }

  &:hover,
  &:focus {
    color: ${p => p.theme.gray200};
  }

  &.focus-visible {
    outline: none;
    background: #584c66;
    padding: 0 19px;
    margin: 0 -19px;

    &:before {
      left: 0;
    }
  }

  ${getActiveStyle};
`;
const SidebarItemWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  width: 100%;
`;
const SidebarItemIcon = (0, styled_1.default)('span') `
  content: '';
  display: inline-flex;
  width: 32px;
  height: 22px;
  font-size: 20px;
  align-items: center;
  flex-shrink: 0;

  svg {
    display: block;
    margin: 0 auto;
  }
`;
const SidebarItemLabel = (0, styled_1.default)('span') `
  margin-left: 12px;
  white-space: nowrap;
  opacity: 1;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;
const getCollapsedBadgeStyle = ({ collapsed, theme }) => {
    if (!collapsed) {
        return '';
    }
    return (0, react_1.css) `
    text-indent: -99999em;
    position: absolute;
    right: 0;
    top: 1px;
    background: ${theme.red300};
    width: ${theme.sidebar.smallBadgeSize};
    height: ${theme.sidebar.smallBadgeSize};
    border-radius: ${theme.sidebar.smallBadgeSize};
    line-height: ${theme.sidebar.smallBadgeSize};
    box-shadow: 0 3px 3px ${theme.sidebar.background};
  `;
};
const SidebarItemBadge = (0, styled_1.default)((_a) => {
    var { collapsed: _ } = _a, props = (0, tslib_1.__rest)(_a, ["collapsed"]);
    return <span {...props}/>;
}) `
  display: block;
  text-align: center;
  color: ${p => p.theme.white};
  font-size: 12px;
  background: ${p => p.theme.red300};
  width: ${p => p.theme.sidebar.badgeSize};
  height: ${p => p.theme.sidebar.badgeSize};
  border-radius: ${p => p.theme.sidebar.badgeSize};
  line-height: ${p => p.theme.sidebar.badgeSize};

  ${getCollapsedBadgeStyle};
`;
const CollapsedFeatureBadge = (0, styled_1.default)(featureBadge_1.default) `
  position: absolute;
  top: 0;
  right: 0;
`;
CollapsedFeatureBadge.defaultProps = {
    variant: 'indicator',
    noTooltip: true,
};
//# sourceMappingURL=sidebarItem.jsx.map