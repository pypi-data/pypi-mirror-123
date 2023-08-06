Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const stacktracePreview_1 = require("app/components/stacktracePreview");
const iconChevron_1 = require("app/icons/iconChevron");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("../utils");
function Expander({ isExpandable, isHoverPreviewed, isExpanded, platform, onToggleContext, }) {
    if (!isExpandable) {
        return null;
    }
    return (<StyledButton className="btn-toggle" css={(0, utils_1.isDotnet)(platform) && { display: 'block !important' }} // remove important once we get rid of css files
     title={(0, locale_1.t)('Toggle Context')} tooltipProps={isHoverPreviewed ? { delay: stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY } : undefined} onClick={onToggleContext}>
      <iconChevron_1.IconChevron direction={isExpanded ? 'up' : 'down'} size="8px"/>
    </StyledButton>);
}
exports.default = Expander;
// the Button's label has the padding of 3px because the button size has to be 16x16 px.
const StyledButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(1)};
  span:first-child {
    padding: 3px;
  }
`;
//# sourceMappingURL=expander.jsx.map