Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const DEFAULT_SIZE = '13px';
function getLevelColor({ level = '', theme }) {
    const COLORS = {
        error: theme.orange400,
        info: theme.blue300,
        warning: theme.orange300,
        fatal: theme.red300,
        sample: theme.purple300,
    };
    return `background-color: ${COLORS[level] || theme.orange400};`;
}
const ErrorLevel = (0, styled_1.default)('span') `
  padding: 0;
  position: relative;
  width: ${p => p.size || DEFAULT_SIZE};
  height: ${p => p.size || DEFAULT_SIZE};
  text-indent: -9999em;
  display: inline-block;
  border-radius: 50%;
  flex-shrink: 0;

  ${getLevelColor}
`;
exports.default = ErrorLevel;
//# sourceMappingURL=errorLevel.jsx.map