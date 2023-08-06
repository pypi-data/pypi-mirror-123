Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function getMemberUser(member) {
    if (member.user) {
        return member.user;
    }
    // Adapt the member into a AvatarUser
    return {
        id: '',
        name: member.name,
        email: member.email,
        username: '',
        ip_address: '',
    };
}
const MemberBadge = ({ avatarSize = 24, useLink = true, hideEmail = false, displayName, displayEmail, member, orgId, className, }) => {
    const user = getMemberUser(member);
    const title = displayName ||
        user.name ||
        user.email ||
        user.username ||
        user.ipAddress ||
        // Because this can be used to render EventUser models, or User *interface*
        // objects from serialized Event models. we try both ipAddress and ip_address.
        user.ip_address;
    return (<StyledUserBadge className={className}>
      <StyledAvatar user={user} size={avatarSize}/>
      <StyledNameAndEmail>
        <StyledName useLink={useLink && !!orgId} hideEmail={hideEmail} to={(member && orgId && `/settings/${orgId}/members/${member.id}/`) || ''}>
          {title}
        </StyledName>
        {!hideEmail && <StyledEmail>{displayEmail || user.email}</StyledEmail>}
      </StyledNameAndEmail>
    </StyledUserBadge>);
};
const StyledUserBadge = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const StyledNameAndEmail = (0, styled_1.default)('div') `
  flex-shrink: 1;
  min-width: 0;
  line-height: 1;
`;
const StyledEmail = (0, styled_1.default)('div') `
  font-size: 0.875em;
  margin-top: ${(0, space_1.default)(0.25)};
  color: ${p => p.theme.gray300};
  ${overflowEllipsis_1.default};
`;
const StyledName = (0, styled_1.default)((_a) => {
    var { useLink, to } = _a, props = (0, tslib_1.__rest)(_a, ["useLink", "to"]);
    const forwardProps = (0, omit_1.default)(props, 'hideEmail');
    return useLink ? <link_1.default to={to} {...forwardProps}/> : <span {...forwardProps}/>;
}) `
  font-weight: ${(p) => (p.hideEmail ? 'inherit' : 'bold')};
  line-height: 1.15em;
  ${overflowEllipsis_1.default};
`;
const StyledAvatar = (0, styled_1.default)(userAvatar_1.default) `
  min-width: ${(0, space_1.default)(3)};
  min-height: ${(0, space_1.default)(3)};
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = MemberBadge;
//# sourceMappingURL=memberBadge.jsx.map