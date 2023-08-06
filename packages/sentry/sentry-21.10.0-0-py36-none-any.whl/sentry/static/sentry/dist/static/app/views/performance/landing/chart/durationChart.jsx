Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const styles_1 = require("app/components/charts/styles");
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const utils_1 = require("app/components/charts/utils");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dates_1 = require("app/utils/dates");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const chart_1 = (0, tslib_1.__importDefault)(require("../../charts/chart"));
const styles_2 = require("../../styles");
const utils_2 = require("../display/utils");
function DurationChart({ organization, eventView, location, router, field, title, titleTooltip, backupField, usingBackupAxis, }) {
    const api = (0, useApi_1.default)();
    // construct request parameters for fetching chart data
    const globalSelection = eventView.getGlobalSelection();
    const start = globalSelection.datetime.start
        ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.start)
        : null;
    const end = globalSelection.datetime.end
        ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.end)
        : null;
    const { utc } = (0, getParams_1.getParams)(location.query);
    const _backupField = backupField ? [backupField] : [];
    const apiPayload = eventView.getEventsAPIPayload(location);
    return (<eventsRequest_1.default organization={organization} api={api} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} team={apiPayload.team} start={start} end={end} interval={(0, utils_1.getInterval)({
            start,
            end,
            period: globalSelection.datetime.period,
        }, 'high')} showLoading={false} query={apiPayload.query} includePrevious={false} yAxis={[field, ..._backupField]} partial hideError referrer="api.performance.homepage.duration-chart">
      {({ loading, reloading, errored, timeseriesData: singleAxisResults, results: multiAxisResults, }) => {
            const _field = usingBackupAxis ? (0, utils_2.getFieldOrBackup)(field, backupField) : field;
            const results = singleAxisResults
                ? singleAxisResults
                : [multiAxisResults === null || multiAxisResults === void 0 ? void 0 : multiAxisResults.find(r => r.seriesName === _field)].filter(Boolean);
            const series = results
                ? results.map((_a) => {
                    var rest = (0, tslib_1.__rest)(_a, []);
                    return Object.assign(Object.assign({}, rest), { seriesName: _field });
                })
                : [];
            if (errored) {
                return (<errorPanel_1.default>
              <icons_1.IconWarning color="gray300" size="lg"/>
            </errorPanel_1.default>);
            }
            return (<div>
            <styles_2.DoubleHeaderContainer>
              <styles_1.HeaderTitleLegend>
                {title}
                <questionTooltip_1.default position="top" size="sm" title={titleTooltip}/>
              </styles_1.HeaderTitleLegend>
            </styles_2.DoubleHeaderContainer>
            {results && (<ChartContainer>
                <MaskContainer>
                  <transparentLoadingMask_1.default visible={loading}/>
                  {(0, getDynamicText_1.default)({
                        value: (<chart_1.default height={250} data={series} loading={loading || reloading} router={router} statsPeriod={globalSelection.datetime.period} start={start} end={end} utc={utc === 'true'} grid={{
                                left: (0, space_1.default)(3),
                                right: (0, space_1.default)(3),
                                top: (0, space_1.default)(3),
                                bottom: loading || reloading ? (0, space_1.default)(4) : (0, space_1.default)(1.5),
                            }} disableMultiAxis/>),
                        fixed: <placeholder_1.default height="250px" testId="skeleton-ui"/>,
                    })}
                </MaskContainer>
              </ChartContainer>)}
          </div>);
        }}
    </eventsRequest_1.default>);
}
const ChartContainer = (0, styled_1.default)('div') `
  padding-top: ${(0, space_1.default)(1)};
`;
const MaskContainer = (0, styled_1.default)('div') `
  position: relative;
`;
exports.default = (0, react_router_1.withRouter)(DurationChart);
//# sourceMappingURL=durationChart.jsx.map