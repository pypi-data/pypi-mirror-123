Object.defineProperty(exports, "__esModule", { value: true });
exports.generateReleaseMarkLines = exports.releaseMarkLinesLabels = exports.releaseComparisonChartHelp = exports.releaseComparisonChartTitles = exports.releaseComparisonChartLabels = exports.getReleaseEventView = exports.getReposToRender = exports.getQuery = exports.getCommitsByRepository = exports.getFilesByRepository = void 0;
const tslib_1 = require("tslib");
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const markLine_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/markLine"));
const utils_1 = require("app/components/organizations/timeRangeSelector/utils");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const dates_1 = require("app/utils/dates");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const list_1 = require("app/views/releases/list");
const utils_2 = require("../utils");
const sessionTerm_1 = require("../utils/sessionTerm");
/**
 * Convert list of individual file changes into a per-file summary grouped by repository
 */
function getFilesByRepository(fileList) {
    return fileList.reduce((filesByRepository, file) => {
        const { filename, repoName, author, type } = file;
        if (!filesByRepository.hasOwnProperty(repoName)) {
            filesByRepository[repoName] = {};
        }
        if (!filesByRepository[repoName].hasOwnProperty(filename)) {
            filesByRepository[repoName][filename] = {
                authors: {},
                types: new Set(),
            };
        }
        if (author.email) {
            filesByRepository[repoName][filename].authors[author.email] = author;
        }
        filesByRepository[repoName][filename].types.add(type);
        return filesByRepository;
    }, {});
}
exports.getFilesByRepository = getFilesByRepository;
/**
 * Convert list of individual commits into a summary grouped by repository
 */
function getCommitsByRepository(commitList) {
    return commitList.reduce((commitsByRepository, commit) => {
        var _a, _b;
        const repositoryName = (_b = (_a = commit.repository) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : (0, locale_1.t)('unknown');
        if (!commitsByRepository.hasOwnProperty(repositoryName)) {
            commitsByRepository[repositoryName] = [];
        }
        commitsByRepository[repositoryName].push(commit);
        return commitsByRepository;
    }, {});
}
exports.getCommitsByRepository = getCommitsByRepository;
function getQuery({ location, perPage = 40, activeRepository }) {
    const query = Object.assign(Object.assign({}, (0, pick_1.default)(location.query, [...Object.values(globalSelectionHeader_1.URL_PARAM), 'cursor'])), { per_page: perPage });
    if (!activeRepository) {
        return query;
    }
    return Object.assign(Object.assign({}, query), { repo_name: activeRepository.name });
}
exports.getQuery = getQuery;
/**
 * Get repositories to render according to the activeRepository
 */
function getReposToRender(repos, activeRepository) {
    if (!activeRepository) {
        return repos;
    }
    return [activeRepository.name];
}
exports.getReposToRender = getReposToRender;
/**
 * Get high level transaction information for this release
 */
function getReleaseEventView(selection, version, _organization) {
    const { projects, environments, datetime } = selection;
    const { start, end, period } = datetime;
    const discoverQuery = {
        id: undefined,
        version: 2,
        name: `${(0, locale_1.t)('Release Apdex')}`,
        fields: ['apdex()'],
        query: new tokenizeSearch_1.MutableSearch([
            `release:${version}`,
            'event.type:transaction',
            'count():>0',
        ]).formatString(),
        range: period,
        environment: environments,
        projects,
        start: start ? (0, dates_1.getUtcDateString)(start) : undefined,
        end: end ? (0, dates_1.getUtcDateString)(end) : undefined,
    };
    return eventView_1.default.fromSavedQuery(discoverQuery);
}
exports.getReleaseEventView = getReleaseEventView;
exports.releaseComparisonChartLabels = {
    [types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS]: (0, locale_1.t)('Crash Free Session Rate'),
    [types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS]: (0, locale_1.t)('Healthy'),
    [types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS]: (0, locale_1.t)('Abnormal'),
    [types_1.ReleaseComparisonChartType.ERRORED_SESSIONS]: (0, locale_1.t)('Errored'),
    [types_1.ReleaseComparisonChartType.CRASHED_SESSIONS]: (0, locale_1.t)('Crashed Session Rate'),
    [types_1.ReleaseComparisonChartType.CRASH_FREE_USERS]: (0, locale_1.t)('Crash Free User Rate'),
    [types_1.ReleaseComparisonChartType.HEALTHY_USERS]: (0, locale_1.t)('Healthy'),
    [types_1.ReleaseComparisonChartType.ABNORMAL_USERS]: (0, locale_1.t)('Abnormal'),
    [types_1.ReleaseComparisonChartType.ERRORED_USERS]: (0, locale_1.t)('Errored'),
    [types_1.ReleaseComparisonChartType.CRASHED_USERS]: (0, locale_1.t)('Crashed User Rate'),
    [types_1.ReleaseComparisonChartType.SESSION_COUNT]: (0, locale_1.t)('Session Count'),
    [types_1.ReleaseComparisonChartType.SESSION_DURATION]: (0, locale_1.t)('Session Duration p50'),
    [types_1.ReleaseComparisonChartType.USER_COUNT]: (0, locale_1.t)('User Count'),
    [types_1.ReleaseComparisonChartType.ERROR_COUNT]: (0, locale_1.t)('Error Count'),
    [types_1.ReleaseComparisonChartType.TRANSACTION_COUNT]: (0, locale_1.t)('Transaction Count'),
    [types_1.ReleaseComparisonChartType.FAILURE_RATE]: (0, locale_1.t)('Failure Rate'),
};
exports.releaseComparisonChartTitles = {
    [types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS]: (0, locale_1.t)('Crash Free Session Rate'),
    [types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS]: (0, locale_1.t)('Healthy Session Rate'),
    [types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS]: (0, locale_1.t)('Abnormal Session Rate'),
    [types_1.ReleaseComparisonChartType.ERRORED_SESSIONS]: (0, locale_1.t)('Errored Session Rate'),
    [types_1.ReleaseComparisonChartType.CRASHED_SESSIONS]: (0, locale_1.t)('Crashed Session Rate'),
    [types_1.ReleaseComparisonChartType.CRASH_FREE_USERS]: (0, locale_1.t)('Crash Free User Rate'),
    [types_1.ReleaseComparisonChartType.HEALTHY_USERS]: (0, locale_1.t)('Healthy User Rate'),
    [types_1.ReleaseComparisonChartType.ABNORMAL_USERS]: (0, locale_1.t)('Abnormal User Rate'),
    [types_1.ReleaseComparisonChartType.ERRORED_USERS]: (0, locale_1.t)('Errored User Rate'),
    [types_1.ReleaseComparisonChartType.CRASHED_USERS]: (0, locale_1.t)('Crashed User Rate'),
    [types_1.ReleaseComparisonChartType.SESSION_COUNT]: (0, locale_1.t)('Session Count'),
    [types_1.ReleaseComparisonChartType.SESSION_DURATION]: (0, locale_1.t)('Session Duration'),
    [types_1.ReleaseComparisonChartType.USER_COUNT]: (0, locale_1.t)('User Count'),
    [types_1.ReleaseComparisonChartType.ERROR_COUNT]: (0, locale_1.t)('Error Count'),
    [types_1.ReleaseComparisonChartType.TRANSACTION_COUNT]: (0, locale_1.t)('Transaction Count'),
    [types_1.ReleaseComparisonChartType.FAILURE_RATE]: (0, locale_1.t)('Failure Rate'),
};
exports.releaseComparisonChartHelp = {
    [types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS]: sessionTerm_1.commonTermsDescription[sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS],
    [types_1.ReleaseComparisonChartType.CRASH_FREE_USERS]: sessionTerm_1.commonTermsDescription[sessionTerm_1.SessionTerm.CRASH_FREE_USERS],
    [types_1.ReleaseComparisonChartType.SESSION_COUNT]: (0, locale_1.t)('The number of sessions in a given period.'),
    [types_1.ReleaseComparisonChartType.USER_COUNT]: (0, locale_1.t)('The number of users in a given period.'),
};
function generateReleaseMarkLine(title, position, theme, options) {
    const { hideLabel, axisIndex } = options || {};
    return {
        seriesName: title,
        type: 'line',
        data: [{ name: position, value: null }],
        yAxisIndex: axisIndex !== null && axisIndex !== void 0 ? axisIndex : undefined,
        xAxisIndex: axisIndex !== null && axisIndex !== void 0 ? axisIndex : undefined,
        color: theme.gray300,
        markLine: (0, markLine_1.default)({
            silent: true,
            lineStyle: { color: theme.gray300, type: 'solid' },
            label: {
                position: 'insideEndBottom',
                formatter: hideLabel ? '' : title,
                font: 'Rubik',
                fontSize: 11,
            },
            data: [
                {
                    xAxis: position,
                },
            ], // TODO(ts): weird echart types
        }),
    };
}
exports.releaseMarkLinesLabels = {
    created: (0, locale_1.t)('Release Created'),
    adopted: (0, locale_1.t)('Adopted'),
    unadopted: (0, locale_1.t)('Replaced'),
};
function generateReleaseMarkLines(release, project, theme, location, options) {
    var _a;
    const markLines = [];
    const adoptionStages = (_a = release.adoptionStages) === null || _a === void 0 ? void 0 : _a[project.slug];
    const isSingleEnv = (0, queryString_1.decodeList)(location.query.environment).length === 1;
    const _b = (0, utils_2.getReleaseParams)({
        location,
        releaseBounds: (0, utils_2.getReleaseBounds)(release),
    }), { statsPeriod } = _b, releaseParamsRest = (0, tslib_1.__rest)(_b, ["statsPeriod"]);
    let { start, end } = releaseParamsRest;
    const isDefaultPeriod = !(location.query.pageStart ||
        location.query.pageEnd ||
        location.query.pageStatsPeriod);
    if (statsPeriod) {
        const parsedStatsPeriod = (0, utils_1.parseStatsPeriod)(statsPeriod, null);
        start = parsedStatsPeriod.start;
        end = parsedStatsPeriod.end;
    }
    const releaseCreated = (0, moment_1.default)(release.dateCreated).startOf('minute');
    if (releaseCreated.isBetween(start, end) || isDefaultPeriod) {
        markLines.push(generateReleaseMarkLine(exports.releaseMarkLinesLabels.created, releaseCreated.valueOf(), theme, options));
    }
    if (!isSingleEnv || !(0, list_1.isProjectMobileForReleases)(project.platform)) {
        // for now want to show marklines only on mobile platforms with single environment selected
        return markLines;
    }
    const releaseAdopted = (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages.adopted) && (0, moment_1.default)(adoptionStages.adopted);
    if (releaseAdopted && releaseAdopted.isBetween(start, end)) {
        markLines.push(generateReleaseMarkLine(exports.releaseMarkLinesLabels.adopted, releaseAdopted.valueOf(), theme, options));
    }
    const releaseReplaced = (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages.unadopted) && (0, moment_1.default)(adoptionStages.unadopted);
    if (releaseReplaced && releaseReplaced.isBetween(start, end)) {
        markLines.push(generateReleaseMarkLine(exports.releaseMarkLinesLabels.unadopted, releaseReplaced.valueOf(), theme, options));
    }
    return markLines;
}
exports.generateReleaseMarkLines = generateReleaseMarkLines;
//# sourceMappingURL=utils.jsx.map