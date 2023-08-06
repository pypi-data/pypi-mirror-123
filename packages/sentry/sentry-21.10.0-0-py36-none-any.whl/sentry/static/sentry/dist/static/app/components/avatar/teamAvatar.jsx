Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const baseAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/baseAvatar"));
const utils_1 = require("app/utils");
class TeamAvatar extends react_1.Component {
    render() {
        const _a = this.props, { team, tooltip: tooltipProp } = _a, props = (0, tslib_1.__rest)(_a, ["team", "tooltip"]);
        if (!team) {
            return null;
        }
        const slug = (team && team.slug) || '';
        const title = (0, utils_1.explodeSlug)(slug);
        const tooltip = tooltipProp !== null && tooltipProp !== void 0 ? tooltipProp : `#${title}`;
        return (<baseAvatar_1.default {...props} type={(team.avatar && team.avatar.avatarType) || 'letter_avatar'} uploadPath="team-avatar" uploadId={team.avatar && team.avatar.avatarUuid} letterId={slug} tooltip={tooltip} title={title}/>);
    }
}
exports.default = TeamAvatar;
//# sourceMappingURL=teamAvatar.jsx.map