Object.defineProperty(exports, "__esModule", { value: true });
exports.SpanBarRectangle = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const constants_1 = require("app/components/performance/waterfall/constants");
exports.SpanBarRectangle = (0, styled_1.default)('div') `
  position: relative;
  height: ${constants_1.ROW_HEIGHT - 2 * constants_1.ROW_PADDING}px;
  top: ${constants_1.ROW_PADDING}px;
  min-width: 1px;
  user-select: none;
  transition: border-color 0.15s ease-in-out;
  border-right: 1px solid rgba(0, 0, 0, 0);
`;
//# sourceMappingURL=styles.jsx.map