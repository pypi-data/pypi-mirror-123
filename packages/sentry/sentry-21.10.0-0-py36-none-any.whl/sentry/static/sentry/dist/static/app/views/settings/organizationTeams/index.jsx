Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationTeamsContainer = void 0;
const tslib_1 = require("tslib");
const projects_1 = require("app/actionCreators/projects");
const teamActions_1 = (0, tslib_1.__importDefault)(require("app/actions/teamActions"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const organizationTeams_1 = (0, tslib_1.__importDefault)(require("./organizationTeams"));
class OrganizationTeamsContainer extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.removeAccessRequest = (id, isApproved) => {
            const requestToRemove = this.state.requestList.find(request => request.id === id);
            this.setState(state => ({
                requestList: state.requestList.filter(request => request.id !== id),
            }));
            if (isApproved && requestToRemove) {
                const team = requestToRemove.team;
                teamActions_1.default.updateSuccess(team.slug, Object.assign(Object.assign({}, team), { memberCount: team.memberCount + 1 }));
            }
        };
    }
    getEndpoints() {
        const { orgId } = this.props.params;
        return [['requestList', `/organizations/${orgId}/access-requests/`]];
    }
    componentDidMount() {
        this.fetchStats();
    }
    fetchStats() {
        (0, projects_1.loadStats)(this.props.api, {
            orgId: this.props.params.orgId,
            query: {
                since: (new Date().getTime() / 1000 - 3600 * 24).toString(),
                stat: 'generated',
                group: 'project',
            },
        });
    }
    renderBody() {
        const { organization } = this.props;
        if (!organization) {
            return null;
        }
        return (<organizationTeams_1.default {...this.props} access={new Set(organization.access)} features={new Set(organization.features)} organization={organization} requestList={this.state.requestList} onRemoveAccessRequest={this.removeAccessRequest}/>);
    }
}
exports.OrganizationTeamsContainer = OrganizationTeamsContainer;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(OrganizationTeamsContainer));
//# sourceMappingURL=index.jsx.map