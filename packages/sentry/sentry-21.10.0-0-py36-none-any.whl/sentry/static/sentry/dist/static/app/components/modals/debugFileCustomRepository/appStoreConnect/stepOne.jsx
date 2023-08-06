Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const textarea_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/textarea"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
function StepOne({ stepOneData, onSetStepOneData }) {
    return (<react_1.Fragment>
      <alert_1.default type="info">
        {(0, locale_1.tct)('Please enter the [docLink:App Store Connect API Key] details. The key needs to have the "Developer" role for Sentry to discover the app builds.', {
            docLink: (<externalLink_1.default href="https://developer.apple.com/documentation/appstoreconnectapi/creating_api_keys_for_app_store_connect_api"/>),
        })}
      </alert_1.default>
      <field_1.default label={(0, locale_1.t)('Issuer')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default type="text" name="issuer" placeholder={(0, locale_1.t)('Issuer')} value={stepOneData.issuer} onChange={e => onSetStepOneData(Object.assign(Object.assign({}, stepOneData), { issuer: e.target.value }))}/>
      </field_1.default>
      <field_1.default label={(0, locale_1.t)('Key ID')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default type="text" name="keyId" placeholder={(0, locale_1.t)('Key Id')} value={stepOneData.keyId} onChange={e => onSetStepOneData(Object.assign(Object.assign({}, stepOneData), { keyId: e.target.value }))}/>
      </field_1.default>
      <field_1.default label={(0, locale_1.t)('Private Key')} inline={false} flexibleControlStateSize stacked required>
        <textarea_1.default name="privateKey" value={stepOneData.privateKey} rows={5} autosize placeholder={stepOneData.privateKey === undefined
            ? (0, locale_1.t)('(Private Key unchanged)')
            : '-----BEGIN PRIVATE KEY-----\n[PRIVATE-KEY]\n-----END PRIVATE KEY-----'} onChange={e => onSetStepOneData(Object.assign(Object.assign({}, stepOneData), { privateKey: e.target.value }))}/>
      </field_1.default>
    </react_1.Fragment>);
}
exports.default = StepOne;
//# sourceMappingURL=stepOne.jsx.map