Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const range_1 = (0, tslib_1.__importDefault)(require("lodash/range"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const dates_1 = require("app/utils/dates");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const timePeriods = (0, range_1.default)(-1, -24 * 7, -1);
const defaultValue = '0.1';
function SessionPercent({ params, selection, organization }) {
    const api = (0, useApi_1.default)();
    const [threshold, setThreshold] = (0, react_1.useState)(defaultValue);
    const [statsArr, setStats] = (0, react_1.useState)([]);
    const requestParams = {
        expand: 'sessions',
        display: 'sessions',
        project: selection.projects,
        query: 'is:unresolved',
        sort: 'freq',
    };
    const fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        for (let idx = 0; idx < timePeriods.length; idx++) {
            const period = timePeriods[idx];
            const start = (0, dates_1.getUtcDateString)((0, moment_1.default)().subtract(Math.abs(period), 'hours').toDate());
            const end = (0, dates_1.getUtcDateString)((0, moment_1.default)()
                .subtract(Math.abs(period) - 1, 'hours')
                .toDate());
            const issuesQuery = Object.assign(Object.assign({}, requestParams), { limit: 5, start, end });
            let results;
            try {
                results = yield api.requestPromise(`/organizations/${params.orgId}/issues/`, {
                    method: 'GET',
                    data: qs.stringify(issuesQuery),
                });
            }
            catch (_a) {
                results = [];
            }
            const groupIds = results.map(group => group.id);
            if (groupIds.length === 0) {
                setStats(prevState => {
                    return [...prevState, []];
                });
                continue;
            }
            const query = Object.assign(Object.assign({}, requestParams), { start,
                end, groups: groupIds });
            try {
                const groupStats = yield api.requestPromise(`/organizations/${params.orgId}/issues-stats/`, {
                    method: 'GET',
                    data: qs.stringify(query),
                });
                const newData = groupStats.map(stats => {
                    return {
                        group: results.find(grp => grp.id === stats.id),
                        percent: stats.sessionCount
                            ? (Number(stats.count) / Number(stats.sessionCount)) * 100
                            : 100,
                    };
                });
                setStats(prevState => {
                    return [...prevState, newData];
                });
            }
            catch (_b) {
                setStats(prevState => {
                    return [...prevState, []];
                });
            }
        }
    });
    (0, react_1.useEffect)(() => {
        fetchData();
    }, []);
    function getDiscoverUrl({ title, id, type }, period) {
        const start = (0, dates_1.getUtcDateString)((0, moment_1.default)()
            .subtract(Math.abs(period - 2), 'hours')
            .toDate());
        const end = (0, dates_1.getUtcDateString)((0, moment_1.default)()
            .subtract(Math.abs(period) - 3, 'hours')
            .toDate());
        const discoverQuery = {
            id: undefined,
            name: title || type,
            fields: ['title', 'release', 'environment', 'user.display', 'timestamp'],
            orderby: '-timestamp',
            query: `issue.id:${id}`,
            projects: selection.projects,
            version: 2,
            start,
            end,
        };
        const discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
        return discoverView.getResultsViewUrlTarget(organization.slug);
    }
    return (<react_1.Fragment>
      <Layout.Header>
        <Layout.HeaderContent>
          <Layout.Title>{(0, locale_1.t)('Session Threshold Percent')}</Layout.Title>
          <StyledInput type="text" value={threshold} onChange={(event) => {
            setThreshold(event.target.value);
        }}/>
        </Layout.HeaderContent>
      </Layout.Header>
      <Layout.Body>
        <Layout.Main fullWidth>
          {timePeriods.map((period, idx) => {
            const stats = statsArr[idx];
            const isLoading = stats === undefined;
            return (<react_1.Fragment key={idx}>
                <h4>{(0, locale_1.tn)('%s hour', '%s hours', period)}</h4>
                <ul>
                  {isLoading && (0, locale_1.t)('Loading\u2026')}
                  {!isLoading &&
                    stats
                        .filter(({ percent }) => percent > parseFloat(threshold))
                        .map(({ group, percent }) => (<li key={group.id}>
                          {percent.toLocaleString()}% -{' '}
                          <link_1.default to={getDiscoverUrl(group, period)}>{group.title}</link_1.default>
                        </li>))}
                </ul>
              </react_1.Fragment>);
        })}
        </Layout.Main>
      </Layout.Body>
    </react_1.Fragment>);
}
function SessionPercentWrapper(props) {
    return (<feature_1.default features={['issue-percent-filters']} renderDisabled={p => <featureDisabled_1.default features={p.features} hideHelpToggle/>}>
      <SessionPercent {...props}/>
    </feature_1.default>);
}
exports.default = (0, withGlobalSelection_1.default)((0, withOrganization_1.default)(SessionPercentWrapper));
const StyledInput = (0, styled_1.default)(input_1.default) `
  width: 100px;
`;
//# sourceMappingURL=testSessionPercent.jsx.map