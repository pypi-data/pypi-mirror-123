Object.defineProperty(exports, "__esModule", { value: true });
exports.MessageRow = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const constants_1 = require("app/components/performance/waterfall/constants");
const row_1 = require("app/components/performance/waterfall/row");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.MessageRow = (0, styled_1.default)(row_1.Row) `
  display: block;
  cursor: auto;
  line-height: ${constants_1.ROW_HEIGHT}px;
  padding-left: ${(0, space_1.default)(1)};
  padding-right: ${(0, space_1.default)(1)};
  color: ${p => p.theme.gray300};
  background-color: ${p => p.theme.backgroundSecondary};
  outline: 1px solid ${p => p.theme.border};
  font-size: ${p => p.theme.fontSizeSmall};

  z-index: ${p => p.theme.zIndex.traceView.rowInfoMessage};

  > * + * {
    margin-left: ${(0, space_1.default)(2)};
  }
`;
//# sourceMappingURL=messageRow.jsx.map