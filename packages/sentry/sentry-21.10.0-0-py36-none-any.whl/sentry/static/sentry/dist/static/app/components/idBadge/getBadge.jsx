Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const memberBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/memberBadge"));
const organizationBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/organizationBadge"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const badge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/teamBadge/badge"));
const userBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/userBadge"));
function getBadge(_a) {
    var { organization, team, project, user, member } = _a, props = (0, tslib_1.__rest)(_a, ["organization", "team", "project", "user", "member"]);
    if (organization) {
        return <organizationBadge_1.default organization={organization} {...props}/>;
    }
    if (team) {
        return <badge_1.default team={team} {...props}/>;
    }
    if (project) {
        return <projectBadge_1.default project={project} {...props}/>;
    }
    if (user) {
        return <userBadge_1.default user={user} {...props}/>;
    }
    if (member) {
        return <memberBadge_1.default member={member} {...props}/>;
    }
    return null;
}
exports.default = getBadge;
//# sourceMappingURL=getBadge.jsx.map