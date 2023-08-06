Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const checkboxFancyContent_1 = (0, tslib_1.__importDefault)(require("./checkboxFancyContent"));
const disabledStyles = (p) => p.isDisabled &&
    (0, react_1.css) `
    background: ${p.isChecked || p.isIndeterminate
        ? p.theme.gray200
        : p.theme.backgroundSecondary};
    border-color: ${p.theme.border};
  `;
const hoverStyles = (p) => !p.isDisabled &&
    (0, react_1.css) `
    border: 2px solid
      ${p.isChecked || p.isIndeterminate ? p.theme.active : p.theme.textColor};
  `;
const CheckboxFancy = (0, styled_1.default)(({ isChecked, className, isDisabled, isIndeterminate, onClick }) => (<div data-test-id="checkbox-fancy" role="checkbox" aria-disabled={isDisabled} aria-checked={isIndeterminate ? 'mixed' : isChecked} className={className} onClick={onClick}>
      <checkboxFancyContent_1.default isIndeterminate={isIndeterminate} isChecked={isChecked}/>
    </div>)) `
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 1px 1px 5px 0px rgba(0, 0, 0, 0.05) inset;
  width: ${p => p.size};
  height: ${p => p.size};
  border-radius: 5px;
  background: ${p => (p.isChecked || p.isIndeterminate ? p.theme.active : 'transparent')};
  border: 2px solid
    ${p => (p.isChecked || p.isIndeterminate ? p.theme.active : p.theme.gray300)};
  cursor: ${p => (p.isDisabled ? 'not-allowed' : 'pointer')};
  ${p => (!p.isChecked || !p.isIndeterminate) && 'transition: 500ms border ease-out'};

  &:hover {
    ${hoverStyles}
  }

  ${disabledStyles}
`;
CheckboxFancy.defaultProps = {
    size: '16px',
    isChecked: false,
    isIndeterminate: false,
};
exports.default = CheckboxFancy;
//# sourceMappingURL=checkboxFancy.jsx.map