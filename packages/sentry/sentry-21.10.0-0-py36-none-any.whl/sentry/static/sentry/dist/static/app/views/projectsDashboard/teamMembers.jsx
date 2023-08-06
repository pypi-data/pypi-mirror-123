Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const avatarList_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/avatarList"));
class TeamMembers extends asyncComponent_1.default {
    getEndpoints() {
        const { orgId, teamId } = this.props;
        return [['members', `/teams/${orgId}/${teamId}/members/`]];
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        const { members } = this.state;
        if (!members) {
            return null;
        }
        const users = members.filter(({ user }) => !!user).map(({ user }) => user);
        return <avatarList_1.default users={users}/>;
    }
}
exports.default = TeamMembers;
//# sourceMappingURL=teamMembers.jsx.map