Object.defineProperty(exports, "__esModule", { value: true });
exports.alertStyles = void 0;
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const DEFAULT_TYPE = 'info';
const IconWrapper = (0, styled_1.default)('span') `
  display: flex;
  margin-right: ${(0, space_1.default)(1)};

  /* Give the wrapper an explicit height so icons are line height with the
   * (common) line height. */
  height: 22px;
  align-items: center;
`;
const getAlertColorStyles = ({ backgroundLight, border, iconColor, }) => (0, react_2.css) `
  background: ${backgroundLight};
  border: 1px solid ${border};
  ${IconWrapper} {
    color: ${iconColor};
  }
`;
const getSystemAlertColorStyles = ({ backgroundLight, border, iconColor, }) => (0, react_2.css) `
  background: ${backgroundLight};
  border: 0;
  border-radius: 0;
  border-bottom: 1px solid ${border};
  ${IconWrapper} {
    color: ${iconColor};
  }
`;
const alertStyles = ({ theme, type = DEFAULT_TYPE, system }) => (0, react_2.css) `
  display: flex;
  flex-direction: column;
  margin: 0 0 ${(0, space_1.default)(3)};
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
  font-size: ${theme.fontSizeLarge};
  box-shadow: ${theme.dropShadowLight};
  border-radius: ${theme.borderRadius};
  background: ${theme.backgroundSecondary};
  border: 1px solid ${theme.border};

  a:not([role='button']) {
    color: ${theme.textColor};
    border-bottom: 1px dotted ${theme.textColor};
  }

  ${getAlertColorStyles(theme.alert[type])};
  ${system && getSystemAlertColorStyles(theme.alert[type])};
`;
exports.alertStyles = alertStyles;
const StyledTextBlock = (0, styled_1.default)('span') `
  line-height: 1.5;
  position: relative;
  flex: 1;
`;
const MessageContainer = (0, styled_1.default)('div') `
  display: flex;
  width: 100%;
`;
const ExpandContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: minmax(${(0, space_1.default)(4)}, 1fr) 30fr 1fr;
  grid-template-areas: '. details details';
  padding: ${(0, space_1.default)(1.5)} 0;
`;
const DetailsContainer = (0, styled_1.default)('div') `
  grid-area: details;
`;
const ExpandIcon = (0, styled_1.default)(props => (<IconWrapper {...props}>{<icons_1.IconChevron size="md"/>}</IconWrapper>)) `
  transform: ${props => (props.isExpanded ? 'rotate(0deg)' : 'rotate(180deg)')};
  cursor: pointer;
  justify-self: flex-end;
`;
const Alert = (0, styled_1.default)((_a) => {
    var { type, icon, children, className, expand, expandIcon, onExpandIconClick, system: _system } = _a, // don't forward to `div`
    props = (0, tslib_1.__rest)(_a, ["type", "icon", "children", "className", "expand", "expandIcon", "onExpandIconClick", "system"]);
    const [isExpanded, setIsExpanded] = (0, react_1.useState)(false);
    const showExpand = expand && expand.length;
    const showExpandItems = showExpand && isExpanded;
    const handleOnExpandIconClick = onExpandIconClick ? onExpandIconClick : setIsExpanded;
    return (<div className={(0, classnames_1.default)(type ? `ref-${type}` : '', className)} {...props}>
        <MessageContainer>
          {icon && <IconWrapper>{icon}</IconWrapper>}
          <StyledTextBlock>{children}</StyledTextBlock>
          {showExpand && (<div onClick={() => handleOnExpandIconClick(!isExpanded)}>
              {expandIcon || <ExpandIcon isExpanded={isExpanded}/>}
            </div>)}
        </MessageContainer>
        {showExpandItems && (<ExpandContainer>
            <DetailsContainer>{(expand || []).map(item => item)}</DetailsContainer>
          </ExpandContainer>)}
      </div>);
}) `
  ${alertStyles}
`;
Alert.defaultProps = {
    type: DEFAULT_TYPE,
};
exports.default = Alert;
//# sourceMappingURL=alert.jsx.map