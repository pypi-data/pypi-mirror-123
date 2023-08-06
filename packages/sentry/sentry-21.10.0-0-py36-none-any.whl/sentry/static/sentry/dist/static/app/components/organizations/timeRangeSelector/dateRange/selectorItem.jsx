Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const BaseSelectorItem = ({ onClick, value, className, label }) => (<div className={className} onClick={e => onClick(value, e)}>
    <Label>{label}</Label>
  </div>);
const SelectorItem = (0, styled_1.default)(BaseSelectorItem) `
  display: flex;
  cursor: pointer;
  white-space: nowrap;
  padding: ${(0, space_1.default)(1)};
  align-items: center;
  flex: 1;
  background-color: ${p => (p.selected ? p.theme.active : 'transparent')};
  color: ${p => (p.selected ? p.theme.white : p.theme.subText)};
  font-weight: ${p => (p.selected ? 'bold' : 'normal')};
  border-bottom: 1px solid ${p => (p.last ? 'transparent' : p.theme.innerBorder)};

  &:hover {
    color: ${p => p.theme.textColor};
    background: ${p => p.theme.focus};
  }
`;
const Label = (0, styled_1.default)('span') `
  flex: 1;
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = SelectorItem;
//# sourceMappingURL=selectorItem.jsx.map