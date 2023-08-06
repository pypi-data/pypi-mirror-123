Object.defineProperty(exports, "__esModule", { value: true });
exports.transformEventsRequestToArea = void 0;
const tslib_1 = require("tslib");
const mean_1 = (0, tslib_1.__importDefault)(require("lodash/mean"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const utils_1 = require("app/utils");
const charts_1 = require("app/utils/discover/charts");
const fields_1 = require("app/utils/discover/fields");
function transformEventsRequestToArea(widgetProps, results, _) {
    var _a, _b;
    const { start, end, utc, interval, statsPeriod } = (0, getParams_1.getParams)(widgetProps.location.query);
    const data = (_a = results.timeseriesData) !== null && _a !== void 0 ? _a : [];
    const dataMean = data.map(series => {
        const meanData = (0, mean_1.default)(series.data.map(({ value }) => value));
        return {
            mean: meanData,
            outputType: (0, fields_1.aggregateOutputType)(series.seriesName),
            label: (0, charts_1.axisLabelFormatter)(meanData, series.seriesName),
        };
    });
    const childData = Object.assign(Object.assign({}, results), { isLoading: results.loading, isErrored: results.errored, hasData: (0, utils_1.defined)(data) && data.length && !!data[0].data.length, data,
        dataMean, previousData: (_b = results.previousTimeseriesData) !== null && _b !== void 0 ? _b : undefined, utc: utc === 'true', interval, statsPeriod: statsPeriod !== null && statsPeriod !== void 0 ? statsPeriod : undefined, start: start !== null && start !== void 0 ? start : '', end: end !== null && end !== void 0 ? end : '' });
    return childData;
}
exports.transformEventsRequestToArea = transformEventsRequestToArea;
//# sourceMappingURL=transformEventsToArea.jsx.map