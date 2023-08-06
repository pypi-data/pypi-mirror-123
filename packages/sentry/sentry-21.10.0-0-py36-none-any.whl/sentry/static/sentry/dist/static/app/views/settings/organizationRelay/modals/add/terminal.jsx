Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Terminal = ({ command }) => (<Wrapper>
    <Prompt>{'\u0024'}</Prompt>
    {command}
  </Wrapper>);
exports.default = Terminal;
const Wrapper = (0, styled_1.default)('div') `
  background: ${p => p.theme.gray500};
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(3)};
  font-family: ${p => p.theme.text.familyMono};
  color: ${p => p.theme.white};
  border-radius: ${p => p.theme.borderRadius};
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(0.75)};
`;
const Prompt = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
`;
//# sourceMappingURL=terminal.jsx.map