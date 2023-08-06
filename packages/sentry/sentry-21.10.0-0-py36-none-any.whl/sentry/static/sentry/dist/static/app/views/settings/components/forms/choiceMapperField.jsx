Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
const defaultProps = {
    addButtonText: (0, locale_1.t)('Add Item'),
    perItemMapping: false,
    allowEmpty: false,
};
class ChoiceMapper extends React.Component {
    constructor() {
        super(...arguments);
        this.hasValue = (value) => (0, utils_1.defined)(value) && !(0, utils_1.objectIsEmpty)(value);
        this.renderField = (props) => {
            var _a, _b, _c, _d;
            const { onChange, onBlur, addButtonText, addDropdown, mappedColumnLabel, columnLabels, mappedSelectors, perItemMapping, disabled, allowEmpty, } = props;
            const mappedKeys = Object.keys(columnLabels);
            const emptyValue = mappedKeys.reduce((a, v) => (Object.assign(Object.assign({}, a), { [v]: null })), {});
            const valueIsEmpty = this.hasValue(props.value);
            const value = valueIsEmpty ? props.value : {};
            const saveChanges = (nextValue) => {
                onChange === null || onChange === void 0 ? void 0 : onChange(nextValue, {});
                const validValues = !Object.values(nextValue)
                    .map(o => Object.values(o).find(v => v === null))
                    .includes(null);
                if (allowEmpty || validValues) {
                    onBlur === null || onBlur === void 0 ? void 0 : onBlur();
                }
            };
            const addRow = (data) => {
                saveChanges(Object.assign(Object.assign({}, value), { [data.value]: emptyValue }));
            };
            const removeRow = (itemKey) => {
                // eslint-disable-next-line no-unused-vars
                saveChanges(Object.fromEntries(Object.entries(value).filter(([key, _]) => key !== itemKey)));
            };
            const setValue = (itemKey, fieldKey, fieldValue) => {
                saveChanges(Object.assign(Object.assign({}, value), { [itemKey]: Object.assign(Object.assign({}, value[itemKey]), { [fieldKey]: fieldValue }) }));
            };
            // Remove already added values from the items list
            const selectableValues = (_b = (_a = addDropdown.items) === null || _a === void 0 ? void 0 : _a.filter(i => !value.hasOwnProperty(i.value))) !== null && _b !== void 0 ? _b : [];
            const valueMap = (_d = (_c = addDropdown.items) === null || _c === void 0 ? void 0 : _c.reduce((map, item) => {
                map[item.value] = item.label;
                return map;
            }, {})) !== null && _d !== void 0 ? _d : {};
            const dropdown = (<dropdownAutoComplete_1.default {...addDropdown} alignMenu={valueIsEmpty ? 'right' : 'left'} items={selectableValues} onSelect={addRow} disabled={disabled}>
        {({ isOpen }) => (<dropdownButton_1.default icon={<icons_1.IconAdd size="xs" isCircled/>} isOpen={isOpen} size="xsmall" disabled={disabled}>
            {addButtonText}
          </dropdownButton_1.default>)}
      </dropdownAutoComplete_1.default>);
            // The field will be set to inline when there is no value set for the
            // field, just show the dropdown.
            if (!valueIsEmpty) {
                return <div>{dropdown}</div>;
            }
            return (<React.Fragment>
        <Header>
          <LabelColumn>
            <HeadingItem>{mappedColumnLabel}</HeadingItem>
          </LabelColumn>
          {mappedKeys.map((fieldKey, i) => (<Heading key={fieldKey}>
              <HeadingItem>{columnLabels[fieldKey]}</HeadingItem>
              {i === mappedKeys.length - 1 && dropdown}
            </Heading>))}
        </Header>
        {Object.keys(value).map(itemKey => (<Row key={itemKey}>
            <LabelColumn>{valueMap[itemKey]}</LabelColumn>
            {mappedKeys.map((fieldKey, i) => (<Column key={fieldKey}>
                <Control>
                  <selectControl_1.default {...(perItemMapping
                        ? mappedSelectors[itemKey][fieldKey]
                        : mappedSelectors[fieldKey])} height={30} disabled={disabled} onChange={v => setValue(itemKey, fieldKey, v ? v.value : null)} value={value[itemKey][fieldKey]}/>
                </Control>
                {i === mappedKeys.length - 1 && (<Actions>
                    <button_1.default icon={<icons_1.IconDelete />} size="small" disabled={disabled} onClick={() => removeRow(itemKey)}/>
                  </Actions>)}
              </Column>))}
          </Row>))}
      </React.Fragment>);
        };
    }
    render() {
        return (<inputField_1.default {...this.props} inline={({ model }) => !this.hasValue(model.getValue(this.props.name))} field={this.renderField}/>);
    }
}
exports.default = ChoiceMapper;
ChoiceMapper.defaultProps = defaultProps;
const Header = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const Heading = (0, styled_1.default)('div') `
  display: flex;
  margin-left: ${(0, space_1.default)(1)};
  flex: 1 0 0;
  align-items: center;
  justify-content: space-between;
`;
const Row = (0, styled_1.default)('div') `
  display: flex;
  margin-top: ${(0, space_1.default)(1)};
  align-items: center;
`;
const Column = (0, styled_1.default)('div') `
  display: flex;
  margin-left: ${(0, space_1.default)(1)};
  align-items: center;
  flex: 1 0 0;
`;
const Control = (0, styled_1.default)('div') `
  flex: 1;
`;
const LabelColumn = (0, styled_1.default)('div') `
  flex: 0 0 200px;
`;
const HeadingItem = (0, styled_1.default)('div') `
  font-size: 0.8em;
  text-transform: uppercase;
  color: ${p => p.theme.subText};
`;
const Actions = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=choiceMapperField.jsx.map