Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const booleanField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/booleanField"));
const emailField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/emailField"));
const numberField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/numberField"));
const passwordField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/passwordField"));
const selectAsyncField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectAsyncField"));
const selectCreatableField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectCreatableField"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectField"));
const textareaField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/textareaField"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/textField"));
const utils_1 = require("app/utils");
const GenericField = ({ config, formData = {}, formErrors = {}, formState, onChange, }) => {
    const required = (0, utils_1.defined)(config.required) ? config.required : true;
    const fieldProps = Object.assign(Object.assign({}, config), { value: formData[config.name], onChange, label: config.label + (required ? '*' : ''), placeholder: config.placeholder, required, name: config.name, error: (formErrors || {})[config.name], defaultValue: config.default, disabled: config.readonly, key: config.name, formState, help: (0, utils_1.defined)(config.help) && config.help !== '' ? (<span dangerouslySetInnerHTML={{ __html: config.help }}/>) : null });
    switch (config.type) {
        case 'secret':
            return <passwordField_1.default {...fieldProps}/>;
        case 'bool':
            return <booleanField_1.default {...fieldProps}/>;
        case 'email':
            return <emailField_1.default {...fieldProps}/>;
        case 'string':
        case 'text':
        case 'url':
            if (fieldProps.choices) {
                return <selectCreatableField_1.default {...fieldProps}/>;
            }
            return <textField_1.default {...fieldProps}/>;
        case 'number':
            return <numberField_1.default {...fieldProps}/>;
        case 'textarea':
            return <textareaField_1.default {...fieldProps}/>;
        case 'choice':
        case 'select':
            // the chrome required tip winds up in weird places
            // for select elements, so just make it look like
            // it's required (with *) and rely on server validation
            const { required: _ } = fieldProps, selectProps = (0, tslib_1.__rest)(fieldProps, ["required"]);
            if (config.has_autocomplete) {
                // Redeclaring field props here as config has been narrowed to include the correct options for SelectAsyncField
                const selectFieldProps = Object.assign(Object.assign({}, config), selectProps);
                return <selectAsyncField_1.default {...selectFieldProps}/>;
            }
            return <selectField_1.default {...selectProps}/>;
        default:
            return null;
    }
};
exports.default = GenericField;
//# sourceMappingURL=genericField.jsx.map