Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function AlertLink({ size = 'normal', priority = 'warning', icon, children, onClick, withoutMarginBottom = false, openInNewTab = false, to, href, ['data-test-id']: dataTestId, }) {
    return (<StyledLink data-test-id={dataTestId} to={to} href={href} onClick={onClick} size={size} priority={priority} withoutMarginBottom={withoutMarginBottom} openInNewTab={openInNewTab}>
      {icon && <IconWrapper>{icon}</IconWrapper>}
      <AlertLinkText>{children}</AlertLinkText>
      <IconLink>
        <icons_1.IconChevron direction="right"/>
      </IconLink>
    </StyledLink>);
}
exports.default = AlertLink;
const StyledLink = (0, styled_1.default)((_a) => {
    var { openInNewTab, to, href } = _a, props = (0, tslib_1.__rest)(_a, ["openInNewTab", "to", "href"]);
    const linkProps = (0, omit_1.default)(props, ['withoutMarginBottom', 'priority', 'size']);
    if (href) {
        return <externalLink_1.default {...linkProps} href={href} openInNewTab={openInNewTab}/>;
    }
    return <link_1.default {...linkProps} to={to || ''}/>;
}) `
  display: flex;
  background-color: ${p => p.theme.alert[p.priority].backgroundLight};
  color: ${p => p.theme.textColor};
  border: 1px dashed ${p => p.theme.alert[p.priority].border};
  padding: ${p => (p.size === 'small' ? `${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)}` : (0, space_1.default)(2))};
  margin-bottom: ${p => (p.withoutMarginBottom ? 0 : (0, space_1.default)(3))};
  border-radius: 0.25em;
  transition: 0.2s border-color;

  &.focus-visible {
    outline: none;
    box-shadow: ${p => p.theme.alert[p.priority].border}7f 0 0 0 2px;
  }
`;
const IconWrapper = (0, styled_1.default)('span') `
  display: flex;
  margin: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1.5)} ${(0, space_1.default)(0.5)} 0;
`;
const IconLink = (0, styled_1.default)(IconWrapper) `
  margin: ${(0, space_1.default)(0.5)} 0;
`;
const AlertLinkText = (0, styled_1.default)('div') `
  line-height: 1.5;
  flex-grow: 1;
`;
//# sourceMappingURL=alertLink.jsx.map