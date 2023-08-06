Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const indicator_1 = require("app/actionCreators/indicator");
const api_1 = require("app/api");
const form_1 = (0, tslib_1.__importDefault)(require("app/components/forms/form"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/formField"));
const state_1 = (0, tslib_1.__importDefault)(require("app/components/forms/state"));
const locale_1 = require("app/locale");
class ApiForm extends form_1.default {
    constructor() {
        super(...arguments);
        this.api = new api_1.Client();
        this.onSubmit = (e) => {
            e.preventDefault();
            if (this.state.state === state_1.default.SAVING) {
                return;
            }
            // Actual HTML forms do not submit data for disabled fields, and because of
            // the way some of our APIs are implemented, we need to start doing the
            // same. But, since some other parts of the app very probably depend on
            // sending disabled fields, keep that the default for now.
            // TODO(chadwhitacre): Expand and upstream this.
            const data = this.props.omitDisabled ? this.getEnabledData() : this.state.data;
            this.props.onSubmit && this.props.onSubmit(data);
            this.setState({
                state: state_1.default.SAVING,
            }, () => {
                (0, indicator_1.addLoadingMessage)(this.props.submitLoadingMessage);
                this.api.request(this.props.apiEndpoint, {
                    method: this.props.apiMethod,
                    data,
                    success: result => {
                        (0, indicator_1.clearIndicators)();
                        this.onSubmitSuccess(result);
                    },
                    error: error => {
                        (0, indicator_1.addErrorMessage)(this.props.submitErrorMessage);
                        this.onSubmitError(error);
                    },
                });
            });
        };
    }
    componentWillUnmount() {
        this.api.clear();
    }
    getEnabledData() {
        // Return a hash of data from non-disabled fields.
        // Start with this.state.data and remove rather than starting from scratch
        // and adding, because a) this.state.data is our source of truth, and b)
        // we'd have to do more work to loop over the state.data Object and lookup
        // against the props.children Array (looping over the Array and looking up
        // in the Object is more natural). Maybe the consequent use of delete
        // carries a slight performance hit. Why is yer form so big? 🤔
        const data = Object.assign({}, this.state.data); // Copy to avoid mutating state.data itself.
        React.Children.forEach(this.props.children, (child) => {
            var _a;
            if (!formField_1.default.isPrototypeOf(child.type)) {
                return; // Form children include h4's, etc.
            }
            if (child.key && ((_a = child.props) === null || _a === void 0 ? void 0 : _a.disabled)) {
                delete data[child.key]; // Assume a link between child.key and data. 🐭
            }
        });
        return data;
    }
}
exports.default = ApiForm;
ApiForm.defaultProps = Object.assign(Object.assign({}, form_1.default.defaultProps), { omitDisabled: false, submitErrorMessage: (0, locale_1.t)('There was an error saving your changes.'), submitLoadingMessage: (0, locale_1.t)('Saving changes\u2026') });
//# sourceMappingURL=apiForm.jsx.map