Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alerts_empty_state_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/alerts-empty-state.svg"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const onboardingPanel_1 = (0, tslib_1.__importDefault)(require("app/components/onboardingPanel"));
const locale_1 = require("app/locale");
function Onboarding({ actions }) {
    return (<onboardingPanel_1.default image={<AlertsImage src={alerts_empty_state_svg_1.default}/>}>
      <h3>{(0, locale_1.t)('More signal, less noise')}</h3>
      <p>
        {(0, locale_1.t)('Not every error is worth an email. Set your own rules for alerts you need, with information that helps.')}
      </p>
      <ButtonList gap={1}>{actions}</ButtonList>
    </onboardingPanel_1.default>);
}
const AlertsImage = (0, styled_1.default)('img') `
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    user-select: none;
    position: absolute;
    top: 0;
    bottom: 0;
    width: 220px;
    margin-top: auto;
    margin-bottom: auto;
    transform: translateX(-50%);
    left: 50%;
  }

  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    transform: translateX(-60%);
    width: 280px;
  }

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    transform: translateX(-75%);
    width: 320px;
  }
`;
const ButtonList = (0, styled_1.default)(buttonBar_1.default) `
  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));
`;
exports.default = Onboarding;
//# sourceMappingURL=onboarding.jsx.map