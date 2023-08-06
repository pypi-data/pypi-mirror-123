Object.defineProperty(exports, "__esModule", { value: true });
exports.getSidebarPanelContainer = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const animations_1 = require("app/styles/animations");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const PanelContainer = (0, styled_1.default)('div') `
  position: fixed;
  bottom: 0;
  display: flex;
  flex-direction: column;
  background: ${p => p.theme.background};
  color: ${p => p.theme.textColor};
  border-right: 1px solid ${p => p.theme.border};
  box-shadow: 1px 0 2px rgba(0, 0, 0, 0.06);
  text-align: left;
  animation: 200ms ${animations_1.slideInLeft};
  z-index: ${p => p.theme.zIndex.sidebar - 1};

  ${p => p.orientation === 'top'
    ? (0, react_2.css) `
          top: ${p.theme.sidebar.mobileHeight};
          left: 0;
          right: 0;
        `
    : (0, react_2.css) `
          width: 460px;
          top: 0;
          left: ${p.collapsed
        ? p.theme.sidebar.collapsedWidth
        : p.theme.sidebar.expandedWidth};
        `};
`;
/**
 * Get the container element of the sidebar that react portals into.
 */
const getSidebarPanelContainer = () => document.getElementById('sidebar-flyout-portal');
exports.getSidebarPanelContainer = getSidebarPanelContainer;
const makePortal = () => {
    const portal = document.createElement('div');
    portal.setAttribute('id', 'sidebar-flyout-portal');
    document.body.appendChild(portal);
    return portal;
};
function SidebarPanel(_a) {
    var { orientation, collapsed, hidePanel, title, children } = _a, props = (0, tslib_1.__rest)(_a, ["orientation", "collapsed", "hidePanel", "title", "children"]);
    const portalEl = (0, react_1.useRef)((0, exports.getSidebarPanelContainer)() || makePortal());
    (0, react_1.useEffect)(() => {
        document.addEventListener('click', panelCloseHandler);
        return function cleanup() {
            document.removeEventListener('click', panelCloseHandler);
        };
    }, []);
    function panelCloseHandler(evt) {
        if (!(evt.target instanceof Element)) {
            return;
        }
        const panel = (0, exports.getSidebarPanelContainer)();
        if (panel === null || panel === void 0 ? void 0 : panel.contains(evt.target)) {
            return;
        }
        hidePanel();
    }
    const sidebar = (<PanelContainer role="dialog" collapsed={collapsed} orientation={orientation} {...props}>
      {title && (<SidebarPanelHeader>
          <Title>{title}</Title>
          <PanelClose onClick={hidePanel}/>
        </SidebarPanelHeader>)}
      <SidebarPanelBody hasHeader={!!title}>{children}</SidebarPanelBody>
    </PanelContainer>);
    return react_dom_1.default.createPortal(sidebar, portalEl.current);
}
exports.default = SidebarPanel;
const SidebarPanelHeader = (0, styled_1.default)('div') `
  border-bottom: 1px solid ${p => p.theme.border};
  padding: ${(0, space_1.default)(3)};
  background: ${p => p.theme.background};
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 1;
`;
const SidebarPanelBody = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow: auto;
  position: relative;
`;
const PanelClose = (0, styled_1.default)(icons_1.IconClose) `
  color: ${p => p.theme.subText};
  cursor: pointer;
  position: relative;
  padding: ${(0, space_1.default)(0.75)};

  &:hover {
    color: ${p => p.theme.textColor};
  }
`;
PanelClose.defaultProps = {
    size: 'lg',
};
const Title = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  margin: 0;
`;
//# sourceMappingURL=sidebarPanel.jsx.map