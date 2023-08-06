Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const chunk_1 = (0, tslib_1.__importDefault)(require("lodash/chunk"));
const maxBy_1 = (0, tslib_1.__importDefault)(require("lodash/maxBy"));
const minBy_1 = (0, tslib_1.__importDefault)(require("lodash/minBy"));
const events_1 = require("app/actionCreators/events");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const markLine_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/markLine"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const sessionsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/sessionsRequest"));
const styles_1 = require("app/components/charts/styles");
const loadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/loadingMask"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
const sessions_1 = require("app/utils/sessions");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const utils_1 = require("app/views/alerts/utils");
const options_1 = require("app/views/alerts/wizard/options");
const utils_2 = require("app/views/alerts/wizard/utils");
const types_1 = require("../../types");
const thresholdsChart_1 = (0, tslib_1.__importDefault)(require("./thresholdsChart"));
const TIME_PERIOD_MAP = {
    [types_1.TimePeriod.SIX_HOURS]: (0, locale_1.t)('Last 6 hours'),
    [types_1.TimePeriod.ONE_DAY]: (0, locale_1.t)('Last 24 hours'),
    [types_1.TimePeriod.THREE_DAYS]: (0, locale_1.t)('Last 3 days'),
    [types_1.TimePeriod.SEVEN_DAYS]: (0, locale_1.t)('Last 7 days'),
    [types_1.TimePeriod.FOURTEEN_DAYS]: (0, locale_1.t)('Last 14 days'),
    [types_1.TimePeriod.THIRTY_DAYS]: (0, locale_1.t)('Last 30 days'),
};
/**
 * If TimeWindow is small we want to limit the stats period
 * If the time window is one day we want to use a larger stats period
 */
const AVAILABLE_TIME_PERIODS = {
    [types_1.TimeWindow.ONE_MINUTE]: [
        types_1.TimePeriod.SIX_HOURS,
        types_1.TimePeriod.ONE_DAY,
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
    ],
    [types_1.TimeWindow.FIVE_MINUTES]: [
        types_1.TimePeriod.ONE_DAY,
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    [types_1.TimeWindow.TEN_MINUTES]: [
        types_1.TimePeriod.ONE_DAY,
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    [types_1.TimeWindow.FIFTEEN_MINUTES]: [
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    [types_1.TimeWindow.THIRTY_MINUTES]: [
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    [types_1.TimeWindow.ONE_HOUR]: [types_1.TimePeriod.FOURTEEN_DAYS, types_1.TimePeriod.THIRTY_DAYS],
    [types_1.TimeWindow.TWO_HOURS]: [types_1.TimePeriod.THIRTY_DAYS],
    [types_1.TimeWindow.FOUR_HOURS]: [types_1.TimePeriod.THIRTY_DAYS],
    [types_1.TimeWindow.ONE_DAY]: [types_1.TimePeriod.THIRTY_DAYS],
};
const AGGREGATE_FUNCTIONS = {
    avg: (seriesChunk) => AGGREGATE_FUNCTIONS.sum(seriesChunk) / seriesChunk.length,
    sum: (seriesChunk) => seriesChunk.reduce((acc, series) => acc + series.value, 0),
    max: (seriesChunk) => Math.max(...seriesChunk.map(series => series.value)),
    min: (seriesChunk) => Math.min(...seriesChunk.map(series => series.value)),
};
const TIME_WINDOW_TO_SESSION_INTERVAL = {
    [types_1.TimeWindow.THIRTY_MINUTES]: '30m',
    [types_1.TimeWindow.ONE_HOUR]: '1h',
    [types_1.TimeWindow.TWO_HOURS]: '2h',
    [types_1.TimeWindow.FOUR_HOURS]: '4h',
    [types_1.TimeWindow.ONE_DAY]: '1d',
};
const SESSION_AGGREGATE_TO_HEADING = {
    [types_1.SessionsAggregate.CRASH_FREE_SESSIONS]: (0, locale_1.t)('Total Sessions'),
    [types_1.SessionsAggregate.CRASH_FREE_USERS]: (0, locale_1.t)('Total Users'),
};
/**
 * Determines the number of datapoints to roll up
 */
const getBucketSize = (timeWindow, dataPoints) => {
    const MAX_DPS = 720;
    for (const bucketSize of [5, 10, 15, 30, 60, 120, 240]) {
        const chunkSize = bucketSize / timeWindow;
        if (dataPoints / chunkSize <= MAX_DPS) {
            return bucketSize / timeWindow;
        }
    }
    return 2;
};
/**
 * This is a chart to be used in Metric Alert rules that fetches events based on
 * query, timewindow, and aggregations.
 */
class TriggersChart extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            statsPeriod: types_1.TimePeriod.ONE_DAY,
            totalCount: null,
        };
        this.handleStatsPeriodChange = (timePeriod) => {
            this.setState({ statsPeriod: timePeriod });
        };
        this.getStatsPeriod = () => {
            const { statsPeriod } = this.state;
            const { timeWindow } = this.props;
            const statsPeriodOptions = this.availableTimePeriods[timeWindow];
            const period = statsPeriodOptions.includes(statsPeriod)
                ? statsPeriod
                : statsPeriodOptions[0];
            return period;
        };
    }
    componentDidMount() {
        if (!(0, utils_1.isSessionAggregate)(this.props.aggregate)) {
            this.fetchTotalCount();
        }
    }
    componentDidUpdate(prevProps, prevState) {
        const { query, environment, timeWindow, aggregate, projects } = this.props;
        const { statsPeriod } = this.state;
        if (!(0, utils_1.isSessionAggregate)(aggregate) &&
            (prevProps.projects !== projects ||
                prevProps.environment !== environment ||
                prevProps.query !== query ||
                prevProps.timeWindow !== timeWindow ||
                prevState.statsPeriod !== statsPeriod)) {
            this.fetchTotalCount();
        }
    }
    get availableTimePeriods() {
        // We need to special case sessions, because sub-hour windows are available
        // only when time period is six hours or less (backend limitation)
        if ((0, utils_1.isSessionAggregate)(this.props.aggregate)) {
            return Object.assign(Object.assign({}, AVAILABLE_TIME_PERIODS), { [types_1.TimeWindow.THIRTY_MINUTES]: [types_1.TimePeriod.SIX_HOURS] });
        }
        return AVAILABLE_TIME_PERIODS;
    }
    getComparisonMarkLines(timeseriesData = [], comparisonTimeseriesData = []) {
        var _a, _b;
        const { timeWindow } = this.props;
        const changeStatuses = [];
        if (((_a = timeseriesData === null || timeseriesData === void 0 ? void 0 : timeseriesData[0]) === null || _a === void 0 ? void 0 : _a.data) !== undefined &&
            timeseriesData[0].data.length > 1 &&
            ((_b = comparisonTimeseriesData === null || comparisonTimeseriesData === void 0 ? void 0 : comparisonTimeseriesData[0]) === null || _b === void 0 ? void 0 : _b.data) !== undefined &&
            comparisonTimeseriesData[0].data.length > 1) {
            const changeData = comparisonTimeseriesData[0].data;
            const baseData = timeseriesData[0].data;
            if (this.props.triggers.some(({ alertThreshold }) => typeof alertThreshold === 'number')) {
                const lastPointLimit = baseData[changeData.length - 1].name - timeWindow * formatters_1.MINUTE;
                changeData.forEach(({ name, value: comparisonValue }, idx) => {
                    const baseValue = baseData[idx].value;
                    const comparisonPercentage = comparisonValue === 0
                        ? baseValue === 0
                            ? 0
                            : Infinity
                        : ((baseValue - comparisonValue) / comparisonValue) * 100;
                    const status = this.checkChangeStatus(comparisonPercentage);
                    if (idx === 0 ||
                        idx === changeData.length - 1 ||
                        status !== changeStatuses[changeStatuses.length - 1].status) {
                        changeStatuses.push({ name, status });
                    }
                });
                return changeStatuses.slice(0, -1).map(({ name, status }, idx) => ({
                    seriesName: (0, locale_1.t)('status'),
                    type: 'line',
                    markLine: (0, markLine_1.default)({
                        silent: true,
                        lineStyle: {
                            color: status === 'critical'
                                ? theme_1.default.red300
                                : status === 'warning'
                                    ? theme_1.default.yellow300
                                    : theme_1.default.green300,
                            type: 'solid',
                            width: 4,
                        },
                        data: [
                            [
                                { coord: [name, 0] },
                                {
                                    coord: [
                                        Math.min(changeStatuses[idx + 1].name, lastPointLimit),
                                        0,
                                    ],
                                },
                            ],
                        ],
                    }),
                    data: [],
                }));
            }
        }
        return [];
    }
    fetchTotalCount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, environment, projects, query } = this.props;
            const statsPeriod = this.getStatsPeriod();
            try {
                const totalCount = yield (0, events_1.fetchTotalCount)(api, organization.slug, {
                    field: [],
                    project: projects.map(({ id }) => id),
                    query,
                    statsPeriod,
                    environment: environment ? [environment] : [],
                });
                this.setState({ totalCount });
            }
            catch (e) {
                this.setState({ totalCount: null });
            }
        });
    }
    checkChangeStatus(value) {
        const { thresholdType, triggers } = this.props;
        const criticalTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(trig => trig.label === 'critical');
        const warningTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(trig => trig.label === 'warning');
        const criticalTriggerAlertThreshold = typeof (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) === 'number'
            ? criticalTrigger.alertThreshold
            : undefined;
        const warningTriggerAlertThreshold = typeof (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) === 'number'
            ? warningTrigger.alertThreshold
            : undefined;
        // Need to catch the critical threshold cases before warning threshold cases
        if (thresholdType === types_1.AlertRuleThresholdType.ABOVE &&
            criticalTriggerAlertThreshold &&
            value >= criticalTriggerAlertThreshold) {
            return 'critical';
        }
        if (thresholdType === types_1.AlertRuleThresholdType.ABOVE &&
            warningTriggerAlertThreshold &&
            value >= warningTriggerAlertThreshold) {
            return 'warning';
        }
        // When threshold is below(lower than in comparison alerts) the % diff value is negative
        // It crosses the threshold if its abs value is greater than threshold
        // -80% change crosses below 60% threshold -1 * (-80) > 60
        if (thresholdType === types_1.AlertRuleThresholdType.BELOW &&
            criticalTriggerAlertThreshold &&
            -1 * value >= criticalTriggerAlertThreshold) {
            return 'critical';
        }
        if (thresholdType === types_1.AlertRuleThresholdType.BELOW &&
            warningTriggerAlertThreshold &&
            -1 * value >= warningTriggerAlertThreshold) {
            return 'warning';
        }
        return '';
    }
    renderChart(timeseriesData = [], isLoading, isReloading, comparisonMarkLines) {
        var _a, _b, _c, _d;
        const { triggers, resolveThreshold, thresholdType, header, timeWindow, aggregate, comparisonType, } = this.props;
        const { statsPeriod, totalCount } = this.state;
        const statsPeriodOptions = this.availableTimePeriods[timeWindow];
        const period = this.getStatsPeriod();
        return (<React.Fragment>
        {header}
        <TransparentLoadingMask visible={isReloading}/>
        {isLoading ? (<ChartPlaceholder />) : (<thresholdsChart_1.default period={statsPeriod} minValue={(_b = (0, minBy_1.default)((_a = timeseriesData[0]) === null || _a === void 0 ? void 0 : _a.data, ({ value }) => value)) === null || _b === void 0 ? void 0 : _b.value} maxValue={(_d = (0, maxBy_1.default)((_c = timeseriesData[0]) === null || _c === void 0 ? void 0 : _c.data, ({ value }) => value)) === null || _d === void 0 ? void 0 : _d.value} data={timeseriesData} comparisonMarkLines={comparisonMarkLines !== null && comparisonMarkLines !== void 0 ? comparisonMarkLines : []} hideThresholdLines={comparisonType === types_1.AlertRuleComparisonType.CHANGE} triggers={triggers} resolveThreshold={resolveThreshold} thresholdType={thresholdType} aggregate={aggregate}/>)}
        <styles_1.ChartControls>
          <styles_1.InlineContainer>
            <styles_1.SectionHeading>
              {(0, utils_1.isSessionAggregate)(aggregate)
                ? SESSION_AGGREGATE_TO_HEADING[aggregate]
                : (0, locale_1.t)('Total Events')}
            </styles_1.SectionHeading>
            <styles_1.SectionValue>
              {totalCount !== null ? totalCount.toLocaleString() : '\u2014'}
            </styles_1.SectionValue>
          </styles_1.InlineContainer>
          <styles_1.InlineContainer>
            <optionSelector_1.default options={statsPeriodOptions.map(timePeriod => ({
                label: TIME_PERIOD_MAP[timePeriod],
                value: timePeriod,
                disabled: isLoading || isReloading,
            }))} selected={period} onChange={this.handleStatsPeriodChange} title={(0, locale_1.t)('Display')}/>
          </styles_1.InlineContainer>
        </styles_1.ChartControls>
      </React.Fragment>);
    }
    render() {
        const { api, organization, projects, timeWindow, query, aggregate, environment, comparisonDelta, } = this.props;
        const period = this.getStatsPeriod();
        const renderComparisonStats = organization.features.includes('change-alerts') && comparisonDelta;
        return (0, utils_1.isSessionAggregate)(aggregate) ? (<sessionsRequest_1.default api={api} organization={organization} project={projects.map(({ id }) => Number(id))} environment={environment ? [environment] : undefined} statsPeriod={period} query={query} interval={TIME_WINDOW_TO_SESSION_INTERVAL[timeWindow]} field={utils_1.SESSION_AGGREGATE_TO_FIELD[aggregate]} groupBy={['session.status']}>
        {({ loading, reloading, response }) => {
                const { groups, intervals } = response || {};
                const sessionTimeSeries = [
                    {
                        seriesName: options_1.AlertWizardAlertNames[(0, utils_2.getAlertTypeFromAggregateDataset)({ aggregate, dataset: types_1.Dataset.SESSIONS })],
                        data: (0, sessions_1.getCrashFreeRateSeries)(groups, intervals, utils_1.SESSION_AGGREGATE_TO_FIELD[aggregate]),
                    },
                ];
                return this.renderChart(sessionTimeSeries, loading, reloading);
            }}
      </sessionsRequest_1.default>) : (<feature_1.default features={['metric-alert-builder-aggregate']} organization={organization}>
        {({ hasFeature }) => {
                return (<eventsRequest_1.default api={api} organization={organization} query={query} environment={environment ? [environment] : undefined} project={projects.map(({ id }) => Number(id))} interval={`${timeWindow}m`} comparisonDelta={comparisonDelta} period={period} yAxis={aggregate} includePrevious={false} currentSeriesNames={[aggregate]} partial={false}>
              {({ loading, reloading, timeseriesData, comparisonTimeseriesData }) => {
                        var _a;
                        let comparisonMarkLines = [];
                        if (renderComparisonStats && comparisonTimeseriesData) {
                            comparisonMarkLines = this.getComparisonMarkLines(timeseriesData, comparisonTimeseriesData);
                        }
                        let timeseriesLength;
                        if (((_a = timeseriesData === null || timeseriesData === void 0 ? void 0 : timeseriesData[0]) === null || _a === void 0 ? void 0 : _a.data) !== undefined) {
                            timeseriesLength = timeseriesData[0].data.length;
                            if (hasFeature && timeseriesLength > 600) {
                                const avgData = [];
                                const minData = [];
                                const maxData = [];
                                const chunkSize = getBucketSize(timeWindow, timeseriesData[0].data.length);
                                (0, chunk_1.default)(timeseriesData[0].data, chunkSize).forEach(seriesChunk => {
                                    avgData.push({
                                        name: seriesChunk[0].name,
                                        value: AGGREGATE_FUNCTIONS.avg(seriesChunk),
                                    });
                                    minData.push({
                                        name: seriesChunk[0].name,
                                        value: AGGREGATE_FUNCTIONS.min(seriesChunk),
                                    });
                                    maxData.push({
                                        name: seriesChunk[0].name,
                                        value: AGGREGATE_FUNCTIONS.max(seriesChunk),
                                    });
                                });
                                timeseriesData = [
                                    timeseriesData[0],
                                    { seriesName: (0, locale_1.t)('Minimum'), data: minData },
                                    { seriesName: (0, locale_1.t)('Average'), data: avgData },
                                    { seriesName: (0, locale_1.t)('Maximum'), data: maxData },
                                ];
                            }
                        }
                        return this.renderChart(timeseriesData, loading, reloading, comparisonMarkLines);
                    }}
            </eventsRequest_1.default>);
            }}
      </feature_1.default>);
    }
}
exports.default = (0, withApi_1.default)(TriggersChart);
const TransparentLoadingMask = (0, styled_1.default)(loadingMask_1.default) `
  ${p => !p.visible && 'display: none;'};
  opacity: 0.4;
  z-index: 1;
`;
const ChartPlaceholder = (0, styled_1.default)(placeholder_1.default) `
  /* Height and margin should add up to graph size (200px) */
  margin: 0 0 ${(0, space_1.default)(2)};
  height: 184px;
`;
//# sourceMappingURL=index.jsx.map