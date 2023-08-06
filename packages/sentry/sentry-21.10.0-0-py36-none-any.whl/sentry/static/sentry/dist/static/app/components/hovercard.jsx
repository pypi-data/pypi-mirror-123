Object.defineProperty(exports, "__esModule", { value: true });
exports.Hovercard = exports.Header = exports.Body = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_popper_1 = require("react-popper");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const animations_1 = require("app/styles/animations");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const domId_1 = require("app/utils/domId");
const VALID_DIRECTIONS = ['top', 'bottom', 'left', 'right'];
class Hovercard extends React.Component {
    constructor(args) {
        super(args);
        this.state = {
            visible: false,
        };
        this.hoverWait = null;
        this.handleToggleOn = () => this.toggleHovercard(true);
        this.handleToggleOff = () => this.toggleHovercard(false);
        this.toggleHovercard = (visible) => {
            const { displayTimeout } = this.props;
            if (this.hoverWait) {
                clearTimeout(this.hoverWait);
            }
            this.hoverWait = window.setTimeout(() => this.setState({ visible }), displayTimeout);
        };
        let portal = document.getElementById('hovercard-portal');
        if (!portal) {
            portal = document.createElement('div');
            portal.setAttribute('id', 'hovercard-portal');
            document.body.appendChild(portal);
        }
        this.portalEl = portal;
        this.tooltipId = (0, domId_1.domId)('hovercard-');
        this.scheduleUpdate = null;
    }
    componentDidUpdate(prevProps) {
        var _a;
        const { body, header } = this.props;
        if (body !== prevProps.body || header !== prevProps.header) {
            // We had a problem with popper not recalculating position when body/header changed while hovercard still opened.
            // This can happen for example when showing a loading spinner in a hovercard and then changing it to the actual content once fetch finishes.
            (_a = this.scheduleUpdate) === null || _a === void 0 ? void 0 : _a.call(this);
        }
    }
    render() {
        const { bodyClassName, containerClassName, className, header, body, position, show, tipColor, tipBorderColor, offset, modifiers, } = this.props;
        // Maintain the hovercard class name for BC with less styles
        const cx = (0, classnames_1.default)('hovercard', className);
        const popperModifiers = Object.assign({ hide: {
                enabled: false,
            }, preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            } }, (modifiers || {}));
        const visible = show !== undefined ? show : this.state.visible;
        const hoverProps = show !== undefined
            ? {}
            : { onMouseEnter: this.handleToggleOn, onMouseLeave: this.handleToggleOff };
        return (<react_popper_1.Manager>
        <react_popper_1.Reference>
          {({ ref }) => (<span ref={ref} aria-describedby={this.tooltipId} className={containerClassName} {...hoverProps}>
              {this.props.children}
            </span>)}
        </react_popper_1.Reference>
        {visible &&
                (header || body) &&
                react_dom_1.default.createPortal(<react_popper_1.Popper placement={position} modifiers={popperModifiers}>
              {({ ref, style, placement, arrowProps, scheduleUpdate }) => {
                        this.scheduleUpdate = scheduleUpdate;
                        return (<StyledHovercard id={this.tooltipId} visible={visible} ref={ref} style={style} placement={placement} offset={offset} className={cx} {...hoverProps}>
                    {header && <Header>{header}</Header>}
                    {body && <Body className={bodyClassName}>{body}</Body>}
                    <HovercardArrow ref={arrowProps.ref} style={arrowProps.style} placement={placement} tipColor={tipColor} tipBorderColor={tipBorderColor}/>
                  </StyledHovercard>);
                    }}
            </react_popper_1.Popper>, this.portalEl)}
      </react_popper_1.Manager>);
    }
}
exports.Hovercard = Hovercard;
Hovercard.defaultProps = {
    displayTimeout: 100,
    position: 'top',
};
// Slide in from the same direction as the placement
// so that the card pops into place.
const slideIn = (p) => (0, react_1.keyframes) `
  from {
    ${p.placement === 'top' ? 'top: -10px;' : ''}
    ${p.placement === 'bottom' ? 'top: 10px;' : ''}
    ${p.placement === 'left' ? 'left: -10px;' : ''}
    ${p.placement === 'right' ? 'left: 10px;' : ''}
  }
  to {
    ${p.placement === 'top' ? 'top: 0;' : ''}
    ${p.placement === 'bottom' ? 'top: 0;' : ''}
    ${p.placement === 'left' ? 'left: 0;' : ''}
    ${p.placement === 'right' ? 'left: 0;' : ''}
  }
`;
const getTipDirection = (p) => VALID_DIRECTIONS.includes(p.placement) ? p.placement : 'top';
const getOffset = (p) => { var _a; return (_a = p.offset) !== null && _a !== void 0 ? _a : (0, space_1.default)(2); };
const StyledHovercard = (0, styled_1.default)('div') `
  border-radius: ${p => p.theme.borderRadius};
  text-align: left;
  padding: 0;
  line-height: 1;
  /* Some hovercards overlap the toplevel header and sidebar, and we need to appear on top */
  z-index: ${p => p.theme.zIndex.hovercard};
  white-space: initial;
  color: ${p => p.theme.textColor};
  border: 1px solid ${p => p.theme.border};
  background: ${p => p.theme.background};
  background-clip: padding-box;
  box-shadow: 0 0 35px 0 rgba(67, 62, 75, 0.2);
  width: 295px;

  /* The hovercard may appear in different contexts, don't inherit fonts */
  font-family: ${p => p.theme.text.family};

  position: absolute;
  visibility: ${p => (p.visible ? 'visible' : 'hidden')};

  animation: ${animations_1.fadeIn} 100ms, ${slideIn} 100ms ease-in-out;
  animation-play-state: ${p => (p.visible ? 'running' : 'paused')};

  /* Offset for the arrow */
  ${p => (p.placement === 'top' ? `margin-bottom: ${getOffset(p)}` : '')};
  ${p => (p.placement === 'bottom' ? `margin-top: ${getOffset(p)}` : '')};
  ${p => (p.placement === 'left' ? `margin-right: ${getOffset(p)}` : '')};
  ${p => (p.placement === 'right' ? `margin-left: ${getOffset(p)}` : '')};
`;
const Header = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  background: ${p => p.theme.backgroundSecondary};
  border-bottom: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadiusTop};
  font-weight: 600;
  word-wrap: break-word;
  padding: ${(0, space_1.default)(1.5)};
`;
exports.Header = Header;
const Body = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
  min-height: 30px;
`;
exports.Body = Body;
const HovercardArrow = (0, styled_1.default)('span') `
  position: absolute;
  width: 20px;
  height: 20px;
  z-index: -1;

  ${p => (p.placement === 'top' ? 'bottom: -20px; left: 0' : '')};
  ${p => (p.placement === 'bottom' ? 'top: -20px; left: 0' : '')};
  ${p => (p.placement === 'left' ? 'right: -20px' : '')};
  ${p => (p.placement === 'right' ? 'left: -20px' : '')};

  &::before,
  &::after {
    content: '';
    margin: auto;
    position: absolute;
    display: block;
    width: 0;
    height: 0;
    top: 0;
    left: 0;
  }

  /* before element is the hairline border, it is repositioned for each orientation */
  &::before {
    top: 1px;
    border: 10px solid transparent;
    border-${getTipDirection}-color: ${p => p.tipBorderColor || p.tipColor || p.theme.border};

    ${p => (p.placement === 'bottom' ? 'top: -1px' : '')};
    ${p => (p.placement === 'left' ? 'top: 0; left: 1px;' : '')};
    ${p => (p.placement === 'right' ? 'top: 0; left: -1px' : '')};
  }
  &::after {
    border: 10px solid transparent;
    border-${getTipDirection}-color: ${p => p.tipColor || (p.placement === 'bottom' ? p.theme.backgroundSecondary : p.theme.white)};
  }
`;
exports.default = Hovercard;
//# sourceMappingURL=hovercard.jsx.map