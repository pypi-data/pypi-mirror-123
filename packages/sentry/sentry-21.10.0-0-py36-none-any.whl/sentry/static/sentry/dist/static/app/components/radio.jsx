Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const animations_1 = require("app/styles/animations");
const checkedCss = (p) => (0, react_1.css) `
  display: block;
  width: ${p.radioSize === 'small' ? '8px' : '1rem'};
  height: ${p.radioSize === 'small' ? '8px' : '1rem'};
  border-radius: 50%;
  background-color: ${p.theme.active};
  animation: 0.2s ${animations_1.growIn} ease;
  opacity: ${p.disabled ? 0.4 : null};
`;
const Radio = (0, styled_1.default)('input') `
  display: flex;
  padding: 0;
  width: ${p => (p.radioSize === 'small' ? '16px' : '1.5em')};
  height: ${p => (p.radioSize === 'small' ? '16px' : '1.5em')};
  position: relative;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
  border: 1px solid ${p => p.theme.border};
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.04);
  background: none;
  appearance: none;

  /* TODO(bootstrap): Our bootstrap CSS adds this, we can remove when we remove that */
  margin: 0 !important;

  &:focus,
  &.focus-visible {
    outline: none !important;
    border: 1px solid ${p => p.theme.border};
    box-shadow: rgba(209, 202, 216, 0.5) 0 0 0 3px;
  }

  &:checked:after {
    content: '';
    ${p => checkedCss(p)}
  }
`;
Radio.defaultProps = {
    type: 'radio',
};
exports.default = Radio;
//# sourceMappingURL=radio.jsx.map