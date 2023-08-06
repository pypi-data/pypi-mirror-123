Object.defineProperty(exports, "__esModule", { value: true });
exports.Icon = exports.ButtonLabel = exports.StyledButton = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const mergeRefs_1 = (0, tslib_1.__importDefault)(require("app/utils/mergeRefs"));
class BaseButton extends React.Component {
    constructor() {
        super(...arguments);
        // Intercept onClick and propagate
        this.handleClick = (e) => {
            const { disabled, busy, onClick } = this.props;
            // Don't allow clicks when disabled or busy
            if (disabled || busy) {
                e.preventDefault();
                e.stopPropagation();
                return;
            }
            if (typeof onClick !== 'function') {
                return;
            }
            onClick(e);
        };
        this.getUrl = (prop) => this.props.disabled ? undefined : prop;
    }
    render() {
        const _a = this.props, { size, to, href, title, icon, children, label, borderless, align, priority, disabled, tooltipProps, 
        // destructure from `buttonProps`
        // not necessary, but just in case someone re-orders props
        onClick: _onClick } = _a, buttonProps = (0, tslib_1.__rest)(_a, ["size", "to", "href", "title", "icon", "children", "label", "borderless", "align", "priority", "disabled", "tooltipProps", "onClick"]);
        // For `aria-label`
        const screenReaderLabel = label || (typeof children === 'string' ? children : undefined);
        // Buttons come in 4 flavors: <Link>, <ExternalLink>, <a>, and <button>.
        // Let's use props to determine which to serve up, so we don't have to think about it.
        // *Note* you must still handle tabindex manually.
        const button = (<StyledButton aria-label={screenReaderLabel} aria-disabled={disabled} disabled={disabled} to={this.getUrl(to)} href={this.getUrl(href)} size={size} priority={priority} borderless={borderless} {...buttonProps} onClick={this.handleClick} role="button">
        <ButtonLabel align={align} size={size} priority={priority} borderless={borderless}>
          {icon && (<Icon size={size} hasChildren={!!children}>
              {icon}
            </Icon>)}
          {children}
        </ButtonLabel>
      </StyledButton>);
        // Doing this instead of using `Tooltip`'s `disabled` prop so that we can minimize snapshot nesting
        if (title) {
            return (<tooltip_1.default skipWrapper={!disabled} {...tooltipProps} title={title}>
          {button}
        </tooltip_1.default>);
        }
        return button;
    }
}
BaseButton.defaultProps = {
    disabled: false,
    align: 'center',
};
const Button = React.forwardRef((props, ref) => (<BaseButton forwardRef={ref} {...props}/>));
Button.displayName = 'Button';
exports.default = Button;
const getFontSize = ({ size, priority, theme }) => {
    if (priority === 'link') {
        return 'inherit';
    }
    switch (size) {
        case 'xsmall':
        case 'small':
            return theme.fontSizeSmall;
        default:
            return theme.fontSizeMedium;
    }
};
const getFontWeight = ({ priority, borderless }) => `font-weight: ${priority === 'link' || borderless ? 'inherit' : 600};`;
const getBoxShadow = (active) => ({ priority, borderless, disabled }) => {
    if (disabled || borderless || priority === 'link') {
        return 'box-shadow: none';
    }
    return `box-shadow: ${active ? 'inset' : ''} 0 2px rgba(0, 0, 0, 0.05)`;
};
const getColors = ({ priority, disabled, borderless, theme }) => {
    const themeName = disabled ? 'disabled' : priority || 'default';
    const { color, colorActive, background, backgroundActive, border, borderActive, focusShadow, } = theme.button[themeName];
    return (0, react_1.css) `
    color: ${color};
    background-color: ${background};
    border: 1px solid
      ${priority !== 'link' && !borderless && !!border ? border : 'transparent'};

    &:hover {
      color: ${color};
    }

    &:hover,
    &:focus,
    &:active {
      color: ${colorActive || color};
      background: ${backgroundActive};
      border-color: ${priority !== 'link' && !borderless && (borderActive || border)
        ? borderActive || border
        : 'transparent'};
    }

    &.focus-visible {
      ${focusShadow && `box-shadow: ${focusShadow} 0 0 0 3px;`}
    }
  `;
};
const StyledButton = (0, styled_1.default)(React.forwardRef((_a, forwardRefAlt) => {
    // XXX: There may be two forwarded refs here, one potentially passed from a
    // wrapped Tooltip, another from callers of Button.
    var { forwardRef, size: _size, external, to, href, disabled } = _a, otherProps = (0, tslib_1.__rest)(_a, ["forwardRef", "size", "external", "to", "href", "disabled"]);
    const ref = (0, mergeRefs_1.default)([forwardRef, forwardRefAlt]);
    // only pass down title to child element if it is a string
    const { title } = otherProps, props = (0, tslib_1.__rest)(otherProps, ["title"]);
    if (typeof title === 'string') {
        props[title] = title;
    }
    // Get component to use based on existence of `to` or `href` properties
    // Can be react-router `Link`, `a`, or `button`
    if (to) {
        return <link_1.default ref={ref} to={to} disabled={disabled} {...props}/>;
    }
    if (!href) {
        return <button ref={ref} disabled={disabled} {...props}/>;
    }
    if (external && href) {
        return <externalLink_1.default ref={ref} href={href} disabled={disabled} {...props}/>;
    }
    return <a ref={ref} {...props} href={href}/>;
}), {
    shouldForwardProp: prop => prop === 'forwardRef' ||
        prop === 'external' ||
        (typeof prop === 'string' && (0, is_prop_valid_1.default)(prop)),
}) `
  display: inline-block;
  line-height: 1;
  border-radius: ${p => p.theme.button.borderRadius};
  padding: 0;
  text-transform: none;
  ${getFontWeight};
  font-size: ${getFontSize};
  ${getColors};
  ${getBoxShadow(false)};
  cursor: ${p => (p.disabled ? 'not-allowed' : 'pointer')};
  opacity: ${p => (p.busy || p.disabled) && '0.65'};

  &:active {
    ${getBoxShadow(true)};
  }
  &:focus {
    outline: none;
  }

  ${p => (p.borderless || p.priority === 'link') && 'border-color: transparent'};
`;
exports.StyledButton = StyledButton;
/**
 * Get label padding determined by size
 */
const getLabelPadding = ({ size, priority, }) => {
    if (priority === 'link') {
        return '0';
    }
    switch (size) {
        case 'zero':
            return '0';
        case 'xsmall':
            return '5px 8px';
        case 'small':
            return '9px 12px';
        default:
            return '12px 16px';
    }
};
const buttonLabelPropKeys = ['size', 'priority', 'borderless', 'align'];
const ButtonLabel = (0, styled_1.default)('span', {
    shouldForwardProp: prop => typeof prop === 'string' && (0, is_prop_valid_1.default)(prop) && !buttonLabelPropKeys.includes(prop),
}) `
  display: grid;
  grid-auto-flow: column;
  align-items: center;
  justify-content: ${p => p.align};
  padding: ${getLabelPadding};
`;
exports.ButtonLabel = ButtonLabel;
const getIconMargin = ({ size, hasChildren }) => {
    // If button is only an icon, then it shouldn't have margin
    if (!hasChildren) {
        return '0';
    }
    return size && size.endsWith('small') ? '6px' : '8px';
};
const Icon = (0, styled_1.default)('span') `
  display: flex;
  align-items: center;
  margin-right: ${getIconMargin};
  height: ${getFontSize};
`;
exports.Icon = Icon;
//# sourceMappingURL=button.jsx.map