Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const groupListHeader_1 = (0, tslib_1.__importDefault)(require("app/components/issues/groupListHeader"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const group_1 = (0, tslib_1.__importDefault)(require("app/components/stream/group"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class List extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            groups: [],
            hasError: false,
            isLoading: true,
        };
        this.getGroups = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, orgSlug, location, issues } = this.props;
            if (!issues.length) {
                this.setState({ isLoading: false });
                return;
            }
            const issuesIds = issues.map(issue => `group=${issue['issue.id']}`).join('&');
            try {
                const groups = yield api.requestPromise(`/organizations/${orgSlug}/issues/?${issuesIds}`, {
                    method: 'GET',
                    data: Object.assign({ sort: 'new' }, (0, pick_1.default)(location.query, [...Object.values(globalSelectionHeader_1.URL_PARAM), 'cursor'])),
                });
                const convertedGroups = this.convertGroupsIntoEventFormat(groups);
                // this is necessary, because the AssigneeSelector component fetches the group from the GroupStore
                groupStore_1.default.add(convertedGroups);
                this.setState({ groups: convertedGroups, isLoading: false });
            }
            catch (error) {
                Sentry.captureException(error);
                this.setState({ isLoading: false, hasError: true });
            }
        });
        // this little hack is necessary until we factored the groupStore or the EventOrGroupHeader component
        // the goal of this function is to insert the properties eventID and groupID, so then the link rendered
        // in the EventOrGroupHeader component will always have the structure '/organization/:orgSlug/issues/:groupId/event/:eventId/',
        // providing a smooth navigation between issues with the same trace ID
        this.convertGroupsIntoEventFormat = (groups) => {
            const { issues } = this.props;
            return groups
                .map(group => {
                // the issue must always be found
                const foundIssue = issues.find(issue => group.id === String(issue['issue.id']));
                if (foundIssue) {
                    // the eventID is the reason why we need to use the DiscoverQuery component.
                    // At the moment the /issues/ endpoint above doesn't return this information
                    return Object.assign(Object.assign({}, group), { eventID: foundIssue.id, groupID: group.id });
                }
                return undefined;
            })
                .filter(event => !!event);
        };
        this.handleCursorChange = (cursor, path, query, delta) => react_router_1.browserHistory.push({
            pathname: path,
            query: Object.assign(Object.assign({}, query), { cursor: delta <= 0 ? undefined : cursor }),
        });
        this.handleRetry = () => {
            this.getGroups();
        };
        this.renderContent = () => {
            const { issues, period, traceID } = this.props;
            if (!issues.length) {
                return (<emptyStateWarning_1.default small withIcon={false}>
          {(0, locale_1.tct)('No issues with the same trace ID [traceID] were found in the period between [start] and [end]', {
                        traceID,
                        start: <dateTime_1.default date={period.start} timeAndDate/>,
                        end: <dateTime_1.default date={period.start} timeAndDate/>,
                    })}
        </emptyStateWarning_1.default>);
            }
            return issues.map(issue => (<group_1.default key={issue.id} id={String(issue['issue.id'])} canSelect={false} withChart={false}/>));
        };
    }
    componentDidMount() {
        this.getGroups();
    }
    render() {
        const { pageLinks, traceID } = this.props;
        const { isLoading, hasError } = this.state;
        if (isLoading) {
            return <loadingIndicator_1.default />;
        }
        if (hasError) {
            return (<loadingError_1.default message={(0, locale_1.tct)('An error occurred while fetching issues with the trace ID [traceID]', {
                    traceID,
                })} onRetry={this.handleRetry}/>);
        }
        return (<react_1.Fragment>
        <StyledPanel>
          <groupListHeader_1.default withChart={false}/>
          <panels_1.PanelBody>{this.renderContent()}</panels_1.PanelBody>
        </StyledPanel>
        <StyledPagination pageLinks={pageLinks} onCursor={this.handleCursorChange}/>
      </react_1.Fragment>);
    }
}
exports.default = (0, withApi_1.default)(List);
const StyledPagination = (0, styled_1.default)(pagination_1.default) `
  margin-top: 0;
`;
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  margin-bottom: 0;
`;
//# sourceMappingURL=list.jsx.map