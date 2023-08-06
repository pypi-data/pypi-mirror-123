Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const indicator_1 = require("app/actionCreators/indicator");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const sessions_1 = require("app/utils/sessions");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_1 = require("app/views/releases/utils");
const utils_2 = require("./utils");
function StatsRequest({ api, organization, projectSlug, groupings, environments, datetime, location, children, searchQuery, }) {
    const [isLoading, setIsLoading] = (0, react_1.useState)(false);
    const [errored, setErrored] = (0, react_1.useState)(false);
    const [series, setSeries] = (0, react_1.useState)([]);
    const filteredGroupings = groupings.filter(({ aggregation, metricMeta }) => !!(metricMeta === null || metricMeta === void 0 ? void 0 : metricMeta.name) && !!aggregation);
    (0, react_1.useEffect)(() => {
        fetchData();
    }, [projectSlug, environments, datetime, groupings, searchQuery]);
    function fetchData() {
        if (!filteredGroupings.length) {
            return;
        }
        setErrored(false);
        setIsLoading(true);
        const requestExtraParams = (0, getParams_1.getParams)((0, pick_1.default)(location.query, Object.values(globalSelectionHeader_1.URL_PARAM).filter(param => param !== globalSelectionHeader_1.URL_PARAM.PROJECT)));
        const promises = filteredGroupings.map(({ metricMeta, aggregation, groupBy }) => {
            const query = Object.assign({ field: `${aggregation}(${metricMeta.name})`, interval: (0, sessions_1.getSessionsInterval)(datetime) }, requestExtraParams);
            if (searchQuery) {
                const tagsWithDoubleQuotes = searchQuery
                    .split(' ')
                    .filter(tag => !!tag)
                    .map(tag => {
                    const [key, value] = tag.split(':');
                    if (key && value) {
                        return `${key}:"${value}"`;
                    }
                    return '';
                })
                    .filter(tag => !!tag);
                if (!!tagsWithDoubleQuotes.length) {
                    query.query = new tokenizeSearch_1.MutableSearch(tagsWithDoubleQuotes).formatString();
                }
            }
            const metricDataEndpoint = `/projects/${organization.slug}/${projectSlug}/metrics/data/`;
            if (!!(groupBy === null || groupBy === void 0 ? void 0 : groupBy.length)) {
                const groupByParameter = [...groupBy].join('&groupBy=');
                return api.requestPromise(`${metricDataEndpoint}?groupBy=${groupByParameter}`, {
                    query,
                });
            }
            return api.requestPromise(metricDataEndpoint, {
                query,
            });
        });
        Promise.all(promises)
            .then(results => {
            getChartData(results);
        })
            .catch(error => {
            var _a, _b;
            (0, indicator_1.addErrorMessage)((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : (0, locale_1.t)('Error loading chart data'));
            setErrored(true);
        });
    }
    function getChartData(sessionReponses) {
        if (!sessionReponses.length) {
            setIsLoading(false);
            return;
        }
        const seriesData = sessionReponses.map((sessionResponse, index) => {
            const { aggregation, legend, metricMeta } = filteredGroupings[index];
            const field = `${aggregation}(${metricMeta.name})`;
            const breakDownChartData = (0, utils_2.getBreakdownChartData)({
                response: sessionResponse,
                sessionResponseIndex: index + 1,
                legend,
            });
            const chartData = (0, utils_2.fillChartDataFromMetricsResponse)({
                response: sessionResponse,
                field,
                chartData: breakDownChartData,
                valueFormatter: metricMeta.name === 'session.duration'
                    ? duration => (0, utils_1.roundDuration)(duration ? duration / 1000 : 0)
                    : undefined,
            });
            return [...Object.values(chartData)];
        });
        const newSeries = seriesData.reduce((mergedSeries, chartDataSeries) => {
            return mergedSeries.concat(chartDataSeries);
        }, []);
        setSeries(newSeries);
        setIsLoading(false);
    }
    return children({ isLoading, errored, series });
}
exports.default = StatsRequest;
//# sourceMappingURL=statsRequest.jsx.map