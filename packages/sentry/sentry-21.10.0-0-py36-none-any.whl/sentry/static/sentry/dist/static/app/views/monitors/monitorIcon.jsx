Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
exports.default = (0, styled_1.default)('div') `
  display: inline-block;
  position: relative;
  border-radius: 50%;
  height: ${p => p.size}px;
  width: ${p => p.size}px;

  ${p => p.color
    ? `background: ${p.color};`
    : `background: ${p.status === 'error'
        ? p.theme.error
        : p.status === 'ok'
            ? p.theme.success
            : p.theme.disabled};`};
`;
//# sourceMappingURL=monitorIcon.jsx.map