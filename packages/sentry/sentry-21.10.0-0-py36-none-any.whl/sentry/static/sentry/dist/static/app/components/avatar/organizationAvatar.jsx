Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const baseAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/baseAvatar"));
const utils_1 = require("app/utils");
class OrganizationAvatar extends react_1.Component {
    render() {
        const _a = this.props, { organization } = _a, props = (0, tslib_1.__rest)(_a, ["organization"]);
        if (!organization) {
            return null;
        }
        const slug = (organization && organization.slug) || '';
        const title = (0, utils_1.explodeSlug)(slug);
        return (<baseAvatar_1.default {...props} type={(organization.avatar && organization.avatar.avatarType) || 'letter_avatar'} uploadPath="organization-avatar" uploadId={organization.avatar && organization.avatar.avatarUuid} letterId={slug} tooltip={slug} title={title}/>);
    }
}
exports.default = OrganizationAvatar;
//# sourceMappingURL=organizationAvatar.jsx.map