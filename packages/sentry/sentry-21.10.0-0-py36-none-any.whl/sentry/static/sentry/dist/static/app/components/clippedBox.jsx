Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const color_1 = (0, tslib_1.__importDefault)(require("color"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class ClippedBox extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            isClipped: !!this.props.defaultClipped,
            isRevealed: false,
            renderedHeight: this.props.renderedHeight,
        };
        this.reveal = () => {
            const { onReveal } = this.props;
            this.setState({
                isClipped: false,
                isRevealed: true,
            });
            if (onReveal) {
                onReveal();
            }
        };
        this.handleClickReveal = (event) => {
            event.stopPropagation();
            this.reveal();
        };
    }
    componentDidMount() {
        // eslint-disable-next-line react/no-find-dom-node
        const renderedHeight = react_dom_1.default.findDOMNode(this).offsetHeight;
        this.calcHeight(renderedHeight);
    }
    componentDidUpdate(_prevProps, prevState) {
        if (prevState.renderedHeight !== this.props.renderedHeight) {
            this.setRenderedHeight();
        }
        if (prevState.renderedHeight !== this.state.renderedHeight) {
            this.calcHeight(this.state.renderedHeight);
        }
        if (this.state.isRevealed || !this.state.isClipped) {
            return;
        }
        if (!this.props.renderedHeight) {
            // eslint-disable-next-line react/no-find-dom-node
            const renderedHeight = react_dom_1.default.findDOMNode(this).offsetHeight;
            if (renderedHeight < this.props.clipHeight) {
                this.reveal();
            }
        }
    }
    setRenderedHeight() {
        this.setState({
            renderedHeight: this.props.renderedHeight,
        });
    }
    calcHeight(renderedHeight) {
        if (!renderedHeight) {
            return;
        }
        if (!this.state.isClipped && renderedHeight > this.props.clipHeight) {
            /* eslint react/no-did-mount-set-state:0 */
            // okay if this causes re-render; cannot determine until
            // rendered first anyways
            this.setState({
                isClipped: true,
            });
        }
    }
    render() {
        const { isClipped, isRevealed } = this.state;
        const { title, children, clipHeight, btnText, className } = this.props;
        return (<ClipWrapper clipHeight={clipHeight} isClipped={isClipped} isRevealed={isRevealed} className={className}>
        {title && <Title>{title}</Title>}
        {children}
        {isClipped && (<ClipFade>
            <button_1.default onClick={this.reveal} priority="primary" size="xsmall">
              {btnText}
            </button_1.default>
          </ClipFade>)}
      </ClipWrapper>);
    }
}
ClippedBox.defaultProps = {
    defaultClipped: false,
    clipHeight: 200,
    btnText: (0, locale_1.t)('Show More'),
};
exports.default = ClippedBox;
const ClipWrapper = (0, styled_1.default)('div', {
    shouldForwardProp: prop => prop !== 'clipHeight' && prop !== 'isClipped' && prop !== 'isRevealed',
}) `
  position: relative;
  margin-left: -${(0, space_1.default)(3)};
  margin-right: -${(0, space_1.default)(3)};
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)} 0;
  border-top: 1px solid ${p => p.theme.backgroundSecondary};
  transition: all 5s ease-in-out;

  /* For "Show More" animation */
  ${p => p.isRevealed && `max-height: 50000px`};

  ${p => p.isClipped &&
    `
    max-height: ${p.clipHeight}px;
    overflow: hidden;
  `};

  :first-of-type {
    margin-top: -${(0, space_1.default)(2)};
    border: 0;
  }
`;
const Title = (0, styled_1.default)('h5') `
  margin-bottom: ${(0, space_1.default)(2)};
`;
const ClipFade = (0, styled_1.default)('div') `
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 40px 0 0;
  background-image: linear-gradient(
    180deg,
    ${p => (0, color_1.default)(p.theme.background).alpha(0.15).string()},
    ${p => p.theme.background}
  );
  text-align: center;
  border-bottom: ${(0, space_1.default)(1.5)} solid ${p => p.theme.background};

  /* Let pointer-events pass through ClipFade to visible elements underneath it */
  pointer-events: none;

  /* Ensure pointer-events trigger event listeners on "Expand" button */
  > * {
    pointer-events: auto;
  }
`;
//# sourceMappingURL=clippedBox.jsx.map