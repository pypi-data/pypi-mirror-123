Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const animations_1 = require("app/styles/animations");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const MultipleSelectorSubmitRow = ({ onSubmit, disabled = false }) => (<SubmitButtonContainer>
    <SubmitButton disabled={disabled} onClick={onSubmit} size="xsmall" priority="primary">
      {(0, locale_1.t)('Apply')}
    </SubmitButton>
  </SubmitButtonContainer>);
const SubmitButtonContainer = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
`;
const SubmitButton = (0, styled_1.default)(button_1.default) `
  animation: 0.1s ${animations_1.growIn} ease-in;
  margin: ${(0, space_1.default)(0.5)} 0;
`;
exports.default = MultipleSelectorSubmitRow;
//# sourceMappingURL=multipleSelectorSubmitRow.jsx.map