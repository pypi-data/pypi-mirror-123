Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const blankField_1 = (0, tslib_1.__importDefault)(require("./blankField"));
const booleanField_1 = (0, tslib_1.__importDefault)(require("./booleanField"));
const choiceMapperField_1 = (0, tslib_1.__importDefault)(require("./choiceMapperField"));
const emailField_1 = (0, tslib_1.__importDefault)(require("./emailField"));
const fieldSeparator_1 = (0, tslib_1.__importDefault)(require("./fieldSeparator"));
const hiddenField_1 = (0, tslib_1.__importDefault)(require("./hiddenField"));
const inputField_1 = (0, tslib_1.__importDefault)(require("./inputField"));
const numberField_1 = (0, tslib_1.__importDefault)(require("./numberField"));
const projectMapperField_1 = (0, tslib_1.__importDefault)(require("./projectMapperField"));
const radioField_1 = (0, tslib_1.__importDefault)(require("./radioField"));
const rangeField_1 = (0, tslib_1.__importDefault)(require("./rangeField"));
const selectAsyncField_1 = (0, tslib_1.__importDefault)(require("./selectAsyncField"));
const selectField_1 = (0, tslib_1.__importDefault)(require("./selectField"));
const sentryProjectSelectorField_1 = (0, tslib_1.__importDefault)(require("./sentryProjectSelectorField"));
const tableField_1 = (0, tslib_1.__importDefault)(require("./tableField"));
const textareaField_1 = (0, tslib_1.__importDefault)(require("./textareaField"));
const textField_1 = (0, tslib_1.__importDefault)(require("./textField"));
class FieldFromConfig extends react_1.Component {
    render() {
        const _a = this.props, { field } = _a, otherProps = (0, tslib_1.__rest)(_a, ["field"]);
        const props = Object.assign(Object.assign({}, otherProps), field);
        switch (field.type) {
            case 'separator':
                return <fieldSeparator_1.default />;
            case 'secret':
                return <inputField_1.default {...props} type="password"/>;
            case 'range':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <rangeField_1.default {...props}/>;
            case 'blank':
                return <blankField_1.default {...props}/>;
            case 'bool':
            case 'boolean':
                return <booleanField_1.default {...props}/>;
            case 'email':
                return <emailField_1.default {...props}/>;
            case 'hidden':
                return <hiddenField_1.default {...props}/>;
            case 'string':
            case 'text':
            case 'url':
                if (props.multiline) {
                    return <textareaField_1.default {...props}/>;
                }
                return <textField_1.default {...props}/>;
            case 'number':
                return <numberField_1.default {...props}/>;
            case 'textarea':
                return <textareaField_1.default {...props}/>;
            case 'choice':
            case 'select':
            case 'array':
                return <selectField_1.default {...props}/>;
            case 'choice_mapper':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <choiceMapperField_1.default {...props}/>;
            case 'radio':
                const choices = props.choices;
                if (!Array.isArray(choices)) {
                    throw new Error('Invalid `choices` type. Use an array of options');
                }
                return <radioField_1.default {...props} choices={choices}/>;
            case 'table':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <tableField_1.default {...props}/>;
            case 'project_mapper':
                return <projectMapperField_1.default {...props}/>;
            case 'sentry_project_selector':
                return <sentryProjectSelectorField_1.default {...props}/>;
            case 'select_async':
                return <selectAsyncField_1.default {...props}/>;
            case 'custom':
                return field.Component(props);
            default:
                return null;
        }
    }
}
exports.default = FieldFromConfig;
//# sourceMappingURL=fieldFromConfig.jsx.map