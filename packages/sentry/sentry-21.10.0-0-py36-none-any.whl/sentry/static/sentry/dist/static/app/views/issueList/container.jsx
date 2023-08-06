Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueListContainer = void 0;
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const groupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/groupStore"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const sampleEventAlert_1 = (0, tslib_1.__importDefault)(require("app/views/organizationGroupDetails/sampleEventAlert"));
class IssueListContainer extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showSampleEventBanner: false,
        };
        this.listener = groupStore_1.default.listen(() => this.onGroupChange(), undefined);
    }
    render() {
        const { organization, children } = this.props;
        return (<react_document_title_1.default title={this.getTitle()}>
        <react_1.default.Fragment>
          {this.state.showSampleEventBanner && <sampleEventAlert_1.default />}
          <globalSelectionHeader_1.default>
            <noProjectMessage_1.default organization={organization}>{children}</noProjectMessage_1.default>
          </globalSelectionHeader_1.default>
        </react_1.default.Fragment>
      </react_document_title_1.default>);
    }
    onGroupChange() {
        this.setState({
            showSampleEventBanner: groupStore_1.default.getAllItemIds().length === 1,
        });
    }
    componentWillUnmount() {
        (0, callIfFunction_1.callIfFunction)(this.listener);
    }
    getTitle() {
        return `Issues - ${this.props.organization.slug} - Sentry`;
    }
}
exports.IssueListContainer = IssueListContainer;
exports.default = (0, withOrganization_1.default)(IssueListContainer);
//# sourceMappingURL=container.jsx.map