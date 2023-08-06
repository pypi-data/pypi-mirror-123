Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const utils_1 = require("app/components/charts/utils");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
const utils_2 = require("../utils");
function Chart({ series: timeseriesResults, displayType, location, errored, isLoading, selection, router, platform, }) {
    const { datetime } = selection;
    const { utc, period, start, end } = datetime;
    const theme = (0, react_1.useTheme)();
    const filteredTimeseriesResults = timeseriesResults.filter(({ seriesName }) => {
        // There is no concept of Abnormal sessions in javascript
        if ((seriesName === sessionTerm_1.sessionTerm.abnormal || seriesName === sessionTerm_1.sessionTerm.otherAbnormal) &&
            platform &&
            ['javascript', 'node'].includes(platform)) {
            return false;
        }
        return true;
    });
    const colors = timeseriesResults
        ? theme.charts.getColorPalette(timeseriesResults.length - 2)
        : [];
    // Create a list of series based on the order of the fields,
    const series = filteredTimeseriesResults
        ? filteredTimeseriesResults.map((values, index) => (Object.assign(Object.assign({}, values), { color: colors[index] })))
        : [];
    const chartProps = {
        series,
        legend: {
            right: 10,
            top: 0,
            selected: (0, utils_1.getSeriesSelection)(location),
        },
        grid: {
            left: '0px',
            right: '10px',
            top: '30px',
            bottom: '0px',
        },
    };
    function renderChart(zoomRenderProps) {
        switch (displayType) {
            case utils_2.DisplayType.BAR:
                return <barChart_1.default {...zoomRenderProps} {...chartProps}/>;
            case utils_2.DisplayType.AREA:
                return <areaChart_1.default {...zoomRenderProps} stacked {...chartProps}/>;
            case utils_2.DisplayType.LINE:
            default:
                return <lineChart_1.default {...zoomRenderProps} {...chartProps}/>;
        }
    }
    return (<chartZoom_1.default router={router} period={period} utc={utc} start={start} end={end}>
      {zoomRenderProps => {
            if (errored) {
                return (<errorPanel_1.default>
              <icons_1.IconWarning color="gray300" size="lg"/>
            </errorPanel_1.default>);
            }
            return (<transitionChart_1.default loading={isLoading} reloading={isLoading}>
            <LoadingScreen loading={isLoading}/>
            {(0, getDynamicText_1.default)({
                    value: renderChart(zoomRenderProps),
                    fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                })}
          </transitionChart_1.default>);
        }}
    </chartZoom_1.default>);
}
exports.default = Chart;
const LoadingScreen = ({ loading }) => {
    if (!loading) {
        return null;
    }
    return (<StyledTransparentLoadingMask visible={loading}>
      <loadingIndicator_1.default mini/>
    </StyledTransparentLoadingMask>);
};
const StyledTransparentLoadingMask = (0, styled_1.default)(props => (<transparentLoadingMask_1.default {...props} maskBackgroundColor="transparent"/>)) `
  display: flex;
  justify-content: center;
  align-items: center;
`;
//# sourceMappingURL=chart.jsx.map