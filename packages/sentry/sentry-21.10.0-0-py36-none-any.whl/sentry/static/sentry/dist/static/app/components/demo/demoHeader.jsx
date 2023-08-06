Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const logoSentry_1 = (0, tslib_1.__importDefault)(require("app/components/logoSentry"));
const locale_1 = require("app/locale");
const preferencesStore_1 = (0, tslib_1.__importDefault)(require("app/stores/preferencesStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const demoMode_1 = require("app/utils/demoMode");
const getCookie_1 = (0, tslib_1.__importDefault)(require("app/utils/getCookie"));
function DemoHeader() {
    // if the user came from a SaaS org, we should send them back to upgrade when they leave the sandbox
    const saasOrgSlug = (0, getCookie_1.default)('saas_org_slug');
    const queryParameter = (0, demoMode_1.emailQueryParameter)();
    const getStartedExtraParameter = (0, demoMode_1.extraQueryParameter)(true);
    const extraParameter = (0, demoMode_1.extraQueryParameter)(false);
    const getStartedText = saasOrgSlug ? (0, locale_1.t)('Upgrade Now') : (0, locale_1.t)('Sign Up for Free');
    const getStartedUrl = saasOrgSlug
        ? `https://sentry.io/settings/${saasOrgSlug}/billing/checkout/`
        : `https://sentry.io/signup/${queryParameter}${getStartedExtraParameter}`;
    const collapsed = !!(0, useLegacyStore_1.useLegacyStore)(preferencesStore_1.default).collapsed;
    return (<Wrapper collapsed={collapsed}>
      <StyledLogoSentry />
      <buttonBar_1.default gap={4}>
        <StyledExternalLink onClick={() => (0, trackAdvancedAnalyticsEvent_1.default)('growth.demo_click_docs', { organization: null })} href={`https://docs.sentry.io/${extraParameter}`}>
          {(0, locale_1.t)('Documentation')}
        </StyledExternalLink>
        <BaseButton priority="form" onClick={() => (0, trackAdvancedAnalyticsEvent_1.default)('growth.demo_click_request_demo', {
            organization: null,
        })} href={`https://sentry.io/_/demo/${extraParameter}`}>
          {(0, locale_1.t)('Request a Demo')}
        </BaseButton>
        <GetStarted onClick={() => (0, trackAdvancedAnalyticsEvent_1.default)('growth.demo_click_get_started', {
            is_upgrade: !!saasOrgSlug,
            organization: null,
        })} href={getStartedUrl}>
          {getStartedText}
        </GetStarted>
      </buttonBar_1.default>
    </Wrapper>);
}
exports.default = DemoHeader;
// Note many of the colors don't come from the theme as they come from the marketing site
const Wrapper = (0, styled_1.default)('div') `
  padding-right: ${(0, space_1.default)(3)};
  background-color: ${p => p.theme.white};
  height: ${p => p.theme.demo.headerSize};
  display: flex;
  justify-content: space-between;
  text-transform: uppercase;

  margin-left: calc(
    -1 * ${p => (p.collapsed ? p.theme.sidebar.collapsedWidth : p.theme.sidebar.expandedWidth)}
  );

  position: fixed;
  width: 100%;
  border-bottom: 1px solid ${p => p.theme.border};
  z-index: ${p => p.theme.zIndex.settingsSidebarNav};

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    height: ${p => p.theme.sidebar.mobileHeight};
    margin-left: 0;
  }
`;
const StyledLogoSentry = (0, styled_1.default)(logoSentry_1.default) `
  margin-top: auto;
  margin-bottom: auto;
  margin-left: 20px;
  width: 130px;
  height: 30px;
  color: ${p => p.theme.textColor};
`;
const BaseButton = (0, styled_1.default)(button_1.default) `
  border-radius: 2rem;
  text-transform: uppercase;
`;
// Note many of the colors don't come from the theme as they come from the marketing site
const GetStarted = (0, styled_1.default)(BaseButton) `
  border-color: transparent;
  box-shadow: 0 2px 0 rgb(54 45 89 / 10%);
  background-color: #e1567c;
  color: #fff;
`;
const StyledExternalLink = (0, styled_1.default)(externalLink_1.default) `
  color: #584774;
`;
//# sourceMappingURL=demoHeader.jsx.map