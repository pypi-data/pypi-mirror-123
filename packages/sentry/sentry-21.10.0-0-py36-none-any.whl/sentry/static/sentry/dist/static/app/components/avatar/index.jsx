Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const organizationAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/organizationAvatar"));
const projectAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/projectAvatar"));
const teamAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/teamAvatar"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const Avatar = React.forwardRef(function Avatar(_a, ref) {
    var { hasTooltip = false, user, team, project, organization } = _a, props = (0, tslib_1.__rest)(_a, ["hasTooltip", "user", "team", "project", "organization"]);
    const commonProps = Object.assign({ hasTooltip, forwardedRef: ref }, props);
    if (user) {
        return <userAvatar_1.default user={user} {...commonProps}/>;
    }
    if (team) {
        return <teamAvatar_1.default team={team} {...commonProps}/>;
    }
    if (project) {
        return <projectAvatar_1.default project={project} {...commonProps}/>;
    }
    return <organizationAvatar_1.default organization={organization} {...commonProps}/>;
});
exports.default = Avatar;
//# sourceMappingURL=index.jsx.map