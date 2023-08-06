Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
function BreakdownBars({ data }) {
    const total = data.reduce((sum, point) => point.value + sum, 0);
    return (<BreakdownGrid>
      {data.map((point, i) => (<react_1.Fragment key={`${i}:${point.label}`}>
          <Percentage>{(0, formatters_1.formatPercentage)(point.value / total, 0)}</Percentage>
          <BarContainer data-test-id={`status-${point.label}`} cursor={point.onClick ? 'pointer' : 'default'} onClick={point.onClick}>
            <Bar style={{ width: `${((point.value / total) * 100).toFixed(2)}%` }}/>
            <Label>{point.label}</Label>
          </BarContainer>
        </react_1.Fragment>))}
    </BreakdownGrid>);
}
exports.default = BreakdownBars;
const BreakdownGrid = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: min-content auto;
  column-gap: ${(0, space_1.default)(1)};
  row-gap: ${(0, space_1.default)(1)};
`;
const Percentage = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  text-align: right;
`;
const BarContainer = (0, styled_1.default)('div') `
  padding-left: ${(0, space_1.default)(1)};
  padding-right: ${(0, space_1.default)(1)};
  position: relative;
  cursor: ${p => p.cursor};
`;
const Label = (0, styled_1.default)('span') `
  position: relative;
  color: ${p => p.theme.textColor};
  z-index: 2;
  font-size: ${p => p.theme.fontSizeSmall};
`;
const Bar = (0, styled_1.default)('div') `
  border-radius: 2px;
  background-color: ${p => p.theme.border};
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
  height: 100%;
  width: 0%;
`;
//# sourceMappingURL=breakdownBars.jsx.map