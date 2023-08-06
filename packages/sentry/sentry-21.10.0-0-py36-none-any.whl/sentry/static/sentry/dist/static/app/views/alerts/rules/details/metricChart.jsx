Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const color_1 = (0, tslib_1.__importDefault)(require("color"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const graphic_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/graphic"));
const markArea_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/markArea"));
const markLine_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/markLine"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const sessionsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/sessionsRequest"));
const styles_1 = require("app/components/charts/styles");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dates_1 = require("app/utils/dates");
const sessions_1 = require("app/utils/sessions");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const details_1 = require("app/views/alerts/details");
const incidentRulePresets_1 = require("app/views/alerts/incidentRules/incidentRulePresets");
const types_1 = require("app/views/alerts/incidentRules/types");
const options_1 = require("app/views/alerts/wizard/options");
const utils_1 = require("app/views/alerts/wizard/utils");
const types_2 = require("../../types");
const utils_2 = require("../../utils");
const X_AXIS_BOUNDARY_GAP = 20;
const VERTICAL_PADDING = 22;
function formatTooltipDate(date, format) {
    const { options: { timezone }, } = configStore_1.default.get('user');
    return moment_timezone_1.default.tz(date, timezone).format(format);
}
function createThresholdSeries(lineColor, threshold) {
    return {
        seriesName: 'Threshold Line',
        type: 'line',
        markLine: (0, markLine_1.default)({
            silent: true,
            lineStyle: { color: lineColor, type: 'dashed', width: 1 },
            data: [{ yAxis: threshold }],
            label: {
                show: false,
            },
        }),
        data: [],
    };
}
function createStatusAreaSeries(lineColor, startTime, endTime, yPosition) {
    return {
        seriesName: '',
        type: 'line',
        markLine: (0, markLine_1.default)({
            silent: true,
            lineStyle: { color: lineColor, type: 'solid', width: 4 },
            data: [[{ coord: [startTime, yPosition] }, { coord: [endTime, yPosition] }]],
        }),
        data: [],
    };
}
function createIncidentSeries(router, organization, lineColor, incidentTimestamp, incident, dataPoint, seriesName, aggregate) {
    const series = {
        seriesName: 'Incident Line',
        type: 'line',
        markLine: (0, markLine_1.default)({
            silent: false,
            lineStyle: { color: lineColor, type: 'solid' },
            data: [
                {
                    xAxis: incidentTimestamp,
                    onClick: () => {
                        router.push({
                            pathname: (0, details_1.alertDetailsLink)(organization, incident),
                            query: { alert: incident.identifier },
                        });
                    },
                },
            ],
            label: {
                show: incident.identifier,
                position: 'insideEndBottom',
                formatter: incident.identifier,
                color: lineColor,
                fontSize: 10,
                fontFamily: 'Rubik',
            },
        }),
        data: [],
    };
    // tooltip conflicts with MarkLine types
    series.markLine.tooltip = {
        trigger: 'item',
        alwaysShowContent: true,
        formatter: ({ value, marker }) => {
            const time = formatTooltipDate((0, moment_1.default)(value), 'MMM D, YYYY LT');
            return [
                `<div class="tooltip-series"><div>`,
                `<span class="tooltip-label">${marker} <strong>${(0, locale_1.t)('Alert')} #${incident.identifier}</strong></span>${(dataPoint === null || dataPoint === void 0 ? void 0 : dataPoint.value)
                    ? `${seriesName} ${(0, utils_2.alertTooltipValueFormatter)(dataPoint.value, seriesName !== null && seriesName !== void 0 ? seriesName : '', aggregate !== null && aggregate !== void 0 ? aggregate : '')}`
                    : ''}`,
                `</div></div>`,
                `<div class="tooltip-date">${time}</div>`,
                `<div class="tooltip-arrow"></div>`,
            ].join('');
        },
    };
    return series;
}
class MetricChart extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            width: -1,
            height: -1,
        };
        this.ref = null;
        /**
         * Syncs component state with the chart's width/heights
         */
        this.updateDimensions = () => {
            var _a, _b;
            const chartRef = (_b = (_a = this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (!chartRef) {
                return;
            }
            const width = chartRef.getWidth();
            const height = chartRef.getHeight();
            if (width !== this.state.width || height !== this.state.height) {
                this.setState({
                    width,
                    height,
                });
            }
        };
        this.handleRef = (ref) => {
            if (ref && !this.ref) {
                this.ref = ref;
                this.updateDimensions();
            }
            if (!ref) {
                this.ref = null;
            }
        };
        this.getRuleChangeThresholdElements = (data) => {
            const { height, width } = this.state;
            const { dateModified } = this.props.rule || {};
            if (!data.length || !data[0].data.length || !dateModified) {
                return [];
            }
            const seriesData = data[0].data;
            const seriesStart = (0, moment_1.default)(seriesData[0].name).valueOf();
            const seriesEnd = (0, moment_1.default)(seriesData[seriesData.length - 1].name).valueOf();
            const ruleChanged = (0, moment_1.default)(dateModified).valueOf();
            if (ruleChanged < seriesStart) {
                return [];
            }
            const chartWidth = width - X_AXIS_BOUNDARY_GAP;
            const position = X_AXIS_BOUNDARY_GAP +
                Math.round((chartWidth * (ruleChanged - seriesStart)) / (seriesEnd - seriesStart));
            return [
                {
                    type: 'line',
                    draggable: false,
                    position: [position, 0],
                    shape: { y1: 0, y2: height - VERTICAL_PADDING, x1: 1, x2: 1 },
                    style: {
                        stroke: theme_1.default.gray200,
                    },
                },
                {
                    type: 'rect',
                    draggable: false,
                    position: [X_AXIS_BOUNDARY_GAP, 0],
                    shape: {
                        // +1 makes the gray area go midway onto the dashed line above
                        width: position - X_AXIS_BOUNDARY_GAP + 1,
                        height: height - VERTICAL_PADDING,
                    },
                    style: {
                        fill: (0, color_1.default)(theme_1.default.gray100).alpha(0.42).rgb().string(),
                    },
                },
            ];
        };
    }
    renderChartActions(totalDuration, criticalDuration, warningDuration) {
        const { rule, orgId, projects, timePeriod, query } = this.props;
        const ctaOpts = {
            orgSlug: orgId,
            projects: projects,
            rule,
            eventType: query,
            start: timePeriod.start,
            end: timePeriod.end,
        };
        const _a = (0, incidentRulePresets_1.makeDefaultCta)(ctaOpts), { buttonText } = _a, props = (0, tslib_1.__rest)(_a, ["buttonText"]);
        const resolvedPercent = (100 * Math.max(totalDuration - criticalDuration - warningDuration, 0)) /
            totalDuration;
        const criticalPercent = 100 * Math.min(criticalDuration / totalDuration, 1);
        const warningPercent = 100 * Math.min(warningDuration / totalDuration, 1);
        return (<ChartActions>
        <ChartSummary>
          <SummaryText>{(0, locale_1.t)('SUMMARY')}</SummaryText>
          <SummaryStats>
            <StatItem>
              <icons_1.IconCheckmark color="green300" isCircled/>
              <StatCount>{resolvedPercent ? resolvedPercent.toFixed(2) : 0}%</StatCount>
            </StatItem>
            <StatItem>
              <icons_1.IconWarning color="yellow300"/>
              <StatCount>{warningPercent ? warningPercent.toFixed(2) : 0}%</StatCount>
            </StatItem>
            <StatItem>
              <icons_1.IconFire color="red300"/>
              <StatCount>{criticalPercent ? criticalPercent.toFixed(2) : 0}%</StatCount>
            </StatItem>
          </SummaryStats>
        </ChartSummary>
        {!(0, utils_2.isSessionAggregate)(rule.aggregate) && (<feature_1.default features={['discover-basic']}>
            <button_1.default size="small" {...props}>
              {buttonText}
            </button_1.default>
          </feature_1.default>)}
      </ChartActions>);
    }
    renderChart(loading, timeseriesData) {
        var _a, _b;
        const { router, selectedIncident, interval, handleZoom, filter, query, incidents, rule, organization, timePeriod: { start, end }, } = this.props;
        const { dateModified, timeWindow, aggregate } = rule;
        if (loading || !timeseriesData) {
            return this.renderEmpty();
        }
        const criticalTrigger = rule.triggers.find(({ label }) => label === 'critical');
        const warningTrigger = rule.triggers.find(({ label }) => label === 'warning');
        const series = [...timeseriesData];
        const areaSeries = [];
        // Ensure series data appears above incident lines
        series[0].z = 100;
        const dataArr = timeseriesData[0].data;
        const maxSeriesValue = dataArr.reduce((currMax, coord) => Math.max(currMax, coord.value), 0);
        // find the lowest value between chart data points, warning threshold,
        // critical threshold and then apply some breathing space
        const minChartValue = (0, utils_2.shouldScaleAlertChart)(aggregate)
            ? Math.floor(Math.min(dataArr.reduce((currMax, coord) => Math.min(currMax, coord.value), Infinity), typeof (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) === 'number'
                ? warningTrigger.alertThreshold
                : Infinity, typeof (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) === 'number'
                ? criticalTrigger.alertThreshold
                : Infinity) / utils_2.ALERT_CHART_MIN_MAX_BUFFER)
            : 0;
        const firstPoint = (0, moment_1.default)((_a = dataArr[0]) === null || _a === void 0 ? void 0 : _a.name).valueOf();
        const lastPoint = (0, moment_1.default)((_b = dataArr[dataArr.length - 1]) === null || _b === void 0 ? void 0 : _b.name).valueOf();
        const totalDuration = lastPoint - firstPoint;
        let criticalDuration = 0;
        let warningDuration = 0;
        series.push(createStatusAreaSeries(theme_1.default.green300, firstPoint, lastPoint, minChartValue));
        if (incidents) {
            // select incidents that fall within the graph range
            const periodStart = moment_1.default.utc(firstPoint);
            incidents
                .filter(incident => !incident.dateClosed || (0, moment_1.default)(incident.dateClosed).isAfter(periodStart))
                .forEach(incident => {
                var _a, _b;
                const statusChanges = (_a = incident.activities) === null || _a === void 0 ? void 0 : _a.filter(({ type, value }) => type === types_2.IncidentActivityType.STATUS_CHANGE &&
                    value &&
                    [`${types_2.IncidentStatus.WARNING}`, `${types_2.IncidentStatus.CRITICAL}`].includes(value)).sort((a, b) => (0, moment_1.default)(a.dateCreated).valueOf() - (0, moment_1.default)(b.dateCreated).valueOf());
                const incidentEnd = (_b = incident.dateClosed) !== null && _b !== void 0 ? _b : (0, moment_1.default)().valueOf();
                const timeWindowMs = rule.timeWindow * 60 * 1000;
                const incidentColor = warningTrigger &&
                    statusChanges &&
                    !statusChanges.find(({ value }) => value === `${types_2.IncidentStatus.CRITICAL}`)
                    ? theme_1.default.yellow300
                    : theme_1.default.red300;
                const incidentStartDate = (0, moment_1.default)(incident.dateStarted).valueOf();
                const incidentCloseDate = incident.dateClosed
                    ? (0, moment_1.default)(incident.dateClosed).valueOf()
                    : lastPoint;
                const incidentStartValue = dataArr.find(point => (0, moment_1.default)(point.name).valueOf() >= incidentStartDate);
                series.push(createIncidentSeries(router, organization, incidentColor, incidentStartDate, incident, incidentStartValue, series[0].seriesName, aggregate));
                const areaStart = Math.max((0, moment_1.default)(incident.dateStarted).valueOf(), firstPoint);
                const areaEnd = Math.min((statusChanges === null || statusChanges === void 0 ? void 0 : statusChanges.length) && statusChanges[0].dateCreated
                    ? (0, moment_1.default)(statusChanges[0].dateCreated).valueOf() - timeWindowMs
                    : (0, moment_1.default)(incidentEnd).valueOf(), lastPoint);
                const areaColor = warningTrigger ? theme_1.default.yellow300 : theme_1.default.red300;
                if (areaEnd > areaStart) {
                    series.push(createStatusAreaSeries(areaColor, areaStart, areaEnd, minChartValue));
                    if (areaColor === theme_1.default.yellow300) {
                        warningDuration += Math.abs(areaEnd - areaStart);
                    }
                    else {
                        criticalDuration += Math.abs(areaEnd - areaStart);
                    }
                }
                statusChanges === null || statusChanges === void 0 ? void 0 : statusChanges.forEach((activity, idx) => {
                    const statusAreaStart = Math.max((0, moment_1.default)(activity.dateCreated).valueOf() - timeWindowMs, firstPoint);
                    const statusAreaEnd = Math.min(idx === statusChanges.length - 1
                        ? (0, moment_1.default)(incidentEnd).valueOf()
                        : (0, moment_1.default)(statusChanges[idx + 1].dateCreated).valueOf() - timeWindowMs, lastPoint);
                    const statusAreaColor = activity.value === `${types_2.IncidentStatus.CRITICAL}`
                        ? theme_1.default.red300
                        : theme_1.default.yellow300;
                    if (statusAreaEnd > statusAreaStart) {
                        series.push(createStatusAreaSeries(statusAreaColor, statusAreaStart, statusAreaEnd, minChartValue));
                        if (statusAreaColor === theme_1.default.yellow300) {
                            warningDuration += Math.abs(statusAreaEnd - statusAreaStart);
                        }
                        else {
                            criticalDuration += Math.abs(statusAreaEnd - statusAreaStart);
                        }
                    }
                });
                if (selectedIncident && incident.id === selectedIncident.id) {
                    const selectedIncidentColor = incidentColor === theme_1.default.yellow300 ? theme_1.default.yellow100 : theme_1.default.red100;
                    areaSeries.push({
                        type: 'line',
                        markArea: (0, markArea_1.default)({
                            silent: true,
                            itemStyle: {
                                color: (0, color_1.default)(selectedIncidentColor).alpha(0.42).rgb().string(),
                            },
                            data: [[{ xAxis: incidentStartDate }, { xAxis: incidentCloseDate }]],
                        }),
                        data: [],
                    });
                }
            });
        }
        let maxThresholdValue = 0;
        if (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) {
            const { alertThreshold } = warningTrigger;
            const warningThresholdLine = createThresholdSeries(theme_1.default.yellow300, alertThreshold);
            series.push(warningThresholdLine);
            maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
        }
        if (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) {
            const { alertThreshold } = criticalTrigger;
            const criticalThresholdLine = createThresholdSeries(theme_1.default.red300, alertThreshold);
            series.push(criticalThresholdLine);
            maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
        }
        return (<ChartPanel>
        <StyledPanelBody withPadding>
          <ChartHeader>
            <ChartTitle>
              {options_1.AlertWizardAlertNames[(0, utils_1.getAlertTypeFromAggregateDataset)(rule)]}
            </ChartTitle>
            {query ? filter : null}
          </ChartHeader>
          <chartZoom_1.default router={router} start={start} end={end} onZoom={zoomArgs => handleZoom(zoomArgs.start, zoomArgs.end)}>
            {zoomRenderProps => (<lineChart_1.default {...zoomRenderProps} isGroupedByDate showTimeInTooltip forwardedRef={this.handleRef} grid={{
                    left: 0,
                    right: (0, space_1.default)(2),
                    top: (0, space_1.default)(2),
                    bottom: 0,
                }} yAxis={{
                    axisLabel: {
                        formatter: (value) => (0, utils_2.alertAxisFormatter)(value, timeseriesData[0].seriesName, rule.aggregate),
                    },
                    max: maxThresholdValue > maxSeriesValue ? maxThresholdValue : undefined,
                    min: minChartValue || undefined,
                }} series={[...series, ...areaSeries]} graphic={(0, graphic_1.default)({
                    elements: this.getRuleChangeThresholdElements(timeseriesData),
                })} tooltip={{
                    formatter: seriesParams => {
                        var _a;
                        // seriesParams can be object instead of array
                        const pointSeries = Array.isArray(seriesParams)
                            ? seriesParams
                            : [seriesParams];
                        const { marker, data: pointData, seriesName } = pointSeries[0];
                        const [pointX, pointY] = pointData;
                        const pointYFormatted = (0, utils_2.alertTooltipValueFormatter)(pointY, seriesName !== null && seriesName !== void 0 ? seriesName : '', rule.aggregate);
                        const isModified = dateModified && pointX <= new Date(dateModified).getTime();
                        const startTime = formatTooltipDate((0, moment_1.default)(pointX), 'MMM D LT');
                        const { period, periodLength } = (_a = (0, getParams_1.parseStatsPeriod)(interval)) !== null && _a !== void 0 ? _a : {
                            periodLength: 'm',
                            period: `${timeWindow}`,
                        };
                        const endTime = formatTooltipDate((0, moment_1.default)(pointX).add(parseInt(period, 10), periodLength), 'MMM D LT');
                        const title = isModified
                            ? `<strong>${(0, locale_1.t)('Alert Rule Modified')}</strong>`
                            : `${marker} <strong>${seriesName}</strong>`;
                        const value = isModified
                            ? `${seriesName} ${pointYFormatted}`
                            : pointYFormatted;
                        return [
                            `<div class="tooltip-series"><div>`,
                            `<span class="tooltip-label">${title}</span>${value}`,
                            `</div></div>`,
                            `<div class="tooltip-date">${startTime} &mdash; ${endTime}</div>`,
                            `<div class="tooltip-arrow"></div>`,
                        ].join('');
                    },
                }} onFinished={() => {
                    // We want to do this whenever the chart finishes re-rendering so that we can update the dimensions of
                    // any graphics related to the triggers (e.g. the threshold areas + boundaries)
                    this.updateDimensions();
                }}/>)}
          </chartZoom_1.default>
        </StyledPanelBody>
        {this.renderChartActions(totalDuration, criticalDuration, warningDuration)}
      </ChartPanel>);
    }
    renderEmpty() {
        return (<ChartPanel>
        <panels_1.PanelBody withPadding>
          <placeholder_1.default height="200px"/>
        </panels_1.PanelBody>
      </ChartPanel>);
    }
    render() {
        const { api, rule, organization, timePeriod, projects, interval, query } = this.props;
        const { aggregate, timeWindow, environment, dataset } = rule;
        // If the chart duration isn't as long as the rollup duration the events-stats
        // endpoint will return an invalid timeseriesData data set
        const viableStartDate = (0, dates_1.getUtcDateString)(moment_1.default.min(moment_1.default.utc(timePeriod.start), moment_1.default.utc(timePeriod.end).subtract(timeWindow, 'minutes')));
        const viableEndDate = (0, dates_1.getUtcDateString)(moment_1.default.utc(timePeriod.end).add(timeWindow, 'minutes'));
        return dataset === types_1.Dataset.SESSIONS ? (<sessionsRequest_1.default api={api} organization={organization} project={projects.filter(p => p.id).map(p => Number(p.id))} environment={environment ? [environment] : undefined} start={viableStartDate} end={viableEndDate} query={query} interval={interval} field={utils_2.SESSION_AGGREGATE_TO_FIELD[aggregate]} groupBy={['session.status']}>
        {({ loading, response }) => this.renderChart(loading, [
                {
                    seriesName: options_1.AlertWizardAlertNames[(0, utils_1.getAlertTypeFromAggregateDataset)({ aggregate, dataset: types_1.Dataset.SESSIONS })],
                    data: (0, sessions_1.getCrashFreeRateSeries)(response === null || response === void 0 ? void 0 : response.groups, response === null || response === void 0 ? void 0 : response.intervals, utils_2.SESSION_AGGREGATE_TO_FIELD[aggregate]),
                },
            ])}
      </sessionsRequest_1.default>) : (<eventsRequest_1.default api={api} organization={organization} query={query} environment={environment ? [environment] : undefined} project={projects
                .filter(p => p && p.slug)
                .map(project => Number(project.id))} interval={interval} start={viableStartDate} end={viableEndDate} yAxis={aggregate} includePrevious={false} currentSeriesNames={[aggregate]} partial={false} referrer="api.alerts.alert-rule-chart">
        {({ loading, timeseriesData }) => this.renderChart(loading, timeseriesData)}
      </eventsRequest_1.default>);
    }
}
exports.default = (0, react_router_1.withRouter)(MetricChart);
const ChartPanel = (0, styled_1.default)(panels_1.Panel) `
  margin-top: ${(0, space_1.default)(2)};
`;
const ChartHeader = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const ChartTitle = (0, styled_1.default)('header') `
  display: flex;
  flex-direction: row;
`;
const ChartActions = (0, styled_1.default)(panels_1.PanelFooter) `
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: ${(0, space_1.default)(1)} 20px;
`;
const ChartSummary = (0, styled_1.default)('div') `
  display: flex;
  margin-right: auto;
`;
const SummaryText = (0, styled_1.default)(styles_1.SectionHeading) `
  flex: 1;
  display: flex;
  align-items: center;
  margin: 0;
  font-weight: bold;
  font-size: ${p => p.theme.fontSizeSmall};
  line-height: 1;
`;
const SummaryStats = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin: 0 ${(0, space_1.default)(2)};
`;
const StatItem = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin: 0 ${(0, space_1.default)(2)} 0 0;
`;
/* Override padding to make chart appear centered */
const StyledPanelBody = (0, styled_1.default)(panels_1.PanelBody) `
  padding-right: 6px;
`;
const StatCount = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(0.5)};
  margin-top: ${(0, space_1.default)(0.25)};
  color: ${p => p.theme.textColor};
`;
//# sourceMappingURL=metricChart.jsx.map