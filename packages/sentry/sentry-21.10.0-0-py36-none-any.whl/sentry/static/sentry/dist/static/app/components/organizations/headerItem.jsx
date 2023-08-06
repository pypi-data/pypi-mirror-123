Object.defineProperty(exports, "__esModule", { value: true });
exports.SettingsIconLink = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function HeaderItem(_a) {
    var { children, isOpen, hasSelected, icon, locked, lockedMessage, settingsLink, hint, loading, forwardRef, onClear, allowClear = true } = _a, props = (0, tslib_1.__rest)(_a, ["children", "isOpen", "hasSelected", "icon", "locked", "lockedMessage", "settingsLink", "hint", "loading", "forwardRef", "onClear", "allowClear"]);
    const handleClear = (e) => {
        e.stopPropagation();
        onClear === null || onClear === void 0 ? void 0 : onClear();
    };
    const textColorProps = {
        locked,
        isOpen,
        hasSelected,
    };
    return (<StyledHeaderItem ref={forwardRef} loading={!!loading} {...(0, omit_1.default)(props, 'onClear')} {...textColorProps}>
      <IconContainer {...textColorProps}>{icon}</IconContainer>
      <Content>
        <StyledContent>{children}</StyledContent>

        {settingsLink && (<exports.SettingsIconLink to={settingsLink}>
            <icons_1.IconSettings />
          </exports.SettingsIconLink>)}
      </Content>
      {hint && (<Hint>
          <tooltip_1.default title={hint} position="bottom">
            <icons_1.IconInfo size="sm"/>
          </tooltip_1.default>
        </Hint>)}
      {hasSelected && !locked && allowClear && (<StyledClose {...textColorProps} onClick={handleClear}/>)}
      {!locked && !loading && (<ChevronWrapper>
          <StyledChevron isOpen={!!isOpen} direction={isOpen ? 'up' : 'down'} size="sm"/>
        </ChevronWrapper>)}
      {locked && (<tooltip_1.default title={lockedMessage || (0, locale_1.t)('This selection is locked')} position="bottom">
          <StyledLock color="gray300"/>
        </tooltip_1.default>)}
    </StyledHeaderItem>);
}
// Infer props here because of styled/theme
const getColor = (p) => {
    if (p.locked) {
        return p.theme.gray300;
    }
    return p.isOpen || p.hasSelected ? p.theme.textColor : p.theme.gray300;
};
const StyledHeaderItem = (0, styled_1.default)('div', {
    shouldForwardProp: p => typeof p === 'string' && (0, is_prop_valid_1.default)(p) && p !== 'loading',
}) `
  display: flex;
  padding: 0 ${(0, space_1.default)(4)};
  align-items: center;
  cursor: ${p => (p.loading ? 'progress' : p.locked ? 'text' : 'pointer')};
  color: ${getColor};
  transition: 0.1s color;
  user-select: none;
`;
const Content = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  margin-right: ${(0, space_1.default)(1.5)};
`;
const StyledContent = (0, styled_1.default)('div') `
  overflow: hidden;
  text-overflow: ellipsis;
`;
const IconContainer = (0, styled_1.default)('span', { shouldForwardProp: is_prop_valid_1.default }) `
  color: ${getColor};
  margin-right: ${(0, space_1.default)(1.5)};
  display: flex;
  font-size: ${p => p.theme.fontSizeMedium};
`;
const Hint = (0, styled_1.default)('div') `
  position: relative;
  top: ${(0, space_1.default)(0.25)};
  margin-right: ${(0, space_1.default)(1)};
`;
const StyledClose = (0, styled_1.default)(icons_1.IconClose, { shouldForwardProp: is_prop_valid_1.default }) `
  color: ${getColor};
  height: ${(0, space_1.default)(1.5)};
  width: ${(0, space_1.default)(1.5)};
  stroke-width: 1.5;
  padding: ${(0, space_1.default)(1)};
  box-sizing: content-box;
  margin: -${(0, space_1.default)(1)} 0px -${(0, space_1.default)(1)} -${(0, space_1.default)(1)};
`;
const ChevronWrapper = (0, styled_1.default)('div') `
  width: ${(0, space_1.default)(2)};
  height: ${(0, space_1.default)(2)};
  display: flex;
  align-items: center;
  justify-content: center;
`;
const StyledChevron = (0, styled_1.default)(icons_1.IconChevron, { shouldForwardProp: is_prop_valid_1.default }) `
  color: ${getColor};
`;
exports.SettingsIconLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.gray300};
  align-items: center;
  display: inline-flex;
  justify-content: space-between;
  margin-right: ${(0, space_1.default)(1.5)};
  margin-left: ${(0, space_1.default)(1.0)};
  transition: 0.5s opacity ease-out;

  &:hover {
    color: ${p => p.theme.textColor};
  }
`;
const StyledLock = (0, styled_1.default)(icons_1.IconLock) `
  margin-top: ${(0, space_1.default)(0.75)};
  stroke-width: 1.5;
`;
exports.default = React.forwardRef((props, ref) => (<HeaderItem forwardRef={ref} {...props}/>));
//# sourceMappingURL=headerItem.jsx.map