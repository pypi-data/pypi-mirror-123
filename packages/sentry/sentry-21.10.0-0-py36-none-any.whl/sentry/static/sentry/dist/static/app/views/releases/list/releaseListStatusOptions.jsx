Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const releaseListDropdown_1 = (0, tslib_1.__importDefault)(require("./releaseListDropdown"));
const utils_1 = require("./utils");
const options = {
    [utils_1.StatusOption.ACTIVE]: { label: (0, locale_1.t)('Active') },
    [utils_1.StatusOption.ARCHIVED]: { label: (0, locale_1.t)('Archived') },
};
function ReleaseListStatusOptions({ selected, onSelect }) {
    return (<StyledReleaseListDropdown label={(0, locale_1.t)('Status')} options={options} selected={selected} onSelect={onSelect}/>);
}
exports.default = ReleaseListStatusOptions;
const StyledReleaseListDropdown = (0, styled_1.default)(releaseListDropdown_1.default) `
  z-index: 3;
  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    order: 1;
  }
`;
//# sourceMappingURL=releaseListStatusOptions.jsx.map