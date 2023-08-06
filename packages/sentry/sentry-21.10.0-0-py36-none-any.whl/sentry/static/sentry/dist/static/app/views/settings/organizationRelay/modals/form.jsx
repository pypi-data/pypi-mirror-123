Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const textarea_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/textarea"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const fieldHelp_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldHelp"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const Form = ({ values, onChange, errors, onValidate, isFormValid, disables, onValidateKey, onSave, }) => {
    const handleChange = (field) => (event) => {
        onChange(field, event.target.value);
    };
    const handleSubmit = () => {
        if (isFormValid) {
            onSave();
        }
    };
    // code below copied from app/views/organizationIntegrations/SplitInstallationIdModal.tsx
    // TODO: fix the common method selectText
    const onCopy = (value) => () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () { 
    // This hack is needed because the normal copying methods with TextCopyInput do not work correctly
    return yield navigator.clipboard.writeText(value); });
    return (<form onSubmit={handleSubmit} id="relay-form">
      <field_1.default flexibleControlStateSize label={(0, locale_1.t)('Display Name')} error={errors.name} inline={false} stacked required>
        <input_1.default type="text" name="name" placeholder={(0, locale_1.t)('Display Name')} onChange={handleChange('name')} value={values.name} onBlur={onValidate('name')} disabled={disables.name}/>
      </field_1.default>

      {disables.publicKey ? (<field_1.default flexibleControlStateSize label={(0, locale_1.t)('Public Key')} inline={false} stacked>
          <textCopyInput_1.default onCopy={onCopy(values.publicKey)}>
            {values.publicKey}
          </textCopyInput_1.default>
        </field_1.default>) : (<FieldWrapper>
          <StyledField label={(0, locale_1.t)('Public Key')} error={errors.publicKey} flexibleControlStateSize inline={false} stacked required>
            <input_1.default type="text" name="publicKey" placeholder={(0, locale_1.t)('Public Key')} onChange={handleChange('publicKey')} value={values.publicKey} onBlur={onValidateKey}/>
          </StyledField>
          <fieldHelp_1.default>
            {(0, locale_1.t)('Only enter the Public Key value from your credentials file. Never share the Secret key with Sentry or any third party')}
          </fieldHelp_1.default>
        </FieldWrapper>)}
      <field_1.default flexibleControlStateSize label={(0, locale_1.t)('Description')} inline={false} stacked>
        <textarea_1.default name="description" placeholder={(0, locale_1.t)('Description')} onChange={handleChange('description')} value={values.description} disabled={disables.description} autosize/>
      </field_1.default>
    </form>);
};
exports.default = Form;
const FieldWrapper = (0, styled_1.default)('div') `
  padding-bottom: ${(0, space_1.default)(2)};
`;
const StyledField = (0, styled_1.default)(field_1.default) `
  padding-bottom: 0;
`;
//# sourceMappingURL=form.jsx.map