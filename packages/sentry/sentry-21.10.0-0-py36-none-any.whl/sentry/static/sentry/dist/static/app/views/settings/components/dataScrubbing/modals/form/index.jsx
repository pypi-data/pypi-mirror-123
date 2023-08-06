Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const sortBy_1 = (0, tslib_1.__importDefault)(require("lodash/sortBy"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const types_1 = require("../../types");
const utils_1 = require("../../utils");
const eventIdField_1 = (0, tslib_1.__importDefault)(require("./eventIdField"));
const selectField_1 = (0, tslib_1.__importDefault)(require("./selectField"));
const sourceField_1 = (0, tslib_1.__importDefault)(require("./sourceField"));
class Form extends React.Component {
    constructor() {
        var _a;
        super(...arguments);
        this.state = { displayEventId: !!((_a = this.props.eventId) === null || _a === void 0 ? void 0 : _a.value) };
        this.handleChange = (field) => (event) => {
            this.props.onChange(field, event.target.value);
        };
        this.handleToggleEventId = () => {
            this.setState(prevState => ({ displayEventId: !prevState.displayEventId }));
        };
    }
    render() {
        const { values, onChange, errors, onValidate, sourceSuggestions, onUpdateEventId, eventId, } = this.props;
        const { method, type, source } = values;
        const { displayEventId } = this.state;
        return (<React.Fragment>
        <FieldGroup hasTwoColumns={values.method === types_1.MethodType.REPLACE}>
          <field_1.default data-test-id="method-field" label={(0, locale_1.t)('Method')} help={(0, locale_1.t)('What to do')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
            <selectField_1.default placeholder={(0, locale_1.t)('Select method')} name="method" options={(0, sortBy_1.default)(Object.values(types_1.MethodType)).map(value => (Object.assign(Object.assign({}, (0, utils_1.getMethodLabel)(value)), { value })))} value={method} onChange={value => onChange('method', value === null || value === void 0 ? void 0 : value.value)}/>
          </field_1.default>
          {values.method === types_1.MethodType.REPLACE && (<field_1.default data-test-id="placeholder-field" label={(0, locale_1.t)('Custom Placeholder (Optional)')} help={(0, locale_1.t)('It will replace the default placeholder [Filtered]')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
              <input_1.default type="text" name="placeholder" placeholder={`[${(0, locale_1.t)('Filtered')}]`} onChange={this.handleChange('placeholder')} value={values.placeholder}/>
            </field_1.default>)}
        </FieldGroup>
        <FieldGroup hasTwoColumns={values.type === types_1.RuleType.PATTERN}>
          <field_1.default data-test-id="type-field" label={(0, locale_1.t)('Data Type')} help={(0, locale_1.t)('What to look for. Use an existing pattern or define your own using regular expressions.')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
            <selectField_1.default placeholder={(0, locale_1.t)('Select type')} name="type" options={(0, sortBy_1.default)(Object.values(types_1.RuleType)).map(value => ({
                label: (0, utils_1.getRuleLabel)(value),
                value,
            }))} value={type} onChange={value => onChange('type', value === null || value === void 0 ? void 0 : value.value)}/>
          </field_1.default>
          {values.type === types_1.RuleType.PATTERN && (<field_1.default data-test-id="regex-field" label={(0, locale_1.t)('Regex matches')} help={(0, locale_1.t)('Custom regular expression (see documentation)')} inline={false} error={errors === null || errors === void 0 ? void 0 : errors.pattern} flexibleControlStateSize stacked required showHelpInTooltip>
              <RegularExpression type="text" name="pattern" placeholder={(0, locale_1.t)('[a-zA-Z0-9]+')} onChange={this.handleChange('pattern')} value={values.pattern} onBlur={onValidate('pattern')}/>
            </field_1.default>)}
        </FieldGroup>
        <ToggleWrapper>
          {displayEventId ? (<Toggle priority="link" onClick={this.handleToggleEventId}>
              {(0, locale_1.t)('Hide event ID field')}
              <icons_1.IconChevron direction="up" size="xs"/>
            </Toggle>) : (<Toggle priority="link" onClick={this.handleToggleEventId}>
              {(0, locale_1.t)('Use event ID for auto-completion')}
              <icons_1.IconChevron direction="down" size="xs"/>
            </Toggle>)}
        </ToggleWrapper>
        <SourceGroup isExpanded={displayEventId}>
          {displayEventId && (<eventIdField_1.default onUpdateEventId={onUpdateEventId} eventId={eventId}/>)}
          <sourceField_1.default onChange={value => onChange('source', value)} value={source} error={errors === null || errors === void 0 ? void 0 : errors.source} onBlur={onValidate('source')} isRegExMatchesSelected={type === types_1.RuleType.PATTERN} suggestions={sourceSuggestions}/>
        </SourceGroup>
      </React.Fragment>);
    }
}
exports.default = Form;
const FieldGroup = (0, styled_1.default)('div') `
  display: grid;
  margin-bottom: ${(0, space_1.default)(2)};
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-gap: ${(0, space_1.default)(2)};
    ${p => p.hasTwoColumns && `grid-template-columns: 1fr 1fr;`}
    margin-bottom: ${p => (p.hasTwoColumns ? 0 : (0, space_1.default)(2))};
  }
`;
const SourceGroup = (0, styled_1.default)('div') `
  height: 65px;
  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
  transition-property: height;
  ${p => p.isExpanded &&
    `
    border-radius: ${p.theme.borderRadius};
    border: 1px solid ${p.theme.border};
    box-shadow: ${p.theme.dropShadowLight};
    margin: ${(0, space_1.default)(2)} 0 ${(0, space_1.default)(3)} 0;
    padding: ${(0, space_1.default)(2)};
    height: 180px;
  `}
`;
const RegularExpression = (0, styled_1.default)(input_1.default) `
  font-family: ${p => p.theme.text.familyMono};
`;
const ToggleWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
`;
const Toggle = (0, styled_1.default)(button_1.default) `
  font-weight: 700;
  color: ${p => p.theme.subText};
  &:hover,
  &:focus {
    color: ${p => p.theme.textColor};
  }
  > *:first-child {
    display: grid;
    grid-gap: ${(0, space_1.default)(0.5)};
    grid-template-columns: repeat(2, max-content);
    align-items: center;
  }
`;
//# sourceMappingURL=index.jsx.map