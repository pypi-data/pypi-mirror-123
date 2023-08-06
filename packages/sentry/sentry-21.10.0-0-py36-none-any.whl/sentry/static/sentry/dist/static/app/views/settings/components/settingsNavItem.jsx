Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const badge_1 = (0, tslib_1.__importDefault)(require("app/components/badge"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const SettingsNavItem = (_a) => {
    var { badge, label, index, id } = _a, props = (0, tslib_1.__rest)(_a, ["badge", "label", "index", "id"]);
    const LabelHook = (0, hookOrDefault_1.default)({
        hookName: 'sidebar:item-label',
        defaultComponent: ({ children }) => <React.Fragment>{children}</React.Fragment>,
    });
    let renderedBadge;
    if (badge === 'new') {
        renderedBadge = <featureBadge_1.default type="new"/>;
    }
    else if (badge === 'beta') {
        renderedBadge = <featureBadge_1.default type="beta"/>;
    }
    else if (badge === 'warning') {
        renderedBadge = (<tooltip_1.default title={(0, locale_1.t)('This settings needs review')} position="right">
        <StyledBadge text={badge} type="warning"/>
      </tooltip_1.default>);
    }
    else {
        renderedBadge = <StyledBadge text={badge}/>;
    }
    return (<StyledNavItem onlyActiveOnIndex={index} activeClassName="active" {...props}>
      <LabelHook id={id}>{label}</LabelHook>
      {badge ? renderedBadge : null}
    </StyledNavItem>);
};
const StyledNavItem = (0, styled_1.default)(react_router_1.Link) `
  display: block;
  color: ${p => p.theme.gray300};
  font-size: 14px;
  line-height: 30px;
  position: relative;

  &.active {
    color: ${p => p.theme.textColor};

    &:before {
      background: ${p => p.theme.active};
    }
  }

  &:hover,
  &:focus,
  &:active {
    color: ${p => p.theme.textColor};
    outline: none;
  }

  &.focus-visible {
    outline: none;
    background: ${p => p.theme.backgroundSecondary};
    padding-left: 15px;
    margin-left: -15px;
    border-radius: 3px;

    &:before {
      left: -15px;
    }
  }

  &:before {
    position: absolute;
    content: '';
    display: block;
    top: 4px;
    left: -30px;
    height: 20px;
    width: 4px;
    background: transparent;
    border-radius: 0 2px 2px 0;
  }
`;
const StyledBadge = (0, styled_1.default)(badge_1.default) `
  font-weight: 400;
  height: auto;
  line-height: 1;
  font-size: ${p => p.theme.fontSizeExtraSmall};
  padding: 3px ${(0, space_1.default)(0.75)};
`;
exports.default = SettingsNavItem;
//# sourceMappingURL=settingsNavItem.jsx.map