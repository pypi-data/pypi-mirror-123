Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const button_1 = (0, tslib_1.__importDefault)(require("./button"));
const confirmableAction_1 = (0, tslib_1.__importDefault)(require("./confirmableAction"));
const StyledAction = (0, styled_1.default)('a') `
  display: flex;
  align-items: center;
  ${p => p.disabled && 'cursor: not-allowed;'}
`;
const StyledActionButton = (0, styled_1.default)(button_1.default) `
  display: flex;
  align-items: center;
  ${p => p.disabled && 'cursor: not-allowed;'}
`;
function ActionLink(_a) {
    var { message, className, title, onAction, type, confirmLabel, disabled, children, shouldConfirm, confirmPriority, header } = _a, props = (0, tslib_1.__rest)(_a, ["message", "className", "title", "onAction", "type", "confirmLabel", "disabled", "children", "shouldConfirm", "confirmPriority", "header"]);
    const actionCommonProps = Object.assign({ ['aria-label']: title, className: (0, classnames_1.default)(className, { disabled }), onClick: disabled ? undefined : onAction, disabled,
        children }, props);
    const action = type === 'button' ? (<StyledActionButton {...actionCommonProps}/>) : (<StyledAction {...actionCommonProps}/>);
    if (shouldConfirm && onAction) {
        return (<confirmableAction_1.default shouldConfirm={shouldConfirm} priority={confirmPriority} disabled={disabled} message={message} header={header} confirmText={confirmLabel} onConfirm={onAction} stopPropagation={disabled}>
        {action}
      </confirmableAction_1.default>);
    }
    return action;
}
exports.default = ActionLink;
//# sourceMappingURL=actionLink.jsx.map