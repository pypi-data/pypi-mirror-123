Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const utils_2 = require("../utils");
const CRASH_FREE_DANGER_THRESHOLD = 98;
const CRASH_FREE_WARNING_THRESHOLD = 99.5;
const getIcon = (percent, iconSize) => {
    if (percent < CRASH_FREE_DANGER_THRESHOLD) {
        return <icons_1.IconFire color="red300" size={iconSize}/>;
    }
    if (percent < CRASH_FREE_WARNING_THRESHOLD) {
        return <icons_1.IconWarning color="yellow300" size={iconSize}/>;
    }
    return <icons_1.IconCheckmark isCircled color="green300" size={iconSize}/>;
};
const CrashFree = ({ percent, iconSize = 'sm', displayOption }) => {
    return (<Wrapper>
      {getIcon(percent, iconSize)}
      <CrashFreePercent>
        {(0, utils_2.displayCrashFreePercent)(percent)}{' '}
        {(0, utils_1.defined)(displayOption) && (0, utils_2.releaseDisplayLabel)(displayOption, 2)}
      </CrashFreePercent>
    </Wrapper>);
};
const Wrapper = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;
  vertical-align: middle;
`;
const CrashFreePercent = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
  font-variant-numeric: tabular-nums;
`;
exports.default = CrashFree;
//# sourceMappingURL=crashFree.jsx.map