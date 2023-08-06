Object.defineProperty(exports, "__esModule", { value: true });
exports.DurationPill = exports.RowRectangle = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const constants_1 = require("app/components/performance/waterfall/constants");
const utils_1 = require("app/components/performance/waterfall/utils");
exports.RowRectangle = (0, styled_1.default)('div') `
  position: absolute;
  height: ${constants_1.ROW_HEIGHT - 2 * constants_1.ROW_PADDING}px;
  top: ${constants_1.ROW_PADDING}px;
  left: 0;
  min-width: 1px;
  user-select: none;
  transition: border-color 0.15s ease-in-out;
  ${p => (0, utils_1.getHatchPattern)(p, '#dedae3', '#f4f2f7')}
`;
exports.DurationPill = (0, styled_1.default)('div') `
  position: absolute;
  top: 50%;
  display: flex;
  align-items: center;
  transform: translateY(-50%);
  white-space: nowrap;
  font-size: ${p => p.theme.fontSizeExtraSmall};
  color: ${p => (p.showDetail === true ? p.theme.gray200 : p.theme.gray300)};
  font-variant-numeric: tabular-nums;

  ${utils_1.getDurationPillAlignment}

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    font-size: 10px;
  }
`;
//# sourceMappingURL=rowBar.jsx.map