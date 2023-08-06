Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const releaseListDropdown_1 = (0, tslib_1.__importDefault)(require("./releaseListDropdown"));
const utils_1 = require("./utils");
function ReleaseListSortOptions({ selected, selectedDisplay, onSelect, organization, environments, }) {
    const sortOptions = Object.assign({ [utils_1.SortOption.DATE]: { label: (0, locale_1.t)('Date Created') }, [utils_1.SortOption.SESSIONS]: { label: (0, locale_1.t)('Total Sessions') } }, (selectedDisplay === utils_1.DisplayOption.USERS
        ? {
            [utils_1.SortOption.USERS_24_HOURS]: { label: (0, locale_1.t)('Active Users') },
            [utils_1.SortOption.CRASH_FREE_USERS]: { label: (0, locale_1.t)('Crash Free Users') },
        }
        : {
            [utils_1.SortOption.SESSIONS_24_HOURS]: { label: (0, locale_1.t)('Active Sessions') },
            [utils_1.SortOption.CRASH_FREE_SESSIONS]: { label: (0, locale_1.t)('Crash Free Sessions') },
        }));
    if (organization.features.includes('semver')) {
        sortOptions[utils_1.SortOption.BUILD] = { label: (0, locale_1.t)('Build Number') };
        sortOptions[utils_1.SortOption.SEMVER] = { label: (0, locale_1.t)('Semantic Version') };
    }
    if (organization.features.includes('release-adoption-stage')) {
        const isDisabled = environments.length !== 1;
        sortOptions[utils_1.SortOption.ADOPTION] = {
            label: (0, locale_1.t)('Date Adopted'),
            disabled: isDisabled,
            tooltip: isDisabled
                ? (0, locale_1.t)('Select one environment to use this sort option.')
                : undefined,
        };
    }
    return (<StyledReleaseListDropdown label={(0, locale_1.t)('Sort By')} options={sortOptions} selected={selected} onSelect={onSelect}/>);
}
exports.default = ReleaseListSortOptions;
const StyledReleaseListDropdown = (0, styled_1.default)(releaseListDropdown_1.default) `
  z-index: 2;
  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    order: 2;
  }
`;
//# sourceMappingURL=releaseListSortOptions.jsx.map