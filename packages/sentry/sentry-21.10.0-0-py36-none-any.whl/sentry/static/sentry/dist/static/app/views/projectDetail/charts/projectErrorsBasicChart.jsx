Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const baseChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/baseChart"));
const styles_1 = require("app/components/charts/styles");
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const ALLOWED_TIME_PERIODS = ['1h', '24h', '7d', '14d', '30d'];
class ProjectErrorsBasicChart extends asyncComponent_1.default {
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { projects: null });
    }
    getEndpoints() {
        const { organization, projectId } = this.props;
        if (!projectId) {
            return [];
        }
        return [
            [
                'projects',
                `/organizations/${organization.slug}/projects/`,
                {
                    query: {
                        statsPeriod: this.getStatsPeriod(),
                        query: `id:${projectId}`,
                    },
                },
            ],
        ];
    }
    componentDidMount() {
        const { location } = this.props;
        if (!ALLOWED_TIME_PERIODS.includes(location.query.statsPeriod)) {
            react_router_1.browserHistory.replace({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { statsPeriod: this.getStatsPeriod(), start: undefined, end: undefined }),
            });
        }
    }
    onLoadAllEndpointsSuccess() {
        var _a, _b, _c, _d;
        this.props.onTotalValuesChange((_d = (_c = (_b = (_a = this.state.projects) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.stats) === null || _c === void 0 ? void 0 : _c.reduce((acc, [, value]) => acc + value, 0)) !== null && _d !== void 0 ? _d : null);
    }
    getStatsPeriod() {
        const { location } = this.props;
        const statsPeriod = location.query.statsPeriod;
        if (ALLOWED_TIME_PERIODS.includes(statsPeriod)) {
            return statsPeriod;
        }
        return constants_1.DEFAULT_STATS_PERIOD;
    }
    getSeries() {
        var _a, _b, _c;
        const { projects } = this.state;
        return [
            {
                cursor: 'normal',
                name: (0, locale_1.t)('Errors'),
                type: 'bar',
                data: (_c = (_b = (_a = projects === null || projects === void 0 ? void 0 : projects[0]) === null || _a === void 0 ? void 0 : _a.stats) === null || _b === void 0 ? void 0 : _b.map(([timestamp, value]) => [timestamp * 1000, value])) !== null && _c !== void 0 ? _c : [],
            },
        ];
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        const { loading, reloading } = this.state;
        return (0, getDynamicText_1.default)({
            value: (<transitionChart_1.default loading={loading} reloading={reloading}>
          <transparentLoadingMask_1.default visible={reloading}/>

          <styles_1.HeaderTitleLegend>{(0, locale_1.t)('Daily Errors')}</styles_1.HeaderTitleLegend>

          <baseChart_1.default series={this.getSeries()} isGroupedByDate showTimeInTooltip colors={theme => [theme.purple300, theme.purple200]} grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }}/>
        </transitionChart_1.default>),
            fixed: (0, locale_1.t)('Number of Errors Chart'),
        });
    }
}
exports.default = ProjectErrorsBasicChart;
//# sourceMappingURL=projectErrorsBasicChart.jsx.map