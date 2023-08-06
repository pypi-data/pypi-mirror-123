Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
function Toggle({ highUp, wrapClassName, children }) {
    const [isExpanded, setIsExpanded] = (0, react_1.useState)(false);
    if (react_1.Children.count(children) === 0) {
        return null;
    }
    const wrappedChildren = <span className={wrapClassName}>{children}</span>;
    if (highUp) {
        return wrappedChildren;
    }
    return (<span>
      <IconWrapper isExpanded={isExpanded} onClick={evt => {
            setIsExpanded(!isExpanded);
            evt.preventDefault();
        }}>
        {isExpanded ? (<icons_1.IconSubtract size="9px" color="white"/>) : (<icons_1.IconAdd size="9px" color="white"/>)}
      </IconWrapper>
      {isExpanded && wrappedChildren}
    </span>);
}
exports.default = Toggle;
const IconWrapper = (0, styled_1.default)('div') `
  border-radius: 2px;
  background: ${p => p.theme.white};
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  ${p => p.isExpanded
    ? `
          background: ${p.theme.gray300};
          border: 1px solid ${p.theme.gray300};
          &:hover {
            background: ${p.theme.gray400};
          }
        `
    : `
          background: ${p.theme.blue300};
          border: 1px solid ${p.theme.blue300};
          &:hover {
            background: ${p.theme.blue200};
          }
        `}
`;
//# sourceMappingURL=toggle.jsx.map