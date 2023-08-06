Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
/**
 * Get priority from alerts or badge styles
 */
const getPriority = (p) => {
    var _a, _b;
    if (p.priority) {
        return (_b = (_a = p.theme.alert[p.priority]) !== null && _a !== void 0 ? _a : p.theme.badge[p.priority]) !== null && _b !== void 0 ? _b : null;
    }
    return null;
};
const getMarginLeft = (p) => p.inline ? `margin-left: ${p.size === 'small' ? '0.25em' : '0.5em'};` : '';
const getBorder = (p) => { var _a, _b; return p.border ? `border: 1px solid ${(_b = (_a = getPriority(p)) === null || _a === void 0 ? void 0 : _a.border) !== null && _b !== void 0 ? _b : p.theme.border};` : ''; };
const Tag = (0, styled_1.default)((_a) => {
    var { children, icon, inline: _inline, priority: _priority, size: _size, border: _border } = _a, props = (0, tslib_1.__rest)(_a, ["children", "icon", "inline", "priority", "size", "border"]);
    return (<div {...props}>
      {icon && (<IconWrapper>
          {React.isValidElement(icon) && React.cloneElement(icon, { size: 'xs' })}
        </IconWrapper>)}
      {children}
    </div>);
}) `
  display: inline-flex;
  box-sizing: border-box;
  padding: ${p => (p.size === 'small' ? '0.1em 0.4em 0.2em' : '0.35em 0.8em 0.4em')};
  font-size: ${p => p.theme.fontSizeExtraSmall};
  line-height: 1;
  color: ${p => (p.priority ? p.theme.background : p.theme.textColor)};
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  align-items: center;
  border-radius: ${p => (p.size === 'small' ? '0.25em' : '2em')};
  text-transform: lowercase;
  font-weight: ${p => (p.size === 'small' ? 'bold' : 'normal')};
  background: ${p => { var _a, _b; return (_b = (_a = getPriority(p)) === null || _a === void 0 ? void 0 : _a.background) !== null && _b !== void 0 ? _b : p.theme.gray100; }};
  ${p => getBorder(p)};
  ${p => getMarginLeft(p)};
`;
const IconWrapper = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
exports.default = Tag;
//# sourceMappingURL=tagDeprecated.jsx.map