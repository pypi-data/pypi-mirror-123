Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const marked_1 = require("app/utils/marked");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
const defaultProps = {
    /**
     * Text used for the 'add' button. An empty string can be used
     * to just render the "+" icon.
     */
    addButtonText: (0, locale_1.t)('Add Item'),
    /**
     * Automatically save even if fields are empty
     */
    allowEmpty: false,
};
class TableField extends React.Component {
    constructor() {
        super(...arguments);
        this.hasValue = value => (0, utils_1.defined)(value) && !(0, utils_1.objectIsEmpty)(value);
        this.renderField = (props) => {
            const { onChange, onBlur, addButtonText, columnLabels, columnKeys, disabled: rawDisabled, allowEmpty, confirmDeleteMessage, } = props;
            const mappedKeys = columnKeys || [];
            const emptyValue = mappedKeys.reduce((a, v) => (Object.assign(Object.assign({}, a), { [v]: null })), { id: '' });
            const valueIsEmpty = this.hasValue(props.value);
            const value = valueIsEmpty ? props.value : [];
            const saveChanges = (nextValue) => {
                onChange === null || onChange === void 0 ? void 0 : onChange(nextValue, []);
                // nextValue is an array of ObservableObjectAdministration objects
                const validValues = !(0, flatten_1.default)(Object.values(nextValue).map(Object.entries)).some(([key, val]) => key !== 'id' && !val // don't allow empty values except if it's the ID field
                );
                if (allowEmpty || validValues) {
                    // TOOD: add debouncing or use a form save button
                    onBlur === null || onBlur === void 0 ? void 0 : onBlur(nextValue, []);
                }
            };
            const addRow = () => {
                saveChanges([...value, emptyValue]);
            };
            const removeRow = rowIndex => {
                const newValue = [...value];
                newValue.splice(rowIndex, 1);
                saveChanges(newValue);
            };
            const setValue = (rowIndex, fieldKey, fieldValue) => {
                const newValue = [...value];
                newValue[rowIndex][fieldKey] = fieldValue.currentTarget
                    ? fieldValue.currentTarget.value
                    : null;
                saveChanges(newValue);
            };
            // should not be a function for this component
            const disabled = typeof rawDisabled === 'function' ? false : rawDisabled;
            const button = (<button_1.default icon={<icons_1.IconAdd size="xs" isCircled/>} onClick={addRow} size="xsmall" disabled={disabled}>
        {addButtonText}
      </button_1.default>);
            // The field will be set to inline when there is no value set for the
            // field, just show the button.
            if (!valueIsEmpty) {
                return <div>{button}</div>;
            }
            const renderConfirmMessage = () => {
                return (<React.Fragment>
          <alert_1.default type="error">
            <span dangerouslySetInnerHTML={{
                        __html: (0, marked_1.singleLineRenderer)(confirmDeleteMessage || (0, locale_1.t)('Are you sure you want to delete this item?')),
                    }}/>
          </alert_1.default>
        </React.Fragment>);
            };
            return (<React.Fragment>
        <HeaderContainer>
          {mappedKeys.map((fieldKey, i) => (<Header key={fieldKey}>
              <HeaderLabel>{columnLabels === null || columnLabels === void 0 ? void 0 : columnLabels[fieldKey]}</HeaderLabel>
              {i === mappedKeys.length - 1 && button}
            </Header>))}
        </HeaderContainer>
        {value.map((row, rowIndex) => (<RowContainer data-test-id="field-row" key={rowIndex}>
            {mappedKeys.map((fieldKey, i) => (<Row key={fieldKey}>
                <RowInput>
                  <input_1.default onChange={v => setValue(rowIndex, fieldKey, v)} value={!(0, utils_1.defined)(row[fieldKey]) ? '' : row[fieldKey]}/>
                </RowInput>
                {i === mappedKeys.length - 1 && (<confirm_1.default priority="danger" disabled={disabled} onConfirm={() => removeRow(rowIndex)} message={renderConfirmMessage()}>
                    <RemoveButton>
                      <button_1.default icon={<icons_1.IconDelete />} size="small" disabled={disabled} label={(0, locale_1.t)('delete')}/>
                    </RemoveButton>
                  </confirm_1.default>)}
              </Row>))}
          </RowContainer>))}
      </React.Fragment>);
        };
    }
    render() {
        // We need formatMessageValue=false since we're saving an object
        // and there isn't a great way to render the
        // change within the toast. Just turn off displaying the from/to portion of
        // the message
        return (<inputField_1.default {...this.props} formatMessageValue={false} inline={({ model }) => !this.hasValue(model.getValue(this.props.name))} field={this.renderField}/>);
    }
}
exports.default = TableField;
TableField.defaultProps = defaultProps;
const HeaderLabel = (0, styled_1.default)('div') `
  font-size: 0.8em;
  text-transform: uppercase;
  color: ${p => p.theme.subText};
`;
const HeaderContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const Header = (0, styled_1.default)('div') `
  display: flex;
  flex: 1 0 0;
  align-items: center;
  justify-content: space-between;
`;
const RowContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-top: ${(0, space_1.default)(1)};
`;
const Row = (0, styled_1.default)('div') `
  display: flex;
  flex: 1 0 0;
  align-items: center;
  margin-top: ${(0, space_1.default)(1)};
`;
const RowInput = (0, styled_1.default)('div') `
  flex: 1;
  margin-right: ${(0, space_1.default)(1)};
`;
const RemoveButton = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=tableField.jsx.map