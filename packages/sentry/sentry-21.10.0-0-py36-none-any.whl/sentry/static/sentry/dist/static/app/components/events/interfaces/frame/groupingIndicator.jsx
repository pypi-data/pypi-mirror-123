Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const iconInfo_1 = require("app/icons/iconInfo");
const locale_1 = require("app/locale");
function GroupingIndicator({ className }) {
    return (<StyledTooltip title={(0, locale_1.t)('This frame appears in all other events related to this issue')} containerDisplayMode="inline-flex" className={className}>
      <iconInfo_1.IconInfo size="xs" color="gray300"/>
    </StyledTooltip>);
}
exports.default = GroupingIndicator;
const StyledTooltip = (0, styled_1.default)(tooltip_1.default) `
  align-items: center;
`;
//# sourceMappingURL=groupingIndicator.jsx.map