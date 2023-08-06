Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
function StepFour({ onStartItunesAuthentication, onStartSmsAuthentication, stepFourData, onSetStepFourData, }) {
    return (<react_1.Fragment>
      <StyledAlert type="info" icon={<icons_1.IconInfo />}>
        <AlertContent>
          {(0, locale_1.t)('Did not get a verification code?')}
          <buttonBar_1.default gap={1}>
            <button_1.default size="small" title={(0, locale_1.t)('Get a new verification code')} onClick={() => onStartItunesAuthentication(false)} icon={<icons_1.IconRefresh />}>
              {(0, locale_1.t)('Resend code')}
            </button_1.default>
            <button_1.default size="small" title={(0, locale_1.t)('Get a text message with a code')} onClick={() => onStartSmsAuthentication()} icon={<icons_1.IconMobile />}>
              {(0, locale_1.t)('Text me')}
            </button_1.default>
          </buttonBar_1.default>
        </AlertContent>
      </StyledAlert>
      <field_1.default label={(0, locale_1.t)('Two Factor authentication code')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default type="text" name="two-factor-authentication-code" placeholder={(0, locale_1.t)('Enter your code')} value={stepFourData.authenticationCode} onChange={e => onSetStepFourData(Object.assign(Object.assign({}, stepFourData), { authenticationCode: e.target.value }))}/>
      </field_1.default>
    </react_1.Fragment>);
}
exports.default = StepFour;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  div {
    align-items: flex-start;
  }
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    div {
      align-items: center;
    }
  }
`;
const AlertContent = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr;
  align-items: center;
  grid-gap: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 1fr max-content;
  }
`;
//# sourceMappingURL=stepFour.jsx.map