Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const processingIssues_1 = require("app/actionCreators/processingIssues");
const api_1 = require("app/api");
const processingIssueHint_1 = (0, tslib_1.__importDefault)(require("app/components/stream/processingIssueHint"));
const defaultProps = {
    showProject: false,
};
class ProcessingIssueList extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            issues: [],
        };
        this.api = new api_1.Client();
    }
    componentDidMount() {
        this.fetchIssues();
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)(prevProps.projectIds, this.props.projectIds)) {
            this.fetchIssues();
        }
    }
    componentWillUnmount() {
        this.api.clear();
    }
    fetchIssues() {
        const { organization, projectIds } = this.props;
        const promise = (0, processingIssues_1.fetchProcessingIssues)(this.api, organization.slug, projectIds);
        promise.then((data) => {
            const hasIssues = data === null || data === void 0 ? void 0 : data.some(p => p.hasIssues || p.resolveableIssues > 0 || p.issuesProcessing > 0);
            if (data && hasIssues) {
                this.setState({ issues: data });
            }
        }, () => {
            // this is okay. it's just a ui hint
        });
    }
    render() {
        const { issues } = this.state;
        const { organization, showProject } = this.props;
        return (<react_1.Fragment>
        {issues.map((p, idx) => (<processingIssueHint_1.default key={idx} issue={p} projectId={p.project} orgId={organization.slug} showProject={showProject}/>))}
      </react_1.Fragment>);
    }
}
ProcessingIssueList.defaultProps = defaultProps;
exports.default = ProcessingIssueList;
//# sourceMappingURL=processingIssueList.jsx.map