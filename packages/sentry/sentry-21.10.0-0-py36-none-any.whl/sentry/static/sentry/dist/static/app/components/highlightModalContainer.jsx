Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const highlight_bottom_left_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/pattern/highlight-bottom-left.svg"));
const highlight_top_right_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/pattern/highlight-top-right.svg"));
function HighlightModalContainer({ topWidth, bottomWidth, children, }) {
    return (<react_1.Fragment>
      <PositionTopRight src={highlight_top_right_svg_1.default} width={topWidth}/>
      {children}
      <PositionBottomLeft src={highlight_bottom_left_svg_1.default} width={bottomWidth}/>
    </react_1.Fragment>);
}
exports.default = HighlightModalContainer;
const PositionTopRight = (0, styled_1.default)('img') `
  position: absolute;
  width: ${p => p.width};
  right: 0;
  top: 0;
  pointer-events: none;
`;
const PositionBottomLeft = (0, styled_1.default)('img') `
  position: absolute;
  width: ${p => p.width};
  bottom: 0;
  left: 0;
  pointer-events: none;
`;
HighlightModalContainer.defaultProps = {
    topWidth: '400px',
    bottomWidth: '200px',
};
//# sourceMappingURL=highlightModalContainer.jsx.map