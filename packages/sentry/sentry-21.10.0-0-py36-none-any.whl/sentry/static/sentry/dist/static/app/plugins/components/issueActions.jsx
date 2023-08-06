Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const groupActions_1 = (0, tslib_1.__importDefault)(require("app/actions/groupActions"));
const pluginComponentBase_1 = (0, tslib_1.__importDefault)(require("app/components/bases/pluginComponentBase"));
const forms_1 = require("app/components/forms");
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
class IssueActions extends pluginComponentBase_1.default {
    constructor(props, context) {
        super(props, context);
        this.loadOptionsForDependentField = (field) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const formData = this.getFormData();
            const groupId = this.getGroup().id;
            const pluginSlug = this.props.plugin.slug;
            const url = `/issues/${groupId}/plugins/${pluginSlug}/options/`;
            // find the fields that this field is dependent on
            const dependentFormValues = Object.fromEntries(field.depends.map(fieldKey => [fieldKey, formData[fieldKey]]));
            const query = Object.assign({ option_field: field.name }, dependentFormValues);
            try {
                this.setDependentFieldState(field.name, forms_1.FormState.LOADING);
                const result = yield this.api.requestPromise(url, { query });
                this.updateOptionsOfDependentField(field, result[field.name]);
                this.setDependentFieldState(field.name, forms_1.FormState.READY);
            }
            catch (err) {
                this.setDependentFieldState(field.name, forms_1.FormState.ERROR);
                this.errorHandler(err);
            }
        });
        this.updateOptionsOfDependentField = (field, choices) => {
            const formListKey = this.getFieldListKey();
            let fieldList = this.state[formListKey];
            if (!fieldList) {
                return;
            }
            // find the location of the field in our list and replace it
            const indexOfField = fieldList.findIndex(({ name }) => name === field.name);
            field = Object.assign(Object.assign({}, field), { choices });
            // make a copy of the array to avoid mutation
            fieldList = fieldList.slice();
            fieldList[indexOfField] = field;
            this.setState(prevState => (Object.assign(Object.assign({}, prevState), { [formListKey]: fieldList })));
        };
        this.resetOptionsOfDependentField = (field) => {
            this.updateOptionsOfDependentField(field, []);
            const formDataKey = this.getFormDataKey();
            const formData = Object.assign({}, this.state[formDataKey]);
            formData[field.name] = '';
            this.setState(prevState => (Object.assign(Object.assign({}, prevState), { [formDataKey]: formData })));
            this.setDependentFieldState(field.name, forms_1.FormState.DISABLED);
        };
        this.createIssue = this.onSave.bind(this, this.createIssue.bind(this));
        this.linkIssue = this.onSave.bind(this, this.linkIssue.bind(this));
        this.unlinkIssue = this.onSave.bind(this, this.unlinkIssue.bind(this));
        this.onSuccess = this.onSaveSuccess.bind(this, this.onSuccess.bind(this));
        this.errorHandler = this.onLoadError.bind(this, this.errorHandler.bind(this));
        this.state = Object.assign(Object.assign({}, this.state), { loading: ['link', 'create'].includes(this.props.actionType), state: ['link', 'create'].includes(this.props.actionType)
                ? forms_1.FormState.LOADING
                : forms_1.FormState.READY, createFormData: {}, linkFormData: {}, dependentFieldState: {} });
    }
    getGroup() {
        return this.props.group;
    }
    getProject() {
        return this.props.project;
    }
    getOrganization() {
        return this.props.organization;
    }
    getFieldListKey() {
        switch (this.props.actionType) {
            case 'link':
                return 'linkFieldList';
            case 'unlink':
                return 'unlinkFieldList';
            case 'create':
                return 'createFieldList';
            default:
                throw new Error('Unexpeced action type');
        }
    }
    getFormDataKey(actionType) {
        switch (actionType || this.props.actionType) {
            case 'link':
                return 'linkFormData';
            case 'unlink':
                return 'unlinkFormData';
            case 'create':
                return 'createFormData';
            default:
                throw new Error('Unexpeced action type');
        }
    }
    getFormData() {
        const key = this.getFormDataKey();
        return this.state[key] || {};
    }
    getFieldList() {
        const key = this.getFieldListKey();
        return this.state[key] || [];
    }
    componentDidMount() {
        const plugin = this.props.plugin;
        if (!plugin.issue && this.props.actionType !== 'unlink') {
            this.fetchData();
        }
    }
    getPluginCreateEndpoint() {
        return ('/issues/' + this.getGroup().id + '/plugins/' + this.props.plugin.slug + '/create/');
    }
    getPluginLinkEndpoint() {
        return ('/issues/' + this.getGroup().id + '/plugins/' + this.props.plugin.slug + '/link/');
    }
    getPluginUnlinkEndpoint() {
        return ('/issues/' + this.getGroup().id + '/plugins/' + this.props.plugin.slug + '/unlink/');
    }
    setDependentFieldState(fieldName, state) {
        const dependentFieldState = Object.assign(Object.assign({}, this.state.dependentFieldState), { [fieldName]: state });
        this.setState({ dependentFieldState });
    }
    getInputProps(field) {
        const props = {};
        // special logic for fields that have dependencies
        if (field.depends && field.depends.length > 0) {
            switch (this.state.dependentFieldState[field.name]) {
                case forms_1.FormState.LOADING:
                    props.isLoading = true;
                    props.readonly = true;
                    break;
                case forms_1.FormState.DISABLED:
                case forms_1.FormState.ERROR:
                    props.readonly = true;
                    break;
                default:
                    break;
            }
        }
        return props;
    }
    setError(error, defaultMessage) {
        let errorBody;
        if (error.status === 400 && error.responseJSON) {
            errorBody = error.responseJSON;
        }
        else {
            errorBody = { message: defaultMessage };
        }
        this.setState({ error: errorBody });
    }
    errorHandler(error) {
        const state = {
            loading: false,
        };
        if (error.status === 400 && error.responseJSON) {
            state.error = error.responseJSON;
        }
        else {
            state.error = { message: (0, locale_1.t)('An unknown error occurred.') };
        }
        this.setState(state);
    }
    onLoadSuccess() {
        super.onLoadSuccess();
        // dependent fields need to be set to disabled upon loading
        const fieldList = this.getFieldList();
        fieldList.forEach(field => {
            if (field.depends && field.depends.length > 0) {
                this.setDependentFieldState(field.name, forms_1.FormState.DISABLED);
            }
        });
    }
    fetchData() {
        if (this.props.actionType === 'create') {
            this.api.request(this.getPluginCreateEndpoint(), {
                success: data => {
                    const createFormData = {};
                    data.forEach(field => {
                        createFormData[field.name] = field.default;
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
        }
        else if (this.props.actionType === 'link') {
            this.api.request(this.getPluginLinkEndpoint(), {
                success: data => {
                    const linkFormData = {};
                    data.forEach(field => {
                        linkFormData[field.name] = field.default;
                    });
                    this.setState({
                        linkFieldList: data,
                        error: undefined,
                        loading: false,
                        linkFormData,
                    }, this.onLoadSuccess);
                },
                error: this.errorHandler,
            });
        }
    }
    onSuccess(data) {
        groupActions_1.default.updateSuccess(null, [this.getGroup().id], { stale: true });
        this.props.onSuccess && this.props.onSuccess(data);
    }
    createIssue() {
        this.api.request(this.getPluginCreateEndpoint(), {
            data: this.state.createFormData,
            success: this.onSuccess,
            error: this.onSaveError.bind(this, error => {
                this.setError(error, (0, locale_1.t)('There was an error creating the issue.'));
            }),
            complete: this.onSaveComplete,
        });
    }
    linkIssue() {
        this.api.request(this.getPluginLinkEndpoint(), {
            data: this.state.linkFormData,
            success: this.onSuccess,
            error: this.onSaveError.bind(this, error => {
                this.setError(error, (0, locale_1.t)('There was an error linking the issue.'));
            }),
            complete: this.onSaveComplete,
        });
    }
    unlinkIssue() {
        this.api.request(this.getPluginUnlinkEndpoint(), {
            success: this.onSuccess,
            error: this.onSaveError.bind(this, error => {
                this.setError(error, (0, locale_1.t)('There was an error unlinking the issue.'));
            }),
            complete: this.onSaveComplete,
        });
    }
    changeField(action, name, value) {
        var _a;
        const formDataKey = this.getFormDataKey(action);
        // copy so we don't mutate
        const formData = Object.assign({}, this.state[formDataKey]);
        const fieldList = this.getFieldList();
        formData[name] = value;
        let callback = () => { };
        // only works with one impacted field
        const impactedField = fieldList.find(({ depends }) => {
            if (!depends || !depends.length) {
                return false;
            }
            // must be dependent on the field we just set
            return depends.includes(name);
        });
        if (impactedField) {
            // if every dependent field is set, then search
            if (!((_a = impactedField.depends) === null || _a === void 0 ? void 0 : _a.some(dependentField => !formData[dependentField]))) {
                callback = () => this.loadOptionsForDependentField(impactedField);
            }
            else {
                // otherwise reset the options
                callback = () => this.resetOptionsOfDependentField(impactedField);
            }
        }
        this.setState(prevState => (Object.assign(Object.assign({}, prevState), { [formDataKey]: formData })), callback);
    }
    renderForm() {
        switch (this.props.actionType) {
            case 'create':
                if (this.state.createFieldList) {
                    return (<forms_1.Form onSubmit={this.createIssue} submitLabel={(0, locale_1.t)('Create Issue')} footerClass="">
              {this.state.createFieldList.map(field => {
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
                                    config: Object.assign(Object.assign({}, field), this.getInputProps(field)),
                                    formData: this.state.createFormData,
                                    onChange: this.changeField.bind(this, 'create', field.name),
                                })}
                  </div>);
                        })}
            </forms_1.Form>);
                }
                break;
            case 'link':
                if (this.state.linkFieldList) {
                    return (<forms_1.Form onSubmit={this.linkIssue} submitLabel={(0, locale_1.t)('Link Issue')} footerClass="">
              {this.state.linkFieldList.map(field => {
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
                                    config: Object.assign(Object.assign({}, field), this.getInputProps(field)),
                                    formData: this.state.linkFormData,
                                    onChange: this.changeField.bind(this, 'link', field.name),
                                })}
                  </div>);
                        })}
            </forms_1.Form>);
                }
                break;
            case 'unlink':
                return (<div>
            <p>{(0, locale_1.t)('Are you sure you want to unlink this issue?')}</p>
            <button onClick={this.unlinkIssue} className="btn btn-danger">
              {(0, locale_1.t)('Unlink Issue')}
            </button>
          </div>);
            default:
                return null;
        }
        return null;
    }
    getPluginConfigureUrl() {
        const org = this.getOrganization();
        const project = this.getProject();
        const plugin = this.props.plugin;
        return '/' + org.slug + '/' + project.slug + '/settings/plugins/' + plugin.slug;
    }
    renderError() {
        var _a;
        const error = this.state.error;
        if (!error) {
            return null;
        }
        if (error.error_type === 'auth') {
            let authUrl = error.auth_url;
            if ((authUrl === null || authUrl === void 0 ? void 0 : authUrl.indexOf('?')) === -1) {
                authUrl += '?next=' + encodeURIComponent(document.location.pathname);
            }
            else {
                authUrl += '&next=' + encodeURIComponent(document.location.pathname);
            }
            return (<div>
          <div className="alert alert-warning m-b-1">
            {'You need to associate an identity with ' +
                    this.props.plugin.name +
                    ' before you can create issues with this service.'}
          </div>
          <a className="btn btn-primary" href={authUrl}>
            Associate Identity
          </a>
        </div>);
        }
        else if (error.error_type === 'config') {
            return (<div className="alert alert-block">
          {!error.has_auth_configured ? (<div>
              <p>
                {'Your server administrator will need to configure authentication with '}
                <strong>{this.props.plugin.name}</strong>
                {' before you can use this integration.'}
              </p>
              <p>The following settings must be configured:</p>
              <ul>
                {(_a = error.required_auth_settings) === null || _a === void 0 ? void 0 : _a.map((setting, i) => (<li key={i}>
                    <code>{setting}</code>
                  </li>))}
              </ul>
            </div>) : (<p>
              You still need to{' '}
              <a href={this.getPluginConfigureUrl()}>configure this plugin</a> before you
              can use it.
            </p>)}
        </div>);
        }
        else if (error.error_type === 'validation') {
            const errors = [];
            for (const name in error.errors) {
                errors.push(<p key={name}>{error.errors[name]}</p>);
            }
            return <div className="alert alert-error alert-block">{errors}</div>;
        }
        else if (error.message) {
            return (<div className="alert alert-error alert-block">
          <p>{error.message}</p>
        </div>);
        }
        return <loadingError_1.default />;
    }
    render() {
        if (this.state.state === forms_1.FormState.LOADING) {
            return <loadingIndicator_1.default />;
        }
        return (<div>
        {this.renderError()}
        {this.renderForm()}
      </div>);
    }
}
exports.default = IssueActions;
//# sourceMappingURL=issueActions.jsx.map