Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const forms_1 = require("app/components/forms");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const settings_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/settings"));
const PAGE_FIELD_LIST = {
    0: ['instance_url', 'username', 'password'],
    1: ['default_project'],
    2: ['ignored_fields', 'default_priority', 'default_issue_type', 'auto_create'],
};
class Settings extends settings_1.default {
    constructor(props, context) {
        super(props, context);
        this.isLastPage = () => {
            return this.state.page === 2;
        };
        this.startEditing = () => {
            this.setState({ editing: true });
        };
        this.back = (ev) => {
            ev.preventDefault();
            if (this.state.state === forms_1.FormState.SAVING) {
                return;
            }
            this.setState({
                page: this.state.page - 1,
            });
        };
        Object.assign(this.state, {
            page: 0,
        });
    }
    isConfigured() {
        return !!(this.state.formData && this.state.formData.default_project);
    }
    fetchData() {
        // This is mostly copy paste of parent class
        // except for setting edit state
        this.api.request(this.getPluginEndpoint(), {
            success: (data) => {
                const formData = {};
                const initialData = {};
                data.config.forEach(field => {
                    formData[field.name] = field.value || field.defaultValue;
                    initialData[field.name] = field.value;
                });
                this.setState({
                    fieldList: data.config,
                    formData,
                    initialData,
                    // start off in edit mode if there isn't a project set
                    editing: !(formData && formData.default_project),
                    // call this here to prevent FormState.READY from being
                    // set before fieldList is
                }, this.onLoadSuccess);
            },
            error: this.onLoadError,
        });
    }
    onSubmit() {
        var _a;
        if ((0, isEqual_1.default)(this.state.initialData, this.state.formData)) {
            if (this.isLastPage()) {
                this.setState({ editing: false, page: 0 });
            }
            else {
                this.setState({ page: this.state.page + 1 });
            }
            this.onSaveSuccess(this.onSaveComplete);
            return;
        }
        const body = Object.assign({}, this.state.formData);
        // if the project has changed, it's likely these values aren't valid anymore
        if (body.default_project !== ((_a = this.state.initialData) === null || _a === void 0 ? void 0 : _a.default_project)) {
            body.default_issue_type = null;
            body.default_priority = null;
        }
        this.api.request(this.getPluginEndpoint(), {
            data: body,
            method: 'PUT',
            success: this.onSaveSuccess.bind(this, (data) => {
                const formData = {};
                const initialData = {};
                data.config.forEach(field => {
                    formData[field.name] = field.value || field.defaultValue;
                    initialData[field.name] = field.value;
                });
                const state = {
                    formData,
                    initialData,
                    errors: {},
                    fieldList: data.config,
                    page: this.state.page,
                    editing: this.state.editing,
                };
                if (this.isLastPage()) {
                    state.editing = false;
                    state.page = 0;
                }
                else {
                    state.page = this.state.page + 1;
                }
                this.setState(state);
            }),
            error: this.onSaveError.bind(this, error => {
                this.setState({
                    errors: (error.responseJSON || {}).errors || {},
                });
            }),
            complete: this.onSaveComplete,
        });
    }
    render() {
        var _a, _b;
        if (this.state.state === forms_1.FormState.LOADING) {
            return <loadingIndicator_1.default />;
        }
        if (this.state.state === forms_1.FormState.ERROR && !this.state.fieldList) {
            return (<div className="alert alert-error m-b-1">
          An unknown error occurred. Need help with this?{' '}
          <a href="https://sentry.io/support/">Contact support</a>
        </div>);
        }
        const isSaving = this.state.state === forms_1.FormState.SAVING;
        let fields;
        let onSubmit;
        let submitLabel;
        if (this.state.editing) {
            fields = (_a = this.state.fieldList) === null || _a === void 0 ? void 0 : _a.filter(f => PAGE_FIELD_LIST[this.state.page].includes(f.name));
            onSubmit = this.onSubmit;
            submitLabel = this.isLastPage() ? 'Finish' : 'Save and Continue';
        }
        else {
            fields = (_b = this.state.fieldList) === null || _b === void 0 ? void 0 : _b.map(f => (Object.assign(Object.assign({}, f), { readonly: true })));
            onSubmit = this.startEditing;
            submitLabel = 'Edit';
        }
        return (<forms_1.Form onSubmit={onSubmit} submitDisabled={isSaving} submitLabel={submitLabel} extraButton={this.state.page === 0 ? null : (<a href="#" className={'btn btn-default pull-left' + (isSaving ? ' disabled' : '')} onClick={this.back}>
              Back
            </a>)}>
        {this.state.errors.__all__ && (<div className="alert alert-block alert-error">
            <ul>
              <li>{this.state.errors.__all__}</li>
            </ul>
          </div>)}
        {fields === null || fields === void 0 ? void 0 : fields.map(f => this.renderField({
                config: f,
                formData: this.state.formData,
                formErrors: this.state.errors,
                onChange: this.changeField.bind(this, f.name),
            }))}
      </forms_1.Form>);
    }
}
exports.default = Settings;
//# sourceMappingURL=settings.jsx.map