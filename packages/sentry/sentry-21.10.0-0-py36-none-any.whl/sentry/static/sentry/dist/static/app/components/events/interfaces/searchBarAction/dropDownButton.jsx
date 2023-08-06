Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function DropDownButton({ isOpen, getActorProps, checkedQuantity }) {
    if (checkedQuantity > 0) {
        return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} size="small" hideBottomBorder={false} priority="primary">
        {(0, locale_1.tn)('%s Active Filter', '%s Active Filters', checkedQuantity)}
      </StyledDropdownButton>);
    }
    return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} size="small" hideBottomBorder={false}>
      {(0, locale_1.t)('Filter By')}
    </StyledDropdownButton>);
}
exports.default = DropDownButton;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  z-index: ${p => p.theme.zIndex.dropdownAutocomplete.actor};
  border-radius: ${p => p.theme.borderRadius};
  max-width: 200px;
  white-space: nowrap;

  ${p => p.isOpen &&
    `
      :before,
      :after {
        position: absolute;
        bottom: calc(${(0, space_1.default)(0.5)} + 1px);
        right: 32px;
        content: '';
        width: 16px;
        border: 8px solid transparent;
        transform: translateY(calc(50% + 2px));
        right: 9px;
        border-bottom-color: ${p.theme.backgroundSecondary};
      }

      :before {
        transform: translateY(calc(50% + 1px));
        border-bottom-color: ${p.theme.border};
      }
    `}

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    border-right: 0;
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }
`;
//# sourceMappingURL=dropDownButton.jsx.map