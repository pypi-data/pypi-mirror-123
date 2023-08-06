Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const spin = (0, react_1.keyframes) `
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
`;
const Spinner = (0, styled_1.default)('div') `
  animation: ${spin} 0.4s linear infinite;
  width: 18px;
  height: 18px;
  border-radius: 18px;
  border-top: 2px solid ${p => p.theme.border};
  border-right: 2px solid ${p => p.theme.border};
  border-bottom: 2px solid ${p => p.theme.border};
  border-left: 2px solid ${p => p.theme.purple300};
  margin-left: auto;
`;
exports.default = Spinner;
//# sourceMappingURL=spinner.jsx.map