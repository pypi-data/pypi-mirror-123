Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class UnstyledSettingsPageHeader extends React.Component {
    render() {
        const _a = this.props, { icon, title, subtitle, action, tabs, noTitleStyles, body } = _a, props = (0, tslib_1.__rest)(_a, ["icon", "title", "subtitle", "action", "tabs", "noTitleStyles", "body"]);
        // If Header is narrow, use align-items to center <Action>.
        // Otherwise, use a fixed margin to prevent an odd alignment.
        // This is needed as Actions could be a button or a dropdown.
        const isNarrow = !subtitle;
        return (<div {...props}>
        <TitleAndActions isNarrow={isNarrow}>
          <TitleWrapper>
            {icon && <Icon>{icon}</Icon>}
            {title && (<Title tabs={tabs} styled={noTitleStyles}>
                <organization_1.HeaderTitle>{title}</organization_1.HeaderTitle>
                {subtitle && <Subtitle>{subtitle}</Subtitle>}
              </Title>)}
          </TitleWrapper>
          {action && <Action isNarrow={isNarrow}>{action}</Action>}
        </TitleAndActions>

        {body && <BodyWrapper>{body}</BodyWrapper>}
        {tabs && <TabsWrapper>{tabs}</TabsWrapper>}
      </div>);
    }
}
UnstyledSettingsPageHeader.defaultProps = {
    noTitleStyles: false,
};
const TitleAndActions = (0, styled_1.default)('div') `
  display: flex;
  align-items: ${p => (p.isNarrow ? 'center' : 'flex-start')};
`;
const TitleWrapper = (0, styled_1.default)('div') `
  flex: 1;
`;
const Title = (0, styled_1.default)('div') `
  ${p => !p.styled && `font-size: 20px; font-weight: 600;`};
  margin: ${(0, space_1.default)(4)} ${(0, space_1.default)(2)} ${(0, space_1.default)(3)} 0;
`;
const Subtitle = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray400};
  font-weight: 400;
  font-size: ${p => p.theme.fontSizeLarge};
  padding: ${(0, space_1.default)(1.5)} 0 0;
`;
const Icon = (0, styled_1.default)('div') `
  margin-right: ${(0, space_1.default)(1)};
`;
const Action = (0, styled_1.default)('div') `
  margin-top: ${p => (p.isNarrow ? '0' : (0, space_1.default)(4))};
`;
const SettingsPageHeader = (0, styled_1.default)(UnstyledSettingsPageHeader) `
  font-size: 14px;
  margin-top: -${(0, space_1.default)(4)};
`;
const BodyWrapper = (0, styled_1.default)('div') `
  flex: 1;
  margin: 0 0 ${(0, space_1.default)(3)};
`;
const TabsWrapper = (0, styled_1.default)('div') `
  flex: 1;
  margin: 0; /* sentry/components/navTabs has added margin */
`;
exports.default = SettingsPageHeader;
//# sourceMappingURL=settingsPageHeader.jsx.map