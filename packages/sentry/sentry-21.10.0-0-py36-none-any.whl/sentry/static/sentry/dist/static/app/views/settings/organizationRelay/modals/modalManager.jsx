Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const form_1 = (0, tslib_1.__importDefault)(require("./form"));
const handleXhrErrorResponse_1 = (0, tslib_1.__importDefault)(require("./handleXhrErrorResponse"));
const modal_1 = (0, tslib_1.__importDefault)(require("./modal"));
class DialogManager extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getDefaultState();
        this.handleChange = (field, value) => {
            this.setState(prevState => ({
                values: Object.assign(Object.assign({}, prevState.values), { [field]: value }),
                errors: (0, omit_1.default)(prevState.errors, field),
            }));
        };
        this.handleSave = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { onSubmitSuccess, closeModal, orgSlug, api } = this.props;
            const trustedRelays = this.getData().trustedRelays.map(trustedRelay => (0, omit_1.default)(trustedRelay, ['created', 'lastModified']));
            try {
                const response = yield api.requestPromise(`/organizations/${orgSlug}/`, {
                    method: 'PUT',
                    data: { trustedRelays },
                });
                onSubmitSuccess(response);
                closeModal();
            }
            catch (error) {
                this.convertErrorXhrResponse((0, handleXhrErrorResponse_1.default)(error));
            }
        });
        this.handleValidate = (field) => () => {
            const isFieldValueEmpty = !this.state.values[field].replace(/\s/g, '');
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
        this.handleValidateKey = () => {
            const { savedRelays } = this.props;
            const { values, errors } = this.state;
            const isKeyAlreadyTaken = savedRelays.find(savedRelay => savedRelay.publicKey === values.publicKey);
            if (isKeyAlreadyTaken && !errors.publicKey) {
                this.setState({
                    errors: Object.assign(Object.assign({}, errors), { publicKey: (0, locale_1.t)('Relay key already taken') }),
                });
                return;
            }
            if (errors.publicKey) {
                this.setState({
                    errors: (0, omit_1.default)(errors, 'publicKey'),
                });
            }
            this.handleValidate('publicKey')();
        };
    }
    componentDidMount() {
        this.validateForm();
    }
    componentDidUpdate(_prevProps, prevState) {
        if (!(0, isEqual_1.default)(prevState.values, this.state.values)) {
            this.validateForm();
        }
        if (!(0, isEqual_1.default)(prevState.errors, this.state.errors) &&
            Object.keys(this.state.errors).length > 0) {
            this.setValidForm(false);
        }
    }
    getDefaultState() {
        return {
            values: { name: '', publicKey: '', description: '' },
            requiredValues: ['name', 'publicKey'],
            errors: {},
            disables: {},
            isFormValid: false,
            title: this.getTitle(),
        };
    }
    getTitle() {
        return '';
    }
    getData() {
        // Child has to implement this
        throw new Error('Not implemented');
    }
    getBtnSaveLabel() {
        return undefined;
    }
    setValidForm(isFormValid) {
        this.setState({ isFormValid });
    }
    validateForm() {
        const { values, requiredValues, errors } = this.state;
        const isFormValid = requiredValues.every(requiredValue => !!values[requiredValue].replace(/\s/g, '') && !errors[requiredValue]);
        this.setValidForm(isFormValid);
    }
    clearError(field) {
        this.setState(prevState => ({
            errors: (0, omit_1.default)(prevState.errors, field),
        }));
    }
    convertErrorXhrResponse(error) {
        switch (error.type) {
            case 'invalid-key':
            case 'missing-key':
                this.setState(prevState => ({
                    errors: Object.assign(Object.assign({}, prevState.errors), { publicKey: error.message }),
                }));
                break;
            case 'empty-name':
            case 'missing-name':
                this.setState(prevState => ({
                    errors: Object.assign(Object.assign({}, prevState.errors), { name: error.message }),
                }));
                break;
            default:
                (0, indicator_1.addErrorMessage)(error.message);
        }
    }
    getForm() {
        const { values, errors, disables, isFormValid } = this.state;
        return (<form_1.default isFormValid={isFormValid} onSave={this.handleSave} onChange={this.handleChange} onValidate={this.handleValidate} onValidateKey={this.handleValidateKey} errors={errors} values={values} disables={disables}/>);
    }
    getContent() {
        return this.getForm();
    }
    render() {
        const { title, isFormValid } = this.state;
        const btnSaveLabel = this.getBtnSaveLabel();
        const content = this.getContent();
        return (<modal_1.default {...this.props} title={title} onSave={this.handleSave} btnSaveLabel={btnSaveLabel} disabled={!isFormValid} content={content}/>);
    }
}
exports.default = DialogManager;
//# sourceMappingURL=modalManager.jsx.map