Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const numberDragControl_1 = (0, tslib_1.__importDefault)(require("app/components/numberDragControl"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/views/alerts/incidentRules/types");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
class ThresholdControl extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            currentValue: null,
        };
        this.handleThresholdChange = (e) => {
            const { value } = e.target;
            // Only allow number and partial number inputs
            if (!/^[0-9]*\.?[0-9]*$/.test(value)) {
                return;
            }
            const { onChange, thresholdType } = this.props;
            // Empty input
            if (value === '') {
                this.setState({ currentValue: null });
                onChange({ thresholdType, threshold: '' }, e);
                return;
            }
            // Only call onChange if the new number is valid, and not partially typed
            // (eg writing out the decimal '5.')
            if (/\.+0*$/.test(value)) {
                this.setState({ currentValue: value });
                return;
            }
            const numberValue = Number(value);
            this.setState({ currentValue: null });
            onChange({ thresholdType, threshold: numberValue }, e);
        };
        /**
         * Coerce the currentValue to a number and trigger the onChange.
         */
        this.handleThresholdBlur = (e) => {
            if (this.state.currentValue === null) {
                return;
            }
            const { onChange, thresholdType } = this.props;
            onChange({ thresholdType, threshold: Number(this.state.currentValue) }, e);
            this.setState({ currentValue: null });
        };
        this.handleTypeChange = ({ value }) => {
            const { onThresholdTypeChange } = this.props;
            onThresholdTypeChange(value);
        };
        this.handleDragChange = (delta, e) => {
            const { onChange, thresholdType, threshold } = this.props;
            const currentValue = threshold || 0;
            onChange({ thresholdType, threshold: currentValue + delta }, e);
        };
    }
    render() {
        var _a;
        const { currentValue } = this.state;
        const _b = this.props, { thresholdType, comparisonType, threshold, placeholder, type, onChange: _, onThresholdTypeChange: __, disabled, disableThresholdType } = _b, props = (0, tslib_1.__rest)(_b, ["thresholdType", "comparisonType", "threshold", "placeholder", "type", "onChange", "onThresholdTypeChange", "disabled", "disableThresholdType"]);
        return (<div {...props}>
        <Container comparisonType={comparisonType}>
          <SelectContainer>
            <selectControl_1.default isDisabled={disabled || disableThresholdType} name={`${type}ThresholdType`} value={thresholdType} options={[
                {
                    value: types_1.AlertRuleThresholdType.BELOW,
                    label: comparisonType === types_1.AlertRuleComparisonType.COUNT
                        ? (0, locale_1.t)('Below')
                        : (0, locale_1.t)('Lower than'),
                },
                {
                    value: types_1.AlertRuleThresholdType.ABOVE,
                    label: comparisonType === types_1.AlertRuleComparisonType.COUNT
                        ? (0, locale_1.t)('Above')
                        : (0, locale_1.t)('Higher than'),
                },
            ]} components={disableThresholdType ? { DropdownIndicator: null } : undefined} styles={disableThresholdType
                ? {
                    control: provided => (Object.assign(Object.assign({}, provided), { cursor: 'not-allowed', pointerEvents: 'auto' })),
                }
                : undefined} onChange={this.handleTypeChange}/>
          </SelectContainer>
          <ThresholdContainer comparisonType={comparisonType}>
            <ThresholdInput>
              <StyledInput disabled={disabled} name={`${type}Threshold`} placeholder={placeholder} value={(_a = currentValue !== null && currentValue !== void 0 ? currentValue : threshold) !== null && _a !== void 0 ? _a : ''} onChange={this.handleThresholdChange} onBlur={this.handleThresholdBlur} 
        // Disable lastpass autocomplete
        data-lpignore="true"/>
              <DragContainer>
                <tooltip_1.default title={(0, locale_1.tct)('Drag to adjust threshold[break]You can hold shift to fine tune', {
                break: <br />,
            })}>
                  <numberDragControl_1.default step={5} axis="y" onChange={this.handleDragChange}/>
                </tooltip_1.default>
              </DragContainer>
            </ThresholdInput>
            {comparisonType === types_1.AlertRuleComparisonType.CHANGE && '%'}
          </ThresholdContainer>
        </Container>
      </div>);
    }
}
const Container = (0, styled_1.default)('div') `
  flex: 1;
  display: flex;
  align-items: center;
  flex-direction: ${p => p.comparisonType === types_1.AlertRuleComparisonType.COUNT ? 'row' : 'row-reverse'};
  gap: ${p => (p.comparisonType === types_1.AlertRuleComparisonType.COUNT ? (0, space_1.default)(1) : (0, space_1.default)(2))};
`;
const SelectContainer = (0, styled_1.default)('div') `
  flex: 1;
`;
const ThresholdContainer = (0, styled_1.default)('div') `
  flex: ${p => (p.comparisonType === types_1.AlertRuleComparisonType.COUNT ? '3' : '2')};
  display: flex;
  flex-direction: row;
  align-items: center;
`;
const StyledInput = (0, styled_1.default)(input_1.default) `
  /* Match the height of the select controls */
  height: 40px;
`;
const ThresholdInput = (0, styled_1.default)('div') `
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-right: ${(0, space_1.default)(1)};
`;
const DragContainer = (0, styled_1.default)('div') `
  position: absolute;
  top: 4px;
  right: 12px;
`;
exports.default = (0, styled_1.default)(ThresholdControl) `
  display: flex;
  flex-direction: row;
  align-items: center;
`;
//# sourceMappingURL=thresholdControl.jsx.map