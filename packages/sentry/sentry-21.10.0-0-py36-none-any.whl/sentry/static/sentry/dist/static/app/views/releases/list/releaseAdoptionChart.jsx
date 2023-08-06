Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const compact_1 = (0, tslib_1.__importDefault)(require("lodash/compact"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const sessionsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/sessionsRequest"));
const styles_1 = require("app/components/charts/styles");
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const utils_1 = require("app/components/charts/utils");
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
const queryString_1 = require("app/utils/queryString");
const sessions_1 = require("app/utils/sessions");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const releaseListRequest_1 = require("app/views/releases/list/releaseListRequest");
const utils_2 = require("app/views/releases/list/utils");
class ReleaseAdoptionChart extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleClick = (params) => {
            const { organization, router, selection, location } = this.props;
            const project = selection.projects[0];
            router.push({
                pathname: `/organizations/${organization === null || organization === void 0 ? void 0 : organization.slug}/releases/${encodeURIComponent(params.seriesId)}/`,
                query: { project, environment: location.query.environment },
            });
        };
    }
    // needs to have different granularity, that's why we use custom getInterval instead of getSessionsInterval
    getInterval() {
        const { organization, location } = this.props;
        const datetimeObj = {
            start: (0, queryString_1.decodeScalar)(location.query.start),
            end: (0, queryString_1.decodeScalar)(location.query.end),
            period: (0, queryString_1.decodeScalar)(location.query.statsPeriod),
        };
        const diffInMinutes = (0, utils_1.getDiffInMinutes)(datetimeObj);
        // use high fidelity intervals when available
        // limit on backend is set to six hour
        if (organization.features.includes('minute-resolution-sessions') &&
            diffInMinutes < 360) {
            return '10m';
        }
        if (diffInMinutes >= utils_1.ONE_WEEK) {
            return '1d';
        }
        else {
            return '1h';
        }
    }
    getReleasesSeries(response) {
        const { activeDisplay } = this.props;
        const releases = response === null || response === void 0 ? void 0 : response.groups.map(group => group.by.release);
        if (!releases) {
            return null;
        }
        return releases.map(release => {
            return {
                id: release,
                seriesName: (0, formatters_1.formatVersion)(release),
                data: (0, sessions_1.getAdoptionSeries)([response === null || response === void 0 ? void 0 : response.groups.find(({ by }) => by.release === release)], response === null || response === void 0 ? void 0 : response.groups, response === null || response === void 0 ? void 0 : response.intervals, (0, releaseListRequest_1.sessionDisplayToField)(activeDisplay)),
            };
        });
    }
    renderEmpty() {
        return (<panels_1.Panel>
        <panels_1.PanelBody withPadding>
          <ChartHeader>
            <placeholder_1.default height="24px"/>
          </ChartHeader>
          <placeholder_1.default height="200px"/>
        </panels_1.PanelBody>
        <ChartFooter>
          <placeholder_1.default height="34px"/>
        </ChartFooter>
      </panels_1.Panel>);
    }
    render() {
        const { activeDisplay, router, selection, api, organization, location } = this.props;
        const { start, end, period, utc } = selection.datetime;
        const query = (0, queryString_1.decodeScalar)(location.query.query);
        const hasSemver = organization.features.includes('semver');
        const interval = this.getInterval();
        const field = (0, releaseListRequest_1.sessionDisplayToField)(activeDisplay);
        return (<sessionsRequest_1.default api={api} organization={organization} interval={interval} groupBy={['release']} field={[field]} query={query ? (hasSemver ? query : `release:${query}`) : undefined} {...(0, getParams_1.getParams)((0, pick_1.default)(location.query, Object.values(globalSelectionHeader_1.URL_PARAM)))}>
        {({ response, loading, reloading }) => {
                const totalCount = (0, sessions_1.getCount)(response === null || response === void 0 ? void 0 : response.groups, field);
                const releasesSeries = this.getReleasesSeries(response);
                if (loading) {
                    return this.renderEmpty();
                }
                if (!(releasesSeries === null || releasesSeries === void 0 ? void 0 : releasesSeries.length)) {
                    return null;
                }
                const numDataPoints = releasesSeries[0].data.length;
                const xAxisData = releasesSeries[0].data.map(point => point.name);
                const hideLastPoint = releasesSeries.findIndex(series => series.data[numDataPoints - 1].value > 0) === -1;
                return (<panels_1.Panel>
              <panels_1.PanelBody withPadding>
                <ChartHeader>
                  <ChartTitle>{(0, locale_1.t)('Release Adoption')}</ChartTitle>
                </ChartHeader>
                <transitionChart_1.default loading={loading} reloading={reloading}>
                  <transparentLoadingMask_1.default visible={reloading}/>
                  <chartZoom_1.default router={router} period={period} utc={utc} start={start} end={end}>
                    {zoomRenderProps => (<lineChart_1.default {...zoomRenderProps} grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} series={releasesSeries.map(series => (Object.assign(Object.assign({}, series), { data: hideLastPoint ? series.data.slice(0, -1) : series.data })))} yAxis={{
                            min: 0,
                            max: 100,
                            type: 'value',
                            interval: 10,
                            splitNumber: 10,
                            data: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                            axisLabel: {
                                formatter: '{value}%',
                            },
                        }} xAxis={{
                            show: true,
                            min: xAxisData[0],
                            max: xAxisData[numDataPoints - 1],
                            type: 'time',
                            data: xAxisData,
                        }} tooltip={{
                            formatter: seriesParams => {
                                const series = Array.isArray(seriesParams)
                                    ? seriesParams
                                    : [seriesParams];
                                const timestamp = series[0].data[0];
                                const [first, second, third, ...rest] = series
                                    .filter(s => s.data[1] > 0)
                                    .sort((a, b) => b.data[1] - a.data[1]);
                                const restSum = rest.reduce((acc, s) => acc + s.data[1], 0);
                                const seriesToRender = (0, compact_1.default)([first, second, third]);
                                if (rest.length) {
                                    seriesToRender.push({
                                        seriesName: (0, locale_1.tn)('%s Other', '%s Others', rest.length),
                                        data: [timestamp, restSum],
                                        marker: '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;"></span>',
                                    });
                                }
                                if (!seriesToRender.length) {
                                    return '<div/>';
                                }
                                const periodObj = (0, getParams_1.parseStatsPeriod)(interval) || {
                                    periodLength: 'd',
                                    period: '1',
                                };
                                const intervalStart = (0, moment_1.default)(timestamp).format('MMM D LT');
                                const intervalEnd = (series[0].dataIndex === numDataPoints - 1
                                    ? (0, moment_1.default)(response === null || response === void 0 ? void 0 : response.end)
                                    : (0, moment_1.default)(timestamp).add(parseInt(periodObj.period, 10), periodObj.periodLength)).format('MMM D LT');
                                return [
                                    '<div class="tooltip-series">',
                                    seriesToRender
                                        .map(s => `<div><span class="tooltip-label">${s.marker}<strong>${s.seriesName &&
                                        (0, utils_1.truncationFormatter)(s.seriesName, 12)}</strong></span>${s.data[1].toFixed(2)}%</div>`)
                                        .join(''),
                                    '</div>',
                                    `<div class="tooltip-date">${intervalStart} &mdash; ${intervalEnd}</div>`,
                                    `<div class="tooltip-arrow"></div>`,
                                ].join('');
                            },
                        }} onClick={this.handleClick}/>)}
                  </chartZoom_1.default>
                </transitionChart_1.default>
              </panels_1.PanelBody>
              <ChartFooter>
                <styles_1.InlineContainer>
                  <styles_1.SectionHeading>
                    {(0, locale_1.tct)('Total [display]', {
                        display: activeDisplay === utils_2.DisplayOption.USERS ? 'Users' : 'Sessions',
                    })}
                  </styles_1.SectionHeading>
                  <styles_1.SectionValue>
                    <count_1.default value={totalCount || 0}/>
                  </styles_1.SectionValue>
                </styles_1.InlineContainer>
              </ChartFooter>
            </panels_1.Panel>);
            }}
      </sessionsRequest_1.default>);
    }
}
exports.default = (0, withApi_1.default)(ReleaseAdoptionChart);
const ChartHeader = (0, styled_1.default)(styles_1.HeaderTitleLegend) `
  margin-bottom: ${(0, space_1.default)(1)};
`;
const ChartTitle = (0, styled_1.default)('header') `
  display: flex;
  flex-direction: row;
`;
const ChartFooter = (0, styled_1.default)(panels_1.PanelFooter) `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(1)} 20px;
`;
//# sourceMappingURL=releaseAdoptionChart.jsx.map