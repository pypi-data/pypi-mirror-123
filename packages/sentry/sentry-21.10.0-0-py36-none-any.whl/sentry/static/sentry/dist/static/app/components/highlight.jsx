Object.defineProperty(exports, "__esModule", { value: true });
exports.HighlightComponent = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const HighlightComponent = ({ className, children, disabled, text }) => {
    // There are instances when children is not string in breadcrumbs but not caught by TS
    if (!text || disabled || typeof children !== 'string') {
        return <React.Fragment>{children}</React.Fragment>;
    }
    const highlightText = text.toLowerCase();
    const idx = children.toLowerCase().indexOf(highlightText);
    if (idx === -1) {
        return <React.Fragment>{children}</React.Fragment>;
    }
    return (<React.Fragment>
      {children.substr(0, idx)}
      <span className={className}>{children.substr(idx, highlightText.length)}</span>
      {children.substr(idx + highlightText.length)}
    </React.Fragment>);
};
exports.HighlightComponent = HighlightComponent;
const Highlight = (0, styled_1.default)(HighlightComponent) `
  font-weight: normal;
  background-color: ${p => p.theme.yellow200};
  color: ${p => p.theme.textColor};
`;
exports.default = Highlight;
//# sourceMappingURL=highlight.jsx.map