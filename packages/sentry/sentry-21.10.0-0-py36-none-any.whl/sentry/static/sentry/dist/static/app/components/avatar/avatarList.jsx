Object.defineProperty(exports, "__esModule", { value: true });
exports.AvatarListWrapper = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const defaultProps = {
    avatarSize: 28,
    maxVisibleAvatars: 5,
    typeMembers: 'users',
    tooltipOptions: {},
};
class AvatarList extends react_1.Component {
    render() {
        const { className, users, avatarSize, maxVisibleAvatars, renderTooltip, typeMembers, tooltipOptions, } = this.props;
        const visibleUsers = users.slice(0, maxVisibleAvatars);
        const numCollapsedUsers = users.length - visibleUsers.length;
        if (!tooltipOptions.position) {
            tooltipOptions.position = 'top';
        }
        return (<exports.AvatarListWrapper className={className}>
        {!!numCollapsedUsers && (<tooltip_1.default title={`${numCollapsedUsers} other ${typeMembers}`}>
            <CollapsedUsers size={avatarSize} data-test-id="avatarList-collapsedusers">
              {numCollapsedUsers < 99 && <Plus>+</Plus>}
              {numCollapsedUsers}
            </CollapsedUsers>
          </tooltip_1.default>)}
        {visibleUsers.map(user => (<StyledAvatar key={`${user.id}-${user.email}`} user={user} size={avatarSize} renderTooltip={renderTooltip} tooltipOptions={tooltipOptions} hasTooltip/>))}
      </exports.AvatarListWrapper>);
    }
}
exports.default = AvatarList;
AvatarList.defaultProps = defaultProps;
// used in releases list page to do some alignment
exports.AvatarListWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row-reverse;
`;
const Circle = p => (0, react_2.css) `
  border-radius: 50%;
  border: 2px solid ${p.theme.background};
  margin-left: -8px;
  cursor: default;

  &:hover {
    z-index: 1;
  }
`;
const StyledAvatar = (0, styled_1.default)(userAvatar_1.default) `
  overflow: hidden;
  ${Circle};
`;
const CollapsedUsers = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  text-align: center;
  font-weight: 600;
  background-color: ${p => p.theme.gray200};
  color: ${p => p.theme.gray300};
  font-size: ${p => Math.floor(p.size / 2.3)}px;
  width: ${p => p.size}px;
  height: ${p => p.size}px;
  ${Circle};
`;
const Plus = (0, styled_1.default)('span') `
  font-size: 10px;
  margin-left: 1px;
  margin-right: -1px;
`;
//# sourceMappingURL=avatarList.jsx.map