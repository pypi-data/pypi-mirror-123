Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorTitle = exports.ErrorLevel = exports.ErrorDot = exports.ErrorMessageContent = exports.ErrorMessageTitle = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.ErrorMessageTitle = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
`;
exports.ErrorMessageContent = (0, styled_1.default)('div') `
  display: grid;
  align-items: center;
  grid-template-columns: 16px 72px auto;
  grid-gap: ${(0, space_1.default)(0.75)};
  margin-top: ${(0, space_1.default)(0.75)};
`;
exports.ErrorDot = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.level[p.level]};
  content: '';
  width: ${(0, space_1.default)(1)};
  min-width: ${(0, space_1.default)(1)};
  height: ${(0, space_1.default)(1)};
  margin-right: ${(0, space_1.default)(1)};
  border-radius: 100%;
  flex: 1;
`;
exports.ErrorLevel = (0, styled_1.default)('span') `
  width: 80px;
`;
exports.ErrorTitle = (0, styled_1.default)('span') `
  ${overflowEllipsis_1.default};
`;
//# sourceMappingURL=rowDetails.jsx.map