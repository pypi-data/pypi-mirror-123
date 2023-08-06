Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const merge_1 = (0, tslib_1.__importDefault)(require("lodash/merge"));
const dates_1 = require("app/utils/dates");
const utils_1 = require("../utils");
function XAxis(_a) {
    var { isGroupedByDate, useShortDate, theme, start, end, period, utc } = _a, props = (0, tslib_1.__rest)(_a, ["isGroupedByDate", "useShortDate", "theme", "start", "end", "period", "utc"]);
    const axisLabelFormatter = (value, index) => {
        if (isGroupedByDate) {
            const timeFormat = (0, dates_1.getTimeFormat)();
            const dateFormat = useShortDate ? 'MMM Do' : `MMM D ${timeFormat}`;
            const firstItem = index === 0;
            const format = (0, utils_1.useShortInterval)({ start, end, period }) && !firstItem ? timeFormat : dateFormat;
            return (0, dates_1.getFormattedDate)(value, format, { local: !utc });
        }
        else if (props.truncate) {
            return (0, utils_1.truncationFormatter)(value, props.truncate);
        }
        else {
            return undefined;
        }
    };
    return (0, merge_1.default)({
        type: isGroupedByDate ? 'time' : 'category',
        boundaryGap: false,
        axisLine: {
            lineStyle: {
                color: theme.chartLabel,
            },
        },
        axisTick: {
            lineStyle: {
                color: theme.chartLabel,
            },
        },
        splitLine: {
            show: false,
        },
        axisLabel: {
            color: theme.chartLabel,
            fontFamily: theme.text.family,
            margin: 12,
            // This was default with ChartZoom, we are making it default for all charts now
            // Otherwise the xAxis can look congested when there is always a min/max label
            showMaxLabel: false,
            showMinLabel: false,
            formatter: axisLabelFormatter,
        },
        axisPointer: {
            show: true,
            type: 'line',
            label: {
                show: false,
            },
            lineStyle: {
                width: 0.5,
            },
        },
    }, props);
}
exports.default = XAxis;
//# sourceMappingURL=xAxis.jsx.map