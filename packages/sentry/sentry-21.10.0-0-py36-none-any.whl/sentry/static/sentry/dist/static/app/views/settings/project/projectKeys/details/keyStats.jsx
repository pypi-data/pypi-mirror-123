Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const getInitialState = () => {
    const until = Math.floor(new Date().getTime() / 1000);
    return {
        since: until - 3600 * 24 * 30,
        until,
        loading: true,
        error: false,
        series: [],
        emptyStats: false,
    };
};
class KeyStats extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = getInitialState();
        this.fetchData = () => {
            const { keyId, orgId, projectId } = this.props.params;
            this.props.api.request(`/projects/${orgId}/${projectId}/keys/${keyId}/stats/`, {
                query: {
                    since: this.state.since,
                    until: this.state.until,
                    resolution: '1d',
                },
                success: data => {
                    let emptyStats = true;
                    const dropped = [];
                    const accepted = [];
                    data.forEach(p => {
                        if (p.total) {
                            emptyStats = false;
                        }
                        dropped.push({ name: p.ts * 1000, value: p.dropped });
                        accepted.push({ name: p.ts * 1000, value: p.accepted });
                    });
                    const series = [
                        {
                            seriesName: (0, locale_1.t)('Accepted'),
                            data: accepted,
                        },
                        {
                            seriesName: (0, locale_1.t)('Rate Limited'),
                            data: dropped,
                        },
                    ];
                    this.setState({
                        series,
                        emptyStats,
                        error: false,
                        loading: false,
                    });
                },
                error: () => {
                    this.setState({ error: true, loading: false });
                },
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    render() {
        if (this.state.error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Key usage in the last 30 days (by day)')}</panels_1.PanelHeader>
        <panels_1.PanelBody withPadding>
          {this.state.loading ? (<placeholder_1.default height="150px"/>) : !this.state.emptyStats ? (<miniBarChart_1.default isGroupedByDate series={this.state.series} height={150} colors={[theme_1.default.gray200, theme_1.default.red300]} stacked labelYAxisExtents/>) : (<emptyMessage_1.default title={(0, locale_1.t)('Nothing recorded in the last 30 days.')} description={(0, locale_1.t)('Total events captured using these credentials.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
exports.default = KeyStats;
//# sourceMappingURL=keyStats.jsx.map