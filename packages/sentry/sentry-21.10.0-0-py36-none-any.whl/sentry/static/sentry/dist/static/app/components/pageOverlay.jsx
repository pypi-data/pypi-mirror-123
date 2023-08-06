Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const text_1 = (0, tslib_1.__importDefault)(require("app/components/text"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
/**
 * The default wrapper for the detail text.
 *
 * This can be overridden using the `customWrapper` prop for when the overlay
 * needs some special sizing due to background illustration constraints.
 */
const DefaultWrapper = (0, styled_1.default)('div') `
  width: 500px;
`;
const subItemAnimation = {
    initial: {
        opacity: 0,
        x: 60,
    },
    animate: {
        opacity: 1,
        x: 0,
        transition: (0, testableTransition_1.default)({
            type: 'spring',
            duration: 0.4,
        }),
    },
};
const Header = (0, styled_1.default)(framer_motion_1.motion.h2) `
  display: flex;
  align-items: center;
  font-weight: normal;
  margin-bottom: ${(0, space_1.default)(1)};
`;
Header.defaultProps = {
    variants: subItemAnimation,
    transition: (0, testableTransition_1.default)(),
};
const Body = (0, styled_1.default)(framer_motion_1.motion.div) `
  margin-bottom: ${(0, space_1.default)(2)};
`;
Body.defaultProps = {
    variants: subItemAnimation,
    transition: (0, testableTransition_1.default)(),
};
/**
 * When a background with a anchor is used and no positioningStrategy is
 * provided, by default we'll align the top left of the container to the anchor
 */
const defaultPositioning = ({ mainRect, anchorRect }) => ({
    x: anchorRect.x - mainRect.x,
    y: anchorRect.y - mainRect.y,
});
/**
 * Wrapper component that will render the wrapped content with an animated
 * overlay.
 *
 * If children are given they will be placed behind the overlay and hidden from
 * pointer events.
 *
 * If a background is given, the background will be rendered _above_ any
 * children (and will receive framer-motion variant changes for animations).
 * The background may also provide a `anchorRef` to aid in alignment of the
 * wrapper to a safe space in the background to aid in alignment of the wrapper
 * to a safe space in the background.
 */
class PageOverlay extends React.Component {
    constructor() {
        super(...arguments);
        /**
         * Used to re-anchor the text wrapper to the anchor point in the background when
         * the size of the page changes.
         */
        this.bgResizeObserver = null;
        this.contentRef = React.createRef();
        this.wrapperRef = React.createRef();
        this.anchorRef = React.createRef();
        /**
         * Align the wrapper component to the anchor by computing x/y values using
         * the passed function. By default if no function is specified it will align
         * to the top left of the anchor.
         */
        this.anchorWrapper = () => {
            if (this.contentRef.current === null ||
                this.wrapperRef.current === null ||
                this.anchorRef.current === null) {
                return;
            }
            // Absolute position the container, this avoids the browser having to reflow
            // the component
            this.wrapperRef.current.style.position = 'absolute';
            this.wrapperRef.current.style.left = `0px`;
            this.wrapperRef.current.style.top = `0px`;
            const mainRect = this.contentRef.current.getBoundingClientRect();
            const anchorRect = this.anchorRef.current.getBoundingClientRect();
            const wrapperRect = this.wrapperRef.current.getBoundingClientRect();
            // Compute the position of the wrapper
            const { x, y } = this.props.positioningStrategy({ mainRect, anchorRect, wrapperRect });
            const transform = `translate(${Math.round(x)}px, ${Math.round(y)}px)`;
            this.wrapperRef.current.style.transform = transform;
        };
    }
    componentDidMount() {
        if (this.contentRef.current === null || this.anchorRef.current === null) {
            return;
        }
        this.anchorWrapper();
        // Observe changes to the upsell container to reanchor if available
        if (window.ResizeObserver) {
            this.bgResizeObserver = new ResizeObserver(this.anchorWrapper);
            this.bgResizeObserver.observe(this.contentRef.current);
        }
    }
    componentWillUnmount() {
        var _a;
        (_a = this.bgResizeObserver) === null || _a === void 0 ? void 0 : _a.disconnect();
    }
    render() {
        const _a = this.props, { text, children, animateDelay, background: BackgroundComponent, customWrapper } = _a, props = (0, tslib_1.__rest)(_a, ["text", "children", "animateDelay", "background", "customWrapper"]);
        const Wrapper = customWrapper !== null && customWrapper !== void 0 ? customWrapper : DefaultWrapper;
        const transition = (0, testableTransition_1.default)({
            delay: 1,
            duration: 1.2,
            ease: 'easeInOut',
            delayChildren: animateDelay !== null && animateDelay !== void 0 ? animateDelay : (BackgroundComponent ? 0.5 : 1.5),
            staggerChildren: 0.15,
        });
        return (<MaskedContent {...props}>
        {children}
        <ContentWrapper ref={this.contentRef} transition={transition} variants={{ animate: {} }}>
          {BackgroundComponent && (<Background>
              <BackgroundComponent anchorRef={this.anchorRef}/>
            </Background>)}
          <Wrapper ref={this.wrapperRef}>
            <text_1.default>{text({ Body, Header })}</text_1.default>
          </Wrapper>
        </ContentWrapper>
      </MaskedContent>);
    }
}
PageOverlay.defaultProps = {
    positioningStrategy: defaultPositioning,
};
const absoluteFull = (0, react_1.css) `
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
`;
const ContentWrapper = (0, styled_1.default)(framer_motion_1.motion.div) `
  ${absoluteFull}
  padding: 10%;
  z-index: 900;
`;
ContentWrapper.defaultProps = {
    initial: 'initial',
    animate: 'animate',
};
const Background = (0, styled_1.default)('div') `
  ${absoluteFull}
  z-index: -1;
  padding: 60px;
  display: flex;
  align-items: center;

  > * {
    width: 100%;
    min-height: 600px;
    height: 100%;
  }
`;
const MaskedContent = (0, styled_1.default)('div') `
  position: relative;
  overflow: hidden;
  flex-grow: 1;
  flex-basis: 0;

  /* Specify bottom margin specifically to offset the margin of the footer, so
   * the hidden content flows directly to the border of the footer
   */
  margin-bottom: -20px;
`;
exports.default = PageOverlay;
//# sourceMappingURL=pageOverlay.jsx.map