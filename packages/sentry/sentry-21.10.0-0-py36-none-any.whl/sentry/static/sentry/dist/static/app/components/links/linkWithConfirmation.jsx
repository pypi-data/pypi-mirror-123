Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
/**
 * <Confirm> is a more generic version of this component
 */
class LinkWithConfirmation extends React.PureComponent {
    render() {
        const _a = this.props, { className, disabled, title, children } = _a, otherProps = (0, tslib_1.__rest)(_a, ["className", "disabled", "title", "children"]);
        return (<confirm_1.default {...otherProps} disabled={disabled}>
        <a href="#" className={(0, classnames_1.default)(className || '', { disabled })} title={title}>
          {children}
        </a>
      </confirm_1.default>);
    }
}
exports.default = LinkWithConfirmation;
//# sourceMappingURL=linkWithConfirmation.jsx.map