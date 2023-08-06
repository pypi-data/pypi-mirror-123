Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fieldDescription_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldDescription"));
const fieldHelp_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldHelp"));
const fieldLabel_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldLabel"));
const fieldRequiredBadge_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldRequiredBadge"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
function CheckboxField(props) {
    const { name, disabled, stacked, id, required, label, help } = props;
    const helpElement = typeof help === 'function' ? help(props) : help;
    return (<formField_1.default name={name} inline={false} stacked={stacked}>
      {({ onChange, value }) => {
            function handleChange(e) {
                const newValue = e.target.checked;
                onChange === null || onChange === void 0 ? void 0 : onChange(newValue, e);
            }
            return (<FieldLayout>
            <ControlWrapper>
              <checkbox_1.default id={id} name={name} disabled={disabled} checked={value === true} onChange={handleChange}/>
            </ControlWrapper>
            <fieldDescription_1.default htmlFor={id}>
              {label && (<fieldLabel_1.default disabled={disabled}>
                  <span>
                    {label}
                    {required && <fieldRequiredBadge_1.default />}
                  </span>
                </fieldLabel_1.default>)}
              {helpElement && (<fieldHelp_1.default stacked={stacked} inline>
                  {helpElement}
                </fieldHelp_1.default>)}
            </fieldDescription_1.default>
          </FieldLayout>);
        }}
    </formField_1.default>);
}
const ControlWrapper = (0, styled_1.default)('span') `
  align-self: flex-start;
  display: flex;
  margin-right: ${(0, space_1.default)(1)};

  & input {
    margin: 0;
  }
`;
const FieldLayout = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
`;
exports.default = CheckboxField;
//# sourceMappingURL=checkboxField.jsx.map