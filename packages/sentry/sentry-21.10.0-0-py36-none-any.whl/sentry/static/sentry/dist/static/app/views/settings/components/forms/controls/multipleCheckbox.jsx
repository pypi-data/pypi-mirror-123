Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("app/utils");
const MultipleCheckboxWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
`;
const Label = (0, styled_1.default)('label') `
  font-weight: normal;
  white-space: nowrap;
  margin-right: 10px;
  margin-bottom: 10px;
  width: 20%;
`;
const CheckboxLabel = (0, styled_1.default)('span') `
  margin-left: 3px;
`;
class MultipleCheckbox extends React.Component {
    constructor() {
        super(...arguments);
        this.onChange = (selectedValue, e) => {
            const { value, onChange } = this.props;
            let newValue = [];
            if (typeof onChange !== 'function') {
                return;
            }
            if (e.target.checked) {
                newValue = value ? [...value, selectedValue] : [value];
            }
            else {
                newValue = value.filter(v => v !== selectedValue);
            }
            onChange(newValue, e);
        };
    }
    render() {
        const { disabled, choices, value } = this.props;
        return (<MultipleCheckboxWrapper>
        {choices.map(([choiceValue, choiceLabel]) => (<LabelContainer key={choiceValue}>
            <Label>
              <input type="checkbox" value={choiceValue} onChange={this.onChange.bind(this, choiceValue)} disabled={disabled} checked={(0, utils_1.defined)(value) && value.indexOf(choiceValue) !== -1}/>
              <CheckboxLabel>{choiceLabel}</CheckboxLabel>
            </Label>
          </LabelContainer>))}
      </MultipleCheckboxWrapper>);
    }
}
exports.default = MultipleCheckbox;
const LabelContainer = (0, styled_1.default)('div') `
  width: 100%;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    width: 50%;
  }
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    width: 33.333%;
  }
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    width: 25%;
  }
`;
//# sourceMappingURL=multipleCheckbox.jsx.map