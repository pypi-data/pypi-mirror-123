Object.defineProperty(exports, "__esModule", { value: true });
exports.PackageStatusIcon = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const PackageStatus = ({ status, tooltip }) => {
    const getIcon = () => {
        switch (status) {
            case 'success':
                return <icons_1.IconCheckmark isCircled color="green300" size="xs"/>;
            case 'empty':
                return <icons_1.IconCircle size="xs"/>;
            case 'error':
            default:
                return <icons_1.IconFlag color="red300" size="xs"/>;
        }
    };
    const icon = getIcon();
    if (status === 'empty') {
        return null;
    }
    return (<StyledTooltip title={tooltip} disabled={!(tooltip && tooltip.length)} containerDisplayMode="inline-flex">
      <exports.PackageStatusIcon>{icon}</exports.PackageStatusIcon>
    </StyledTooltip>);
};
const StyledTooltip = (0, styled_1.default)(tooltip_1.default) `
  margin-left: ${(0, space_1.default)(0.75)};
`;
exports.PackageStatusIcon = (0, styled_1.default)('span') `
  height: 12px;
  align-items: center;
  cursor: pointer;
  visibility: hidden;
  display: none;
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
  }
`;
exports.default = PackageStatus;
//# sourceMappingURL=packageStatus.jsx.map