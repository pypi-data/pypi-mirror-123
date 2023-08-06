Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const throttle_1 = (0, tslib_1.__importDefault)(require("lodash/throttle"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const barChartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChartZoom"));
const markLine_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/markLine"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const discoverButton_1 = (0, tslib_1.__importDefault)(require("app/components/discoverButton"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const fields_1 = require("app/utils/discover/fields");
const formatters_1 = require("app/utils/formatters");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const utils_1 = require("app/utils/performance/histogram/utils");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_2 = require("app/views/performance/transactionSummary/transactionEvents/utils");
const vitalsCards_1 = require("../../landing/vitalsCards");
const utils_3 = require("../../vitalDetail/utils");
const constants_1 = require("./constants");
const styles_1 = require("./styles");
const utils_4 = require("./utils");
class VitalCard extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            refDataRect: null,
            refPixelRect: null,
        };
        this.trackOpenInDiscoverClicked = () => {
            const { organization } = this.props;
            const { vitalDetails: vital } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.vitals.open_in_discover',
                eventName: 'Performance Views: Open vitals in discover',
                organization_id: organization.id,
                vital: vital.slug,
            });
        };
        this.trackOpenAllEventsClicked = () => {
            const { organization } = this.props;
            const { vitalDetails: vital } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'performance_views.vitals.open_all_events',
                eventName: 'Performance Views: Open vitals in all events',
                organization_id: organization.id,
                vital: vital.slug,
            });
        };
        /**
         * This callback happens everytime ECharts renders. This is NOT when ECharts
         * finishes rendering, so it can be called quite frequently. The calculations
         * here can get expensive if done frequently, furthermore, this can trigger a
         * state change leading to a re-render. So slow down the updates here as they
         * do not need to be updated every single time.
         */
        this.handleRendered = (0, throttle_1.default)((_, chartRef) => {
            const { chartData } = this.props;
            const { refDataRect } = this.state;
            if (refDataRect === null || chartData.length < 1) {
                return;
            }
            const refPixelRect = refDataRect === null ? null : (0, utils_4.asPixelRect)(chartRef, refDataRect);
            if (refPixelRect !== null && !(0, isEqual_1.default)(refPixelRect, this.state.refPixelRect)) {
                this.setState({ refPixelRect });
            }
        }, 200, { leading: true });
        this.handleDataZoomCancelled = () => { };
    }
    static getDerivedStateFromProps(nextProps, prevState) {
        const { isLoading, error, chartData } = nextProps;
        if (isLoading || error === null) {
            return Object.assign({}, prevState);
        }
        const refDataRect = (0, utils_4.getRefRect)(chartData);
        if (prevState.refDataRect === null ||
            (refDataRect !== null && !(0, isEqual_1.default)(refDataRect, prevState.refDataRect))) {
            return Object.assign(Object.assign({}, prevState), { refDataRect });
        }
        return Object.assign({}, prevState);
    }
    get summary() {
        var _a;
        const { summaryData } = this.props;
        return (_a = summaryData === null || summaryData === void 0 ? void 0 : summaryData.p75) !== null && _a !== void 0 ? _a : null;
    }
    get failureRate() {
        var _a, _b;
        const { summaryData } = this.props;
        const numerator = (_a = summaryData === null || summaryData === void 0 ? void 0 : summaryData.poor) !== null && _a !== void 0 ? _a : 0;
        const denominator = (_b = summaryData === null || summaryData === void 0 ? void 0 : summaryData.total) !== null && _b !== void 0 ? _b : 0;
        return denominator <= 0 ? 0 : numerator / denominator;
    }
    getFormattedStatNumber() {
        const { vitalDetails: vital } = this.props;
        const summary = this.summary;
        const { type } = vital;
        return summary === null
            ? '\u2014'
            : type === 'duration'
                ? (0, formatters_1.getDuration)(summary / 1000, 2, true)
                : (0, formatters_1.formatFloat)(summary, 2);
    }
    renderSummary() {
        var _a;
        const { vitalDetails: vital, eventView, organization, min, max, dataFilter, } = this.props;
        const { slug, name, description } = vital;
        const hasPerformanceEventsPage = organization.features.includes('performance-events-page');
        const column = `measurements.${slug}`;
        const newEventView = eventView
            .withColumns([
            { kind: 'field', field: 'transaction' },
            {
                kind: 'function',
                function: ['percentile', column, constants_1.PERCENTILE.toString(), undefined],
            },
            { kind: 'function', function: ['count', '', '', undefined] },
        ])
            .withSorts([
            {
                kind: 'desc',
                field: (0, fields_1.getAggregateAlias)(`percentile(${column},${constants_1.PERCENTILE.toString()})`),
            },
        ]);
        const query = new tokenizeSearch_1.MutableSearch((_a = newEventView.query) !== null && _a !== void 0 ? _a : '');
        query.addFilterValues('has', [column]);
        // add in any range constraints if any
        if (min !== undefined || max !== undefined) {
            if (min !== undefined) {
                query.addFilterValues(column, [`>=${min}`]);
            }
            if (max !== undefined) {
                query.addFilterValues(column, [`<=${max}`]);
            }
        }
        newEventView.query = query.formatString();
        return (<styles_1.CardSummary>
        <SummaryHeading>
          <styles_1.CardSectionHeading>{`${name} (${slug.toUpperCase()})`}</styles_1.CardSectionHeading>
        </SummaryHeading>
        <styles_1.StatNumber>
          {(0, getDynamicText_1.default)({
                value: this.getFormattedStatNumber(),
                fixed: '\u2014',
            })}
        </styles_1.StatNumber>
        <styles_1.Description>{description}</styles_1.Description>
        <div>
          {hasPerformanceEventsPage ? (<button_1.default size="small" to={newEventView
                    .withColumns([{ kind: 'field', field: column }])
                    .withSorts([{ kind: 'desc', field: column }])
                    .getPerformanceTransactionEventsViewUrlTarget(organization.slug, {
                    showTransactions: dataFilter === 'all'
                        ? utils_2.EventsDisplayFilterName.p100
                        : utils_2.EventsDisplayFilterName.p75,
                    webVital: column,
                })} onClick={this.trackOpenAllEventsClicked}>
              {(0, locale_1.t)('View All Events')}
            </button_1.default>) : (<discoverButton_1.default size="small" to={newEventView.getResultsViewUrlTarget(organization.slug)} onClick={this.trackOpenInDiscoverClicked}>
              {(0, locale_1.t)('Open in Discover')}
            </discoverButton_1.default>)}
        </div>
      </styles_1.CardSummary>);
    }
    renderHistogram() {
        const { theme, location, isLoading, chartData, summaryData, error, colors, vital, vitalDetails, precision = 0, } = this.props;
        const { slug } = vitalDetails;
        const series = this.getSeries();
        const xAxis = {
            type: 'category',
            truncate: true,
            axisTick: {
                alignWithLabel: true,
            },
        };
        const values = series.data.map(point => point.value);
        const max = values.length ? Math.max(...values) : undefined;
        const yAxis = {
            type: 'value',
            max,
            axisLabel: {
                color: theme.chartLabel,
                formatter: formatters_1.formatAbbreviatedNumber,
            },
        };
        const allSeries = [series];
        if (!isLoading && !error) {
            const baselineSeries = this.getBaselineSeries();
            if (baselineSeries !== null) {
                allSeries.push(baselineSeries);
            }
        }
        const vitalData = !isLoading && !error && summaryData !== null ? { [vital]: summaryData } : {};
        return (<barChartZoom_1.default minZoomWidth={Math.pow(10, -precision) * constants_1.NUM_BUCKETS} location={location} paramStart={`${slug}Start`} paramEnd={`${slug}End`} xAxisIndex={[0]} buckets={(0, utils_1.computeBuckets)(chartData)} onDataZoomCancelled={this.handleDataZoomCancelled}>
        {zoomRenderProps => (<Container>
            <transparentLoadingMask_1.default visible={isLoading}/>
            <PercentContainer>
              <vitalsCards_1.VitalBar isLoading={isLoading} data={vitalData} vital={vital} showBar={false} showStates={false} showVitalPercentNames={false} showDurationDetail={false}/>
            </PercentContainer>
            {(0, getDynamicText_1.default)({
                    value: (<barChart_1.default series={allSeries} xAxis={xAxis} yAxis={yAxis} colors={colors} onRendered={this.handleRendered} grid={{
                            left: (0, space_1.default)(3),
                            right: (0, space_1.default)(3),
                            top: (0, space_1.default)(3),
                            bottom: (0, space_1.default)(1.5),
                        }} stacked {...zoomRenderProps}/>),
                    fixed: <placeholder_1.default testId="skeleton-ui" height="200px"/>,
                })}
          </Container>)}
      </barChartZoom_1.default>);
    }
    bucketWidth() {
        const { chartData } = this.props;
        // We can assume that all buckets are of equal width, use the first two
        // buckets to get the width. The value of each histogram function indicates
        // the beginning of the bucket.
        return chartData.length >= 2 ? chartData[1].bin - chartData[0].bin : 0;
    }
    getSeries() {
        const { theme, chartData, precision, vitalDetails, vital } = this.props;
        const additionalFieldsFn = bucket => {
            return {
                itemStyle: { color: theme[this.getVitalsColor(vital, bucket)] },
            };
        };
        const data = (0, utils_1.formatHistogramData)(chartData, {
            precision: precision === 0 ? undefined : precision,
            type: vitalDetails.type,
            additionalFieldsFn,
        });
        return {
            seriesName: (0, locale_1.t)('Count'),
            data,
        };
    }
    getVitalsColor(vital, value) {
        const poorThreshold = utils_3.webVitalPoor[vital];
        const mehThreshold = utils_3.webVitalMeh[vital];
        if (value >= poorThreshold) {
            return utils_3.vitalStateColors[utils_3.VitalState.POOR];
        }
        else if (value >= mehThreshold) {
            return utils_3.vitalStateColors[utils_3.VitalState.MEH];
        }
        else {
            return utils_3.vitalStateColors[utils_3.VitalState.GOOD];
        }
    }
    getBaselineSeries() {
        const { theme, chartData } = this.props;
        const summary = this.summary;
        if (summary === null || this.state.refPixelRect === null) {
            return null;
        }
        const summaryBucket = (0, utils_4.findNearestBucketIndex)(chartData, summary);
        if (summaryBucket === null || summaryBucket === -1) {
            return null;
        }
        const thresholdPixelBottom = (0, utils_4.mapPoint)({
            // subtract 0.5 from the x here to ensure that the threshold lies between buckets
            x: summaryBucket - 0.5,
            y: 0,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (thresholdPixelBottom === null) {
            return null;
        }
        const thresholdPixelTop = (0, utils_4.mapPoint)({
            // subtract 0.5 from the x here to ensure that the threshold lies between buckets
            x: summaryBucket - 0.5,
            y: Math.max(...chartData.map(data => data.count)) || 1,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (thresholdPixelTop === null) {
            return null;
        }
        const markLine = (0, markLine_1.default)({
            animationDuration: 200,
            data: [[thresholdPixelBottom, thresholdPixelTop]],
            label: {
                show: false,
            },
            lineStyle: {
                color: theme.textColor,
                type: 'solid',
            },
        });
        // TODO(tonyx): This conflicts with the types declaration of `MarkLine`
        // if we add it in the constructor. So we opt to add it here so typescript
        // doesn't complain.
        markLine.tooltip = {
            formatter: () => {
                return [
                    '<div class="tooltip-series tooltip-series-solo">',
                    '<span class="tooltip-label">',
                    `<strong>${(0, locale_1.t)('p75')}</strong>`,
                    '</span>',
                    '</div>',
                    '<div class="tooltip-arrow"></div>',
                ].join('');
            },
        };
        return {
            seriesName: (0, locale_1.t)('p75'),
            data: [],
            markLine,
        };
    }
    render() {
        return (<styles_1.Card>
        {this.renderSummary()}
        {this.renderHistogram()}
      </styles_1.Card>);
    }
}
const SummaryHeading = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
`;
const Container = (0, styled_1.default)('div') `
  position: relative;
`;
const PercentContainer = (0, styled_1.default)('div') `
  position: absolute;
  top: ${(0, space_1.default)(2)};
  right: ${(0, space_1.default)(3)};
  z-index: 2;
`;
exports.default = (0, react_2.withTheme)(VitalCard);
//# sourceMappingURL=vitalCard.jsx.map