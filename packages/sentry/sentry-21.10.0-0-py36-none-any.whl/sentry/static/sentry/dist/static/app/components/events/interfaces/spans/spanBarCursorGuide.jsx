Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("app/components/performance/waterfall/utils");
const CursorGuideHandler = (0, tslib_1.__importStar)(require("./cursorGuideHandler"));
function SpanBarCursorGuide() {
    return (<CursorGuideHandler.Consumer>
      {({ showCursorGuide, traceViewMouseLeft, }) => {
            if (!showCursorGuide || !traceViewMouseLeft) {
                return null;
            }
            return (<CursorGuide style={{
                    left: (0, utils_1.toPercent)(traceViewMouseLeft),
                }}/>);
        }}
    </CursorGuideHandler.Consumer>);
}
const CursorGuide = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  width: 1px;
  background-color: ${p => p.theme.red300};
  transform: translateX(-50%);
  height: 100%;
`;
exports.default = SpanBarCursorGuide;
//# sourceMappingURL=spanBarCursorGuide.jsx.map