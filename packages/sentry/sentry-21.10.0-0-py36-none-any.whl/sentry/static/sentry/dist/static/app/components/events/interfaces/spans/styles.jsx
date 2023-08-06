Object.defineProperty(exports, "__esModule", { value: true });
exports.MeasurementMarker = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const constants_1 = require("app/components/performance/waterfall/constants");
exports.MeasurementMarker = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  height: ${constants_1.ROW_HEIGHT}px;
  user-select: none;
  width: 1px;
  background: repeating-linear-gradient(
      to bottom,
      transparent 0 4px,
      ${p => (p.failedThreshold ? p.theme.red300 : 'black')} 4px 8px
    )
    80%/2px 100% no-repeat;
  z-index: ${p => p.theme.zIndex.traceView.dividerLine};
  color: ${p => p.theme.textColor};
`;
//# sourceMappingURL=styles.jsx.map