Object.defineProperty(exports, "__esModule", { value: true });
exports.QueryField = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_select_1 = require("react-select");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const cloneDeep_1 = (0, tslib_1.__importDefault)(require("lodash/cloneDeep"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const animations_1 = require("app/styles/animations");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fields_1 = require("app/utils/discover/fields");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const arithmeticInput_1 = (0, tslib_1.__importDefault)(require("./arithmeticInput"));
const types_1 = require("./types");
class QueryField extends React.Component {
    constructor() {
        super(...arguments);
        this.FieldSelectComponents = {
            Option: (_a) => {
                var { label, data } = _a, props = (0, tslib_1.__rest)(_a, ["label", "data"]);
                return (<react_select_1.components.Option label={label} data={data} {...props}>
          <span data-test-id="label">{label}</span>
          {data.value && this.renderTag(data.value.kind, label)}
        </react_select_1.components.Option>);
            },
            SingleValue: (_a) => {
                var { data } = _a, props = (0, tslib_1.__rest)(_a, ["data"]);
                return (<react_select_1.components.SingleValue data={data} {...props}>
          <span data-test-id="label">{data.label}</span>
          {data.value && this.renderTag(data.value.kind, data.label)}
        </react_select_1.components.SingleValue>);
            },
        };
        this.FieldSelectStyles = {
            singleValue(provided) {
                const custom = {
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    width: 'calc(100% - 10px)',
                };
                return Object.assign(Object.assign({}, provided), custom);
            },
            option(provided) {
                const custom = {
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    width: '100%',
                };
                return Object.assign(Object.assign({}, provided), custom);
            },
        };
        this.handleFieldChange = (selected) => {
            if (!selected) {
                return;
            }
            const { value } = selected;
            const current = this.props.fieldValue;
            let fieldValue = (0, cloneDeep_1.default)(this.props.fieldValue);
            switch (value.kind) {
                case types_1.FieldValueKind.TAG:
                case types_1.FieldValueKind.MEASUREMENT:
                case types_1.FieldValueKind.BREAKDOWN:
                case types_1.FieldValueKind.FIELD:
                    fieldValue = { kind: 'field', field: value.meta.name };
                    break;
                case types_1.FieldValueKind.FUNCTION:
                    if (current.kind === 'field') {
                        fieldValue = {
                            kind: 'function',
                            function: [value.meta.name, '', undefined, undefined],
                        };
                    }
                    else if (current.kind === 'function') {
                        fieldValue = {
                            kind: 'function',
                            function: [
                                value.meta.name,
                                current.function[1],
                                current.function[2],
                                current.function[3],
                            ],
                        };
                    }
                    break;
                default:
                    throw new Error('Invalid field type found in column picker');
            }
            if (value.kind === types_1.FieldValueKind.FUNCTION) {
                value.meta.parameters.forEach((param, i) => {
                    if (fieldValue.kind !== 'function') {
                        return;
                    }
                    if (param.kind === 'column') {
                        const field = this.getFieldOrTagOrMeasurementValue(fieldValue.function[i + 1]);
                        if (field === null) {
                            fieldValue.function[i + 1] = param.defaultValue || '';
                        }
                        else if ((field.kind === types_1.FieldValueKind.FIELD ||
                            field.kind === types_1.FieldValueKind.TAG ||
                            field.kind === types_1.FieldValueKind.MEASUREMENT ||
                            field.kind === types_1.FieldValueKind.BREAKDOWN) &&
                            validateColumnTypes(param.columnTypes, field)) {
                            // New function accepts current field.
                            fieldValue.function[i + 1] = field.meta.name;
                        }
                        else {
                            // field does not fit within new function requirements, use the default.
                            fieldValue.function[i + 1] = param.defaultValue || '';
                            fieldValue.function[i + 2] = undefined;
                            fieldValue.function[i + 3] = undefined;
                        }
                    }
                    else {
                        fieldValue.function[i + 1] = param.defaultValue || '';
                    }
                });
                if (fieldValue.kind === 'function') {
                    if (value.meta.parameters.length === 0) {
                        fieldValue.function = [fieldValue.function[0], '', undefined, undefined];
                    }
                    else if (value.meta.parameters.length === 1) {
                        fieldValue.function[2] = undefined;
                        fieldValue.function[3] = undefined;
                    }
                    else if (value.meta.parameters.length === 2) {
                        fieldValue.function[3] = undefined;
                    }
                }
            }
            this.triggerChange(fieldValue);
        };
        this.handleEquationChange = (value) => {
            const newColumn = (0, cloneDeep_1.default)(this.props.fieldValue);
            if (newColumn.kind === types_1.FieldValueKind.EQUATION) {
                newColumn.field = value;
            }
            this.triggerChange(newColumn);
        };
        this.handleFieldParameterChange = ({ value }) => {
            const newColumn = (0, cloneDeep_1.default)(this.props.fieldValue);
            if (newColumn.kind === 'function') {
                newColumn.function[1] = value.meta.name;
            }
            this.triggerChange(newColumn);
        };
        this.handleDropdownParameterChange = (index) => {
            return (value) => {
                const newColumn = (0, cloneDeep_1.default)(this.props.fieldValue);
                if (newColumn.kind === 'function') {
                    newColumn.function[index] = value.value;
                }
                this.triggerChange(newColumn);
            };
        };
        this.handleScalarParameterChange = (index) => {
            return (value) => {
                const newColumn = (0, cloneDeep_1.default)(this.props.fieldValue);
                if (newColumn.kind === 'function') {
                    newColumn.function[index] = value;
                }
                this.triggerChange(newColumn);
            };
        };
    }
    triggerChange(fieldValue) {
        this.props.onChange(fieldValue);
    }
    getFieldOrTagOrMeasurementValue(name) {
        const { fieldOptions } = this.props;
        if (name === undefined) {
            return null;
        }
        const fieldName = `field:${name}`;
        if (fieldOptions[fieldName]) {
            return fieldOptions[fieldName].value;
        }
        const measurementName = `measurement:${name}`;
        if (fieldOptions[measurementName]) {
            return fieldOptions[measurementName].value;
        }
        const spanOperationBreakdownName = `span_op_breakdown:${name}`;
        if (fieldOptions[spanOperationBreakdownName]) {
            return fieldOptions[spanOperationBreakdownName].value;
        }
        const tagName = name.indexOf('tags[') === 0
            ? `tag:${name.replace(/tags\[(.*?)\]/, '$1')}`
            : `tag:${name}`;
        if (fieldOptions[tagName]) {
            return fieldOptions[tagName].value;
        }
        // Likely a tag that was deleted but left behind in a saved query
        // Cook up a tag option so select control works.
        if (name.length > 0) {
            return {
                kind: types_1.FieldValueKind.TAG,
                meta: {
                    name,
                    dataType: 'string',
                    unknown: true,
                },
            };
        }
        return null;
    }
    getFieldData() {
        let field = null;
        const { fieldValue } = this.props;
        let { fieldOptions } = this.props;
        if (fieldValue.kind === 'function') {
            const funcName = `function:${fieldValue.function[0]}`;
            if (fieldOptions[funcName] !== undefined) {
                field = fieldOptions[funcName].value;
            }
        }
        if (fieldValue.kind === 'field') {
            field = this.getFieldOrTagOrMeasurementValue(fieldValue.field);
            fieldOptions = this.appendFieldIfUnknown(fieldOptions, field);
        }
        let parameterDescriptions = [];
        // Generate options and values for each parameter.
        if (field &&
            field.kind === types_1.FieldValueKind.FUNCTION &&
            field.meta.parameters.length > 0 &&
            fieldValue.kind === types_1.FieldValueKind.FUNCTION) {
            parameterDescriptions = field.meta.parameters.map((param, index) => {
                if (param.kind === 'column') {
                    const fieldParameter = this.getFieldOrTagOrMeasurementValue(fieldValue.function[1]);
                    fieldOptions = this.appendFieldIfUnknown(fieldOptions, fieldParameter);
                    return {
                        kind: 'column',
                        value: fieldParameter,
                        required: param.required,
                        options: Object.values(fieldOptions).filter(({ value }) => (value.kind === types_1.FieldValueKind.FIELD ||
                            value.kind === types_1.FieldValueKind.TAG ||
                            value.kind === types_1.FieldValueKind.MEASUREMENT ||
                            value.kind === types_1.FieldValueKind.BREAKDOWN) &&
                            validateColumnTypes(param.columnTypes, value)),
                    };
                }
                else if (param.kind === 'dropdown') {
                    return {
                        kind: 'dropdown',
                        options: param.options,
                        dataType: param.dataType,
                        required: param.required,
                        value: (fieldValue.kind === 'function' && fieldValue.function[index + 1]) ||
                            param.defaultValue ||
                            '',
                    };
                }
                return {
                    kind: 'value',
                    value: (fieldValue.kind === 'function' && fieldValue.function[index + 1]) ||
                        param.defaultValue ||
                        '',
                    dataType: param.dataType,
                    required: param.required,
                    placeholder: param.placeholder,
                };
            });
        }
        return { field, fieldOptions, parameterDescriptions };
    }
    appendFieldIfUnknown(fieldOptions, field) {
        if (!field) {
            return fieldOptions;
        }
        if (field && field.kind === types_1.FieldValueKind.TAG && field.meta.unknown) {
            // Clone the options so we don't mutate other rows.
            fieldOptions = Object.assign({}, fieldOptions);
            fieldOptions[field.meta.name] = { label: field.meta.name, value: field };
        }
        return fieldOptions;
    }
    renderParameterInputs(parameters) {
        const { disabled, inFieldLabels, filterAggregateParameters, hideParameterSelector } = this.props;
        const inputs = parameters.map((descriptor, index) => {
            if (descriptor.kind === 'column' && descriptor.options.length > 0) {
                if (hideParameterSelector) {
                    return null;
                }
                const aggregateParameters = filterAggregateParameters
                    ? descriptor.options.filter(filterAggregateParameters)
                    : descriptor.options;
                return (<selectControl_1.default key="select" name="parameter" placeholder={(0, locale_1.t)('Select value')} options={aggregateParameters} value={descriptor.value} required={descriptor.required} onChange={this.handleFieldParameterChange} inFieldLabel={inFieldLabels ? (0, locale_1.t)('Parameter: ') : undefined} disabled={disabled} styles={!inFieldLabels ? this.FieldSelectStyles : undefined} components={this.FieldSelectComponents}/>);
            }
            if (descriptor.kind === 'value') {
                const inputProps = {
                    required: descriptor.required,
                    value: descriptor.value,
                    onUpdate: this.handleScalarParameterChange(index + 1),
                    placeholder: descriptor.placeholder,
                    disabled,
                };
                switch (descriptor.dataType) {
                    case 'number':
                        return (<BufferedInput name="refinement" key="parameter:number" type="text" inputMode="numeric" pattern="[0-9]*(\.[0-9]*)?" {...inputProps}/>);
                    case 'integer':
                        return (<BufferedInput name="refinement" key="parameter:integer" type="text" inputMode="numeric" pattern="[0-9]*" {...inputProps}/>);
                    default:
                        return (<BufferedInput name="refinement" key="parameter:text" type="text" {...inputProps}/>);
                }
            }
            if (descriptor.kind === 'dropdown') {
                return (<selectControl_1.default key="dropdown" name="dropdown" placeholder={(0, locale_1.t)('Select value')} options={descriptor.options} value={descriptor.value} required={descriptor.required} onChange={this.handleDropdownParameterChange(index + 1)} inFieldLabel={inFieldLabels ? (0, locale_1.t)('Parameter: ') : undefined} disabled={disabled}/>);
            }
            throw new Error(`Unknown parameter type encountered for ${this.props.fieldValue}`);
        });
        // Add enough disabled inputs to fill the grid up.
        // We always have 1 input.
        const { gridColumns } = this.props;
        const requiredInputs = (gridColumns !== null && gridColumns !== void 0 ? gridColumns : inputs.length + 1) - inputs.length - 1;
        if (gridColumns !== undefined && requiredInputs > 0) {
            for (let i = 0; i < requiredInputs; i++) {
                inputs.push(<BlankSpace key={i}/>);
            }
        }
        return inputs;
    }
    renderTag(kind, label) {
        const { shouldRenderTag } = this.props;
        if (shouldRenderTag === false) {
            return null;
        }
        let text, tagType;
        switch (kind) {
            case types_1.FieldValueKind.FUNCTION:
                text = 'f(x)';
                tagType = 'success';
                break;
            case types_1.FieldValueKind.MEASUREMENT:
                text = 'measure';
                tagType = 'info';
                break;
            case types_1.FieldValueKind.BREAKDOWN:
                text = 'breakdown';
                tagType = 'error';
                break;
            case types_1.FieldValueKind.TAG:
                text = kind;
                tagType = 'warning';
                break;
            case types_1.FieldValueKind.FIELD:
                text = fields_1.DEPRECATED_FIELDS.includes(label) ? 'deprecated' : kind;
                tagType = 'highlight';
                break;
            default:
                text = kind;
        }
        return <tag_1.default type={tagType}>{text}</tag_1.default>;
    }
    render() {
        const { className, takeFocus, filterPrimaryOptions, fieldValue, inFieldLabels, disabled, error, hidePrimarySelector, gridColumns, otherColumns, } = this.props;
        const { field, fieldOptions, parameterDescriptions } = this.getFieldData();
        const allFieldOptions = filterPrimaryOptions
            ? Object.values(fieldOptions).filter(filterPrimaryOptions)
            : Object.values(fieldOptions);
        const selectProps = {
            name: 'field',
            options: Object.values(allFieldOptions),
            placeholder: (0, locale_1.t)('(Required)'),
            value: field,
            onChange: this.handleFieldChange,
            inFieldLabel: inFieldLabels ? (0, locale_1.t)('Function: ') : undefined,
            disabled,
        };
        if (takeFocus && field === null) {
            selectProps.autoFocus = true;
        }
        const parameters = this.renderParameterInputs(parameterDescriptions);
        if (fieldValue.kind === types_1.FieldValueKind.EQUATION) {
            return (<Container className={className} gridColumns={1} tripleLayout={false} error={error !== undefined}>
          <arithmeticInput_1.default name="arithmetic" key="parameter:text" type="text" required value={fieldValue.field} onUpdate={this.handleEquationChange} options={otherColumns}/>
          {error ? (<ArithmeticError title={error}>
              <icons_1.IconWarning color="red300"/>
            </ArithmeticError>) : null}
        </Container>);
        }
        // if there's more than 2 parameters, set gridColumns to 2 so they go onto the next line instead
        const containerColumns = parameters.length > 2 ? 2 : gridColumns ? gridColumns : parameters.length + 1;
        return (<Container className={className} gridColumns={containerColumns} tripleLayout={gridColumns === 3 && parameters.length > 2}>
        {!hidePrimarySelector && (<selectControl_1.default {...selectProps} styles={!inFieldLabels ? this.FieldSelectStyles : undefined} components={this.FieldSelectComponents}/>)}
        {parameters}
      </Container>);
    }
}
exports.QueryField = QueryField;
function validateColumnTypes(columnTypes, input) {
    if (typeof columnTypes === 'function') {
        return columnTypes({ name: input.meta.name, dataType: input.meta.dataType });
    }
    return columnTypes.includes(input.meta.dataType);
}
const Container = (0, styled_1.default)('div') `
  display: grid;
  ${p => p.tripleLayout
    ? `grid-template-columns: 1fr 2fr;`
    : `grid-template-columns: repeat(${p.gridColumns}, 1fr) ${p.error ? 'auto' : ''};`}
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;

  flex-grow: 1;
`;
/**
 * Because controlled inputs fire onChange on every key stroke,
 * we can't update the QueryField that often as it would re-render
 * the input elements causing focus to be lost.
 *
 * Using a buffered input lets us throttle rendering and enforce data
 * constraints better.
 */
class BufferedInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: this.props.value,
        };
        this.handleBlur = () => {
            if (this.isValid) {
                this.props.onUpdate(this.state.value);
            }
            else {
                this.setState({ value: this.props.value });
            }
        };
        this.handleChange = (event) => {
            if (this.isValid) {
                this.setState({ value: event.target.value });
            }
        };
        this.input = React.createRef();
    }
    get isValid() {
        if (!this.input.current) {
            return true;
        }
        return this.input.current.validity.valid;
    }
    render() {
        const _a = this.props, { onUpdate: _ } = _a, props = (0, tslib_1.__rest)(_a, ["onUpdate"]);
        return (<StyledInput {...props} ref={this.input} className="form-control" value={this.state.value} onChange={this.handleChange} onBlur={this.handleBlur}/>);
    }
}
// Set a min-width to allow shrinkage in grid.
const StyledInput = (0, styled_1.default)(input_1.default) `
  /* Match the height of the select boxes */
  height: 41px;
  min-width: 50px;
`;
const BlankSpace = (0, styled_1.default)('div') `
  /* Match the height of the select boxes */
  height: 41px;
  min-width: 50px;
  background: ${p => p.theme.backgroundSecondary};
  border-radius: ${p => p.theme.borderRadius};
  display: flex;
  align-items: center;
  justify-content: center;

  &:after {
    font-size: ${p => p.theme.fontSizeMedium};
    content: '${(0, locale_1.t)('No parameter')}';
    color: ${p => p.theme.gray300};
  }
`;
const ArithmeticError = (0, styled_1.default)(tooltip_1.default) `
  color: ${p => p.theme.red300};
  animation: ${() => (0, animations_1.pulse)(1.15)} 1s ease infinite;
  display: flex;
`;
//# sourceMappingURL=queryField.jsx.map