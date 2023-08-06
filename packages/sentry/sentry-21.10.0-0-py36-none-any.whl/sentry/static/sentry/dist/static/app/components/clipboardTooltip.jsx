Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function ClipboardTooltip(_a) {
    var { title, onSuccess } = _a, props = (0, tslib_1.__rest)(_a, ["title", "onSuccess"]);
    return (<tooltip_1.default {...props} title={<TooltipClipboardWrapper onClick={event => {
                event.stopPropagation();
            }}>
          <textOverflow_1.default>{title}</textOverflow_1.default>
          <clipboard_1.default value={title} onSuccess={onSuccess}>
            <TooltipClipboardIconWrapper>
              <icons_1.IconCopy size="xs" color="white" aria-label={(0, locale_1.t)('Copy to clipboard')}/>
            </TooltipClipboardIconWrapper>
          </clipboard_1.default>
        </TooltipClipboardWrapper>} isHoverable/>);
}
exports.default = ClipboardTooltip;
const TooltipClipboardWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto max-content;
  align-items: center;
  grid-gap: ${(0, space_1.default)(0.5)};
`;
const TooltipClipboardIconWrapper = (0, styled_1.default)('div') `
  position: relative;
  bottom: -${(0, space_1.default)(0.25)};
  :hover {
    cursor: pointer;
  }
`;
//# sourceMappingURL=clipboardTooltip.jsx.map