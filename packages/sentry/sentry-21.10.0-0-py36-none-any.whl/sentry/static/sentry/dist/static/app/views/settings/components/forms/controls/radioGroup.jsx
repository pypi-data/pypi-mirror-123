Object.defineProperty(exports, "__esModule", { value: true });
exports.RadioLineItem = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const radio_1 = (0, tslib_1.__importDefault)(require("app/components/radio"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Container = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${p => (0, space_1.default)(p.orientInline ? 3 : 1)};
  grid-auto-flow: ${p => (p.orientInline ? 'column' : 'row')};
  grid-auto-rows: max-content;
  grid-auto-columns: max-content;
`;
const RadioGroup = (_a) => {
    var { value, disabled, choices, label, onChange, orientInline } = _a, props = (0, tslib_1.__rest)(_a, ["value", "disabled", "choices", "label", "onChange", "orientInline"]);
    return (<Container orientInline={orientInline} {...props} role="radiogroup" aria-labelledby={label}>
    {(choices || []).map(([id, name, description], index) => (<exports.RadioLineItem key={index} role="radio" index={index} aria-checked={value === id} disabled={disabled}>
        <radio_1.default aria-label={id} disabled={disabled} checked={value === id} onChange={(e) => !disabled && onChange(id, e)}/>
        <RadioLineText disabled={disabled}>{name}</RadioLineText>
        {description && (<React.Fragment>
            {/* If there is a description then we want to have a 2x2 grid so the first column width aligns with Radio Button */}
            <div />
            <Description>{description}</Description>
          </React.Fragment>)}
      </exports.RadioLineItem>))}
  </Container>);
};
const shouldForwardProp = (p) => typeof p === 'string' && !['disabled', 'animate'].includes(p) && (0, is_prop_valid_1.default)(p);
exports.RadioLineItem = (0, styled_1.default)('label', { shouldForwardProp }) `
  display: grid;
  grid-gap: 0.25em 0.5em;
  grid-template-columns: max-content auto;
  align-items: center;
  cursor: ${p => (p.disabled ? 'default' : 'pointer')};
  outline: none;
  font-weight: normal;
  margin: 0;
`;
const RadioLineText = (0, styled_1.default)('div', { shouldForwardProp }) `
  opacity: ${p => (p.disabled ? 0.4 : null)};
`;
const Description = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeRelativeSmall};
  line-height: 1.4em;
`;
exports.default = RadioGroup;
//# sourceMappingURL=radioGroup.jsx.map