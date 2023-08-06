Object.defineProperty(exports, "__esModule", { value: true });
exports.TransactionsListOption = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const release_1 = require("app/actionCreators/release");
const api_1 = require("app/api");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const sessionsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/sessionsRequest"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const performanceCardTable_1 = (0, tslib_1.__importDefault)(require("app/components/discover/performanceCardTable"));
const transactionsList_1 = (0, tslib_1.__importDefault)(require("app/components/discover/transactionsList"));
const thirds_1 = require("app/components/layouts/thirds");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const pageTimeRangeSelector_1 = (0, tslib_1.__importDefault)(require("app/components/pageTimeRangeSelector"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const dates_1 = require("app/utils/dates");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const formatters_1 = require("app/utils/formatters");
const queryString_1 = require("app/utils/queryString");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const charts_1 = require("app/views/performance/transactionSummary/transactionOverview/charts");
const utils_1 = require("app/views/performance/transactionSummary/utils");
const types_2 = require("app/views/performance/trends/types");
const utils_2 = require("../../utils");
const __1 = require("..");
const commitAuthorBreakdown_1 = (0, tslib_1.__importDefault)(require("./commitAuthorBreakdown"));
const deploys_1 = (0, tslib_1.__importDefault)(require("./deploys"));
const issues_1 = (0, tslib_1.__importDefault)(require("./issues"));
const otherProjects_1 = (0, tslib_1.__importDefault)(require("./otherProjects"));
const projectReleaseDetails_1 = (0, tslib_1.__importDefault)(require("./projectReleaseDetails"));
const releaseAdoption_1 = (0, tslib_1.__importDefault)(require("./releaseAdoption"));
const releaseArchivedNotice_1 = (0, tslib_1.__importDefault)(require("./releaseArchivedNotice"));
const releaseComparisonChart_1 = (0, tslib_1.__importDefault)(require("./releaseComparisonChart"));
const releaseStats_1 = (0, tslib_1.__importDefault)(require("./releaseStats"));
const totalCrashFreeUsers_1 = (0, tslib_1.__importDefault)(require("./totalCrashFreeUsers"));
const RELEASE_PERIOD_KEY = 'release';
var TransactionsListOption;
(function (TransactionsListOption) {
    TransactionsListOption["FAILURE_COUNT"] = "failure_count";
    TransactionsListOption["TPM"] = "tpm";
    TransactionsListOption["SLOW"] = "slow";
    TransactionsListOption["SLOW_LCP"] = "slow_lcp";
    TransactionsListOption["REGRESSION"] = "regression";
    TransactionsListOption["IMPROVEMENT"] = "improved";
})(TransactionsListOption = exports.TransactionsListOption || (exports.TransactionsListOption = {}));
class ReleaseOverview extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleRestore = (project, successCallback) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params, organization } = this.props;
            try {
                yield (0, release_1.restoreRelease)(new api_1.Client(), {
                    orgSlug: organization.slug,
                    projectSlug: project.slug,
                    releaseVersion: params.release,
                });
                successCallback();
            }
            catch (_a) {
                // do nothing, action creator is already displaying error message
            }
        });
        this.handleTransactionsListSortChange = (value) => {
            const { location } = this.props;
            const target = {
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { showTransactions: value, transactionCursor: undefined }),
            };
            react_router_1.browserHistory.push(target);
        };
        this.handleDateChange = (datetime) => {
            const { router, location } = this.props;
            const { start, end, relative, utc } = datetime;
            if (start && end) {
                const parser = utc ? moment_1.default.utc : moment_1.default;
                router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { pageStatsPeriod: undefined, pageStart: parser(start).format(), pageEnd: parser(end).format(), pageUtc: utc !== null && utc !== void 0 ? utc : undefined }) }));
                return;
            }
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { pageStatsPeriod: relative === RELEASE_PERIOD_KEY ? undefined : relative, pageStart: undefined, pageEnd: undefined, pageUtc: undefined }) }));
        };
    }
    getTitle() {
        const { params, organization } = this.props;
        return (0, routeTitle_1.default)((0, locale_1.t)('Release %s', (0, formatters_1.formatVersion)(params.release)), organization.slug, false);
    }
    getReleaseEventView(version, projectId, selectedSort, releaseBounds) {
        const { selection, location } = this.props;
        const { environments } = selection;
        const { start, end, statsPeriod } = (0, utils_2.getReleaseParams)({
            location,
            releaseBounds,
        });
        const baseQuery = {
            id: undefined,
            version: 2,
            name: `Release ${(0, formatters_1.formatVersion)(version)}`,
            query: `event.type:transaction release:${version}`,
            fields: ['transaction', 'failure_count()', 'epm()', 'p50()'],
            orderby: '-failure_count',
            range: statsPeriod || undefined,
            environment: environments,
            projects: [projectId],
            start: start ? (0, dates_1.getUtcDateString)(start) : undefined,
            end: end ? (0, dates_1.getUtcDateString)(end) : undefined,
        };
        switch (selectedSort.value) {
            case TransactionsListOption.SLOW_LCP:
                return eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, baseQuery), { query: `event.type:transaction release:${version} epm():>0.01 has:measurements.lcp`, fields: ['transaction', 'failure_count()', 'epm()', 'p75(measurements.lcp)'], orderby: 'p75_measurements_lcp' }));
            case TransactionsListOption.SLOW:
                return eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, baseQuery), { query: `event.type:transaction release:${version} epm():>0.01` }));
            case TransactionsListOption.FAILURE_COUNT:
                return eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, baseQuery), { query: `event.type:transaction release:${version} failure_count():>0` }));
            default:
                return eventView_1.default.fromSavedQuery(baseQuery);
        }
    }
    getReleaseTrendView(version, projectId, versionDate, releaseBounds) {
        const { selection, location } = this.props;
        const { environments } = selection;
        const { start, end, statsPeriod } = (0, utils_2.getReleaseParams)({
            location,
            releaseBounds,
        });
        const trendView = eventView_1.default.fromSavedQuery({
            id: undefined,
            version: 2,
            name: `Release ${(0, formatters_1.formatVersion)(version)}`,
            fields: ['transaction'],
            query: 'tpm():>0.01 trend_percentage():>0%',
            range: statsPeriod || undefined,
            environment: environments,
            projects: [projectId],
            start: start ? (0, dates_1.getUtcDateString)(start) : undefined,
            end: end ? (0, dates_1.getUtcDateString)(end) : undefined,
        });
        trendView.middle = versionDate;
        return trendView;
    }
    get pageDateTime() {
        const query = this.props.location.query;
        const { start, end, statsPeriod } = (0, getParams_1.getParams)(query, {
            allowEmptyPeriod: true,
            allowAbsoluteDatetime: true,
            allowAbsolutePageDatetime: true,
        });
        if (statsPeriod) {
            return { period: statsPeriod };
        }
        if (start && end) {
            return {
                start: moment_1.default.utc(start).format(),
                end: moment_1.default.utc(end).format(),
            };
        }
        return {};
    }
    render() {
        const { organization, selection, location, api } = this.props;
        const { start, end, period, utc } = this.pageDateTime;
        return (<__1.ReleaseContext.Consumer>
        {({ release, project, deploys, releaseMeta, refetchData, hasHealthData, releaseBounds, }) => {
                const { commitCount, version } = release;
                const hasDiscover = organization.features.includes('discover-basic');
                const hasPerformance = organization.features.includes('performance-view');
                const hasReleaseComparisonPerformance = organization.features.includes('release-comparison-performance');
                const { environments } = selection;
                const { selectedSort, sortOptions } = getTransactionsListSort(location);
                const releaseEventView = this.getReleaseEventView(version, project.id, selectedSort, releaseBounds);
                const titles = selectedSort.value !== TransactionsListOption.SLOW_LCP
                    ? [(0, locale_1.t)('transaction'), (0, locale_1.t)('failure_count()'), (0, locale_1.t)('tpm()'), (0, locale_1.t)('p50()')]
                    : [(0, locale_1.t)('transaction'), (0, locale_1.t)('failure_count()'), (0, locale_1.t)('tpm()'), (0, locale_1.t)('p75(lcp)')];
                const releaseTrendView = this.getReleaseTrendView(version, project.id, releaseMeta.released, releaseBounds);
                const generateLink = {
                    transaction: generateTransactionLink(version, project.id, selection, location.query.showTransactions),
                };
                const sessionsRequestProps = Object.assign(Object.assign({ api,
                    organization, field: [types_1.SessionField.USERS, types_1.SessionField.SESSIONS, types_1.SessionField.DURATION], groupBy: ['session.status'] }, (0, utils_2.getReleaseParams)({ location, releaseBounds })), { shouldFilterSessionsInTimeWindow: true });
                return (<sessionsRequest_1.default {...sessionsRequestProps}>
              {({ loading: allReleasesLoading, reloading: allReleasesReloading, errored: allReleasesErrored, response: allReleases, }) => (<sessionsRequest_1.default {...sessionsRequestProps} query={`release:"${version}"`}>
                  {({ loading: thisReleaseLoading, reloading: thisReleaseReloading, errored: thisReleaseErrored, response: thisRelease, }) => {
                            const loading = allReleasesLoading || thisReleaseLoading;
                            const reloading = allReleasesReloading || thisReleaseReloading;
                            const errored = allReleasesErrored || thisReleaseErrored;
                            return (<thirds_1.Body>
                        <thirds_1.Main>
                          {(0, utils_2.isReleaseArchived)(release) && (<releaseArchivedNotice_1.default onRestore={() => this.handleRestore(project, refetchData)}/>)}

                          <StyledPageTimeRangeSelector organization={organization} relative={period !== null && period !== void 0 ? period : ''} start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} utc={utc !== null && utc !== void 0 ? utc : null} onUpdate={this.handleDateChange} relativeOptions={Object.assign({ [RELEASE_PERIOD_KEY]: (<react_1.Fragment>
                                  {(0, locale_1.t)('Entire Release Period')} (
                                  <dateTime_1.default date={releaseBounds.releaseStart} timeAndDate/>{' '}
                                  -{' '}
                                  <dateTime_1.default date={releaseBounds.releaseEnd} timeAndDate/>
                                  )
                                </react_1.Fragment>) }, constants_1.DEFAULT_RELATIVE_PERIODS)} defaultPeriod={RELEASE_PERIOD_KEY}/>

                          {(hasDiscover || hasPerformance || hasHealthData) && (<releaseComparisonChart_1.default release={release} releaseSessions={thisRelease} allSessions={allReleases} platform={project.platform} location={location} loading={loading} reloading={reloading} errored={errored} project={project} organization={organization} api={api} hasHealthData={hasHealthData}/>)}

                          <issues_1.default organization={organization} selection={selection} version={version} location={location} releaseBounds={releaseBounds} queryFilterDescription={(0, locale_1.t)('In this release')} withChart/>

                          <feature_1.default features={['performance-view']}>
                            {hasReleaseComparisonPerformance ? (<performanceCardTable_1.default organization={organization} project={project} isLoading={loading} 
                                // TODO(kelly): hardcoding this until I have data
                                isEmpty={false}/>) : (<transactionsList_1.default location={location} organization={organization} eventView={releaseEventView} trendView={releaseTrendView} selected={selectedSort} options={sortOptions} handleDropdownChange={this.handleTransactionsListSortChange} titles={titles} generateLink={generateLink}/>)}
                          </feature_1.default>
                        </thirds_1.Main>
                        <thirds_1.Side>
                          <releaseStats_1.default organization={organization} release={release} project={project}/>
                          {hasHealthData && (<releaseAdoption_1.default releaseSessions={thisRelease} allSessions={allReleases} loading={loading} reloading={reloading} errored={errored} release={release} project={project} environment={environments}/>)}
                          <projectReleaseDetails_1.default release={release} releaseMeta={releaseMeta} orgSlug={organization.slug} projectSlug={project.slug}/>
                          {commitCount > 0 && (<commitAuthorBreakdown_1.default version={version} orgId={organization.slug} projectSlug={project.slug}/>)}
                          {releaseMeta.projects.length > 1 && (<otherProjects_1.default projects={releaseMeta.projects.filter(p => p.slug !== project.slug)} location={location} version={version} organization={organization}/>)}
                          {hasHealthData && (<totalCrashFreeUsers_1.default organization={organization} version={version} projectSlug={project.slug} location={location}/>)}
                          {deploys.length > 0 && (<deploys_1.default version={version} orgSlug={organization.slug} deploys={deploys} projectId={project.id}/>)}
                        </thirds_1.Side>
                      </thirds_1.Body>);
                        }}
                </sessionsRequest_1.default>)}
            </sessionsRequest_1.default>);
            }}
      </__1.ReleaseContext.Consumer>);
    }
}
function generateTransactionLink(version, projectId, selection, value) {
    return (organization, tableRow, _query) => {
        const { transaction } = tableRow;
        const trendTransaction = ['regression', 'improved'].includes(value);
        const { environments, datetime } = selection;
        const { start, end, period } = datetime;
        return (0, utils_1.transactionSummaryRouteWithQuery)({
            orgSlug: organization.slug,
            transaction: transaction,
            query: {
                query: trendTransaction ? '' : `release:${version}`,
                environment: environments,
                start: start ? (0, dates_1.getUtcDateString)(start) : undefined,
                end: end ? (0, dates_1.getUtcDateString)(end) : undefined,
                statsPeriod: period,
            },
            projectID: projectId.toString(),
            display: trendTransaction ? charts_1.DisplayModes.TREND : charts_1.DisplayModes.DURATION,
        });
    };
}
function getDropdownOptions() {
    return [
        {
            sort: { kind: 'desc', field: 'failure_count' },
            value: TransactionsListOption.FAILURE_COUNT,
            label: (0, locale_1.t)('Failing Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'epm' },
            value: TransactionsListOption.TPM,
            label: (0, locale_1.t)('Frequent Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'p50' },
            value: TransactionsListOption.SLOW,
            label: (0, locale_1.t)('Slow Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'p75_measurements_lcp' },
            value: TransactionsListOption.SLOW_LCP,
            label: (0, locale_1.t)('Slow LCP'),
        },
        {
            sort: { kind: 'desc', field: 'trend_percentage()' },
            query: [['confidence()', '>6']],
            trendType: types_2.TrendChangeType.REGRESSION,
            value: TransactionsListOption.REGRESSION,
            label: (0, locale_1.t)('Trending Regressions'),
        },
        {
            sort: { kind: 'asc', field: 'trend_percentage()' },
            query: [['confidence()', '>6']],
            trendType: types_2.TrendChangeType.IMPROVED,
            value: TransactionsListOption.IMPROVEMENT,
            label: (0, locale_1.t)('Trending Improvements'),
        },
    ];
}
function getTransactionsListSort(location) {
    const sortOptions = getDropdownOptions();
    const urlParam = (0, queryString_1.decodeScalar)(location.query.showTransactions, TransactionsListOption.FAILURE_COUNT);
    const selectedSort = sortOptions.find(opt => opt.value === urlParam) || sortOptions[0];
    return { selectedSort, sortOptions };
}
const StyledPageTimeRangeSelector = (0, styled_1.default)(pageTimeRangeSelector_1.default) `
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
exports.default = (0, withApi_1.default)((0, withGlobalSelection_1.default)((0, withOrganization_1.default)(ReleaseOverview)));
//# sourceMappingURL=index.jsx.map