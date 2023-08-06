Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const userFeedback_1 = (0, tslib_1.__importDefault)(require("app/components/events/userFeedback"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const userFeedbackEmpty_1 = (0, tslib_1.__importDefault)(require("app/views/userFeedback/userFeedbackEmpty"));
const utils_1 = require("./utils");
class GroupUserFeedback extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            error: false,
            reportList: [],
            pageLinks: '',
        };
        this.fetchData = () => {
            this.setState({
                loading: true,
                error: false,
            });
            (0, utils_1.fetchGroupUserReports)(this.props.group.id, Object.assign(Object.assign({}, this.props.params), { cursor: this.props.location.query.cursor || '' }))
                .then(([data, _, resp]) => {
                this.setState({
                    error: false,
                    loading: false,
                    reportList: data,
                    pageLinks: resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link'),
                });
            })
                .catch(() => {
                this.setState({
                    error: true,
                    loading: false,
                });
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)(prevProps.params, this.props.params) ||
            prevProps.location.pathname !== this.props.location.pathname ||
            prevProps.location.search !== this.props.location.search) {
            this.fetchData();
        }
    }
    render() {
        const { reportList, loading, error } = this.state;
        const { organization, group } = this.props;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        if (reportList.length) {
            return (<div className="row">
          <div className="col-md-9">
            {reportList.map((item, idx) => (<userFeedback_1.default key={idx} report={item} orgId={organization.slug} issueId={group.id}/>))}
            <pagination_1.default pageLinks={this.state.pageLinks} {...this.props}/>
          </div>
        </div>);
        }
        return <userFeedbackEmpty_1.default projectIds={[group.project.id]}/>;
    }
}
exports.default = (0, withOrganization_1.default)(GroupUserFeedback);
//# sourceMappingURL=groupUserFeedback.jsx.map