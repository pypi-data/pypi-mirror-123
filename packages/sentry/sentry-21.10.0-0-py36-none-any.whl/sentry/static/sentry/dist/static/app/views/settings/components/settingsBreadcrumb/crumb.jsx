Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Crumb = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  position: relative;
  font-size: 18px;
  color: ${p => p.theme.subText};
  padding-right: ${(0, space_1.default)(1)};
  cursor: pointer;
  white-space: nowrap;

  &:hover {
    color: ${p => p.theme.textColor};
  }
`;
exports.default = Crumb;
//# sourceMappingURL=crumb.jsx.map