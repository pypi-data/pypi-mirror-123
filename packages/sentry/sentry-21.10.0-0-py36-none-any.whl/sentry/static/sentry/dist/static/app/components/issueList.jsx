Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueList = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const compactIssue_1 = (0, tslib_1.__importDefault)(require("app/components/issues/compactIssue"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
class IssueList extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.fetchData = () => {
            const { location, api, endpoint, query } = this.props;
            api.clear();
            api.request(endpoint, {
                method: 'GET',
                query: Object.assign({ cursor: (location && location.query && location.query.cursor) || '' }, query),
                success: (data, _, resp) => {
                    var _a;
                    this.setState({
                        data,
                        loading: false,
                        error: false,
                        issueIds: data.map(item => item.id),
                        pageLinks: (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                    });
                },
                error: () => {
                    this.setState({ loading: false, error: true });
                },
            });
        };
    }
    getInitialState() {
        return {
            issueIds: [],
            loading: true,
            error: false,
            pageLinks: null,
            data: [],
        };
    }
    componentWillMount() {
        this.fetchData();
    }
    componentWillReceiveProps(nextProps) {
        const { location } = this.props;
        const nextLocation = nextProps.location;
        if (!location) {
            return;
        }
        if (location.pathname !== nextLocation.pathname ||
            location.search !== nextLocation.search) {
            this.remountComponent();
        }
    }
    remountComponent() {
        this.setState(this.getInitialState(), this.fetchData);
    }
    renderError() {
        return (<div style={{ margin: `${(0, space_1.default)(2)} ${(0, space_1.default)(2)} 0` }}>
        <loadingError_1.default onRetry={this.fetchData}/>
      </div>);
    }
    renderLoading() {
        return (<div style={{ margin: '18px 18px 0' }}>
        <loadingIndicator_1.default />
      </div>);
    }
    renderEmpty() {
        const { emptyText } = this.props;
        const { noBorder, noMargin } = this.props;
        const panelStyle = noBorder ? { border: 0, borderRadius: 0 } : {};
        if (noMargin) {
            panelStyle.marginBottom = 0;
        }
        return (<panels_1.Panel style={panelStyle}>
        <emptyMessage_1.default icon={<icons_1.IconSearch size="xl"/>}>
          {emptyText ? emptyText : (0, locale_1.t)('Nothing to show here, move along.')}
        </emptyMessage_1.default>
      </panels_1.Panel>);
    }
    renderResults() {
        const { noBorder, noMargin, renderEmpty } = this.props;
        const { loading, error, issueIds, data } = this.state;
        if (loading) {
            return this.renderLoading();
        }
        if (error) {
            return this.renderError();
        }
        if (issueIds.length > 0) {
            const panelStyle = noBorder
                ? { border: 0, borderRadius: 0 }
                : {};
            if (noMargin) {
                panelStyle.marginBottom = 0;
            }
            return (<panels_1.Panel style={panelStyle}>
          <panels_1.PanelBody className="issue-list">
            {data.map(issue => (<compactIssue_1.default key={issue.id} id={issue.id} data={issue}/>))}
          </panels_1.PanelBody>
        </panels_1.Panel>);
        }
        return (renderEmpty === null || renderEmpty === void 0 ? void 0 : renderEmpty()) || this.renderEmpty();
    }
    render() {
        const { pageLinks } = this.state;
        const { pagination } = this.props;
        return (<React.Fragment>
        {this.renderResults()}
        {pagination && pageLinks && <pagination_1.default pageLinks={pageLinks} {...this.props}/>}
      </React.Fragment>);
    }
}
exports.IssueList = IssueList;
exports.default = (0, react_router_1.withRouter)((0, withApi_1.default)(IssueList));
//# sourceMappingURL=issueList.jsx.map