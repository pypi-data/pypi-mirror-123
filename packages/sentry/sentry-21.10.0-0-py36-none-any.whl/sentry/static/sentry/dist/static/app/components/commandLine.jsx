Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const CommandLine = ({ children }) => <Wrapper>{children}</Wrapper>;
exports.default = CommandLine;
const Wrapper = (0, styled_1.default)('code') `
  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1)};
  color: ${p => p.theme.pink300};
  background: ${p => p.theme.pink100};
  border: 1px solid ${p => p.theme.pink200};
  font-family: ${p => p.theme.text.familyMono};
  font-size: ${p => p.theme.fontSizeMedium};
  white-space: nowrap;
`;
//# sourceMappingURL=commandLine.jsx.map