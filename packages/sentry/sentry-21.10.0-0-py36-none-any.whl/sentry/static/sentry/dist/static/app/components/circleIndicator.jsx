Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const defaultProps = {
    enabled: true,
    size: 14,
};
const getBackgroundColor = (p) => {
    if (p.color) {
        return `background: ${p.color};`;
    }
    return `background: ${p.enabled ? p.theme.success : p.theme.error};`;
};
const getSize = (p) => `
  height: ${p.size}px;
  width: ${p.size}px;
`;
const CircleIndicator = (0, styled_1.default)('div') `
  display: inline-block;
  position: relative;
  border-radius: 50%;
  ${getSize};
  ${getBackgroundColor};
`;
CircleIndicator.defaultProps = defaultProps;
exports.default = CircleIndicator;
//# sourceMappingURL=circleIndicator.jsx.map