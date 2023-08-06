Object.defineProperty(exports, "__esModule", { value: true });
exports.sessionDisplayToField = exports.reduceTimeSeriesGroups = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const indicator_1 = require("app/actionCreators/indicator");
const utils_1 = require("app/components/charts/utils");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const utils_2 = require("app/utils");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const utils_3 = require("../utils");
const utils_4 = require("./utils");
function omitIgnoredProps(props) {
    return (0, omit_1.default)(props, [
        'api',
        'organization',
        'children',
        'selection.datetime.utc',
        'location',
    ]);
}
function getInterval(datetimeObj) {
    const diffInMinutes = (0, utils_1.getDiffInMinutes)(datetimeObj);
    if (diffInMinutes >= utils_1.TWO_WEEKS) {
        return '1d';
    }
    if (diffInMinutes >= utils_1.ONE_WEEK) {
        return '6h';
    }
    if (diffInMinutes > utils_1.TWENTY_FOUR_HOURS) {
        return '4h';
    }
    // TODO(sessions): sub-hour session resolution is still not possible
    return '1h';
}
function reduceTimeSeriesGroups(acc, group, field) {
    var _a;
    (_a = group.series[field]) === null || _a === void 0 ? void 0 : _a.forEach((value, index) => { var _a; return (acc[index] = ((_a = acc[index]) !== null && _a !== void 0 ? _a : 0) + value); });
    return acc;
}
exports.reduceTimeSeriesGroups = reduceTimeSeriesGroups;
function sessionDisplayToField(display) {
    switch (display) {
        case utils_4.DisplayOption.USERS:
            return types_1.SessionField.USERS;
        case utils_4.DisplayOption.SESSIONS:
        default:
            return types_1.SessionField.SESSIONS;
    }
}
exports.sessionDisplayToField = sessionDisplayToField;
class ReleaseListRequest extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
            errored: false,
            statusCountByReleaseInPeriod: null,
            totalCountByReleaseIn24h: null,
            totalCountByProjectIn24h: null,
            statusCountByProjectInPeriod: null,
            totalCountByReleaseInPeriod: null,
            totalCountByProjectInPeriod: null,
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a, _b;
            const { api, healthStatsPeriod, disable } = this.props;
            if (disable) {
                return;
            }
            api.clear();
            this.setState({
                loading: true,
                errored: false,
                statusCountByReleaseInPeriod: null,
                totalCountByReleaseIn24h: null,
                totalCountByProjectIn24h: null,
            });
            const promises = [
                this.fetchStatusCountByReleaseInPeriod(),
                this.fetchTotalCountByReleaseIn24h(),
                this.fetchTotalCountByProjectIn24h(),
            ];
            if (healthStatsPeriod === types_1.HealthStatsPeriodOption.AUTO) {
                promises.push(this.fetchStatusCountByProjectInPeriod());
                promises.push(this.fetchTotalCountByReleaseInPeriod());
                promises.push(this.fetchTotalCountByProjectInPeriod());
            }
            try {
                const [statusCountByReleaseInPeriod, totalCountByReleaseIn24h, totalCountByProjectIn24h, statusCountByProjectInPeriod, totalCountByReleaseInPeriod, totalCountByProjectInPeriod,] = yield Promise.all(promises);
                this.setState({
                    loading: false,
                    statusCountByReleaseInPeriod,
                    totalCountByReleaseIn24h,
                    totalCountByProjectIn24h,
                    statusCountByProjectInPeriod,
                    totalCountByReleaseInPeriod,
                    totalCountByProjectInPeriod,
                });
            }
            catch (error) {
                (0, indicator_1.addErrorMessage)((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : (0, locale_1.t)('Error loading health data'));
                this.setState({
                    loading: false,
                    errored: true,
                });
            }
        });
        this.getHealthData = () => {
            // TODO(sessions): investigate if this needs to be optimized to lower O(n) complexity
            return {
                getCrashCount: this.getCrashCount,
                getCrashFreeRate: this.getCrashFreeRate,
                get24hCountByRelease: this.get24hCountByRelease,
                get24hCountByProject: this.get24hCountByProject,
                getTimeSeries: this.getTimeSeries,
                getAdoption: this.getAdoption,
            };
        };
        this.getCrashCount = (version, project, display) => {
            var _a;
            const { statusCountByReleaseInPeriod } = this.state;
            const field = sessionDisplayToField(display);
            return (_a = statusCountByReleaseInPeriod === null || statusCountByReleaseInPeriod === void 0 ? void 0 : statusCountByReleaseInPeriod.groups.find(({ by }) => by.release === version &&
                by.project === project &&
                by['session.status'] === 'crashed')) === null || _a === void 0 ? void 0 : _a.totals[field];
        };
        this.getCrashFreeRate = (version, project, display) => {
            var _a;
            const { statusCountByReleaseInPeriod } = this.state;
            const field = sessionDisplayToField(display);
            const totalCount = (_a = statusCountByReleaseInPeriod === null || statusCountByReleaseInPeriod === void 0 ? void 0 : statusCountByReleaseInPeriod.groups.filter(({ by }) => by.release === version && by.project === project)) === null || _a === void 0 ? void 0 : _a.reduce((acc, group) => acc + group.totals[field], 0);
            const crashedCount = this.getCrashCount(version, project, display);
            return !(0, utils_2.defined)(totalCount) || totalCount === 0
                ? null
                : (0, utils_3.getCrashFreePercent)(100 - (0, utils_2.percent)(crashedCount !== null && crashedCount !== void 0 ? crashedCount : 0, totalCount !== null && totalCount !== void 0 ? totalCount : 0));
        };
        this.get24hCountByRelease = (version, project, display) => {
            var _a;
            const { totalCountByReleaseIn24h } = this.state;
            const field = sessionDisplayToField(display);
            return (_a = totalCountByReleaseIn24h === null || totalCountByReleaseIn24h === void 0 ? void 0 : totalCountByReleaseIn24h.groups.filter(({ by }) => by.release === version && by.project === project)) === null || _a === void 0 ? void 0 : _a.reduce((acc, group) => acc + group.totals[field], 0);
        };
        this.getPeriodCountByRelease = (version, project, display) => {
            var _a;
            const { totalCountByReleaseInPeriod } = this.state;
            const field = sessionDisplayToField(display);
            return (_a = totalCountByReleaseInPeriod === null || totalCountByReleaseInPeriod === void 0 ? void 0 : totalCountByReleaseInPeriod.groups.filter(({ by }) => by.release === version && by.project === project)) === null || _a === void 0 ? void 0 : _a.reduce((acc, group) => acc + group.totals[field], 0);
        };
        this.get24hCountByProject = (project, display) => {
            var _a;
            const { totalCountByProjectIn24h } = this.state;
            const field = sessionDisplayToField(display);
            return (_a = totalCountByProjectIn24h === null || totalCountByProjectIn24h === void 0 ? void 0 : totalCountByProjectIn24h.groups.filter(({ by }) => by.project === project)) === null || _a === void 0 ? void 0 : _a.reduce((acc, group) => acc + group.totals[field], 0);
        };
        this.getPeriodCountByProject = (project, display) => {
            var _a;
            const { totalCountByProjectInPeriod } = this.state;
            const field = sessionDisplayToField(display);
            return (_a = totalCountByProjectInPeriod === null || totalCountByProjectInPeriod === void 0 ? void 0 : totalCountByProjectInPeriod.groups.filter(({ by }) => by.project === project)) === null || _a === void 0 ? void 0 : _a.reduce((acc, group) => acc + group.totals[field], 0);
        };
        this.getTimeSeries = (version, project, display) => {
            const { healthStatsPeriod } = this.props;
            if (healthStatsPeriod === types_1.HealthStatsPeriodOption.AUTO) {
                return this.getPeriodTimeSeries(version, project, display);
            }
            return this.get24hTimeSeries(version, project, display);
        };
        this.get24hTimeSeries = (version, project, display) => {
            var _a, _b, _c;
            const { totalCountByReleaseIn24h, totalCountByProjectIn24h } = this.state;
            const field = sessionDisplayToField(display);
            const intervals = (_a = totalCountByProjectIn24h === null || totalCountByProjectIn24h === void 0 ? void 0 : totalCountByProjectIn24h.intervals) !== null && _a !== void 0 ? _a : [];
            const projectData = (_b = totalCountByProjectIn24h === null || totalCountByProjectIn24h === void 0 ? void 0 : totalCountByProjectIn24h.groups.find(({ by }) => by.project === project)) === null || _b === void 0 ? void 0 : _b.series[field];
            const releaseData = (_c = totalCountByReleaseIn24h === null || totalCountByReleaseIn24h === void 0 ? void 0 : totalCountByReleaseIn24h.groups.find(({ by }) => by.project === project && by.release === version)) === null || _c === void 0 ? void 0 : _c.series[field];
            return [
                {
                    seriesName: (0, locale_1.t)('This Release'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map((interval, index) => {
                        var _a;
                        return ({
                            name: (0, moment_1.default)(interval).valueOf(),
                            value: (_a = releaseData === null || releaseData === void 0 ? void 0 : releaseData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                },
                {
                    seriesName: (0, locale_1.t)('Total Project'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map((interval, index) => {
                        var _a;
                        return ({
                            name: (0, moment_1.default)(interval).valueOf(),
                            value: (_a = projectData === null || projectData === void 0 ? void 0 : projectData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                    z: 0,
                },
            ];
        };
        this.getPeriodTimeSeries = (version, project, display) => {
            var _a, _b, _c;
            const { statusCountByReleaseInPeriod, statusCountByProjectInPeriod } = this.state;
            const field = sessionDisplayToField(display);
            const intervals = (_a = statusCountByProjectInPeriod === null || statusCountByProjectInPeriod === void 0 ? void 0 : statusCountByProjectInPeriod.intervals) !== null && _a !== void 0 ? _a : [];
            const projectData = (_b = statusCountByProjectInPeriod === null || statusCountByProjectInPeriod === void 0 ? void 0 : statusCountByProjectInPeriod.groups.filter(({ by }) => by.project === project)) === null || _b === void 0 ? void 0 : _b.reduce((acc, group) => reduceTimeSeriesGroups(acc, group, field), []);
            const releaseData = (_c = statusCountByReleaseInPeriod === null || statusCountByReleaseInPeriod === void 0 ? void 0 : statusCountByReleaseInPeriod.groups.filter(({ by }) => by.project === project && by.release === version)) === null || _c === void 0 ? void 0 : _c.reduce((acc, group) => reduceTimeSeriesGroups(acc, group, field), []);
            return [
                {
                    seriesName: (0, locale_1.t)('This Release'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map((interval, index) => {
                        var _a;
                        return ({
                            name: (0, moment_1.default)(interval).valueOf(),
                            value: (_a = releaseData === null || releaseData === void 0 ? void 0 : releaseData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                },
                {
                    seriesName: (0, locale_1.t)('Total Project'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map((interval, index) => {
                        var _a;
                        return ({
                            name: (0, moment_1.default)(interval).valueOf(),
                            value: (_a = projectData === null || projectData === void 0 ? void 0 : projectData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                    z: 0,
                },
            ];
        };
        this.getAdoption = (version, project, display) => {
            const { healthStatsPeriod } = this.props;
            const countByRelease = (healthStatsPeriod === types_1.HealthStatsPeriodOption.AUTO
                ? this.getPeriodCountByRelease
                : this.get24hCountByRelease)(version, project, display);
            const countByProject = (healthStatsPeriod === types_1.HealthStatsPeriodOption.AUTO
                ? this.getPeriodCountByProject
                : this.get24hCountByProject)(project, display);
            return (0, utils_2.defined)(countByRelease) && (0, utils_2.defined)(countByProject)
                ? (0, utils_2.percent)(countByRelease, countByProject)
                : undefined;
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if (this.props.releasesReloading) {
            return;
        }
        if ((0, isEqual_1.default)(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    }
    get path() {
        const { organization } = this.props;
        return `/organizations/${organization.slug}/sessions/`;
    }
    get baseQueryParams() {
        const { location, selection, defaultStatsPeriod, releases } = this.props;
        return Object.assign({ query: new tokenizeSearch_1.MutableSearch(releases.reduce((acc, release, index, allReleases) => {
                acc.push(`release:"${release}"`);
                if (index < allReleases.length - 1) {
                    acc.push('OR');
                }
                return acc;
            }, [])).formatString(), interval: getInterval(selection.datetime) }, (0, getParams_1.getParams)((0, pick_1.default)(location.query, Object.values(globalSelectionHeader_1.URL_PARAM)), {
            defaultStatsPeriod,
        }));
    }
    /**
     * Used to calculate crash free rate, count histogram (This Release series), and crash count
     */
    fetchStatusCountByReleaseInPeriod() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, display } = this.props;
            const response = yield api.requestPromise(this.path, {
                query: Object.assign(Object.assign({}, this.baseQueryParams), { field: [
                        ...new Set([...display.map(d => sessionDisplayToField(d)), 'sum(session)']),
                    ], groupBy: ['project', 'release', 'session.status'] }),
            });
            return response;
        });
    }
    /**
     * Used to calculate count histogram (Total Project series)
     */
    fetchStatusCountByProjectInPeriod() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, display } = this.props;
            const response = yield api.requestPromise(this.path, {
                query: Object.assign(Object.assign({}, this.baseQueryParams), { query: undefined, field: [
                        ...new Set([...display.map(d => sessionDisplayToField(d)), 'sum(session)']),
                    ], groupBy: ['project', 'session.status'] }),
            });
            return response;
        });
    }
    /**
     * Used to calculate adoption, and count histogram (This Release series)
     */
    fetchTotalCountByReleaseIn24h() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, display } = this.props;
            const response = yield api.requestPromise(this.path, {
                query: Object.assign(Object.assign({}, this.baseQueryParams), { field: display.map(d => sessionDisplayToField(d)), groupBy: ['project', 'release'], interval: '1h', statsPeriod: '24h' }),
            });
            return response;
        });
    }
    fetchTotalCountByReleaseInPeriod() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, display } = this.props;
            const response = yield api.requestPromise(this.path, {
                query: Object.assign(Object.assign({}, this.baseQueryParams), { field: display.map(d => sessionDisplayToField(d)), groupBy: ['project', 'release'] }),
            });
            return response;
        });
    }
    /**
     * Used to calculate adoption, and count histogram (Total Project series)
     */
    fetchTotalCountByProjectIn24h() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, display } = this.props;
            const response = yield api.requestPromise(this.path, {
                query: Object.assign(Object.assign({}, this.baseQueryParams), { query: undefined, field: display.map(d => sessionDisplayToField(d)), groupBy: ['project'], interval: '1h', statsPeriod: '24h' }),
            });
            return response;
        });
    }
    fetchTotalCountByProjectInPeriod() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, display } = this.props;
            const response = yield api.requestPromise(this.path, {
                query: Object.assign(Object.assign({}, this.baseQueryParams), { query: undefined, field: display.map(d => sessionDisplayToField(d)), groupBy: ['project'] }),
            });
            return response;
        });
    }
    render() {
        const { loading, errored } = this.state;
        const { children } = this.props;
        return children({
            isHealthLoading: loading,
            errored,
            getHealthData: this.getHealthData(),
        });
    }
}
exports.default = (0, withApi_1.default)(ReleaseListRequest);
//# sourceMappingURL=releaseListRequest.jsx.map