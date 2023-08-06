Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const styles_1 = require("app/components/charts/styles");
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const utils_1 = require("app/utils");
const formatters_1 = require("app/utils/formatters");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const queryString_1 = require("app/utils/queryString");
const sessions_1 = require("app/utils/sessions");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_2 = require("app/views/releases/utils");
const releaseComparisonChartRow_1 = (0, tslib_1.__importDefault)(require("./releaseComparisonChartRow"));
const releaseEventsChart_1 = (0, tslib_1.__importDefault)(require("./releaseEventsChart"));
const releaseSessionsChart_1 = (0, tslib_1.__importDefault)(require("./releaseSessionsChart"));
function ReleaseComparisonChart({ release, project, releaseSessions, allSessions, platform, location, loading, reloading, errored, api, organization, hasHealthData, }) {
    var _a, _b;
    const [issuesTotals, setIssuesTotals] = (0, react_1.useState)(null);
    const [eventsTotals, setEventsTotals] = (0, react_1.useState)(null);
    const [eventsLoading, setEventsLoading] = (0, react_1.useState)(false);
    const [expanded, setExpanded] = (0, react_1.useState)(new Set());
    const [isOtherExpanded, setIsOtherExpanded] = (0, react_1.useState)(false);
    const charts = [];
    const additionalCharts = [];
    const hasDiscover = organization.features.includes('discover-basic') ||
        organization.features.includes('performance-view');
    const hasPerformance = organization.features.includes('performance-view');
    const { statsPeriod: period, start, end, utc, } = (0, react_1.useMemo)(() => 
    // Memoizing this so that it does not calculate different `end` for releases without events+sessions each rerender
    (0, utils_2.getReleaseParams)({
        location,
        releaseBounds: (0, utils_2.getReleaseBounds)(release),
    }), [release, location]);
    (0, react_1.useEffect)(() => {
        if (hasDiscover || hasPerformance) {
            fetchEventsTotals();
            fetchIssuesTotals();
        }
    }, [period, start, end, organization.slug, location]);
    (0, react_1.useEffect)(() => {
        const chartInUrl = (0, queryString_1.decodeScalar)(location.query.chart);
        if ([
            types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS,
            types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS,
            types_1.ReleaseComparisonChartType.ERRORED_SESSIONS,
            types_1.ReleaseComparisonChartType.CRASHED_SESSIONS,
        ].includes(chartInUrl)) {
            setExpanded(new Set(expanded.add(types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS)));
        }
        if ([
            types_1.ReleaseComparisonChartType.HEALTHY_USERS,
            types_1.ReleaseComparisonChartType.ABNORMAL_USERS,
            types_1.ReleaseComparisonChartType.ERRORED_USERS,
            types_1.ReleaseComparisonChartType.CRASHED_USERS,
        ].includes(chartInUrl)) {
            setExpanded(new Set(expanded.add(types_1.ReleaseComparisonChartType.CRASH_FREE_USERS)));
        }
        if ([
            types_1.ReleaseComparisonChartType.SESSION_COUNT,
            types_1.ReleaseComparisonChartType.USER_COUNT,
            types_1.ReleaseComparisonChartType.ERROR_COUNT,
            types_1.ReleaseComparisonChartType.TRANSACTION_COUNT,
        ].includes(chartInUrl)) {
            setIsOtherExpanded(true);
        }
    }, [location.query.chart]);
    function fetchEventsTotals() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const url = `/organizations/${organization.slug}/eventsv2/`;
            const commonQuery = Object.assign({ environment: (0, queryString_1.decodeList)(location.query.environment), project: (0, queryString_1.decodeList)(location.query.project), start,
                end }, (period ? { statsPeriod: period } : {}));
            if (eventsTotals === null) {
                setEventsLoading(true);
            }
            try {
                const [releaseTransactionTotals, allTransactionTotals, releaseErrorTotals, allErrorTotals,] = yield Promise.all([
                    api.requestPromise(url, {
                        query: Object.assign({ field: ['failure_rate()', 'count()'], query: new tokenizeSearch_1.MutableSearch([
                                'event.type:transaction',
                                `release:${release.version}`,
                            ]).formatString() }, commonQuery),
                    }),
                    api.requestPromise(url, {
                        query: Object.assign({ field: ['failure_rate()', 'count()'], query: new tokenizeSearch_1.MutableSearch(['event.type:transaction']).formatString() }, commonQuery),
                    }),
                    api.requestPromise(url, {
                        query: Object.assign({ field: ['count()'], query: new tokenizeSearch_1.MutableSearch([
                                'event.type:error',
                                `release:${release.version}`,
                            ]).formatString() }, commonQuery),
                    }),
                    api.requestPromise(url, {
                        query: Object.assign({ field: ['count()'], query: new tokenizeSearch_1.MutableSearch(['event.type:error']).formatString() }, commonQuery),
                    }),
                ]);
                setEventsTotals({
                    allErrorCount: allErrorTotals.data[0].count,
                    releaseErrorCount: releaseErrorTotals.data[0].count,
                    allTransactionCount: allTransactionTotals.data[0].count,
                    releaseTransactionCount: releaseTransactionTotals.data[0].count,
                    releaseFailureRate: releaseTransactionTotals.data[0].failure_rate,
                    allFailureRate: allTransactionTotals.data[0].failure_rate,
                });
                setEventsLoading(false);
            }
            catch (err) {
                setEventsTotals(null);
                setEventsLoading(false);
                Sentry.captureException(err);
            }
        });
    }
    function fetchIssuesTotals() {
        var _a, _b;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const UNHANDLED_QUERY = `release:"${release.version}" error.handled:0`;
            const HANDLED_QUERY = `release:"${release.version}" error.handled:1`;
            try {
                const response = yield api.requestPromise(`/organizations/${organization.slug}/issues-count/`, {
                    query: Object.assign(Object.assign({ project: project.id, environment: (0, queryString_1.decodeList)(location.query.environment), start,
                        end }, (period ? { statsPeriod: period } : {})), { query: [UNHANDLED_QUERY, HANDLED_QUERY] }),
                });
                setIssuesTotals({
                    handled: (_a = response[HANDLED_QUERY]) !== null && _a !== void 0 ? _a : 0,
                    unhandled: (_b = response[UNHANDLED_QUERY]) !== null && _b !== void 0 ? _b : 0,
                });
            }
            catch (err) {
                setIssuesTotals(null);
                Sentry.captureException(err);
            }
        });
    }
    const releaseCrashFreeSessions = (0, sessions_1.getCrashFreeRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS);
    const allCrashFreeSessions = (0, sessions_1.getCrashFreeRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS);
    const diffCrashFreeSessions = (0, utils_1.defined)(releaseCrashFreeSessions) && (0, utils_1.defined)(allCrashFreeSessions)
        ? releaseCrashFreeSessions - allCrashFreeSessions
        : null;
    const releaseHealthySessions = (0, sessions_1.getSessionStatusRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY);
    const allHealthySessions = (0, sessions_1.getSessionStatusRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY);
    const diffHealthySessions = (0, utils_1.defined)(releaseHealthySessions) && (0, utils_1.defined)(allHealthySessions)
        ? releaseHealthySessions - allHealthySessions
        : null;
    const releaseAbnormalSessions = (0, sessions_1.getSessionStatusRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL);
    const allAbnormalSessions = (0, sessions_1.getSessionStatusRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL);
    const diffAbnormalSessions = (0, utils_1.defined)(releaseAbnormalSessions) && (0, utils_1.defined)(allAbnormalSessions)
        ? releaseAbnormalSessions - allAbnormalSessions
        : null;
    const releaseErroredSessions = (0, sessions_1.getSessionStatusRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED);
    const allErroredSessions = (0, sessions_1.getSessionStatusRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED);
    const diffErroredSessions = (0, utils_1.defined)(releaseErroredSessions) && (0, utils_1.defined)(allErroredSessions)
        ? releaseErroredSessions - allErroredSessions
        : null;
    const releaseCrashedSessions = (0, sessions_1.getSessionStatusRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED);
    const allCrashedSessions = (0, sessions_1.getSessionStatusRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED);
    const diffCrashedSessions = (0, utils_1.defined)(releaseCrashedSessions) && (0, utils_1.defined)(allCrashedSessions)
        ? releaseCrashedSessions - allCrashedSessions
        : null;
    const releaseCrashFreeUsers = (0, sessions_1.getCrashFreeRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    const allCrashFreeUsers = (0, sessions_1.getCrashFreeRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS);
    const diffCrashFreeUsers = (0, utils_1.defined)(releaseCrashFreeUsers) && (0, utils_1.defined)(allCrashFreeUsers)
        ? releaseCrashFreeUsers - allCrashFreeUsers
        : null;
    const releaseHealthyUsers = (0, sessions_1.getSessionStatusRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY);
    const allHealthyUsers = (0, sessions_1.getSessionStatusRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY);
    const diffHealthyUsers = (0, utils_1.defined)(releaseHealthyUsers) && (0, utils_1.defined)(allHealthyUsers)
        ? releaseHealthyUsers - allHealthyUsers
        : null;
    const releaseAbnormalUsers = (0, sessions_1.getSessionStatusRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL);
    const allAbnormalUsers = (0, sessions_1.getSessionStatusRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL);
    const diffAbnormalUsers = (0, utils_1.defined)(releaseAbnormalUsers) && (0, utils_1.defined)(allAbnormalUsers)
        ? releaseAbnormalUsers - allAbnormalUsers
        : null;
    const releaseErroredUsers = (0, sessions_1.getSessionStatusRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED);
    const allErroredUsers = (0, sessions_1.getSessionStatusRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED);
    const diffErroredUsers = (0, utils_1.defined)(releaseErroredUsers) && (0, utils_1.defined)(allErroredUsers)
        ? releaseErroredUsers - allErroredUsers
        : null;
    const releaseCrashedUsers = (0, sessions_1.getSessionStatusRate)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED);
    const allCrashedUsers = (0, sessions_1.getSessionStatusRate)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED);
    const diffCrashedUsers = (0, utils_1.defined)(releaseCrashedUsers) && (0, utils_1.defined)(allCrashedUsers)
        ? releaseCrashedUsers - allCrashedUsers
        : null;
    const releaseSessionsCount = (0, sessions_1.getCount)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS);
    const allSessionsCount = (0, sessions_1.getCount)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS);
    const releaseUsersCount = (0, sessions_1.getCount)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    const allUsersCount = (0, sessions_1.getCount)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS);
    const sessionDurationTotal = (0, utils_2.roundDuration)(((_a = (0, sessions_1.getSeriesAverage)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.DURATION)) !== null && _a !== void 0 ? _a : 0) / 1000);
    const allSessionDurationTotal = (0, utils_2.roundDuration)(((_b = (0, sessions_1.getSeriesAverage)(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.DURATION)) !== null && _b !== void 0 ? _b : 0) / 1000);
    const diffFailure = (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseFailureRate) && (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allFailureRate)
        ? eventsTotals.releaseFailureRate - eventsTotals.allFailureRate
        : null;
    if (hasHealthData) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS,
            role: 'parent',
            drilldown: null,
            thisRelease: (0, utils_1.defined)(releaseCrashFreeSessions)
                ? (0, utils_2.displaySessionStatusPercent)(releaseCrashFreeSessions)
                : null,
            allReleases: (0, utils_1.defined)(allCrashFreeSessions)
                ? (0, utils_2.displaySessionStatusPercent)(allCrashFreeSessions)
                : null,
            diff: (0, utils_1.defined)(diffCrashFreeSessions)
                ? (0, utils_2.displaySessionStatusPercent)(diffCrashFreeSessions)
                : null,
            diffDirection: diffCrashFreeSessions
                ? diffCrashFreeSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffCrashFreeSessions
                ? diffCrashFreeSessions > 0
                    ? 'green300'
                    : 'red300'
                : null,
        });
        if (expanded.has(types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS)) {
            charts.push({
                type: types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS,
                role: 'children',
                drilldown: null,
                thisRelease: (0, utils_1.defined)(releaseHealthySessions)
                    ? (0, utils_2.displaySessionStatusPercent)(releaseHealthySessions)
                    : null,
                allReleases: (0, utils_1.defined)(allHealthySessions)
                    ? (0, utils_2.displaySessionStatusPercent)(allHealthySessions)
                    : null,
                diff: (0, utils_1.defined)(diffHealthySessions)
                    ? (0, utils_2.displaySessionStatusPercent)(diffHealthySessions)
                    : null,
                diffDirection: diffHealthySessions
                    ? diffHealthySessions > 0
                        ? 'up'
                        : 'down'
                    : null,
                diffColor: diffHealthySessions
                    ? diffHealthySessions > 0
                        ? 'green300'
                        : 'red300'
                    : null,
            }, {
                type: types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS,
                role: 'children',
                drilldown: null,
                thisRelease: (0, utils_1.defined)(releaseAbnormalSessions)
                    ? (0, utils_2.displaySessionStatusPercent)(releaseAbnormalSessions)
                    : null,
                allReleases: (0, utils_1.defined)(allAbnormalSessions)
                    ? (0, utils_2.displaySessionStatusPercent)(allAbnormalSessions)
                    : null,
                diff: (0, utils_1.defined)(diffAbnormalSessions)
                    ? (0, utils_2.displaySessionStatusPercent)(diffAbnormalSessions)
                    : null,
                diffDirection: diffAbnormalSessions
                    ? diffAbnormalSessions > 0
                        ? 'up'
                        : 'down'
                    : null,
                diffColor: diffAbnormalSessions
                    ? diffAbnormalSessions > 0
                        ? 'red300'
                        : 'green300'
                    : null,
            }, {
                type: types_1.ReleaseComparisonChartType.ERRORED_SESSIONS,
                role: 'children',
                drilldown: (0, utils_1.defined)(issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.handled) ? (<tooltip_1.default title={(0, locale_1.t)('Open in Issues')}>
              <globalSelectionLink_1.default to={(0, utils_2.getReleaseHandledIssuesUrl)(organization.slug, project.id, release.version, { start, end, period: period !== null && period !== void 0 ? period : undefined })}>
                {(0, locale_1.tct)('([count] handled [issues])', {
                        count: (issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.handled)
                            ? issuesTotals.handled >= 100
                                ? '99+'
                                : issuesTotals.handled
                            : 0,
                        issues: (0, locale_1.tn)('issue', 'issues', issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.handled),
                    })}
              </globalSelectionLink_1.default>
            </tooltip_1.default>) : null,
                thisRelease: (0, utils_1.defined)(releaseErroredSessions)
                    ? (0, utils_2.displaySessionStatusPercent)(releaseErroredSessions)
                    : null,
                allReleases: (0, utils_1.defined)(allErroredSessions)
                    ? (0, utils_2.displaySessionStatusPercent)(allErroredSessions)
                    : null,
                diff: (0, utils_1.defined)(diffErroredSessions)
                    ? (0, utils_2.displaySessionStatusPercent)(diffErroredSessions)
                    : null,
                diffDirection: diffErroredSessions
                    ? diffErroredSessions > 0
                        ? 'up'
                        : 'down'
                    : null,
                diffColor: diffErroredSessions
                    ? diffErroredSessions > 0
                        ? 'red300'
                        : 'green300'
                    : null,
            }, {
                type: types_1.ReleaseComparisonChartType.CRASHED_SESSIONS,
                role: 'default',
                drilldown: (0, utils_1.defined)(issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.unhandled) ? (<tooltip_1.default title={(0, locale_1.t)('Open in Issues')}>
              <globalSelectionLink_1.default to={(0, utils_2.getReleaseUnhandledIssuesUrl)(organization.slug, project.id, release.version, { start, end, period: period !== null && period !== void 0 ? period : undefined })}>
                {(0, locale_1.tct)('([count] unhandled [issues])', {
                        count: (issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.unhandled)
                            ? issuesTotals.unhandled >= 100
                                ? '99+'
                                : issuesTotals.unhandled
                            : 0,
                        issues: (0, locale_1.tn)('issue', 'issues', issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.unhandled),
                    })}
              </globalSelectionLink_1.default>
            </tooltip_1.default>) : null,
                thisRelease: (0, utils_1.defined)(releaseCrashedSessions)
                    ? (0, utils_2.displaySessionStatusPercent)(releaseCrashedSessions)
                    : null,
                allReleases: (0, utils_1.defined)(allCrashedSessions)
                    ? (0, utils_2.displaySessionStatusPercent)(allCrashedSessions)
                    : null,
                diff: (0, utils_1.defined)(diffCrashedSessions)
                    ? (0, utils_2.displaySessionStatusPercent)(diffCrashedSessions)
                    : null,
                diffDirection: diffCrashedSessions
                    ? diffCrashedSessions > 0
                        ? 'up'
                        : 'down'
                    : null,
                diffColor: diffCrashedSessions
                    ? diffCrashedSessions > 0
                        ? 'red300'
                        : 'green300'
                    : null,
            });
        }
    }
    const hasUsers = !!(0, sessions_1.getCount)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    if (hasHealthData && (hasUsers || loading)) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.CRASH_FREE_USERS,
            role: 'parent',
            drilldown: null,
            thisRelease: (0, utils_1.defined)(releaseCrashFreeUsers)
                ? (0, utils_2.displaySessionStatusPercent)(releaseCrashFreeUsers)
                : null,
            allReleases: (0, utils_1.defined)(allCrashFreeUsers)
                ? (0, utils_2.displaySessionStatusPercent)(allCrashFreeUsers)
                : null,
            diff: (0, utils_1.defined)(diffCrashFreeUsers)
                ? (0, utils_2.displaySessionStatusPercent)(diffCrashFreeUsers)
                : null,
            diffDirection: diffCrashFreeUsers ? (diffCrashFreeUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffCrashFreeUsers
                ? diffCrashFreeUsers > 0
                    ? 'green300'
                    : 'red300'
                : null,
        });
        if (expanded.has(types_1.ReleaseComparisonChartType.CRASH_FREE_USERS)) {
            charts.push({
                type: types_1.ReleaseComparisonChartType.HEALTHY_USERS,
                role: 'children',
                drilldown: null,
                thisRelease: (0, utils_1.defined)(releaseHealthyUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(releaseHealthyUsers)
                    : null,
                allReleases: (0, utils_1.defined)(allHealthyUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(allHealthyUsers)
                    : null,
                diff: (0, utils_1.defined)(diffHealthyUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(diffHealthyUsers)
                    : null,
                diffDirection: diffHealthyUsers ? (diffHealthyUsers > 0 ? 'up' : 'down') : null,
                diffColor: diffHealthyUsers
                    ? diffHealthyUsers > 0
                        ? 'green300'
                        : 'red300'
                    : null,
            }, {
                type: types_1.ReleaseComparisonChartType.ABNORMAL_USERS,
                role: 'children',
                drilldown: null,
                thisRelease: (0, utils_1.defined)(releaseAbnormalUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(releaseAbnormalUsers)
                    : null,
                allReleases: (0, utils_1.defined)(allAbnormalUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(allAbnormalUsers)
                    : null,
                diff: (0, utils_1.defined)(diffAbnormalUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(diffAbnormalUsers)
                    : null,
                diffDirection: diffAbnormalUsers
                    ? diffAbnormalUsers > 0
                        ? 'up'
                        : 'down'
                    : null,
                diffColor: diffAbnormalUsers
                    ? diffAbnormalUsers > 0
                        ? 'red300'
                        : 'green300'
                    : null,
            }, {
                type: types_1.ReleaseComparisonChartType.ERRORED_USERS,
                role: 'children',
                drilldown: null,
                thisRelease: (0, utils_1.defined)(releaseErroredUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(releaseErroredUsers)
                    : null,
                allReleases: (0, utils_1.defined)(allErroredUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(allErroredUsers)
                    : null,
                diff: (0, utils_1.defined)(diffErroredUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(diffErroredUsers)
                    : null,
                diffDirection: diffErroredUsers ? (diffErroredUsers > 0 ? 'up' : 'down') : null,
                diffColor: diffErroredUsers
                    ? diffErroredUsers > 0
                        ? 'red300'
                        : 'green300'
                    : null,
            }, {
                type: types_1.ReleaseComparisonChartType.CRASHED_USERS,
                role: 'default',
                drilldown: null,
                thisRelease: (0, utils_1.defined)(releaseCrashedUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(releaseCrashedUsers)
                    : null,
                allReleases: (0, utils_1.defined)(allCrashedUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(allCrashedUsers)
                    : null,
                diff: (0, utils_1.defined)(diffCrashedUsers)
                    ? (0, utils_2.displaySessionStatusPercent)(diffCrashedUsers)
                    : null,
                diffDirection: diffCrashedUsers ? (diffCrashedUsers > 0 ? 'up' : 'down') : null,
                diffColor: diffCrashedUsers
                    ? diffCrashedUsers > 0
                        ? 'red300'
                        : 'green300'
                    : null,
            });
        }
    }
    if (hasPerformance) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.FAILURE_RATE,
            role: 'default',
            drilldown: null,
            thisRelease: (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseFailureRate)
                ? (0, formatters_1.formatPercentage)(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseFailureRate)
                : null,
            allReleases: (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allFailureRate)
                ? (0, formatters_1.formatPercentage)(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allFailureRate)
                : null,
            diff: diffFailure ? (0, formatters_1.formatPercentage)(Math.abs(diffFailure)) : null,
            diffDirection: diffFailure ? (diffFailure > 0 ? 'up' : 'down') : null,
            diffColor: diffFailure ? (diffFailure > 0 ? 'red300' : 'green300') : null,
        });
    }
    if (hasHealthData) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.SESSION_DURATION,
            role: 'default',
            drilldown: null,
            thisRelease: (0, utils_1.defined)(sessionDurationTotal) ? (<duration_1.default seconds={sessionDurationTotal} abbreviation/>) : null,
            allReleases: (0, utils_1.defined)(allSessionDurationTotal) ? (<duration_1.default seconds={allSessionDurationTotal} abbreviation/>) : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        });
        additionalCharts.push({
            type: types_1.ReleaseComparisonChartType.SESSION_COUNT,
            role: 'default',
            drilldown: null,
            thisRelease: (0, utils_1.defined)(releaseSessionsCount) ? (<count_1.default value={releaseSessionsCount}/>) : null,
            allReleases: (0, utils_1.defined)(allSessionsCount) ? <count_1.default value={allSessionsCount}/> : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        });
        if (hasUsers || loading) {
            additionalCharts.push({
                type: types_1.ReleaseComparisonChartType.USER_COUNT,
                role: 'default',
                drilldown: null,
                thisRelease: (0, utils_1.defined)(releaseUsersCount) ? (<count_1.default value={releaseUsersCount}/>) : null,
                allReleases: (0, utils_1.defined)(allUsersCount) ? <count_1.default value={allUsersCount}/> : null,
                diff: null,
                diffDirection: null,
                diffColor: null,
            });
        }
    }
    if (hasDiscover) {
        additionalCharts.push({
            type: types_1.ReleaseComparisonChartType.ERROR_COUNT,
            role: 'default',
            drilldown: null,
            thisRelease: (0, utils_1.defined)(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseErrorCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseErrorCount}/>) : null,
            allReleases: (0, utils_1.defined)(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allErrorCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allErrorCount}/>) : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        });
    }
    if (hasPerformance) {
        additionalCharts.push({
            type: types_1.ReleaseComparisonChartType.TRANSACTION_COUNT,
            role: 'default',
            drilldown: null,
            thisRelease: (0, utils_1.defined)(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseTransactionCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseTransactionCount}/>) : null,
            allReleases: (0, utils_1.defined)(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allTransactionCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allTransactionCount}/>) : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        });
    }
    function handleChartChange(chartType) {
        react_router_1.browserHistory.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { chart: chartType }) }));
    }
    function handleExpanderToggle(chartType) {
        if (expanded.has(chartType)) {
            expanded.delete(chartType);
            setExpanded(new Set(expanded));
        }
        else {
            setExpanded(new Set(expanded.add(chartType)));
        }
    }
    function getTableHeaders(withExpanders) {
        const headers = [
            <DescriptionCell key="description">{(0, locale_1.t)('Description')}</DescriptionCell>,
            <Cell key="releases">{(0, locale_1.t)('All Releases')}</Cell>,
            <Cell key="release">{(0, locale_1.t)('This Release')}</Cell>,
            <Cell key="change">{(0, locale_1.t)('Change')}</Cell>,
        ];
        if (withExpanders) {
            headers.push(<Cell key="expanders"/>);
        }
        return headers;
    }
    function getChartDiff(diff, diffColor, diffDirection) {
        return diff ? (<Change color={(0, utils_1.defined)(diffColor) ? diffColor : undefined}>
        {diff}{' '}
        {(0, utils_1.defined)(diffDirection) ? (<icons_1.IconArrow direction={diffDirection} size="xs"/>) : (<StyledNotAvailable />)}
      </Change>) : null;
    }
    // if there are no sessions, we do not need to do row toggling because there won't be as many rows
    if (!hasHealthData) {
        charts.push(...additionalCharts);
        additionalCharts.splice(0, additionalCharts.length);
    }
    let activeChart = (0, queryString_1.decodeScalar)(location.query.chart, hasHealthData
        ? types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS
        : hasPerformance
            ? types_1.ReleaseComparisonChartType.FAILURE_RATE
            : types_1.ReleaseComparisonChartType.ERROR_COUNT);
    let chart = [...charts, ...additionalCharts].find(ch => ch.type === activeChart);
    if (!chart) {
        chart = charts[0];
        activeChart = charts[0].type;
    }
    const showPlaceholders = loading || eventsLoading;
    const withExpanders = hasHealthData || additionalCharts.length > 0;
    if (errored || !chart) {
        return (<panels_1.Panel>
        <errorPanel_1.default>
          <icons_1.IconWarning color="gray300" size="lg"/>
        </errorPanel_1.default>
      </panels_1.Panel>);
    }
    const titleChartDiff = chart.diff !== '0%' && chart.thisRelease !== '0%'
        ? getChartDiff(chart.diff, chart.diffColor, chart.diffDirection)
        : null;
    function renderChartRow(_a) {
        var { diff, diffColor, diffDirection } = _a, rest = (0, tslib_1.__rest)(_a, ["diff", "diffColor", "diffDirection"]);
        return (<releaseComparisonChartRow_1.default {...rest} key={rest.type} diff={diff} showPlaceholders={showPlaceholders} activeChart={activeChart} onChartChange={handleChartChange} chartDiff={getChartDiff(diff, diffColor, diffDirection)} onExpanderToggle={handleExpanderToggle} expanded={expanded.has(rest.type)} withExpanders={withExpanders}/>);
    }
    return (<react_1.Fragment>
      <ChartPanel>
        <styles_1.ChartContainer>
          {[
            types_1.ReleaseComparisonChartType.ERROR_COUNT,
            types_1.ReleaseComparisonChartType.TRANSACTION_COUNT,
            types_1.ReleaseComparisonChartType.FAILURE_RATE,
        ].includes(activeChart)
            ? (0, getDynamicText_1.default)({
                value: (<releaseEventsChart_1.default release={release} project={project} chartType={activeChart} period={period !== null && period !== void 0 ? period : undefined} start={start} end={end} utc={utc === 'true'} value={chart.thisRelease} diff={titleChartDiff}/>),
                fixed: 'Events Chart',
            })
            : (0, getDynamicText_1.default)({
                value: (<releaseSessionsChart_1.default releaseSessions={releaseSessions} allSessions={allSessions} release={release} project={project} chartType={activeChart} platform={platform} period={period !== null && period !== void 0 ? period : undefined} start={start} end={end} utc={utc === 'true'} value={chart.thisRelease} diff={titleChartDiff} loading={loading} reloading={reloading}/>),
                fixed: 'Sessions Chart',
            })}
        </styles_1.ChartContainer>
      </ChartPanel>
      <ChartTable headers={getTableHeaders(withExpanders)} data-test-id="release-comparison-table" withExpanders={withExpanders}>
        {charts.map(chartRow => renderChartRow(chartRow))}
        {additionalCharts.length > 0 && (<ShowMoreWrapper onClick={() => setIsOtherExpanded(!isOtherExpanded)} isExpanded={isOtherExpanded}>
            <ShowMoreTitle>
              <icons_1.IconActivity size="xs"/>
              {isOtherExpanded
                ? (0, locale_1.tn)('Hide %s Other', 'Hide %s Others', additionalCharts.length)
                : (0, locale_1.tn)('Show %s Other', 'Show %s Others', additionalCharts.length)}
            </ShowMoreTitle>
            <ShowMoreButton>
              <button_1.default borderless size="zero" icon={<icons_1.IconChevron direction={isOtherExpanded ? 'up' : 'down'}/>} label={(0, locale_1.t)('Toggle additional charts')}/>
            </ShowMoreButton>
          </ShowMoreWrapper>)}
        {isOtherExpanded && additionalCharts.map(chartRow => renderChartRow(chartRow))}
      </ChartTable>
    </react_1.Fragment>);
}
const ChartPanel = (0, styled_1.default)(panels_1.Panel) `
  margin-bottom: 0;
  border-bottom-left-radius: 0;
  border-bottom: none;
  border-bottom-right-radius: 0;
`;
const Cell = (0, styled_1.default)('div') `
  text-align: right;
  ${overflowEllipsis_1.default}
`;
const DescriptionCell = (0, styled_1.default)(Cell) `
  text-align: left;
  overflow: visible;
`;
const Change = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeLarge};
  ${p => p.color && `color: ${p.theme[p.color]}`}
`;
const ChartTable = (0, styled_1.default)(panels_1.PanelTable) `
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  grid-template-columns: minmax(400px, auto) repeat(3, minmax(min-content, 1fr)) ${p => p.withExpanders ? '75px' : ''};

  > * {
    border-bottom: 1px solid ${p => p.theme.border};
  }

  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    grid-template-columns: repeat(4, minmax(min-content, 1fr)) ${p => p.withExpanders ? '75px' : ''};
  }
`;
const StyledNotAvailable = (0, styled_1.default)(notAvailable_1.default) `
  display: inline-block;
`;
const ShowMoreWrapper = (0, styled_1.default)('div') `
  display: contents;
  &:hover {
    cursor: pointer;
  }
  > * {
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
    ${p => p.isExpanded && `border-bottom: 1px solid ${p.theme.border};`}
  }
`;
const ShowMoreTitle = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  display: inline-grid;
  grid-template-columns: auto auto;
  gap: 10px;
  align-items: center;
  justify-content: flex-start;
  svg {
    margin-left: ${(0, space_1.default)(0.25)};
  }
`;
const ShowMoreButton = (0, styled_1.default)('div') `
  grid-column: 2 / -1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
`;
exports.default = ReleaseComparisonChart;
//# sourceMappingURL=index.jsx.map