Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const animations_1 = require("app/styles/animations");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const settingsBreadcrumb_1 = (0, tslib_1.__importDefault)(require("./settingsBreadcrumb"));
const settingsHeader_1 = (0, tslib_1.__importDefault)(require("./settingsHeader"));
const settingsSearch_1 = (0, tslib_1.__importDefault)(require("./settingsSearch"));
class SettingsLayout extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            navVisible: false,
            navOffsetTop: 0,
        };
        this.headerRef = React.createRef();
    }
    componentDidMount() {
        // Close the navigation when navigating.
        this.unlisten = react_router_1.browserHistory.listen(() => this.toggleNav(false));
    }
    componentWillUnmount() {
        this.unlisten();
    }
    toggleNav(navVisible) {
        var _a, _b;
        // when the navigation is opened, body should be scroll-locked
        this.toggleBodyScrollLock(navVisible);
        this.setState({
            navOffsetTop: (_b = (_a = this.headerRef.current) === null || _a === void 0 ? void 0 : _a.getBoundingClientRect().bottom) !== null && _b !== void 0 ? _b : 0,
            navVisible,
        });
    }
    toggleBodyScrollLock(lock) {
        const bodyElement = document.getElementsByTagName('body')[0];
        if (window.scrollTo) {
            window.scrollTo(0, 0);
        }
        bodyElement.classList[lock ? 'add' : 'remove']('scroll-lock');
    }
    render() {
        const { params, routes, route, renderNavigation, children } = this.props;
        const { navVisible, navOffsetTop } = this.state;
        // We want child's view's props
        const childProps = children && React.isValidElement(children) ? children.props : this.props;
        const childRoutes = childProps.routes || routes || [];
        const childRoute = childProps.route || route || {};
        const shouldRenderNavigation = typeof renderNavigation === 'function';
        return (<SettingsColumn>
        <settingsHeader_1.default ref={this.headerRef}>
          <HeaderContent>
            {shouldRenderNavigation && (<NavMenuToggle priority="link" label={(0, locale_1.t)('Open the menu')} icon={navVisible ? <icons_1.IconClose aria-hidden/> : <icons_1.IconMenu aria-hidden/>} onClick={() => this.toggleNav(!navVisible)}/>)}
            <StyledSettingsBreadcrumb params={params} routes={childRoutes} route={childRoute}/>
            <settingsSearch_1.default />
          </HeaderContent>
        </settingsHeader_1.default>

        <MaxWidthContainer>
          {shouldRenderNavigation && (<SidebarWrapper isVisible={navVisible} offsetTop={navOffsetTop}>
              {renderNavigation()}
            </SidebarWrapper>)}
          <NavMask isVisible={navVisible} onClick={() => this.toggleNav(false)}/>
          <Content>{children}</Content>
        </MaxWidthContainer>
      </SettingsColumn>);
    }
}
const SettingsColumn = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  flex: 1; /* so this stretches vertically so that footer is fixed at bottom */
  min-width: 0; /* fixes problem when child content stretches beyond layout width */
  footer {
    margin-top: 0;
  }
`;
const HeaderContent = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
`;
const NavMenuToggle = (0, styled_1.default)(button_1.default) `
  display: none;
  margin: -${(0, space_1.default)(1)} ${(0, space_1.default)(1)} -${(0, space_1.default)(1)} -${(0, space_1.default)(1)};
  padding: ${(0, space_1.default)(1)};
  color: ${p => p.theme.subText};
  &:hover,
  &:focus,
  &:active {
    color: ${p => p.theme.textColor};
  }
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
  }
`;
const StyledSettingsBreadcrumb = (0, styled_1.default)(settingsBreadcrumb_1.default) `
  flex: 1;
`;
const MaxWidthContainer = (0, styled_1.default)('div') `
  display: flex;
  max-width: ${p => p.theme.settings.containerWidth};
  flex: 1;
`;
const SidebarWrapper = (0, styled_1.default)('div') `
  flex-shrink: 0;
  width: ${p => p.theme.settings.sidebarWidth};
  background: ${p => p.theme.background};
  border-right: 1px solid ${p => p.theme.border};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: ${p => (p.isVisible ? 'block' : 'none')};
    position: fixed;
    top: ${p => p.offsetTop}px;
    bottom: 0;
    overflow-y: auto;
    animation: ${animations_1.slideInLeft} 100ms ease-in-out;
    z-index: ${p => p.theme.zIndex.settingsSidebarNav};
    box-shadow: ${p => p.theme.dropShadowHeavy};
  }
`;
const NavMask = (0, styled_1.default)('div') `
  display: none;
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: ${p => (p.isVisible ? 'block' : 'none')};
    background: rgba(0, 0, 0, 0.35);
    height: 100%;
    width: 100%;
    position: absolute;
    z-index: ${p => p.theme.zIndex.settingsSidebarNavMask};
    animation: ${animations_1.fadeIn} 250ms ease-in-out;
  }
`;
/**
 * Note: `overflow: hidden` will cause some buttons in `SettingsPageHeader` to be cut off because it has negative margin.
 * Will also cut off tooltips.
 */
const Content = (0, styled_1.default)('div') `
  flex: 1;
  padding: ${(0, space_1.default)(4)};
  min-width: 0; /* keep children from stretching container */
`;
exports.default = SettingsLayout;
//# sourceMappingURL=settingsLayout.jsx.map