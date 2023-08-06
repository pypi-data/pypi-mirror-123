Object.defineProperty(exports, "__esModule", { value: true });
exports.SentryAppExternalForm = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_select_1 = require("react-select");
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const replaceAtArrayIndex_1 = require("app/utils/replaceAtArrayIndex");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const fieldFromConfig_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/fieldFromConfig"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
// 0 is a valid choice but empty string, undefined, and null are not
const hasValue = value => !!value || value === 0;
/**
 *  This component is the result of a refactor of sentryAppExternalIssueForm.tsx.
 *  Most of it contains a direct copy of the code from that original file (comments included)
 *  to allow for an abstract way of turning Sentry App Schema -> Form UI, rather than being
 *  specific to Issue Linking.
 *
 *  See (#28465) for more details.
 */
class SentryAppExternalForm extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { optionsByField: new Map() };
        this.model = new model_1.default();
        this.onSubmitError = () => {
            const { action, appName } = this.props;
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to %s %s %s.', action, appName, this.getElementText()));
        };
        this.getOptions = (field, input) => new Promise(resolve => {
            this.debouncedOptionLoad(field, input, resolve);
        });
        this.getElementText = () => {
            const { element } = this.props;
            switch (element) {
                case 'issue-link':
                    return 'issue';
                case 'alert-rule-action':
                    return 'alert';
                default:
                    return 'connection';
            }
        };
        this.debouncedOptionLoad = (0, debounce_1.default)(
        // debounce is used to prevent making a request for every input change and
        // instead makes the requests every 200ms
        (field, input, resolve) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const choices = yield this.makeExternalRequest(field, input);
            const options = choices.map(([value, label]) => ({ value, label }));
            const optionsByField = new Map(this.state.optionsByField);
            optionsByField.set(field.name, options);
            this.setState({
                optionsByField,
            });
            return resolve(options);
        }), 200, { trailing: true });
        this.makeExternalRequest = (field, input) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { extraRequestBody = {}, sentryAppInstallationUuid } = this.props;
            const query = Object.assign(Object.assign({}, extraRequestBody), { uri: field.uri, query: input });
            if (field.depends_on) {
                const dependentData = field.depends_on.reduce((accum, dependentField) => {
                    accum[dependentField] = this.model.getValue(dependentField);
                    return accum;
                }, {});
                // stringify the data
                query.dependentData = JSON.stringify(dependentData);
            }
            const { choices } = yield this.props.api.requestPromise(`/sentry-app-installations/${sentryAppInstallationUuid}/external-requests/`, {
                query,
            });
            return choices || [];
        });
        /**
         * This function determines which fields need to be reset and new options fetched
         * based on the dependencies defined with the depends_on attribute.
         * This is done because the autoload flag causes fields to load at different times
         * if you have multiple dependent fields while this solution updates state at once.
         */
        this.handleFieldChange = (id) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const config = this.state;
            let requiredFields = config.required_fields || [];
            let optionalFields = config.optional_fields || [];
            const fieldList = requiredFields.concat(optionalFields);
            // could have multiple impacted fields
            const impactedFields = fieldList.filter(({ depends_on }) => {
                if (!depends_on) {
                    return false;
                }
                // must be dependent on the field we just set
                return depends_on.includes(id);
            });
            // load all options in parallel
            const choiceArray = yield Promise.all(impactedFields.map(field => {
                // reset all impacted fields first
                this.model.setValue(field.name || '', '', { quiet: true });
                return this.makeExternalRequest(field, '');
            }));
            this.setState(state => {
                // pull the field lists from latest state
                requiredFields = state.required_fields || [];
                optionalFields = state.optional_fields || [];
                // iterate through all the impacted fields and get new values
                impactedFields.forEach((impactedField, i) => {
                    const choices = choiceArray[i];
                    const requiredIndex = requiredFields.indexOf(impactedField);
                    const optionalIndex = optionalFields.indexOf(impactedField);
                    const updatedField = Object.assign(Object.assign({}, impactedField), { choices });
                    // immutably update the lists with the updated field depending where we got it from
                    if (requiredIndex > -1) {
                        requiredFields = (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(requiredFields, requiredIndex, updatedField);
                    }
                    else if (optionalIndex > -1) {
                        optionalFields = (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(optionalFields, optionalIndex, updatedField);
                    }
                });
                return {
                    required_fields: requiredFields,
                    optional_fields: optionalFields,
                };
            });
        });
        this.renderField = (field, required) => {
            // This function converts the field we get from the backend into
            // the field we need to pass down
            let fieldToPass = Object.assign(Object.assign({}, field), { inline: false, stacked: true, flexibleControlStateSize: true, required });
            // async only used for select components
            const isAsync = typeof field.async === 'undefined' ? true : !!field.async; // default to true
            const defaultResetValues = (this.props.resetValues || {}).settings || {};
            if (fieldToPass.type === 'select') {
                // find the options from state to pass down
                const defaultOptions = (field.choices || []).map(([value, label]) => ({
                    value,
                    label,
                }));
                const options = this.state.optionsByField.get(field.name) || defaultOptions;
                const allowClear = !required;
                // filter by what the user is typing
                const filterOption = (0, react_select_1.createFilter)({});
                fieldToPass = Object.assign(Object.assign({}, fieldToPass), { options, defaultValue: defaultResetValues[field.name], defaultOptions,
                    filterOption,
                    allowClear });
                // default message for async select fields
                if (isAsync) {
                    fieldToPass.noOptionsMessage = () => 'Type to search';
                }
            }
            else if (['text', 'textarea'].includes(fieldToPass.type || '')) {
                // Interpret the default if a getFieldDefault function is provided
                let defaultValue = '';
                if (field.default && this.props.getFieldDefault) {
                    defaultValue = this.props.getFieldDefault(field);
                }
                // Override this default if a reset value is provided
                defaultValue = defaultResetValues[field.name] || defaultValue;
                fieldToPass = Object.assign(Object.assign({}, fieldToPass), { defaultValue });
            }
            if (field.depends_on) {
                // check if this is dependent on other fields which haven't been set yet
                const shouldDisable = field.depends_on.some(dependentField => !hasValue(this.model.getValue(dependentField)));
                if (shouldDisable) {
                    fieldToPass = Object.assign(Object.assign({}, fieldToPass), { disabled: true });
                }
            }
            // if we have a uri, we need to set extra parameters
            const extraProps = field.uri
                ? {
                    loadOptions: (input) => this.getOptions(field, input),
                    async: isAsync,
                    cache: false,
                    onSelectResetsInput: false,
                    onCloseResetsInput: false,
                    onBlurResetsInput: false,
                    autoload: false,
                }
                : {};
            return (<fieldFromConfig_1.default key={field.name} field={fieldToPass} data-test-id={field.name} {...extraProps}/>);
        };
        this.handleAlertRuleSubmit = (formData, onSubmitSuccess) => {
            const { sentryAppInstallationUuid } = this.props;
            if (this.model.validateForm()) {
                onSubmitSuccess({
                    // The form data must be nested in 'settings' to ensure they don't overlap with any other field names.
                    settings: formData,
                    sentryAppInstallationUuid,
                    // Used on the backend to explicitly associate with a different rule than those without a custom form.
                    hasSchemaFormConfig: true,
                });
            }
        };
    }
    componentDidMount() {
        this.resetStateFromProps();
    }
    componentDidUpdate(prevProps) {
        if (prevProps.action !== this.props.action) {
            this.model.reset();
            this.resetStateFromProps();
        }
    }
    // reset the state when we mount or the action changes
    resetStateFromProps() {
        const { config, action, extraFields, element } = this.props;
        this.setState({
            required_fields: config.required_fields,
            optional_fields: config.optional_fields,
        });
        // For alert-rule-actions, the forms are entirely custom, extra fields are
        // passed in on submission, not as part of the form. See handleAlertRuleSubmit().
        if (element !== 'alert-rule-action') {
            this.model.setInitialData(Object.assign(Object.assign({}, extraFields), { 
                // we need to pass these fields in the API so just set them as values so we don't need hidden form fields
                action, uri: config.uri }));
        }
    }
    render() {
        const { sentryAppInstallationUuid, action, element, onSubmitSuccess } = this.props;
        const requiredFields = this.state.required_fields || [];
        const optionalFields = this.state.optional_fields || [];
        if (!sentryAppInstallationUuid)
            return '';
        return (<form_1.default key={action} apiEndpoint={`/sentry-app-installations/${sentryAppInstallationUuid}/external-issue-actions/`} apiMethod="POST" 
        // Without defining onSubmit, the Form will send an `apiMethod` request to the above `apiEndpoint`
        onSubmit={element === 'alert-rule-action' ? this.handleAlertRuleSubmit : undefined} onSubmitSuccess={(...params) => {
                onSubmitSuccess(...params);
            }} onSubmitError={this.onSubmitError} onFieldChange={this.handleFieldChange} model={this.model}>
        {requiredFields.map((field) => {
                return this.renderField(field, true);
            })}

        {optionalFields.map((field) => {
                return this.renderField(field, false);
            })}
      </form_1.default>);
    }
}
exports.SentryAppExternalForm = SentryAppExternalForm;
exports.default = (0, withApi_1.default)(SentryAppExternalForm);
//# sourceMappingURL=sentryAppExternalForm.jsx.map