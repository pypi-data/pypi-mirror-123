Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const avatarList_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/avatarList"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
const SeenByList = ({ avatarSize = 28, seenBy = [], iconTooltip = (0, locale_1.t)('People who have viewed this'), maxVisibleAvatars = 10, iconPosition = 'left', className, }) => {
    const activeUser = configStore_1.default.get('user');
    const displayUsers = seenBy.filter(user => activeUser.id !== user.id);
    if (displayUsers.length === 0) {
        return null;
    }
    // Note className="seen-by" is required for responsive design
    return (<SeenByWrapper iconPosition={iconPosition} className={(0, classnames_1.default)('seen-by', className)}>
      <avatarList_1.default users={displayUsers} avatarSize={avatarSize} maxVisibleAvatars={maxVisibleAvatars} renderTooltip={user => (<react_1.Fragment>
            {(0, formatters_1.userDisplayName)(user)}
            <br />
            {(0, moment_1.default)(user.lastSeen).format('LL')}
          </react_1.Fragment>)}/>
      <IconWrapper iconPosition={iconPosition}>
        <tooltip_1.default title={iconTooltip}>
          <icons_1.IconShow size="sm" color="gray200"/>
        </tooltip_1.default>
      </IconWrapper>
    </SeenByWrapper>);
};
const SeenByWrapper = (0, styled_1.default)('div') `
  display: flex;
  margin-top: 15px;
  float: right;
  ${p => (p.iconPosition === 'left' ? 'flex-direction: row-reverse' : '')};
`;
const IconWrapper = (0, styled_1.default)('div') `
  background-color: transparent;
  color: ${p => p.theme.textColor};
  height: 28px;
  width: 24px;
  line-height: 26px;
  text-align: center;
  padding-top: ${(0, space_1.default)(0.5)};
  ${p => (p.iconPosition === 'left' ? 'margin-right: 10px' : '')};
`;
exports.default = SeenByList;
//# sourceMappingURL=seenByList.jsx.map