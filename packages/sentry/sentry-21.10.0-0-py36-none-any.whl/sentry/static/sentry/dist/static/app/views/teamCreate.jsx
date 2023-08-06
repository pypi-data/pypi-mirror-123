Object.defineProperty(exports, "__esModule", { value: true });
exports.TeamCreate = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const narrowLayout_1 = (0, tslib_1.__importDefault)(require("app/components/narrowLayout"));
const createTeamForm_1 = (0, tslib_1.__importDefault)(require("app/components/teams/createTeamForm"));
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
class TeamCreate extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSubmitSuccess = data => {
            const { orgId } = this.props.params;
            const redirectUrl = `/settings/${orgId}/teams/${data.slug}/`;
            this.props.router.push(redirectUrl);
        };
    }
    getTitle() {
        return (0, locale_1.t)('Create Team');
    }
    getEndpoints() {
        return [];
    }
    renderBody() {
        return (<narrowLayout_1.default>
        <h3>{(0, locale_1.t)('Create a New Team')}</h3>

        <createTeamForm_1.default onSuccess={this.handleSubmitSuccess} organization={this.props.organization}/>
      </narrowLayout_1.default>);
    }
}
exports.TeamCreate = TeamCreate;
exports.default = (0, react_router_1.withRouter)((0, withOrganization_1.default)(TeamCreate));
//# sourceMappingURL=teamCreate.jsx.map