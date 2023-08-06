Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_lazyload_1 = (0, tslib_1.__importDefault)(require("react-lazyload"));
const react_1 = require("@emotion/react");
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const locale_1 = require("app/locale");
const utils_1 = require("./utils");
function HealthStatsChart({ activeDisplay, data, height = 24 }) {
    const theme = (0, react_1.useTheme)();
    const formatTooltip = (value) => {
        const suffix = activeDisplay === utils_1.DisplayOption.USERS
            ? (0, locale_1.tn)('user', 'users', value)
            : (0, locale_1.tn)('session', 'sessions', value);
        return `${value.toLocaleString()} ${suffix}`;
    };
    return (<react_lazyload_1.default debounce={50} height={height}>
      <miniBarChart_1.default series={data} height={height} isGroupedByDate showTimeInTooltip hideDelay={50} tooltipFormatter={formatTooltip} colors={[theme.purple300, theme.gray200]}/>
    </react_lazyload_1.default>);
}
exports.default = HealthStatsChart;
//# sourceMappingURL=healthStatsChart.jsx.map