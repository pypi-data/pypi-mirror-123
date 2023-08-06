Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const settingsNavigationGroup_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsNavigationGroup"));
class SettingsNavigation extends React.Component {
    componentDidCatch(error, errorInfo) {
        Sentry.withScope(scope => {
            Object.keys(errorInfo).forEach(key => {
                scope.setExtra(key, errorInfo[key]);
            });
            scope.setExtra('url', window.location.href);
            Sentry.captureException(error);
        });
    }
    render() {
        const _a = this.props, { navigationObjects, hooks, hookConfigs, stickyTop } = _a, otherProps = (0, tslib_1.__rest)(_a, ["navigationObjects", "hooks", "hookConfigs", "stickyTop"]);
        const navWithHooks = navigationObjects.concat(hookConfigs);
        return (<PositionStickyWrapper stickyTop={stickyTop}>
        {navWithHooks.map(config => (<settingsNavigationGroup_1.default key={config.name} {...otherProps} {...config}/>))}
        {hooks.map((Hook, i) => React.cloneElement(Hook, { key: `hook-${i}` }))}
      </PositionStickyWrapper>);
    }
}
SettingsNavigation.defaultProps = {
    hooks: [],
    hookConfigs: [],
    stickyTop: '69px',
};
const PositionStickyWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(4)};
  padding-right: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    position: sticky;
    top: ${p => p.stickyTop};
    overflow: scroll;
    -ms-overflow-style: none;
    scrollbar-width: none;

    &::-webkit-scrollbar {
      display: none;
    }
  }
`;
exports.default = SettingsNavigation;
//# sourceMappingURL=settingsNavigation.jsx.map