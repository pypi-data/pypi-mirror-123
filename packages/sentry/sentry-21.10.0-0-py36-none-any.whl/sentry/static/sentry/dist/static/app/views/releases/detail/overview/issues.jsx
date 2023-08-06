Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const button_1 = (0, tslib_1.__importStar)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importStar)(require("app/components/buttonBar"));
const groupList_1 = (0, tslib_1.__importDefault)(require("app/components/issues/groupList"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const queryCount_1 = (0, tslib_1.__importDefault)(require("app/components/queryCount"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const utils_1 = require("app/views/issueList/utils");
const utils_2 = require("../../utils");
const emptyState_1 = (0, tslib_1.__importDefault)(require("../emptyState"));
var IssuesType;
(function (IssuesType) {
    IssuesType["NEW"] = "new";
    IssuesType["UNHANDLED"] = "unhandled";
    IssuesType["RESOLVED"] = "resolved";
    IssuesType["ALL"] = "all";
})(IssuesType || (IssuesType = {}));
var IssuesQuery;
(function (IssuesQuery) {
    IssuesQuery["NEW"] = "first-release";
    IssuesQuery["UNHANDLED"] = "error.handled:0";
    IssuesQuery["RESOLVED"] = "is:resolved";
    IssuesQuery["ALL"] = "release";
})(IssuesQuery || (IssuesQuery = {}));
const defaultProps = {
    withChart: false,
};
class Issues extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.handleIssuesTypeSelection = (issuesType) => {
            const { location } = this.props;
            const issuesTypeQuery = issuesType === IssuesType.ALL
                ? IssuesType.ALL
                : issuesType === IssuesType.NEW
                    ? IssuesType.NEW
                    : issuesType === IssuesType.RESOLVED
                        ? IssuesType.RESOLVED
                        : issuesType === IssuesType.UNHANDLED
                            ? IssuesType.UNHANDLED
                            : '';
            const to = Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { issuesType: issuesTypeQuery }) });
            react_router_1.browserHistory.replace(to);
            this.setState({ issuesType });
        };
        this.handleFetchSuccess = (groupListState, onCursor) => {
            this.setState({ pageLinks: groupListState.pageLinks, onCursor });
        };
        this.renderEmptyMessage = () => {
            const { location, releaseBounds } = this.props;
            const { issuesType } = this.state;
            const isEntireReleasePeriod = !location.query.pageStatsPeriod && !location.query.pageStart;
            const { statsPeriod } = (0, utils_2.getReleaseParams)({
                location,
                releaseBounds,
            });
            const selectedTimePeriod = statsPeriod ? constants_1.DEFAULT_RELATIVE_PERIODS[statsPeriod] : null;
            const displayedPeriod = selectedTimePeriod
                ? selectedTimePeriod.toLowerCase()
                : (0, locale_1.t)('given timeframe');
            return (<emptyState_1.default>
        {issuesType === IssuesType.NEW
                    ? isEntireReleasePeriod
                        ? (0, locale_1.t)('No new issues in this release.')
                        : (0, locale_1.tct)('No new issues for the [timePeriod].', {
                            timePeriod: displayedPeriod,
                        })
                    : null}
        {issuesType === IssuesType.UNHANDLED
                    ? isEntireReleasePeriod
                        ? (0, locale_1.t)('No unhandled issues in this release.')
                        : (0, locale_1.tct)('No unhandled issues for the [timePeriod].', {
                            timePeriod: displayedPeriod,
                        })
                    : null}
        {issuesType === IssuesType.RESOLVED && (0, locale_1.t)('No resolved issues in this release.')}
        {issuesType === IssuesType.ALL
                    ? isEntireReleasePeriod
                        ? (0, locale_1.t)('No issues in this release')
                        : (0, locale_1.tct)('No issues for the [timePeriod].', {
                            timePeriod: displayedPeriod,
                        })
                    : null}
      </emptyState_1.default>);
        };
    }
    getInitialState() {
        const { location } = this.props;
        const query = location.query ? location.query.issuesType : null;
        const issuesTypeState = !query
            ? IssuesType.NEW
            : query.includes(IssuesType.NEW)
                ? IssuesType.NEW
                : query.includes(IssuesType.UNHANDLED)
                    ? IssuesType.UNHANDLED
                    : query.includes(IssuesType.RESOLVED)
                        ? IssuesType.RESOLVED
                        : query.includes(IssuesType.ALL)
                            ? IssuesType.ALL
                            : IssuesType.ALL;
        return {
            issuesType: issuesTypeState,
            count: {
                new: null,
                all: null,
                resolved: null,
                unhandled: null,
            },
        };
    }
    componentDidMount() {
        this.fetchIssuesCount();
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)((0, utils_2.getReleaseParams)({
            location: this.props.location,
            releaseBounds: this.props.releaseBounds,
        }), (0, utils_2.getReleaseParams)({
            location: prevProps.location,
            releaseBounds: prevProps.releaseBounds,
        }))) {
            this.fetchIssuesCount();
        }
    }
    getIssuesUrl() {
        const { version, organization } = this.props;
        const { issuesType } = this.state;
        const { queryParams } = this.getIssuesEndpoint();
        const query = new tokenizeSearch_1.MutableSearch([]);
        switch (issuesType) {
            case IssuesType.NEW:
                query.setFilterValues('firstRelease', [version]);
                break;
            case IssuesType.UNHANDLED:
                query.setFilterValues('release', [version]);
                query.setFilterValues('error.handled', ['0']);
                break;
            case IssuesType.RESOLVED:
            case IssuesType.ALL:
            default:
                query.setFilterValues('release', [version]);
        }
        return {
            pathname: `/organizations/${organization.slug}/issues/`,
            query: Object.assign(Object.assign({}, queryParams), { limit: undefined, cursor: undefined, query: query.formatString() }),
        };
    }
    getIssuesEndpoint() {
        const { version, organization, location, releaseBounds } = this.props;
        const { issuesType } = this.state;
        const queryParams = Object.assign(Object.assign({}, (0, utils_2.getReleaseParams)({
            location,
            releaseBounds,
        })), { limit: 10, sort: utils_1.IssueSortOptions.FREQ, groupStatsPeriod: 'auto' });
        switch (issuesType) {
            case IssuesType.ALL:
                return {
                    path: `/organizations/${organization.slug}/issues/`,
                    queryParams: Object.assign(Object.assign({}, queryParams), { query: new tokenizeSearch_1.MutableSearch([`${IssuesQuery.ALL}:${version}`]).formatString() }),
                };
            case IssuesType.RESOLVED:
                return {
                    path: `/organizations/${organization.slug}/releases/${version}/resolved/`,
                    queryParams: Object.assign(Object.assign({}, queryParams), { query: '' }),
                };
            case IssuesType.UNHANDLED:
                return {
                    path: `/organizations/${organization.slug}/issues/`,
                    queryParams: Object.assign(Object.assign({}, queryParams), { query: new tokenizeSearch_1.MutableSearch([
                            `${IssuesQuery.ALL}:${version}`,
                            IssuesQuery.UNHANDLED,
                        ]).formatString() }),
                };
            case IssuesType.NEW:
            default:
                return {
                    path: `/organizations/${organization.slug}/issues/`,
                    queryParams: Object.assign(Object.assign({}, queryParams), { query: new tokenizeSearch_1.MutableSearch([`${IssuesQuery.NEW}:${version}`]).formatString() }),
                };
        }
    }
    fetchIssuesCount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, version } = this.props;
            const issueCountEndpoint = this.getIssueCountEndpoint();
            const resolvedEndpoint = `/organizations/${organization.slug}/releases/${version}/resolved/`;
            try {
                yield Promise.all([
                    api.requestPromise(issueCountEndpoint),
                    api.requestPromise(resolvedEndpoint),
                ]).then(([issueResponse, resolvedResponse]) => {
                    this.setState({
                        count: {
                            all: issueResponse[`${IssuesQuery.ALL}:"${version}"`] || 0,
                            new: issueResponse[`${IssuesQuery.NEW}:"${version}"`] || 0,
                            resolved: resolvedResponse.length,
                            unhandled: issueResponse[`${IssuesQuery.UNHANDLED} ${IssuesQuery.ALL}:"${version}"`] ||
                                0,
                        },
                    });
                });
            }
            catch (_a) {
                // do nothing
            }
        });
    }
    getIssueCountEndpoint() {
        const { organization, version, location, releaseBounds } = this.props;
        const issuesCountPath = `/organizations/${organization.slug}/issues-count/`;
        const params = [
            `${IssuesQuery.NEW}:"${version}"`,
            `${IssuesQuery.ALL}:"${version}"`,
            `${IssuesQuery.UNHANDLED} ${IssuesQuery.ALL}:"${version}"`,
        ];
        const queryParams = params.map(param => param);
        const queryParameters = Object.assign(Object.assign({}, (0, utils_2.getReleaseParams)({
            location,
            releaseBounds,
        })), { query: queryParams });
        return `${issuesCountPath}?${qs.stringify(queryParameters)}`;
    }
    render() {
        const { issuesType, count, pageLinks, onCursor } = this.state;
        const { organization, queryFilterDescription, withChart } = this.props;
        const { path, queryParams } = this.getIssuesEndpoint();
        const issuesTypes = [
            { value: IssuesType.ALL, label: (0, locale_1.t)('All Issues'), issueCount: count.all },
            { value: IssuesType.NEW, label: (0, locale_1.t)('New Issues'), issueCount: count.new },
            {
                value: IssuesType.UNHANDLED,
                label: (0, locale_1.t)('Unhandled Issues'),
                issueCount: count.unhandled,
            },
            {
                value: IssuesType.RESOLVED,
                label: (0, locale_1.t)('Resolved Issues'),
                issueCount: count.resolved,
            },
        ];
        return (<react_1.Fragment>
        <ControlsWrapper>
          <StyledButtonBar active={issuesType} merged>
            {issuesTypes.map(({ value, label, issueCount }) => (<button_1.default key={value} barId={value} size="small" onClick={() => this.handleIssuesTypeSelection(value)} data-test-id={`filter-${value}`}>
                {label}
                <queryCount_1.default count={issueCount} max={99} hideParens hideIfEmpty={false}/>
              </button_1.default>))}
          </StyledButtonBar>

          <OpenInButtonBar gap={1}>
            <button_1.default to={this.getIssuesUrl()} size="small" data-test-id="issues-button">
              {(0, locale_1.t)('Open in Issues')}
            </button_1.default>

            <StyledPagination pageLinks={pageLinks} onCursor={onCursor}/>
          </OpenInButtonBar>
        </ControlsWrapper>
        <div data-test-id="release-wrapper">
          <groupList_1.default orgId={organization.slug} endpointPath={path} queryParams={queryParams} query="" canSelectGroups={false} queryFilterDescription={queryFilterDescription} withChart={withChart} narrowGroups renderEmptyMessage={this.renderEmptyMessage} withPagination={false} onFetchSuccess={this.handleFetchSuccess}/>
        </div>
      </react_1.Fragment>);
    }
}
Issues.defaultProps = defaultProps;
const ControlsWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
    ${buttonBar_1.ButtonGrid} {
      overflow: auto;
    }
  }
`;
const OpenInButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  margin: ${(0, space_1.default)(1)} 0;
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  grid-template-columns: repeat(4, 1fr);
  ${button_1.ButtonLabel} {
    white-space: nowrap;
    grid-gap: ${(0, space_1.default)(0.5)};
    span:last-child {
      color: ${p => p.theme.buttonCount};
    }
  }
  .active {
    ${button_1.ButtonLabel} {
      span:last-child {
        color: ${p => p.theme.buttonCountActive};
      }
    }
  }
`;
const StyledPagination = (0, styled_1.default)(pagination_1.default) `
  margin: 0;
`;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(Issues));
//# sourceMappingURL=issues.jsx.map