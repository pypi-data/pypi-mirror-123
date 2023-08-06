Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const BackToIssues = (0, styled_1.default)(link_1.default) `
  display: flex;
  width: ${(0, space_1.default)(1.5)};
  height: ${(0, space_1.default)(1.5)};
  align-items: center;
  justify-content: center;

  box-sizing: content-box;
  padding: ${(0, space_1.default)(1)};
  border-radius: 50%;

  color: ${p => p.theme.textColor};
  background: ${p => p.theme.backgroundSecondary};
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);

  z-index: 1;

  &:hover {
    background: ${p => p.theme.background};
    transform: scale(1.125);
  }
`;
exports.default = BackToIssues;
//# sourceMappingURL=backToIssues.jsx.map