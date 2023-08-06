Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const radio_1 = (0, tslib_1.__importDefault)(require("app/components/radio"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const RadioPanelGroup = (_a) => {
    var { value, choices, label, onChange } = _a, props = (0, tslib_1.__rest)(_a, ["value", "choices", "label", "onChange"]);
    return (<Container {...props} role="radiogroup" aria-labelledby={label}>
    {(choices || []).map(([id, name, extraContent], index) => (<RadioPanel key={index}>
        <RadioLineItem role="radio" index={index} aria-checked={value === id}>
          <radio_1.default radioSize="small" aria-label={id} checked={value === id} onChange={(e) => onChange(id, e)}/>
          <div>{name}</div>
          {extraContent}
        </RadioLineItem>
      </RadioPanel>))}
  </Container>);
};
exports.default = RadioPanelGroup;
const Container = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-auto-flow: row;
  grid-auto-rows: max-content;
  grid-auto-columns: auto;
`;
const RadioLineItem = (0, styled_1.default)('label') `
  display: grid;
  grid-gap: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(1)};
  grid-template-columns: max-content auto max-content;
  align-items: center;
  cursor: pointer;
  outline: none;
  font-weight: normal;
  margin: 0;
  color: ${p => p.theme.subText};
  transition: color 0.3s ease-in;
  padding: 0;
  position: relative;

  &:hover,
  &:focus {
    color: ${p => p.theme.textColor};
  }

  svg {
    display: none;
    opacity: 0;
  }

  &[aria-checked='true'] {
    color: ${p => p.theme.textColor};
  }
`;
const RadioPanel = (0, styled_1.default)('div') `
  margin: 0;
`;
//# sourceMappingURL=radioPanelGroup.jsx.map