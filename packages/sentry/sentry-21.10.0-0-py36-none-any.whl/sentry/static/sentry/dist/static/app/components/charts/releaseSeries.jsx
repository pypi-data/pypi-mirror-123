Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const indicator_1 = require("app/actionCreators/indicator");
const markLine_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/markLine"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const dates_1 = require("app/utils/dates");
const formatters_1 = require("app/utils/formatters");
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
// This is not an exported action/function because releases list uses AsyncComponent
// and this is not re-used anywhere else afaict
function getOrganizationReleases(api, organization, conditions) {
    const query = {};
    Object.keys(conditions).forEach(key => {
        let value = conditions[key];
        if (value && (key === 'start' || key === 'end')) {
            value = (0, dates_1.getUtcDateString)(value);
        }
        if (value) {
            query[key] = value;
        }
    });
    api.clear();
    return api.requestPromise(`/organizations/${organization.slug}/releases/stats/`, {
        includeAllArgs: true,
        method: 'GET',
        query,
    });
}
class ReleaseSeries extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            releases: null,
            releaseSeries: [],
        };
        this._isMounted = false;
        this.getOrganizationReleasesMemoized = (0, memoize_1.default)((api, conditions, organization) => getOrganizationReleases(api, conditions, organization), (_, __, conditions) => Object.values(conditions)
            .map(val => JSON.stringify(val))
            .join('-'));
        this.getReleaseSeries = (releases, lineStyle = {}) => {
            const { organization, router, tooltip, environments, start, end, period, preserveQueryParams, queryExtra, theme, } = this.props;
            const query = Object.assign({}, queryExtra);
            if (organization.features.includes('global-views')) {
                query.project = router.location.query.project;
            }
            if (preserveQueryParams) {
                query.environment = [...environments];
                query.start = start ? (0, dates_1.getUtcDateString)(start) : undefined;
                query.end = end ? (0, dates_1.getUtcDateString)(end) : undefined;
                query.statsPeriod = period || undefined;
            }
            const markLine = (0, markLine_1.default)({
                animation: false,
                lineStyle: Object.assign({ color: theme.purple300, opacity: 0.3, type: 'solid' }, lineStyle),
                label: {
                    show: false,
                },
                data: releases.map(release => ({
                    xAxis: +new Date(release.date),
                    name: (0, formatters_1.formatVersion)(release.version, true),
                    value: (0, formatters_1.formatVersion)(release.version, true),
                    onClick: () => {
                        router.push({
                            pathname: `/organizations/${organization.slug}/releases/${release.version}/`,
                            query,
                        });
                    },
                    label: {
                        formatter: () => (0, formatters_1.formatVersion)(release.version, true),
                    },
                })),
            });
            // TODO(tonyx): This conflicts with the types declaration of `MarkLine`
            // if we add it in the constructor. So we opt to add it here so typescript
            // doesn't complain.
            markLine.tooltip =
                tooltip ||
                    {
                        trigger: 'item',
                        formatter: ({ data }) => {
                            // XXX using this.props here as this function does not get re-run
                            // unless projects are changed. Using a closure variable would result
                            // in stale values.
                            const time = (0, dates_1.getFormattedDate)(data.value, 'MMM D, YYYY LT', {
                                local: !this.props.utc,
                            });
                            const version = (0, utils_1.escape)((0, formatters_1.formatVersion)(data.name, true));
                            return [
                                '<div class="tooltip-series">',
                                `<div><span class="tooltip-label"><strong>${(0, locale_1.t)('Release')}</strong></span> ${version}</div>`,
                                '</div>',
                                '<div class="tooltip-date">',
                                time,
                                '</div>',
                                '</div>',
                                '<div class="tooltip-arrow"></div>',
                            ].join('');
                        },
                    };
            return {
                seriesName: 'Releases',
                color: theme.purple200,
                data: [],
                markLine,
            };
        };
    }
    componentDidMount() {
        this._isMounted = true;
        const { releases } = this.props;
        if (releases) {
            // No need to fetch releases if passed in from props
            this.setReleasesWithSeries(releases);
            return;
        }
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)(prevProps.projects, this.props.projects) ||
            !(0, isEqual_1.default)(prevProps.environments, this.props.environments) ||
            !(0, isEqual_1.default)(prevProps.start, this.props.start) ||
            !(0, isEqual_1.default)(prevProps.end, this.props.end) ||
            !(0, isEqual_1.default)(prevProps.period, this.props.period) ||
            !(0, isEqual_1.default)(prevProps.query, this.props.query)) {
            this.fetchData();
        }
        else if (!(0, isEqual_1.default)(prevProps.emphasizeReleases, this.props.emphasizeReleases)) {
            this.setReleasesWithSeries(this.state.releases);
        }
    }
    componentWillUnmount() {
        this._isMounted = false;
        this.props.api.clear();
    }
    fetchData() {
        var _a, _b;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, projects, environments, period, start, end, memoized, query, } = this.props;
            const conditions = {
                start,
                end,
                project: projects,
                environment: environments,
                statsPeriod: period,
                query,
            };
            let hasMore = true;
            const releases = [];
            while (hasMore) {
                try {
                    const getReleases = memoized
                        ? this.getOrganizationReleasesMemoized
                        : getOrganizationReleases;
                    const [newReleases, , resp] = yield getReleases(api, organization, conditions);
                    releases.push(...newReleases);
                    if (this._isMounted) {
                        this.setReleasesWithSeries(releases);
                    }
                    const pageLinks = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link');
                    if (pageLinks) {
                        const paginationObject = (0, parseLinkHeader_1.default)(pageLinks);
                        hasMore = (_b = (_a = paginationObject === null || paginationObject === void 0 ? void 0 : paginationObject.next) === null || _a === void 0 ? void 0 : _a.results) !== null && _b !== void 0 ? _b : false;
                        conditions.cursor = paginationObject.next.cursor;
                    }
                    else {
                        hasMore = false;
                    }
                }
                catch (_c) {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error fetching releases'));
                    hasMore = false;
                }
            }
        });
    }
    setReleasesWithSeries(releases) {
        const { emphasizeReleases = [] } = this.props;
        const releaseSeries = [];
        if (emphasizeReleases.length) {
            const [unemphasizedReleases, emphasizedReleases] = (0, partition_1.default)(releases, release => !emphasizeReleases.includes(release.version));
            if (unemphasizedReleases.length) {
                releaseSeries.push(this.getReleaseSeries(unemphasizedReleases, { type: 'dotted' }));
            }
            if (emphasizedReleases.length) {
                releaseSeries.push(this.getReleaseSeries(emphasizedReleases, {
                    opacity: 0.8,
                }));
            }
        }
        else {
            releaseSeries.push(this.getReleaseSeries(releases));
        }
        this.setState({
            releases,
            releaseSeries,
        });
    }
    render() {
        const { children } = this.props;
        return children({
            releases: this.state.releases,
            releaseSeries: this.state.releaseSeries,
        });
    }
}
exports.default = (0, react_router_1.withRouter)((0, withOrganization_1.default)((0, withApi_1.default)((0, react_1.withTheme)(ReleaseSeries))));
//# sourceMappingURL=releaseSeries.jsx.map