Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const baseAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/baseAvatar"));
const formatters_1 = require("app/utils/formatters");
const isRenderFunc_1 = require("app/utils/isRenderFunc");
const defaultProps = {
    // Default gravatar to false in order to support transparent avatars
    // Avatar falls through to letter avatars if a remote image fails to load,
    // however gravatar sends back a transparent image when it does not find a gravatar,
    // so there's little we have to control whether we need to fallback to letter avatar
    gravatar: false,
};
function isActor(maybe) {
    return typeof maybe.email === 'undefined';
}
class UserAvatar extends React.Component {
    constructor() {
        super(...arguments);
        this.getType = (user, gravatar) => {
            if (isActor(user)) {
                return 'letter_avatar';
            }
            if (user.avatar) {
                return user.avatar.avatarType;
            }
            if (user.options && user.options.avatarType) {
                return user.options.avatarType;
            }
            return user.email && gravatar ? 'gravatar' : 'letter_avatar';
        };
    }
    render() {
        var _a, _b, _c;
        const _d = this.props, { user, gravatar, renderTooltip } = _d, props = (0, tslib_1.__rest)(_d, ["user", "gravatar", "renderTooltip"]);
        if (!user) {
            return null;
        }
        const type = this.getType(user, gravatar);
        let tooltip = null;
        if ((0, isRenderFunc_1.isRenderFunc)(renderTooltip)) {
            tooltip = renderTooltip(user);
        }
        else if (props.tooltip) {
            tooltip = props.tooltip;
        }
        else {
            tooltip = (0, formatters_1.userDisplayName)(user);
        }
        const avatarData = isActor(user)
            ? {
                uploadId: '',
                gravatarId: '',
                letterId: user.name,
                title: user.name,
            }
            : {
                uploadId: (_b = (_a = user.avatar) === null || _a === void 0 ? void 0 : _a.avatarUuid) !== null && _b !== void 0 ? _b : '',
                gravatarId: (_c = user.email) === null || _c === void 0 ? void 0 : _c.toLowerCase(),
                letterId: user.email || user.username || user.id || user.ip_address,
                title: user.name || user.email || user.username || '',
            };
        return (<baseAvatar_1.default round {...props} type={type} uploadPath="avatar" uploadId={avatarData.uploadId} gravatarId={avatarData.gravatarId} letterId={avatarData.letterId} title={avatarData.title} tooltip={tooltip}/>);
    }
}
UserAvatar.defaultProps = defaultProps;
exports.default = UserAvatar;
//# sourceMappingURL=userAvatar.jsx.map