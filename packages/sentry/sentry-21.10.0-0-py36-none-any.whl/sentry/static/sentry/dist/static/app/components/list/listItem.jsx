Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const ListItem = (0, styled_1.default)(({ children, className, symbol, onClick }) => (<li className={className} onClick={onClick}>
    {symbol && <Symbol>{symbol}</Symbol>}
    {children}
  </li>)) `
  position: relative;
  ${p => p.symbol && `padding-left: ${(0, space_1.default)(4)};`}
`;
const Symbol = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  min-height: 22.5px;
`;
exports.default = ListItem;
//# sourceMappingURL=listItem.jsx.map