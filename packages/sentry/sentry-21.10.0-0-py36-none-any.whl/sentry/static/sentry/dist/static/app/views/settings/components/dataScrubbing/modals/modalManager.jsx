Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const submitRules_1 = (0, tslib_1.__importDefault)(require("../submitRules"));
const types_1 = require("../types");
const utils_1 = require("../utils");
const form_1 = (0, tslib_1.__importDefault)(require("./form"));
const handleError_1 = (0, tslib_1.__importStar)(require("./handleError"));
const modal_1 = (0, tslib_1.__importDefault)(require("./modal"));
const utils_2 = require("./utils");
class ModalManager extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getDefaultState();
        this.handleChange = (field, value) => {
            const values = Object.assign(Object.assign({}, this.state.values), { [field]: value });
            if (values.type !== types_1.RuleType.PATTERN && values.pattern) {
                values.pattern = '';
            }
            if (values.method !== types_1.MethodType.REPLACE && values.placeholder) {
                values.placeholder = '';
            }
            this.setState(prevState => ({
                values,
                requiredValues: this.getRequiredValues(values),
                errors: (0, omit_1.default)(prevState.errors, field),
            }));
        };
        this.handleSave = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { endpoint, api, onSubmitSuccess, closeModal, onGetNewRules } = this.props;
            const newRules = onGetNewRules(this.state.values);
            try {
                const data = yield (0, submitRules_1.default)(api, endpoint, newRules);
                onSubmitSuccess(data);
                closeModal();
            }
            catch (error) {
                this.convertRequestError((0, handleError_1.default)(error));
            }
        });
        this.handleValidate = (field) => () => {
            const isFieldValueEmpty = !this.state.values[field].trim();
            const fieldErrorAlreadyExist = this.state.errors[field];
            if (isFieldValueEmpty && fieldErrorAlreadyExist) {
                return;
            }
            if (isFieldValueEmpty && !fieldErrorAlreadyExist) {
                this.setState(prevState => ({
                    errors: Object.assign(Object.assign({}, prevState.errors), { [field]: (0, locale_1.t)('Field Required') }),
                }));
                return;
            }
            if (!isFieldValueEmpty && fieldErrorAlreadyExist) {
                this.clearError(field);
            }
        };
        this.handleUpdateEventId = (eventId) => {
            if (eventId === this.state.eventId.value) {
                return;
            }
            this.setState({
                eventId: { value: eventId, status: types_1.EventIdStatus.UNDEFINED },
            });
        };
    }
    componentDidMount() {
        this.handleValidateForm();
    }
    componentDidUpdate(_prevProps, prevState) {
        if (!(0, isEqual_1.default)(prevState.values, this.state.values)) {
            this.handleValidateForm();
        }
        if (prevState.eventId.value !== this.state.eventId.value) {
            this.loadSourceSuggestions();
        }
        if (prevState.eventId.status !== this.state.eventId.status) {
            (0, utils_2.saveToSourceGroupData)(this.state.eventId, this.state.sourceSuggestions);
        }
    }
    getDefaultState() {
        const { eventId, sourceSuggestions } = (0, utils_2.fetchSourceGroupData)();
        const values = this.getInitialValues();
        return {
            values,
            requiredValues: this.getRequiredValues(values),
            errors: {},
            isFormValid: false,
            eventId: {
                value: eventId,
                status: !eventId ? types_1.EventIdStatus.UNDEFINED : types_1.EventIdStatus.LOADED,
            },
            sourceSuggestions,
        };
    }
    getInitialValues() {
        var _a, _b, _c, _d, _e;
        const { initialState } = this.props;
        return {
            type: (_a = initialState === null || initialState === void 0 ? void 0 : initialState.type) !== null && _a !== void 0 ? _a : types_1.RuleType.CREDITCARD,
            method: (_b = initialState === null || initialState === void 0 ? void 0 : initialState.method) !== null && _b !== void 0 ? _b : types_1.MethodType.MASK,
            source: (_c = initialState === null || initialState === void 0 ? void 0 : initialState.source) !== null && _c !== void 0 ? _c : '',
            placeholder: (_d = initialState === null || initialState === void 0 ? void 0 : initialState.placeholder) !== null && _d !== void 0 ? _d : '',
            pattern: (_e = initialState === null || initialState === void 0 ? void 0 : initialState.pattern) !== null && _e !== void 0 ? _e : '',
        };
    }
    getRequiredValues(values) {
        const { type } = values;
        const requiredValues = ['type', 'method', 'source'];
        if (type === types_1.RuleType.PATTERN) {
            requiredValues.push('pattern');
        }
        return requiredValues;
    }
    clearError(field) {
        this.setState(prevState => ({
            errors: (0, omit_1.default)(prevState.errors, field),
        }));
    }
    loadSourceSuggestions() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { orgSlug, projectId, api } = this.props;
            const { eventId } = this.state;
            if (!eventId.value) {
                this.setState(prevState => ({
                    sourceSuggestions: utils_1.valueSuggestions,
                    eventId: Object.assign(Object.assign({}, prevState.eventId), { status: types_1.EventIdStatus.UNDEFINED }),
                }));
                return;
            }
            this.setState(prevState => ({
                sourceSuggestions: utils_1.valueSuggestions,
                eventId: Object.assign(Object.assign({}, prevState.eventId), { status: types_1.EventIdStatus.LOADING }),
            }));
            try {
                const query = { eventId: eventId.value };
                if (projectId) {
                    query.projectId = projectId;
                }
                const rawSuggestions = yield api.requestPromise(`/organizations/${orgSlug}/data-scrubbing-selector-suggestions/`, { query });
                const sourceSuggestions = rawSuggestions.suggestions;
                if (sourceSuggestions && sourceSuggestions.length > 0) {
                    this.setState(prevState => ({
                        sourceSuggestions,
                        eventId: Object.assign(Object.assign({}, prevState.eventId), { status: types_1.EventIdStatus.LOADED }),
                    }));
                    return;
                }
                this.setState(prevState => ({
                    sourceSuggestions: utils_1.valueSuggestions,
                    eventId: Object.assign(Object.assign({}, prevState.eventId), { status: types_1.EventIdStatus.NOT_FOUND }),
                }));
            }
            catch (_a) {
                this.setState(prevState => ({
                    eventId: Object.assign(Object.assign({}, prevState.eventId), { status: types_1.EventIdStatus.ERROR }),
                }));
            }
        });
    }
    convertRequestError(error) {
        switch (error.type) {
            case handleError_1.ErrorType.InvalidSelector:
                this.setState(prevState => ({
                    errors: Object.assign(Object.assign({}, prevState.errors), { source: error.message }),
                }));
                break;
            case handleError_1.ErrorType.RegexParse:
                this.setState(prevState => ({
                    errors: Object.assign(Object.assign({}, prevState.errors), { pattern: error.message }),
                }));
                break;
            default:
                (0, indicator_1.addErrorMessage)(error.message);
        }
    }
    handleValidateForm() {
        const { values, requiredValues } = this.state;
        const isFormValid = requiredValues.every(requiredValue => !!values[requiredValue]);
        this.setState({ isFormValid });
    }
    render() {
        const { values, errors, isFormValid, eventId, sourceSuggestions } = this.state;
        const { title } = this.props;
        return (<modal_1.default {...this.props} title={title} onSave={this.handleSave} disabled={!isFormValid} content={<form_1.default onChange={this.handleChange} onValidate={this.handleValidate} onUpdateEventId={this.handleUpdateEventId} eventId={eventId} errors={errors} values={values} sourceSuggestions={sourceSuggestions}/>}/>);
    }
}
exports.default = ModalManager;
//# sourceMappingURL=modalManager.jsx.map