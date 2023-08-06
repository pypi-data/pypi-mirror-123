Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const styles_1 = require("app/components/charts/styles");
const utils_1 = require("app/components/charts/utils");
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const scoreCard_1 = (0, tslib_1.__importDefault)(require("app/components/scoreCard"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dates_1 = require("app/utils/dates");
const utils_2 = require("./usageChart/utils");
const types_1 = require("./types");
const usageChart_1 = (0, tslib_1.__importStar)(require("./usageChart"));
const usageStatsPerMin_1 = (0, tslib_1.__importDefault)(require("./usageStatsPerMin"));
const utils_3 = require("./utils");
class UsageStatsOrganization extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.renderChartFooter = () => {
            const { handleChangeState } = this.props;
            const { loading, error } = this.state;
            const { chartDateInterval, chartTransform, chartDateStartDisplay, chartDateEndDisplay, chartDateTimezoneDisplay, } = this.chartData;
            return (<Footer>
        <styles_1.InlineContainer>
          <FooterDate>
            <styles_1.SectionHeading>{(0, locale_1.t)('Date Range:')}</styles_1.SectionHeading>
            <span>
              {loading || error ? (<notAvailable_1.default />) : ((0, locale_1.tct)('[start] — [end] ([timezone] UTC, [interval] interval)', {
                    start: chartDateStartDisplay,
                    end: chartDateEndDisplay,
                    timezone: chartDateTimezoneDisplay,
                    interval: chartDateInterval,
                }))}
            </span>
          </FooterDate>
        </styles_1.InlineContainer>
        <styles_1.InlineContainer>
          <optionSelector_1.default title={(0, locale_1.t)('Type')} selected={chartTransform} options={usageChart_1.CHART_OPTIONS_DATA_TRANSFORM} onChange={(val) => handleChangeState({ transform: val })}/>
        </styles_1.InlineContainer>
      </Footer>);
        };
    }
    componentDidUpdate(prevProps) {
        const { dataDatetime: prevDateTime } = prevProps;
        const { dataDatetime: currDateTime } = this.props;
        if (prevDateTime.start !== currDateTime.start ||
            prevDateTime.end !== currDateTime.end ||
            prevDateTime.period !== currDateTime.period ||
            prevDateTime.utc !== currDateTime.utc) {
            this.reloadData();
        }
    }
    getEndpoints() {
        return [['orgStats', this.endpointPath, { query: this.endpointQuery }]];
    }
    get endpointPath() {
        const { organization } = this.props;
        return `/organizations/${organization.slug}/stats_v2/`;
    }
    get endpointQuery() {
        const { dataDatetime } = this.props;
        const queryDatetime = dataDatetime.start && dataDatetime.end
            ? {
                start: dataDatetime.start,
                end: dataDatetime.end,
                utc: dataDatetime.utc,
            }
            : {
                statsPeriod: dataDatetime.period || constants_1.DEFAULT_STATS_PERIOD,
            };
        return Object.assign(Object.assign({}, queryDatetime), { interval: (0, utils_1.getSeriesApiInterval)(dataDatetime), groupBy: ['category', 'outcome'], field: ['sum(quantity)'] });
    }
    get chartData() {
        const { orgStats } = this.state;
        return Object.assign(Object.assign(Object.assign({}, this.mapSeriesToChart(orgStats)), this.chartDateRange), this.chartTransform);
    }
    get chartTransform() {
        const { chartTransform } = this.props;
        switch (chartTransform) {
            case usageChart_1.ChartDataTransform.CUMULATIVE:
            case usageChart_1.ChartDataTransform.PERIODIC:
                return { chartTransform };
            default:
                return { chartTransform: usageChart_1.ChartDataTransform.PERIODIC };
        }
    }
    get chartDateRange() {
        const { orgStats } = this.state;
        const { dataDatetime } = this.props;
        const interval = (0, utils_1.getSeriesApiInterval)(dataDatetime);
        // Use fillers as loading/error states will not display datetime at all
        if (!orgStats || !orgStats.intervals) {
            return {
                chartDateInterval: interval,
                chartDateStart: '',
                chartDateEnd: '',
                chartDateUtc: true,
                chartDateStartDisplay: '',
                chartDateEndDisplay: '',
                chartDateTimezoneDisplay: '',
            };
        }
        const { intervals } = orgStats;
        const intervalHours = (0, dates_1.parsePeriodToHours)(interval);
        // Keep datetime in UTC until we want to display it to users
        const startTime = (0, moment_1.default)(intervals[0]).utc();
        const endTime = intervals.length < 2
            ? (0, moment_1.default)(startTime) // when statsPeriod and interval is the same value
            : (0, moment_1.default)(intervals[intervals.length - 1]).utc();
        const useUtc = (0, utils_3.isDisplayUtc)(dataDatetime);
        // If interval is a day or more, use UTC to format date. Otherwise, the date
        // may shift ahead/behind when converting to the user's local time.
        const FORMAT_DATETIME = intervalHours >= 24 ? utils_2.FORMAT_DATETIME_DAILY : utils_2.FORMAT_DATETIME_HOURLY;
        const xAxisStart = (0, moment_1.default)(startTime);
        const xAxisEnd = (0, moment_1.default)(endTime);
        const displayStart = useUtc ? (0, moment_1.default)(startTime).utc() : (0, moment_1.default)(startTime).local();
        const displayEnd = useUtc ? (0, moment_1.default)(endTime).utc() : (0, moment_1.default)(endTime).local();
        if (intervalHours < 24) {
            displayEnd.add(intervalHours, 'h');
        }
        return {
            chartDateInterval: interval,
            chartDateStart: xAxisStart.format(),
            chartDateEnd: xAxisEnd.format(),
            chartDateUtc: useUtc,
            chartDateStartDisplay: displayStart.format(FORMAT_DATETIME),
            chartDateEndDisplay: displayEnd.format(FORMAT_DATETIME),
            chartDateTimezoneDisplay: displayStart.format('Z'),
        };
    }
    mapSeriesToChart(orgStats) {
        const cardStats = {
            total: undefined,
            accepted: undefined,
            dropped: undefined,
            filtered: undefined,
        };
        const chartStats = {
            accepted: [],
            dropped: [],
            projected: [],
            filtered: [],
        };
        if (!orgStats) {
            return { cardStats, chartStats };
        }
        try {
            const { dataCategory } = this.props;
            const { chartDateInterval, chartDateUtc } = this.chartDateRange;
            const usageStats = orgStats.intervals.map(interval => {
                const dateTime = (0, moment_1.default)(interval);
                return {
                    date: (0, utils_2.getDateFromMoment)(dateTime, chartDateInterval, chartDateUtc),
                    total: 0,
                    accepted: 0,
                    filtered: 0,
                    dropped: { total: 0 },
                };
            });
            // Tally totals for card data
            const count = {
                total: 0,
                [types_1.Outcome.ACCEPTED]: 0,
                [types_1.Outcome.FILTERED]: 0,
                [types_1.Outcome.DROPPED]: 0,
                [types_1.Outcome.INVALID]: 0,
                [types_1.Outcome.RATE_LIMITED]: 0,
                [types_1.Outcome.CLIENT_DISCARD]: 0, // Not exposed yet
            };
            orgStats.groups.forEach(group => {
                const { outcome, category } = group.by;
                // HACK: The backend enum are singular, but the frontend enums are plural
                if (!dataCategory.includes(`${category}`)) {
                    return;
                }
                if (outcome !== types_1.Outcome.CLIENT_DISCARD) {
                    count.total += group.totals['sum(quantity)'];
                }
                count[outcome] += group.totals['sum(quantity)'];
                group.series['sum(quantity)'].forEach((stat, i) => {
                    switch (outcome) {
                        case types_1.Outcome.ACCEPTED:
                        case types_1.Outcome.FILTERED:
                            usageStats[i][outcome] += stat;
                            return;
                        case types_1.Outcome.DROPPED:
                        case types_1.Outcome.RATE_LIMITED:
                        case types_1.Outcome.INVALID:
                            usageStats[i].dropped.total += stat;
                            // TODO: add client discards to dropped?
                            return;
                        default:
                            return;
                    }
                });
            });
            // Invalid and rate_limited data is combined with dropped
            count[types_1.Outcome.DROPPED] += count[types_1.Outcome.INVALID];
            count[types_1.Outcome.DROPPED] += count[types_1.Outcome.RATE_LIMITED];
            usageStats.forEach(stat => {
                var _a;
                stat.total = stat.accepted + stat.filtered + stat.dropped.total;
                // Chart Data
                chartStats.accepted.push({ value: [stat.date, stat.accepted] });
                chartStats.dropped.push({ value: [stat.date, stat.dropped.total] });
                (_a = chartStats.filtered) === null || _a === void 0 ? void 0 : _a.push({ value: [stat.date, stat.filtered] });
            });
            return {
                cardStats: {
                    total: (0, utils_3.formatUsageWithUnits)(count.total, dataCategory, (0, utils_3.getFormatUsageOptions)(dataCategory)),
                    accepted: (0, utils_3.formatUsageWithUnits)(count[types_1.Outcome.ACCEPTED], dataCategory, (0, utils_3.getFormatUsageOptions)(dataCategory)),
                    filtered: (0, utils_3.formatUsageWithUnits)(count[types_1.Outcome.FILTERED], dataCategory, (0, utils_3.getFormatUsageOptions)(dataCategory)),
                    dropped: (0, utils_3.formatUsageWithUnits)(count[types_1.Outcome.DROPPED], dataCategory, (0, utils_3.getFormatUsageOptions)(dataCategory)),
                },
                chartStats,
            };
        }
        catch (err) {
            Sentry.withScope(scope => {
                scope.setContext('query', this.endpointQuery);
                scope.setContext('body', orgStats);
                Sentry.captureException(err);
            });
            return {
                cardStats,
                chartStats,
                dataError: new Error('Failed to parse stats data'),
            };
        }
    }
    renderCards() {
        const { dataCategory, dataCategoryName, organization } = this.props;
        const { loading } = this.state;
        const { total, accepted, dropped, filtered } = this.chartData.cardStats;
        const cardMetadata = [
            {
                title: (0, locale_1.tct)('Total [dataCategory]', { dataCategory: dataCategoryName }),
                value: total,
            },
            {
                title: (0, locale_1.t)('Accepted'),
                help: (0, locale_1.tct)('Accepted [dataCategory] were successfully processed by Sentry', {
                    dataCategory,
                }),
                value: accepted,
                secondaryValue: (<usageStatsPerMin_1.default organization={organization} dataCategory={dataCategory}/>),
            },
            {
                title: (0, locale_1.t)('Filtered'),
                help: (0, locale_1.tct)('Filtered [dataCategory] were blocked due to your inbound data filter rules', { dataCategory }),
                value: filtered,
            },
            {
                title: (0, locale_1.t)('Dropped'),
                help: (0, locale_1.tct)('Dropped [dataCategory] were discarded due to invalid data, rate-limits, quota limits, or spike protection', { dataCategory }),
                value: dropped,
            },
        ];
        return cardMetadata.map((card, i) => (<StyledScoreCard key={i} title={card.title} score={loading ? undefined : card.value} help={card.help} trend={card.secondaryValue}/>));
    }
    renderChart() {
        const { dataCategory } = this.props;
        const { error, errors, loading } = this.state;
        const { chartStats, dataError, chartDateInterval, chartDateStart, chartDateEnd, chartDateUtc, chartTransform, } = this.chartData;
        const hasError = error || !!dataError;
        const chartErrors = dataError ? Object.assign(Object.assign({}, errors), { data: dataError }) : errors; // TODO(ts): AsyncComponent
        return (<usageChart_1.default isLoading={loading} isError={hasError} errors={chartErrors} title=" " // Force the title to be blank
         footer={this.renderChartFooter()} dataCategory={dataCategory} dataTransform={chartTransform} usageDateStart={chartDateStart} usageDateEnd={chartDateEnd} usageDateShowUtc={chartDateUtc} usageDateInterval={chartDateInterval} usageStats={chartStats}/>);
    }
    renderComponent() {
        return (<react_1.Fragment>
        {this.renderCards()}
        <ChartWrapper>{this.renderChart()}</ChartWrapper>
      </react_1.Fragment>);
    }
}
exports.default = UsageStatsOrganization;
const StyledScoreCard = (0, styled_1.default)(scoreCard_1.default) `
  grid-column: auto / span 1;
  margin: 0;
`;
const ChartWrapper = (0, styled_1.default)('div') `
  grid-column: 1 / -1;
`;
const Footer = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(3)};
  border-top: 1px solid ${p => p.theme.border};
`;
const FooterDate = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  align-items: center;

  > ${styles_1.SectionHeading} {
    margin-right: ${(0, space_1.default)(1.5)};
  }

  > span:last-child {
    font-weight: 400;
    font-size: ${p => p.theme.fontSizeMedium};
  }
`;
//# sourceMappingURL=usageStatsOrg.jsx.map