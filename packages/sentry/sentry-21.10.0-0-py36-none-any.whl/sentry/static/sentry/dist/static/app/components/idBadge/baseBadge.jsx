Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const BaseBadge = React.memo(({ displayName, hideName = false, hideAvatar = false, avatarProps = {}, avatarSize = 24, description, team, organization, project, className, }) => (<Wrapper className={className}>
      {!hideAvatar && (<StyledAvatar {...avatarProps} size={avatarSize} hideName={hideName} team={team} organization={organization} project={project}/>)}

      {(!hideName || !!description) && (<DisplayNameAndDescription>
          {!hideName && (<DisplayName data-test-id="badge-display-name">{displayName}</DisplayName>)}
          {!!description && <Description>{description}</Description>}
        </DisplayNameAndDescription>)}
    </Wrapper>));
exports.default = BaseBadge;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  flex-shrink: 0;
`;
const StyledAvatar = (0, styled_1.default)(avatar_1.default) `
  margin-right: ${p => (p.hideName ? 0 : (0, space_1.default)(1))};
  flex-shrink: 0;
`;
const DisplayNameAndDescription = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  line-height: 1;
  overflow: hidden;
`;
const DisplayName = (0, styled_1.default)('span') `
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2;
`;
const Description = (0, styled_1.default)('div') `
  font-size: 0.875em;
  margin-top: ${(0, space_1.default)(0.25)};
  color: ${p => p.theme.gray300};
  line-height: 14px;
  ${overflowEllipsis_1.default};
`;
//# sourceMappingURL=baseBadge.jsx.map