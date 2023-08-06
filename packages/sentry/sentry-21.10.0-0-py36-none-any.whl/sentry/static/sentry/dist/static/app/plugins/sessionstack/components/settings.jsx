Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const forms_1 = require("app/components/forms");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const settings_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/settings"));
class Settings extends settings_1.default {
    constructor() {
        super(...arguments);
        this.REQUIRED_FIELDS = ['account_email', 'api_token', 'website_id'];
        this.ON_PREMISES_FIELDS = ['api_url', 'player_url'];
        this.toggleOnPremisesConfiguration = () => {
            this.setState({
                showOnPremisesConfiguration: !this.state.showOnPremisesConfiguration,
            });
        };
    }
    renderFields(fields) {
        return fields === null || fields === void 0 ? void 0 : fields.map(f => this.renderField({
            config: f,
            formData: this.state.formData,
            formErrors: this.state.errors,
            onChange: this.changeField.bind(this, f.name),
        }));
    }
    filterFields(fields, fieldNames) {
        var _a;
        return (_a = fields === null || fields === void 0 ? void 0 : fields.filter(field => fieldNames.includes(field.name))) !== null && _a !== void 0 ? _a : [];
    }
    render() {
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
        const hasChanges = !(0, isEqual_1.default)(this.state.initialData, this.state.formData);
        const requiredFields = this.filterFields(this.state.fieldList, this.REQUIRED_FIELDS);
        const onPremisesFields = this.filterFields(this.state.fieldList, this.ON_PREMISES_FIELDS);
        return (<forms_1.Form onSubmit={this.onSubmit} submitDisabled={isSaving || !hasChanges}>
        {this.state.errors.__all__ && (<div className="alert alert-block alert-error">
            <ul>
              <li>{this.state.errors.__all__}</li>
            </ul>
          </div>)}
        {this.renderFields(requiredFields)}
        {onPremisesFields.length > 0 ? (<div className="control-group">
            <button className="btn btn-default" type="button" onClick={this.toggleOnPremisesConfiguration}>
              Configure on-premises
            </button>
          </div>) : null}
        {this.state.showOnPremisesConfiguration
                ? this.renderFields(onPremisesFields)
                : null}
      </forms_1.Form>);
    }
}
exports.default = Settings;
//# sourceMappingURL=settings.jsx.map