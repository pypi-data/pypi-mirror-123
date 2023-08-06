Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const hook_1 = (0, tslib_1.__importDefault)(require("app/components/hook"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
function BaseFooter({ className }) {
    const config = configStore_1.default.getConfig();
    return (<footer className={className}>
      <LeftLinks>
        {config.isOnPremise && (<react_1.Fragment>
            {'Sentry '}
            {(0, getDynamicText_1.default)({
                fixed: 'Acceptance Test',
                value: config.version.current,
            })}
            <Build>
              {(0, getDynamicText_1.default)({
                fixed: 'test',
                value: config.version.build.substring(0, 7),
            })}
            </Build>
          </react_1.Fragment>)}
        {config.privacyUrl && (<FooterLink href={config.privacyUrl}>{(0, locale_1.t)('Privacy Policy')}</FooterLink>)}
        {config.termsUrl && (<FooterLink href={config.termsUrl}>{(0, locale_1.t)('Terms of Use')}</FooterLink>)}
      </LeftLinks>
      <LogoLink />
      <RightLinks>
        <FooterLink href="/api/">{(0, locale_1.t)('API')}</FooterLink>
        <FooterLink href="/docs/">{(0, locale_1.t)('Docs')}</FooterLink>
        <FooterLink href="https://github.com/getsentry/sentry">
          {(0, locale_1.t)('Contribute')}
        </FooterLink>
        {config.isOnPremise && !config.demoMode && (<FooterLink href="/out/">{(0, locale_1.t)('Migrate to SaaS')}</FooterLink>)}
      </RightLinks>
      <hook_1.default name="footer"/>
    </footer>);
}
const LeftLinks = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: max-content;
  align-items: center;
  justify-self: flex-start;
  gap: ${(0, space_1.default)(2)};
`;
const RightLinks = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: max-content;
  align-items: center;
  justify-self: flex-end;
  gap: ${(0, space_1.default)(2)};
`;
const FooterLink = (0, styled_1.default)(externalLink_1.default) `
  color: ${p => p.theme.subText};
  &.focus-visible {
    outline: none;
    box-shadow: ${p => p.theme.blue300} 0 2px 0;
  }
`;
const LogoLink = (0, styled_1.default)(props => (<externalLink_1.default href="https://sentry.io/welcome/" tabIndex={-1} {...props}>
    <icons_1.IconSentry size="xl"/>
  </externalLink_1.default>)) `
  color: ${p => p.theme.subText};
  display: block;
  width: 32px;
  height: 32px;
  margin: 0 auto;
`;
const Build = (0, styled_1.default)('span') `
  font-size: ${p => p.theme.fontSizeRelativeSmall};
  color: ${p => p.theme.subText};
  font-weight: bold;
  margin-left: ${(0, space_1.default)(1)};
`;
const Footer = (0, styled_1.default)(BaseFooter) `
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  color: ${p => p.theme.subText};
  border-top: 1px solid ${p => p.theme.border};
  padding: ${(0, space_1.default)(4)};
  margin-top: 20px;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: none;
  }
`;
exports.default = Footer;
//# sourceMappingURL=footer.jsx.map