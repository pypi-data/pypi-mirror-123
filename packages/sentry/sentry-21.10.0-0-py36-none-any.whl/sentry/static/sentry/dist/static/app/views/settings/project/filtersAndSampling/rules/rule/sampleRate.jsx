Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
function SampleRate({ sampleRate }) {
    return <Wrapper>{`${sampleRate * 100}\u0025`}</Wrapper>;
}
exports.default = SampleRate;
const Wrapper = (0, styled_1.default)('div') `
  white-space: pre-wrap;
  word-break: break-all;
`;
//# sourceMappingURL=sampleRate.jsx.map