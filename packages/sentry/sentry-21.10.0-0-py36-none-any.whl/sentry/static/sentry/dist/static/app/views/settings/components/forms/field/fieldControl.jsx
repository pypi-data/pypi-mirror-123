Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fieldControlState_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldControlState"));
const defaultProps = {
    flexibleControlStateSize: false,
};
const FieldControl = ({ inline, alignRight, disabled, disabledReason, errorState, controlState, children, hideControlState, flexibleControlStateSize = false, }) => (<FieldControlErrorWrapper inline={inline}>
    <FieldControlWrapper>
      <FieldControlStyled alignRight={alignRight}>{children}</FieldControlStyled>

      {disabled && disabledReason && (<DisabledIndicator className="disabled-indicator">
          <StyledQuestionTooltip title={disabledReason} size="sm" position="top"/>
        </DisabledIndicator>)}

      {!hideControlState && (<fieldControlState_1.default flexibleControlStateSize={!!flexibleControlStateSize}>
          {controlState}
        </fieldControlState_1.default>)}
    </FieldControlWrapper>

    {!hideControlState && errorState}
  </FieldControlErrorWrapper>);
exports.default = FieldControl;
// This wraps Control + ControlError message
// * can NOT be a flex box here because of `position: absolute` on "control error message"
// * can NOT have overflow hidden because "control error message" overflows
const FieldControlErrorWrapper = (0, styled_1.default)('div') `
  ${p => (p.inline ? 'width: 50%; padding-left: 10px;' : '')};
  position: relative;
`;
const FieldControlStyled = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  flex-direction: column;
  position: relative;
  max-width: 100%;
  ${p => (p.alignRight ? 'align-items: flex-end;' : '')};
`;
const FieldControlWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-shrink: 0;
`;
const StyledQuestionTooltip = (0, styled_1.default)(questionTooltip_1.default) `
  display: block;
  margin: 0 auto;
`;
const DisabledIndicator = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=fieldControl.jsx.map