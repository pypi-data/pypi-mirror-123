Object.defineProperty(exports, "__esModule", { value: true });
exports.OPEN_DELAY = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_popper_1 = require("react-popper");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const constants_1 = require("app/constants");
const domId_1 = require("app/utils/domId");
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
exports.OPEN_DELAY = 50;
/**
 * How long to wait before closing the tooltip when isHoverable is set
 */
const CLOSE_DELAY = 50;
/**
 * Used to compute the transform origin to give the scale-down micro-animation
 * a pleasant feeling. Without this the animation can feel somewhat 'wrong'.
 */
function computeOriginFromArrow(placement, arrowProps) {
    // XXX: Bottom means the arrow will be pointing up
    switch (placement) {
        case 'top':
            return { originX: `${arrowProps.style.left}px`, originY: '100%' };
        case 'bottom':
            return { originX: `${arrowProps.style.left}px`, originY: 0 };
        case 'left':
            return { originX: '100%', originY: `${arrowProps.style.top}px` };
        case 'right':
            return { originX: 0, originY: `${arrowProps.style.top}px` };
        default:
            return { originX: `50%`, originY: '100%' };
    }
}
class Tooltip extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isOpen: false,
            usesGlobalPortal: true,
        };
        this.tooltipId = (0, domId_1.domId)('tooltip-');
        this.delayTimeout = null;
        this.delayHideTimeout = null;
        this.getPortal = (0, memoize_1.default)((usesGlobalPortal) => {
            if (usesGlobalPortal) {
                let portal = document.getElementById('tooltip-portal');
                if (!portal) {
                    portal = document.createElement('div');
                    portal.setAttribute('id', 'tooltip-portal');
                    document.body.appendChild(portal);
                }
                return portal;
            }
            const portal = document.createElement('div');
            document.body.appendChild(portal);
            return portal;
        });
        this.setOpen = () => {
            this.setState({ isOpen: true });
        };
        this.setClose = () => {
            this.setState({ isOpen: false });
        };
        this.handleOpen = () => {
            const { delay } = this.props;
            if (this.delayHideTimeout) {
                window.clearTimeout(this.delayHideTimeout);
                this.delayHideTimeout = null;
            }
            if (delay === 0) {
                this.setOpen();
                return;
            }
            this.delayTimeout = window.setTimeout(this.setOpen, delay !== null && delay !== void 0 ? delay : exports.OPEN_DELAY);
        };
        this.handleClose = () => {
            const { isHoverable } = this.props;
            if (this.delayTimeout) {
                window.clearTimeout(this.delayTimeout);
                this.delayTimeout = null;
            }
            if (isHoverable) {
                this.delayHideTimeout = window.setTimeout(this.setClose, CLOSE_DELAY);
            }
            else {
                this.setClose();
            }
        };
    }
    componentDidMount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (constants_1.IS_ACCEPTANCE_TEST) {
                const TooltipStore = (yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/stores/tooltipStore')))).default;
                TooltipStore.addTooltip(this);
            }
        });
    }
    componentWillUnmount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { usesGlobalPortal } = this.state;
            if (constants_1.IS_ACCEPTANCE_TEST) {
                const TooltipStore = (yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/stores/tooltipStore')))).default;
                TooltipStore.removeTooltip(this);
            }
            if (!usesGlobalPortal) {
                document.body.removeChild(this.getPortal(usesGlobalPortal));
            }
        });
    }
    renderTrigger(children, ref) {
        const propList = {
            'aria-describedby': this.tooltipId,
            onFocus: this.handleOpen,
            onBlur: this.handleClose,
            onMouseEnter: this.handleOpen,
            onMouseLeave: this.handleClose,
        };
        // Use the `type` property of the react instance to detect whether we
        // have a basic element (type=string) or a class/function component (type=function or object)
        // Because we can't rely on the child element implementing forwardRefs we wrap
        // it with a span tag so that popper has ref
        if (React.isValidElement(children) &&
            (this.props.skipWrapper || typeof children.type === 'string')) {
            // Basic DOM nodes can be cloned and have more props applied.
            return React.cloneElement(children, Object.assign(Object.assign({}, propList), { ref }));
        }
        propList.containerDisplayMode = this.props.containerDisplayMode;
        return (<Container {...propList} className={this.props.className} ref={ref}>
        {children}
      </Container>);
    }
    render() {
        const { disabled, forceShow, children, title, position, popperStyle, isHoverable } = this.props;
        const { isOpen, usesGlobalPortal } = this.state;
        if (disabled || !title) {
            return children;
        }
        const modifiers = {
            hide: { enabled: false },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
            applyStyle: {
                gpuAcceleration: true,
            },
        };
        const visible = forceShow || isOpen;
        const tip = visible ? (<react_popper_1.Popper placement={position} modifiers={modifiers}>
        {({ ref, style, placement, arrowProps }) => {
                var _a;
                return (<PositionWrapper style={style}>
            <TooltipContent id={this.tooltipId} initial={{ opacity: 0 }} animate={{
                        opacity: 1,
                        scale: 1,
                        transition: (0, testableTransition_1.default)({
                            type: 'linear',
                            ease: [0.5, 1, 0.89, 1],
                            duration: 0.2,
                        }),
                    }} exit={{
                        opacity: 0,
                        scale: 0.95,
                        transition: (0, testableTransition_1.default)({ type: 'spring', delay: 0.1 }),
                    }} style={computeOriginFromArrow(position, arrowProps)} transition={{ duration: 0.2 }} className="tooltip-content" aria-hidden={!visible} ref={ref} data-placement={placement} popperStyle={popperStyle} onMouseEnter={() => isHoverable && this.handleOpen()} onMouseLeave={() => isHoverable && this.handleClose()}>
              {title}
              <TooltipArrow ref={arrowProps.ref} data-placement={placement} style={arrowProps.style} background={((_a = popperStyle) === null || _a === void 0 ? void 0 : _a.background) || '#000'}/>
            </TooltipContent>
          </PositionWrapper>);
            }}
      </react_popper_1.Popper>) : null;
        return (<react_popper_1.Manager>
        <react_popper_1.Reference>{({ ref }) => this.renderTrigger(children, ref)}</react_popper_1.Reference>
        {react_dom_1.default.createPortal(<framer_motion_1.AnimatePresence>{tip}</framer_motion_1.AnimatePresence>, this.getPortal(usesGlobalPortal))}
      </react_popper_1.Manager>);
    }
}
Tooltip.defaultProps = {
    position: 'top',
    containerDisplayMode: 'inline-block',
};
// Using an inline-block solves the container being smaller
// than the elements it is wrapping
const Container = (0, styled_1.default)('span') `
  ${p => p.containerDisplayMode && `display: ${p.containerDisplayMode}`};
  max-width: 100%;
`;
const PositionWrapper = (0, styled_1.default)('div') `
  z-index: ${p => p.theme.zIndex.tooltip};
`;
const TooltipContent = (0, styled_1.default)(framer_motion_1.motion.div) `
  will-change: transform, opacity;
  position: relative;
  color: ${p => p.theme.white};
  background: #000;
  opacity: 0.9;
  padding: 5px 10px;
  border-radius: ${p => p.theme.borderRadius};
  overflow-wrap: break-word;
  max-width: 225px;

  font-weight: bold;
  font-size: ${p => p.theme.fontSizeSmall};
  line-height: 1.4;

  margin: 6px;
  text-align: center;
  ${p => p.popperStyle};
`;
const TooltipArrow = (0, styled_1.default)('span') `
  position: absolute;
  width: 10px;
  height: 5px;

  &[data-placement*='bottom'] {
    top: 0;
    left: 0;
    margin-top: -5px;
    &::before {
      border-width: 0 5px 5px 5px;
      border-color: transparent transparent ${p => p.background} transparent;
    }
  }

  &[data-placement*='top'] {
    bottom: 0;
    left: 0;
    margin-bottom: -5px;
    &::before {
      border-width: 5px 5px 0 5px;
      border-color: ${p => p.background} transparent transparent transparent;
    }
  }

  &[data-placement*='right'] {
    left: 0;
    margin-left: -5px;
    &::before {
      border-width: 5px 5px 5px 0;
      border-color: transparent ${p => p.background} transparent transparent;
    }
  }

  &[data-placement*='left'] {
    right: 0;
    margin-right: -5px;
    &::before {
      border-width: 5px 0 5px 5px;
      border-color: transparent transparent transparent ${p => p.background};
    }
  }

  &::before {
    content: '';
    margin: auto;
    display: block;
    width: 0;
    height: 0;
    border-style: solid;
  }
`;
exports.default = Tooltip;
//# sourceMappingURL=tooltip.jsx.map