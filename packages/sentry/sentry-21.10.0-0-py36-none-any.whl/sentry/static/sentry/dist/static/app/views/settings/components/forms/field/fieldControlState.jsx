Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const width = '36px';
const FieldControlState = (0, styled_1.default)('div') `
  display: flex;
  position: relative;
  ${p => !p.flexibleControlStateSize && `width: ${width}`};
  flex-shrink: 0;
  justify-content: center;
  align-items: center;
`;
exports.default = FieldControlState;
//# sourceMappingURL=fieldControlState.jsx.map