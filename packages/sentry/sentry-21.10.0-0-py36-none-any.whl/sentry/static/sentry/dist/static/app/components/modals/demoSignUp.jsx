Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const highlightModalContainer_1 = (0, tslib_1.__importDefault)(require("app/components/highlightModalContainer"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const demoMode_1 = require("app/utils/demoMode");
const DemoSignUpModal = ({ closeModal }) => {
    const queryParameter = (0, demoMode_1.emailQueryParameter)();
    const getStartedExtraParameter = (0, demoMode_1.extraQueryParameter)(true);
    const signupUrl = `https://sentry.io/signup/${queryParameter}${getStartedExtraParameter}`;
    return (<highlightModalContainer_1.default>
      <div>
        <TrialCheckInfo>
          <Subheader>{(0, locale_1.t)('Sandbox Signup')}</Subheader>
          <h2>{(0, locale_1.t)('Hey, love what you see?')}</h2>
          <p>
            {(0, locale_1.t)('Sign up now to setup your own project to see problems within your code and learn how to quickly improve your project.')}
          </p>
        </TrialCheckInfo>
        <StyledButtonBar gap={2}>
          <button_1.default priority="primary" href={signupUrl} onClick={() => (0, trackAdvancedAnalyticsEvent_1.default)('growth.demo_modal_clicked_signup', {
            organization: null,
        })}>
            {(0, locale_1.t)('Sign up now')}
          </button_1.default>
          <button_1.default priority="default" onClick={() => {
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.demo_modal_clicked_continue', {
                organization: null,
            });
            closeModal();
        }}>
            {(0, locale_1.t)('Keep Exploring')}
          </button_1.default>
        </StyledButtonBar>
      </div>
    </highlightModalContainer_1.default>);
};
const TrialCheckInfo = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(3)} 0;
  p {
    font-size: ${p => p.theme.fontSizeMedium};
    margin: 0;
  }
  h2 {
    font-size: 1.5em;
  }
`;
exports.modalCss = (0, react_1.css) `
  width: 100%;
  max-width: 730px;
  [role='document'] {
    position: relative;
    padding: 70px 80px;
    overflow: hidden;
  }
`;
const Subheader = (0, styled_1.default)('h4') `
  margin-bottom: ${(0, space_1.default)(2)};
  text-transform: uppercase;
  font-weight: bold;
  color: ${p => p.theme.purple300};
  font-size: ${p => p.theme.fontSizeExtraSmall};
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  margin-top: ${(0, space_1.default)(2)};
  max-width: fit-content;
`;
exports.default = DemoSignUpModal;
//# sourceMappingURL=demoSignUp.jsx.map