Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const FEATURE_TOOLTIPS = {
    symtab: (0, locale_1.t)('Symbol tables are used as a fallback when full debug information is not available'),
    debug: (0, locale_1.t)('Debug information provides function names and resolves inlined frames during symbolication'),
    unwind: (0, locale_1.t)('Stack unwinding information improves the quality of stack traces extracted from minidumps'),
    sources: (0, locale_1.t)('Source code information allows Sentry to display source code context for stack frames'),
};
const DebugFileFeature = ({ available = true, feature }) => {
    const tooltipText = FEATURE_TOOLTIPS[feature];
    if (available === true) {
        return (<StyledTag type="success" tooltipText={tooltipText} icon={<icons_1.IconCheckmark />}>
        {feature}
      </StyledTag>);
    }
    return (<StyledTag type="error" tooltipText={tooltipText} icon={<icons_1.IconClose />}>
      {feature}
    </StyledTag>);
};
exports.default = DebugFileFeature;
const StyledTag = (0, styled_1.default)(tag_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=debugFileFeature.jsx.map