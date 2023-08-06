Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
class InputField extends React.Component {
    render() {
        const { className, field } = this.props;
        return (<formField_1.default className={className} {...this.props}>
        {formFieldProps => field && field((0, omit_1.default)(formFieldProps, 'children'))}
      </formField_1.default>);
    }
}
exports.default = InputField;
InputField.defaultProps = {
    field: (_a) => {
        var { onChange, onBlur, onKeyDown } = _a, props = (0, tslib_1.__rest)(_a, ["onChange", "onBlur", "onKeyDown"]);
        return (<input_1.default {...props} onBlur={e => onBlur(e.target.value, e)} onKeyDown={e => onKeyDown(e.target.value, e)} onChange={e => onChange(e.target.value, e)}/>);
    },
};
//# sourceMappingURL=inputField.jsx.map