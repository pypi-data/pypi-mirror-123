Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const analytics_1 = require("app/utils/analytics");
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const groupDetails_1 = (0, tslib_1.__importDefault)(require("./groupDetails"));
const sampleEventAlert_1 = (0, tslib_1.__importDefault)(require("./sampleEventAlert"));
class OrganizationGroupDetails extends React.Component {
    componentDidMount() {
        (0, analytics_1.analytics)('issue_page.viewed', {
            group_id: parseInt(this.props.params.groupId, 10),
            org_id: parseInt(this.props.organization.id, 10),
        });
    }
    render() {
        const _a = this.props, { selection } = _a, props = (0, tslib_1.__rest)(_a, ["selection"]);
        return (<React.Fragment>
        <sampleEventAlert_1.default />

        <groupDetails_1.default key={`${this.props.params.groupId}-envs:${selection.environments.join(',')}`} environments={selection.environments} {...props}/>
      </React.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)((0, withProjects_1.default)((0, withGlobalSelection_1.default)(OrganizationGroupDetails)));
//# sourceMappingURL=index.jsx.map