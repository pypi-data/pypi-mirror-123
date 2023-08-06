Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
function StepThree({ stepThreeData, onSetStepOneData }) {
    return (<react_1.Fragment>
      <alert_1.default type="info">
        {(0, locale_1.tct)('Please enter the iTunes credentials that Sentry should use to download dSYMs from App Store Connect. It is recommended to [docLink:create a new Apple ID] with the "Developer" role for this.', {
            docLink: <externalLink_1.default href="https://support.apple.com/en-us/HT204316"/>,
        })}
      </alert_1.default>
      <field_1.default label={(0, locale_1.t)('Username')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default type="text" name="username" placeholder={(0, locale_1.t)('Username')} value={stepThreeData.username} onChange={e => onSetStepOneData(Object.assign(Object.assign({}, stepThreeData), { username: e.target.value }))}/>
      </field_1.default>
      <field_1.default label={(0, locale_1.t)('Password')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default name="password" type={stepThreeData.password === undefined ? 'text' : 'password'} value={stepThreeData.password} placeholder={stepThreeData.password === undefined
            ? (0, locale_1.t)('(Password unchanged)')
            : (0, locale_1.t)('Password')} onChange={e => onSetStepOneData(Object.assign(Object.assign({}, stepThreeData), { password: e.target.value }))}/>
      </field_1.default>
    </react_1.Fragment>);
}
exports.default = StepThree;
//# sourceMappingURL=stepThree.jsx.map