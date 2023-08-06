Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const QuestionIconContainer = (0, styled_1.default)('span') `
  display: inline-block;
  height: ${p => { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }};
  line-height: ${p => { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }};

  & svg {
    transition: 120ms color;
    color: ${p => p.theme.gray200};

    &:hover {
      color: ${p => p.theme.gray300};
    }
  }
`;
function QuestionTooltip(_a) {
    var { title, size, className } = _a, tooltipProps = (0, tslib_1.__rest)(_a, ["title", "size", "className"]);
    return (<QuestionIconContainer size={size} className={className}>
      <tooltip_1.default title={title} {...tooltipProps}>
        <icons_1.IconQuestion size={size}/>
      </tooltip_1.default>
    </QuestionIconContainer>);
}
exports.default = QuestionTooltip;
//# sourceMappingURL=questionTooltip.jsx.map