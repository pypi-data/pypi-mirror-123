Object.defineProperty(exports, "__esModule", { value: true });
exports.Content = exports.DropdownItem = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dropdownBubble_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownBubble"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
/*
 * A higher level dropdown component that helps with building complete dropdowns
 * including the button + menu options. Use the `button` or `label` prop to set
 * the button content and `children` to provide menu options.
 */
class DropdownControl extends React.Component {
    renderButton(isOpen, getActorProps) {
        const { label, button, buttonProps, buttonTooltipTitle, priority } = this.props;
        if (button) {
            return button({ isOpen, getActorProps });
        }
        if (buttonTooltipTitle && !isOpen) {
            return (<tooltip_1.default skipWrapper position="top" title={buttonTooltipTitle}>
          <StyledDropdownButton priority={priority} {...getActorProps(buttonProps)} isOpen={isOpen}>
            {label}
          </StyledDropdownButton>
        </tooltip_1.default>);
        }
        return (<StyledDropdownButton priority={priority} {...getActorProps(buttonProps)} isOpen={isOpen}>
        {label}
      </StyledDropdownButton>);
    }
    renderChildren(isOpen, getMenuProps) {
        const { children, alignRight, menuWidth, blendWithActor, priority } = this.props;
        if (typeof children === 'function') {
            return children({ isOpen, getMenuProps });
        }
        const alignMenu = alignRight ? 'right' : 'left';
        return (<Content {...getMenuProps()} priority={priority} alignMenu={alignMenu} width={menuWidth} isOpen={isOpen} blendWithActor={blendWithActor} blendCorner>
        {children}
      </Content>);
    }
    render() {
        const { alwaysRenderMenu, className } = this.props;
        return (<Container className={className}>
        <dropdownMenu_1.default alwaysRenderMenu={alwaysRenderMenu}>
          {({ isOpen, getMenuProps, getActorProps }) => (<React.Fragment>
              {this.renderButton(isOpen, getActorProps)}
              {this.renderChildren(isOpen, getMenuProps)}
            </React.Fragment>)}
        </dropdownMenu_1.default>
      </Container>);
    }
}
DropdownControl.defaultProps = {
    alwaysRenderMenu: true,
    menuWidth: '100%',
};
const Container = (0, styled_1.default)('div') `
  display: inline-block;
  position: relative;
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  z-index: ${p => p.theme.zIndex.dropdownAutocomplete.actor};
  white-space: nowrap;
`;
const Content = (0, styled_1.default)(dropdownBubble_1.default) `
  display: ${p => (p.isOpen ? 'block' : 'none')};
  border-color: ${p => p.theme.button[p.priority || 'form'].border};
`;
exports.Content = Content;
const DropdownItem = (0, styled_1.default)(menuItem_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};
`;
exports.DropdownItem = DropdownItem;
exports.default = DropdownControl;
//# sourceMappingURL=dropdownControl.jsx.map