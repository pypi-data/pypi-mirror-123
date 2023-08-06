Object.defineProperty(exports, "__esModule", { value: true });
exports.DoubleChartRow = exports.TripleChartRow = void 0;
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const layouts_1 = require("app/components/performance/layouts");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const widgetContainer_1 = (0, tslib_1.__importDefault)(require("./widgetContainer"));
const ChartRow = (props) => {
    const charts = props.chartCount;
    const theme = (0, react_1.useTheme)();
    const palette = theme.charts.getColorPalette(charts);
    if (props.allowedCharts.length < charts) {
        throw new Error('Not enough allowed chart types to show row.');
    }
    return (<StyledRow minSize={200}>
      {new Array(charts).fill(0).map((_, index) => (<widgetContainer_1.default {...props} key={index} index={index} chartHeight={props.chartHeight} chartColor={palette[index]} defaultChartSetting={props.allowedCharts[index]}/>))}
    </StyledRow>);
};
const TripleChartRow = (props) => <ChartRow {...props}/>;
exports.TripleChartRow = TripleChartRow;
exports.TripleChartRow.defaultProps = {
    chartCount: 3,
    chartHeight: 160,
};
const DoubleChartRow = (props) => <ChartRow {...props}/>;
exports.DoubleChartRow = DoubleChartRow;
exports.DoubleChartRow.defaultProps = {
    chartCount: 2,
    chartHeight: 300,
};
const StyledRow = (0, styled_1.default)(layouts_1.PerformanceLayoutBodyRow) `
  margin-bottom: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=widgetChartRow.jsx.map