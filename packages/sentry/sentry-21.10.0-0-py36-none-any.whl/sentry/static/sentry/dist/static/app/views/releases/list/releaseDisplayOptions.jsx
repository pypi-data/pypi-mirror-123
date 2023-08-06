Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const releaseListDropdown_1 = (0, tslib_1.__importDefault)(require("./releaseListDropdown"));
const utils_1 = require("./utils");
const displayOptions = {
    [utils_1.DisplayOption.SESSIONS]: { label: (0, locale_1.t)('Sessions') },
    [utils_1.DisplayOption.USERS]: { label: (0, locale_1.t)('Users') },
};
function ReleaseListDisplayOptions({ selected, onSelect }) {
    return (<StyledReleaseListDropdown label={(0, locale_1.t)('Display')} options={displayOptions} selected={selected} onSelect={onSelect}/>);
}
exports.default = ReleaseListDisplayOptions;
const StyledReleaseListDropdown = (0, styled_1.default)(releaseListDropdown_1.default) `
  z-index: 1;
  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    order: 3;
  }
`;
//# sourceMappingURL=releaseDisplayOptions.jsx.map