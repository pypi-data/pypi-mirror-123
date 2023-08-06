Object.defineProperty(exports, "__esModule", { value: true });
exports.KeyValueTableRow = exports.KeyValueTable = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.KeyValueTable = (0, styled_1.default)('dl') `
  display: grid;
  grid-template-columns: 50% 50%;
`;
const KeyValueTableRow = ({ keyName, value }) => {
    return (<React.Fragment>
      <Key>{keyName}</Key>
      <Value>{value}</Value>
    </React.Fragment>);
};
exports.KeyValueTableRow = KeyValueTableRow;
const commonStyles = ({ theme }) => `
font-size: ${theme.fontSizeMedium};
padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1)};
font-weight: normal;
line-height: inherit;
${overflowEllipsis_1.default};
&:nth-of-type(2n-1) {
  background-color: ${theme.backgroundSecondary};
}
`;
const Key = (0, styled_1.default)('dt') `
  ${commonStyles};
  color: ${p => p.theme.textColor};
`;
const Value = (0, styled_1.default)('dd') `
  ${commonStyles};
  color: ${p => p.theme.subText};
  text-align: right;
`;
//# sourceMappingURL=keyValueTable.jsx.map