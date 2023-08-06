Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectFiltersChart = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const STAT_OPS = {
    'browser-extensions': { title: (0, locale_1.t)('Browser Extension'), color: theme_1.default.gray200 },
    cors: { title: 'CORS', color: theme_1.default.orange400 },
    'error-message': { title: (0, locale_1.t)('Error Message'), color: theme_1.default.purple300 },
    'discarded-hash': { title: (0, locale_1.t)('Discarded Issue'), color: theme_1.default.gray200 },
    'invalid-csp': { title: (0, locale_1.t)('Invalid CSP'), color: theme_1.default.blue300 },
    'ip-address': { title: (0, locale_1.t)('IP Address'), color: theme_1.default.red200 },
    'legacy-browsers': { title: (0, locale_1.t)('Legacy Browser'), color: theme_1.default.gray200 },
    localhost: { title: (0, locale_1.t)('Localhost'), color: theme_1.default.blue300 },
    'release-version': { title: (0, locale_1.t)('Release'), color: theme_1.default.purple200 },
    'web-crawlers': { title: (0, locale_1.t)('Web Crawler'), color: theme_1.default.red300 },
};
class ProjectFiltersChart extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            error: false,
            statsError: false,
            formattedData: [],
            blankStats: true,
        };
        this.fetchData = () => {
            this.getFilterStats();
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if (prevProps.project !== this.props.project) {
            this.fetchData();
        }
    }
    formatData(rawData) {
        const seriesWithData = new Set();
        const transformed = Object.keys(STAT_OPS).map(stat => ({
            data: rawData[stat].map(([timestamp, value]) => {
                if (value > 0) {
                    seriesWithData.add(STAT_OPS[stat].title);
                    this.setState({ blankStats: false });
                }
                return { name: timestamp * 1000, value };
            }),
            seriesName: STAT_OPS[stat].title,
            color: STAT_OPS[stat].color,
        }));
        return transformed.filter((series) => seriesWithData.has(series.seriesName));
    }
    getFilterStats() {
        const statOptions = Object.keys(STAT_OPS);
        const { project } = this.props;
        const { orgId } = this.props.params;
        const until = Math.floor(new Date().getTime() / 1000);
        const since = until - 3600 * 24 * 30;
        const statEndpoint = `/projects/${orgId}/${project.slug}/stats/`;
        const query = {
            since,
            until,
            resolution: '1d',
        };
        const requests = statOptions.map(stat => this.props.api.requestPromise(statEndpoint, {
            query: Object.assign({ stat }, query),
        }));
        Promise.all(requests)
            .then(results => {
            const rawStatsData = {};
            for (let i = 0; i < statOptions.length; i++) {
                rawStatsData[statOptions[i]] = results[i];
            }
            this.setState({
                formattedData: this.formatData(rawStatsData),
                error: false,
                loading: false,
            });
        })
            .catch(() => {
            this.setState({ error: true, loading: false });
        });
    }
    render() {
        const { loading, error, formattedData } = this.state;
        const isLoading = loading || !formattedData;
        const hasError = !isLoading && error;
        const hasLoaded = !isLoading && !error;
        const colors = formattedData
            ? formattedData.map(series => series.color || theme_1.default.gray200)
            : undefined;
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Errors filtered in the last 30 days (by day)')}</panels_1.PanelHeader>

        <panels_1.PanelBody withPadding>
          {isLoading && <placeholder_1.default height="100px"/>}
          {hasError && <loadingError_1.default onRetry={this.fetchData}/>}
          {hasLoaded && !this.state.blankStats && (<miniBarChart_1.default series={formattedData} colors={colors} height={100} isGroupedByDate stacked labelYAxisExtents/>)}
          {hasLoaded && this.state.blankStats && (<emptyMessage_1.default title={(0, locale_1.t)('Nothing filtered in the last 30 days.')} description={(0, locale_1.t)('Issues filtered as a result of your settings below will be shown here.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
exports.ProjectFiltersChart = ProjectFiltersChart;
exports.default = (0, withApi_1.default)(ProjectFiltersChart);
//# sourceMappingURL=projectFiltersChart.jsx.map