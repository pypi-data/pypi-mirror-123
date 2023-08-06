Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const ColorBar = (props) => {
    return (<VitalBar fractions={props.colorStops.map(({ percent }) => percent)}>
      {props.colorStops.map(colorStop => {
            return <BarStatus color={colorStop.color} key={colorStop.color}/>;
        })}
    </VitalBar>);
};
const VitalBar = (0, styled_1.default)('div') `
  height: 16px;
  width: 100%;
  overflow: hidden;
  position: relative;
  background: ${p => p.theme.gray100};
  display: grid;
  grid-template-columns: ${p => p.fractions.map(f => `${f}fr`).join(' ')};
  margin-bottom: ${(0, space_1.default)(1)};
  border-radius: 2px;
`;
const BarStatus = (0, styled_1.default)('div') `
  background-color: ${p => p.theme[p.color]};
`;
exports.default = ColorBar;
//# sourceMappingURL=colorBar.jsx.map