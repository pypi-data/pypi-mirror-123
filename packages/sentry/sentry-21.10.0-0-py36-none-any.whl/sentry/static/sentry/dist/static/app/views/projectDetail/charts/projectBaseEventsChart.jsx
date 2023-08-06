Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const events_1 = require("app/actionCreators/events");
const eventsChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsChart"));
const styles_1 = require("app/components/charts/styles");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const locale_1 = require("app/locale");
const charts_1 = require("app/utils/discover/charts");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
class ProjectBaseEventsChart extends react_1.Component {
    componentDidMount() {
        this.fetchTotalCount();
    }
    componentDidUpdate(prevProps) {
        if (!(0, utils_1.isSelectionEqual)(this.props.selection, prevProps.selection)) {
            this.fetchTotalCount();
        }
    }
    fetchTotalCount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, selection, onTotalValuesChange, query } = this.props;
            const { projects, environments, datetime } = selection;
            try {
                const totals = yield (0, events_1.fetchTotalCount)(api, organization.slug, Object.assign({ field: [], query, environment: environments, project: projects.map(proj => String(proj)) }, (0, getParams_1.getParams)(datetime)));
                onTotalValuesChange(totals);
            }
            catch (err) {
                onTotalValuesChange(null);
                Sentry.captureException(err);
            }
        });
    }
    render() {
        const _a = this.props, { router, organization, selection, api, yAxis, query, field, title, theme, help } = _a, eventsChartProps = (0, tslib_1.__rest)(_a, ["router", "organization", "selection", "api", "yAxis", "query", "field", "title", "theme", "help"]);
        const { projects, environments, datetime } = selection;
        const { start, end, period, utc } = datetime;
        return (0, getDynamicText_1.default)({
            value: (<eventsChart_1.default {...eventsChartProps} router={router} organization={organization} showLegend yAxis={yAxis} query={query} api={api} projects={projects} environments={environments} start={start} end={end} period={period} utc={utc} field={field} currentSeriesName={(0, locale_1.t)('This Period')} previousSeriesName={(0, locale_1.t)('Previous Period')} disableableSeries={[(0, locale_1.t)('This Period'), (0, locale_1.t)('Previous Period')]} chartHeader={<styles_1.HeaderTitleLegend>
              {title}
              {help && <questionTooltip_1.default size="sm" position="top" title={help}/>}
            </styles_1.HeaderTitleLegend>} legendOptions={{ right: 10, top: 0 }} chartOptions={{
                    grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' },
                    yAxis: {
                        axisLabel: {
                            color: theme.gray200,
                            formatter: (value) => (0, charts_1.axisLabelFormatter)(value, yAxis),
                        },
                        scale: true,
                    },
                }}/>),
            fixed: `${title} Chart`,
        });
    }
}
exports.default = (0, withGlobalSelection_1.default)((0, react_2.withTheme)(ProjectBaseEventsChart));
//# sourceMappingURL=projectBaseEventsChart.jsx.map