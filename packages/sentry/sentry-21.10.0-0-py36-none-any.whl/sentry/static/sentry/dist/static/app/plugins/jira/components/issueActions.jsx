Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const forms_1 = require("app/components/forms");
const issueActions_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/issueActions"));
class IssueActions extends issueActions_1.default {
    constructor() {
        super(...arguments);
        this.changeField = (action, name, value) => {
            const key = this.getFormDataKey(action);
            const formData = Object.assign(Object.assign({}, this.state[key]), { [name]: value });
            const state = Object.assign(Object.assign({}, this.state), { [key]: formData });
            if (name === 'issuetype') {
                state.state = forms_1.FormState.LOADING;
                this.setState(state, this.onLoad.bind(this, () => {
                    this.api.request(this.getPluginCreateEndpoint() + '?issuetype=' + encodeURIComponent(value), {
                        success: (data) => {
                            // Try not to change things the user might have edited
                            // unless they're no longer valid
                            const oldData = this.state.createFormData;
                            const createFormData = {};
                            data === null || data === void 0 ? void 0 : data.forEach(field => {
                                let val;
                                if (field.choices &&
                                    !field.choices.find(c => c[0] === oldData[field.name])) {
                                    val = field.default;
                                }
                                else {
                                    val = oldData[field.name] || field.default;
                                }
                                createFormData[field.name] = val;
                            });
                            this.setState({
                                createFieldList: data,
                                error: undefined,
                                loading: false,
                                createFormData,
                            }, this.onLoadSuccess);
                        },
                        error: this.errorHandler,
                    });
                }));
                return;
            }
            this.setState(state);
        };
    }
    renderForm() {
        let form = null;
        // For create form, split into required and optional fields
        if (this.props.actionType === 'create') {
            if (this.state.createFieldList) {
                const renderField = field => {
                    if (field.has_autocomplete) {
                        field = Object.assign({
                            url: '/api/0/issues/' +
                                this.getGroup().id +
                                '/plugins/' +
                                this.props.plugin.slug +
                                '/autocomplete',
                        }, field);
                    }
                    return (<div key={field.name}>
              {this.renderField({
                            config: field,
                            formData: this.state.createFormData,
                            onChange: this.changeField.bind(this, 'create', field.name),
                        })}
            </div>);
                };
                const isRequired = f => (f.required !== null ? f.required : true);
                const fields = this.state.createFieldList;
                const requiredFields = fields.filter(f => isRequired(f)).map(f => renderField(f));
                const optionalFields = fields
                    .filter(f => !isRequired(f))
                    .map(f => renderField(f));
                form = (<forms_1.Form onSubmit={this.createIssue} submitLabel="Create Issue" footerClass="">
            <h5>Required Fields</h5>
            {requiredFields}
            {optionalFields.length ? <h5>Optional Fields</h5> : null}
            {optionalFields}
          </forms_1.Form>);
            }
        }
        else {
            form = super.renderForm();
        }
        return form;
    }
}
exports.default = IssueActions;
//# sourceMappingURL=issueActions.jsx.map