Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupList = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const members_1 = require("app/actionCreators/members");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const group_1 = (0, tslib_1.__importStar)(require("app/components/stream/group"));
const locale_1 = require("app/locale");
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const streamManager_1 = (0, tslib_1.__importDefault)(require("app/utils/streamManager"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const groupListHeader_1 = (0, tslib_1.__importDefault)(require("./groupListHeader"));
const defaultProps = {
    canSelectGroups: true,
    withChart: true,
    withPagination: true,
    useFilteredStats: true,
    useTintRow: true,
    narrowGroups: false,
};
class GroupList extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            error: false,
            groups: [],
            pageLinks: null,
        };
        this.listener = groupStore_1.default.listen(() => this.onGroupChange(), undefined);
        this._streamManager = new streamManager_1.default(groupStore_1.default);
        this.fetchData = () => {
            groupStore_1.default.loadInitialData([]);
            const { api, orgId } = this.props;
            api.clear();
            this.setState({ loading: true, error: false });
            (0, members_1.fetchOrgMembers)(api, orgId).then(members => {
                this.setState({ memberList: (0, members_1.indexMembersByProject)(members) });
            });
            const endpoint = this.getGroupListEndpoint();
            api.request(endpoint, {
                success: (data, _, resp) => {
                    var _a;
                    this._streamManager.push(data);
                    this.setState({
                        error: false,
                        loading: false,
                        pageLinks: (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                    }, () => {
                        var _a, _b;
                        (_b = (_a = this.props).onFetchSuccess) === null || _b === void 0 ? void 0 : _b.call(_a, this.state, this.handleCursorChange);
                    });
                },
                error: err => {
                    Sentry.captureException(err);
                    this.setState({ error: true, loading: false });
                },
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    shouldComponentUpdate(nextProps, nextState) {
        return (!(0, isEqual_1.default)(this.state, nextState) ||
            nextProps.endpointPath !== this.props.endpointPath ||
            nextProps.query !== this.props.query ||
            !(0, isEqual_1.default)(nextProps.queryParams, this.props.queryParams));
    }
    componentDidUpdate(prevProps) {
        const ignoredQueryParams = ['end'];
        if (prevProps.orgId !== this.props.orgId ||
            prevProps.endpointPath !== this.props.endpointPath ||
            prevProps.query !== this.props.query ||
            !(0, isEqual_1.default)((0, omit_1.default)(prevProps.queryParams, ignoredQueryParams), (0, omit_1.default)(this.props.queryParams, ignoredQueryParams))) {
            this.fetchData();
        }
    }
    componentWillUnmount() {
        groupStore_1.default.reset();
        (0, callIfFunction_1.callIfFunction)(this.listener);
    }
    getGroupListEndpoint() {
        const { orgId, endpointPath, queryParams } = this.props;
        const path = endpointPath !== null && endpointPath !== void 0 ? endpointPath : `/organizations/${orgId}/issues/`;
        const queryParameters = queryParams !== null && queryParams !== void 0 ? queryParams : this.getQueryParams();
        return `${path}?${qs.stringify(queryParameters)}`;
    }
    getQueryParams() {
        const { location, query } = this.props;
        const queryParams = location.query;
        queryParams.limit = 50;
        queryParams.sort = 'new';
        queryParams.query = query;
        return queryParams;
    }
    handleCursorChange(cursor, path, query, pageDiff) {
        const queryPageInt = parseInt(query.page, 10);
        let nextPage = isNaN(queryPageInt)
            ? pageDiff
            : queryPageInt + pageDiff;
        // unset cursor and page when we navigate back to the first page
        // also reset cursor if somehow the previous button is enabled on
        // first page and user attempts to go backwards
        if (nextPage <= 0) {
            cursor = undefined;
            nextPage = undefined;
        }
        react_router_1.browserHistory.push({
            pathname: path,
            query: Object.assign(Object.assign({}, query), { cursor, page: nextPage }),
        });
    }
    onGroupChange() {
        const groups = this._streamManager.getAllItems();
        if (!(0, isEqual_1.default)(groups, this.state.groups)) {
            this.setState({ groups });
        }
    }
    render() {
        const { canSelectGroups, withChart, renderEmptyMessage, withPagination, useFilteredStats, useTintRow, customStatsPeriod, queryParams, queryFilterDescription, narrowGroups, } = this.props;
        const { loading, error, groups, memberList, pageLinks } = this.state;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        if (groups.length === 0) {
            if (typeof renderEmptyMessage === 'function') {
                return renderEmptyMessage();
            }
            return (<panels_1.Panel>
          <panels_1.PanelBody>
            <emptyStateWarning_1.default>
              <p>{(0, locale_1.t)("There don't seem to be any events fitting the query.")}</p>
            </emptyStateWarning_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>);
        }
        const statsPeriod = (queryParams === null || queryParams === void 0 ? void 0 : queryParams.groupStatsPeriod) === 'auto'
            ? queryParams === null || queryParams === void 0 ? void 0 : queryParams.groupStatsPeriod
            : group_1.DEFAULT_STREAM_GROUP_STATS_PERIOD;
        return (<React.Fragment>
        <panels_1.Panel>
          <groupListHeader_1.default withChart={!!withChart} narrowGroups={narrowGroups}/>
          <panels_1.PanelBody>
            {groups.map(({ id, project }) => {
                const members = (memberList === null || memberList === void 0 ? void 0 : memberList.hasOwnProperty(project.slug))
                    ? memberList[project.slug]
                    : undefined;
                return (<group_1.default key={id} id={id} canSelect={canSelectGroups} withChart={withChart} memberList={members} useFilteredStats={useFilteredStats} useTintRow={useTintRow} customStatsPeriod={customStatsPeriod} statsPeriod={statsPeriod} queryFilterDescription={queryFilterDescription} narrowGroups={narrowGroups}/>);
            })}
          </panels_1.PanelBody>
        </panels_1.Panel>
        {withPagination && (<pagination_1.default pageLinks={pageLinks} onCursor={this.handleCursorChange}/>)}
      </React.Fragment>);
    }
}
exports.GroupList = GroupList;
GroupList.defaultProps = defaultProps;
exports.default = (0, withApi_1.default)((0, react_router_1.withRouter)(GroupList));
//# sourceMappingURL=groupList.jsx.map