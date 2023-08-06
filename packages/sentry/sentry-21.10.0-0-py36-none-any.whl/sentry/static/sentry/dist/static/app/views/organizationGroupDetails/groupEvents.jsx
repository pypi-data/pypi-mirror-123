Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupEvents = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const eventsTable_1 = (0, tslib_1.__importDefault)(require("app/components/eventsTable/eventsTable"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const locale_1 = require("app/locale");
const parseApiError_1 = (0, tslib_1.__importDefault)(require("app/utils/parseApiError"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class GroupEvents extends React.Component {
    constructor(props) {
        super(props);
        this.handleSearch = (query) => {
            const targetQueryParams = Object.assign({}, this.props.location.query);
            targetQueryParams.query = query;
            const { groupId, orgId } = this.props.params;
            react_router_1.browserHistory.push({
                pathname: `/organizations/${orgId}/issues/${groupId}/events/`,
                query: targetQueryParams,
            });
        };
        this.fetchData = () => {
            this.setState({
                loading: true,
                error: false,
            });
            const query = Object.assign(Object.assign({}, (0, pick_1.default)(this.props.location.query, ['cursor', 'environment'])), { limit: 50, query: this.state.query });
            this.props.api.request(`/issues/${this.props.params.groupId}/events/`, {
                query,
                method: 'GET',
                success: (data, _, resp) => {
                    var _a;
                    this.setState({
                        eventList: data,
                        error: false,
                        loading: false,
                        pageLinks: (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : '',
                    });
                },
                error: err => {
                    this.setState({
                        error: (0, parseApiError_1.default)(err),
                        loading: false,
                    });
                },
            });
        };
        const queryParams = this.props.location.query;
        this.state = {
            eventList: [],
            loading: true,
            error: false,
            pageLinks: '',
            query: queryParams.query || '',
        };
    }
    UNSAFE_componentWillMount() {
        this.fetchData();
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        if (this.props.location.search !== nextProps.location.search) {
            const queryParams = nextProps.location.query;
            this.setState({
                query: queryParams.query,
            }, this.fetchData);
        }
    }
    renderNoQueryResults() {
        return (<emptyStateWarning_1.default>
        <p>{(0, locale_1.t)('Sorry, no events match your search query.')}</p>
      </emptyStateWarning_1.default>);
    }
    renderEmpty() {
        return (<emptyStateWarning_1.default>
        <p>{(0, locale_1.t)("There don't seem to be any events yet.")}</p>
      </emptyStateWarning_1.default>);
    }
    renderResults() {
        const { group, params } = this.props;
        const tagList = group.tags.filter(tag => tag.key !== 'user') || [];
        return (<eventsTable_1.default tagList={tagList} events={this.state.eventList} orgId={params.orgId} projectId={group.project.slug} groupId={params.groupId}/>);
    }
    renderBody() {
        let body;
        if (this.state.loading) {
            body = <loadingIndicator_1.default />;
        }
        else if (this.state.error) {
            body = <loadingError_1.default message={this.state.error} onRetry={this.fetchData}/>;
        }
        else if (this.state.eventList.length > 0) {
            body = this.renderResults();
        }
        else if (this.state.query && this.state.query !== '') {
            body = this.renderNoQueryResults();
        }
        else {
            body = this.renderEmpty();
        }
        return body;
    }
    render() {
        return (<div>
        <div style={{ marginBottom: 20 }}>
          <searchBar_1.default defaultQuery="" placeholder={(0, locale_1.t)('search event id, message, or tags')} query={this.state.query} onSearch={this.handleSearch}/>
        </div>
        <panels_1.Panel className="event-list">
          <panels_1.PanelBody>{this.renderBody()}</panels_1.PanelBody>
        </panels_1.Panel>
        <pagination_1.default pageLinks={this.state.pageLinks}/>
      </div>);
    }
}
exports.GroupEvents = GroupEvents;
exports.default = (0, withApi_1.default)(GroupEvents);
//# sourceMappingURL=groupEvents.jsx.map