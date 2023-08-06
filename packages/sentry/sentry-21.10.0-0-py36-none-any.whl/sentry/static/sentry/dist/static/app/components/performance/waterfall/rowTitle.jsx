Object.defineProperty(exports, "__esModule", { value: true });
exports.SpanGroupRowTitleContent = exports.RowTitleContent = exports.RowTitle = exports.RowTitleContainer = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const constants_1 = require("app/components/performance/waterfall/constants");
exports.RowTitleContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  height: ${constants_1.ROW_HEIGHT}px;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  user-select: none;
`;
exports.RowTitle = (0, styled_1.default)('div') `
  position: relative;
  height: 100%;
  font-size: ${p => p.theme.fontSizeSmall};
  white-space: nowrap;
  display: flex;
  flex: 1;
  align-items: center;
`;
exports.RowTitleContent = (0, styled_1.default)('span') `
  color: ${p => (p.errored ? p.theme.error : 'inherit')};
`;
exports.SpanGroupRowTitleContent = (0, styled_1.default)('span') `
  color: ${p => p.theme.linkColor};
`;
//# sourceMappingURL=rowTitle.jsx.map