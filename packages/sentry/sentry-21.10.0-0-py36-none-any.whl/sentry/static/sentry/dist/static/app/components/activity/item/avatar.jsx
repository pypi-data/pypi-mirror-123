Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
function ActivityAvatar({ className, type, user, size = 38 }) {
    if (user) {
        return <userAvatar_1.default user={user} size={size} className={className}/>;
    }
    if (type === 'system') {
        // Return Sentry avatar
        return (<SystemAvatar className={className} size={size}>
        <StyledIconSentry size="md"/>
      </SystemAvatar>);
    }
    return (<placeholder_1.default className={className} width={`${size}px`} height={`${size}px`} shape="circle"/>);
}
exports.default = ActivityAvatar;
const SystemAvatar = (0, styled_1.default)('span') `
  display: flex;
  justify-content: center;
  align-items: center;
  width: ${p => p.size}px;
  height: ${p => p.size}px;
  background-color: ${p => p.theme.textColor};
  color: ${p => p.theme.background};
  border-radius: 50%;
`;
const StyledIconSentry = (0, styled_1.default)(icons_1.IconSentry) `
  padding-bottom: 3px;
`;
//# sourceMappingURL=avatar.jsx.map