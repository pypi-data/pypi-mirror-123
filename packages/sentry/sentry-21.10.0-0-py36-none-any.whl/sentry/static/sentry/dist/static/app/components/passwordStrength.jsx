Object.defineProperty(exports, "__esModule", { value: true });
exports.attachTo = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const throttle_1 = (0, tslib_1.__importDefault)(require("lodash/throttle"));
const zxcvbn_1 = (0, tslib_1.__importDefault)(require("zxcvbn"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
/**
 * NOTE: Do not import this component synchronously. The zxcvbn library is
 * relatively large. This component should be loaded async as a split chunk.
 */
/**
 * The maximum score that zxcvbn reports
 */
const MAX_SCORE = 5;
const PasswordStrength = ({ value, labels = ['Very Weak', 'Very Weak', 'Weak', 'Strong', 'Very Strong'], colors = [theme_1.default.red300, theme_1.default.red300, theme_1.default.yellow300, theme_1.default.green300, theme_1.default.green300], }) => {
    if (value === '') {
        return null;
    }
    const result = (0, zxcvbn_1.default)(value);
    if (!result) {
        return null;
    }
    const { score } = result;
    const percent = Math.round(((score + 1) / MAX_SCORE) * 100);
    const styles = (0, react_2.css) `
    background: ${colors[score]};
    width: ${percent}%;
  `;
    return (<react_1.Fragment>
      <StrengthProgress role="progressbar" aria-valuenow={score} aria-valuemin={0} aria-valuemax={100}>
        <StrengthProgressBar css={styles}/>
      </StrengthProgress>
      <StrengthLabel>
        {(0, locale_1.tct)('Strength: [textScore]', {
            textScore: <ScoreText>{labels[score]}</ScoreText>,
        })}
      </StrengthLabel>
    </react_1.Fragment>);
};
const StrengthProgress = (0, styled_1.default)('div') `
  background: ${theme_1.default.gray200};
  height: 8px;
  border-radius: 2px;
  overflow: hidden;
`;
const StrengthProgressBar = (0, styled_1.default)('div') `
  height: 100%;
`;
const StrengthLabel = (0, styled_1.default)('div') `
  font-size: 0.8em;
  margin-top: ${(0, space_1.default)(0.25)};
  color: ${theme_1.default.gray400};
`;
const ScoreText = (0, styled_1.default)('strong') `
  color: ${p => p.theme.black};
`;
exports.default = PasswordStrength;
/**
 * This is a shim that allows the password strength component to be used
 * outside of our main react application. Mostly useful since all of our
 * registration pages aren't in the react app.
 */
const attachTo = ({ input, element }) => element &&
    input &&
    input.addEventListener('input', (0, throttle_1.default)(e => {
        react_dom_1.default.render(<PasswordStrength value={e.target.value}/>, element);
    }));
exports.attachTo = attachTo;
//# sourceMappingURL=passwordStrength.jsx.map