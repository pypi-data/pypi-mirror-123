Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const pluginComponentBase_1 = (0, tslib_1.__importDefault)(require("app/components/bases/pluginComponentBase"));
const forms_1 = require("app/components/forms");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const integrationUtil_1 = require("app/utils/integrationUtil");
class PluginSettings extends pluginComponentBase_1.default {
    constructor(props, context) {
        super(props, context);
        this.trackPluginEvent = (eventKey) => {
            (0, integrationUtil_1.trackIntegrationAnalytics)(eventKey, {
                integration: this.props.plugin.id,
                integration_type: 'plugin',
                view: 'plugin_details',
                already_installed: this.state.wasConfiguredOnPageLoad,
                organization: this.props.organization,
            });
        };
        Object.assign(this.state, {
            fieldList: null,
            initialData: null,
            formData: null,
            errors: {},
            rawData: {},
            // override default FormState.READY if api requests are
            // necessary to even load the form
            state: forms_1.FormState.LOADING,
            wasConfiguredOnPageLoad: false,
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    getPluginEndpoint() {
        const org = this.props.organization;
        const project = this.props.project;
        return `/projects/${org.slug}/${project.slug}/plugins/${this.props.plugin.id}/`;
    }
    changeField(name, value) {
        const formData = this.state.formData;
        formData[name] = value;
        // upon changing a field, remove errors
        const errors = this.state.errors;
        delete errors[name];
        this.setState({ formData, errors });
    }
    onSubmit() {
        if (!this.state.wasConfiguredOnPageLoad) {
            // Users cannot install plugins like other integrations but we need the events for the funnel
            // we will treat a user saving a plugin that wasn't already configured as an installation event
            this.trackPluginEvent('integrations.installation_start');
        }
        let repo = this.state.formData.repo;
        repo = repo && (0, utils_1.parseRepo)(repo);
        const parsedFormData = Object.assign(Object.assign({}, this.state.formData), { repo });
        this.api.request(this.getPluginEndpoint(), {
            data: parsedFormData,
            method: 'PUT',
            success: this.onSaveSuccess.bind(this, data => {
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
                    errors: {},
                });
                this.trackPluginEvent('integrations.config_saved');
                if (!this.state.wasConfiguredOnPageLoad) {
                    this.trackPluginEvent('integrations.installation_complete');
                }
            }),
            error: this.onSaveError.bind(this, error => {
                this.setState({
                    errors: (error.responseJSON || {}).errors || {},
                });
            }),
            complete: this.onSaveComplete,
        });
    }
    fetchData() {
        this.api.request(this.getPluginEndpoint(), {
            success: data => {
                if (!data.config) {
                    this.setState({
                        rawData: data,
                    }, this.onLoadSuccess);
                    return;
                }
                let wasConfiguredOnPageLoad = false;
                const formData = {};
                const initialData = {};
                data.config.forEach((field) => {
                    formData[field.name] = field.value || field.defaultValue;
                    initialData[field.name] = field.value;
                    // for simplicity sake, we will consider a plugin was configured if we have any value that is stored in the DB
                    wasConfiguredOnPageLoad = wasConfiguredOnPageLoad || !!field.value;
                });
                this.setState({
                    fieldList: data.config,
                    formData,
                    initialData,
                    wasConfiguredOnPageLoad,
                    // call this here to prevent FormState.READY from being
                    // set before fieldList is
                }, this.onLoadSuccess);
            },
            error: this.onLoadError,
        });
    }
    render() {
        var _a;
        if (this.state.state === forms_1.FormState.LOADING) {
            return <loadingIndicator_1.default />;
        }
        const isSaving = this.state.state === forms_1.FormState.SAVING;
        const hasChanges = !(0, isEqual_1.default)(this.state.initialData, this.state.formData);
        const data = this.state.rawData;
        if (data.config_error) {
            let authUrl = data.auth_url;
            if (authUrl.indexOf('?') === -1) {
                authUrl += '?next=' + encodeURIComponent(document.location.pathname);
            }
            else {
                authUrl += '&next=' + encodeURIComponent(document.location.pathname);
            }
            return (<div className="m-b-1">
          <div className="alert alert-warning m-b-1">{data.config_error}</div>
          <a className="btn btn-primary" href={authUrl}>
            {(0, locale_1.t)('Associate Identity')}
          </a>
        </div>);
        }
        if (this.state.state === forms_1.FormState.ERROR && !this.state.fieldList) {
            return (<div className="alert alert-error m-b-1">
          {(0, locale_1.tct)('An unknown error occurred. Need help with this? [link:Contact support]', {
                    link: <a href="https://sentry.io/support/"/>,
                })}
        </div>);
        }
        const fieldList = this.state.fieldList;
        if (!(fieldList === null || fieldList === void 0 ? void 0 : fieldList.length)) {
            return null;
        }
        return (<forms_1.Form css={{ width: '100%' }} onSubmit={this.onSubmit} submitDisabled={isSaving || !hasChanges}>
        <Flex>
          {this.state.errors.__all__ && (<div className="alert alert-block alert-error">
              <ul>
                <li>{this.state.errors.__all__}</li>
              </ul>
            </div>)}
          {(_a = this.state.fieldList) === null || _a === void 0 ? void 0 : _a.map(f => this.renderField({
                config: f,
                formData: this.state.formData,
                formErrors: this.state.errors,
                onChange: this.changeField.bind(this, f.name),
            }))}
        </Flex>
      </forms_1.Form>);
    }
}
const Flex = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
`;
exports.default = PluginSettings;
//# sourceMappingURL=settings.jsx.map