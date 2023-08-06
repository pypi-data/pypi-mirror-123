Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
function Divider() {
    return <Wrapper>{'|'}</Wrapper>;
}
exports.default = Divider;
const Wrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray200};
`;
//# sourceMappingURL=divider.jsx.map