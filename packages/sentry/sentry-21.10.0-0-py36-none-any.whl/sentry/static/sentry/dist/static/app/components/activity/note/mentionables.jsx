Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const uniqBy_1 = (0, tslib_1.__importDefault)(require("lodash/uniqBy"));
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const isRenderFunc_1 = require("app/utils/isRenderFunc");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const buildUserId = (id) => `user:${id}`;
const buildTeamId = (id) => `team:${id}`;
/**
 * Make sure the actionCreator, `fetchOrgMembers`, has been called somewhere
 * higher up the component chain.
 *
 * Will provide a list of users and teams that can be used for @-mentions
 * */
class Mentionables extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            members: memberListStore_1.default.getAll(),
        };
        this.listeners = [
            memberListStore_1.default.listen((users) => {
                this.handleMemberListUpdate(users);
            }, undefined),
        ];
        this.handleMemberListUpdate = (members) => {
            if (members === this.state.members) {
                return;
            }
            this.setState({
                members,
            });
        };
        this.renderChildren = ({ projects }) => {
            const { children, me } = this.props;
            if ((0, isRenderFunc_1.isRenderFunc)(children)) {
                return children({
                    members: this.getMemberList(this.state.members, me),
                    teams: this.getTeams(projects),
                });
            }
            return null;
        };
    }
    componentWillUnmount() {
        this.listeners.forEach(callIfFunction_1.callIfFunction);
    }
    getMemberList(memberList, sessionUser) {
        const members = (0, uniqBy_1.default)(memberList, ({ id }) => id).filter(({ id }) => !sessionUser || sessionUser.id !== id);
        return members.map(member => ({
            id: buildUserId(member.id),
            display: member.name,
            email: member.email,
        }));
    }
    getTeams(projects) {
        const uniqueTeams = (0, uniqBy_1.default)(projects
            .map(({ teams }) => teams)
            .reduce((acc, teams) => acc.concat(teams || []), []), 'id');
        return uniqueTeams.map(team => ({
            id: buildTeamId(team.id),
            display: `#${team.slug}`,
            email: team.id,
        }));
    }
    render() {
        const { organization, projectSlugs } = this.props;
        if (!projectSlugs || !projectSlugs.length) {
            return this.renderChildren({ projects: [] });
        }
        return (<projects_1.default slugs={projectSlugs} orgId={organization.slug}>
        {this.renderChildren}
      </projects_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)(Mentionables);
//# sourceMappingURL=mentionables.jsx.map