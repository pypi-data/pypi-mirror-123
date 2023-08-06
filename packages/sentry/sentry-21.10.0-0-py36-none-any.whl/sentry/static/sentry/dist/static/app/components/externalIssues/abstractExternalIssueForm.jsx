Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const queryString = (0, tslib_1.__importStar)(require("query-string"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const locale_1 = require("app/locale");
const fieldFromConfig_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/fieldFromConfig"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const DEBOUNCE_MS = 200;
/**
 * @abstract
 */
class AbstractExternalIssueForm extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldRenderBadRequests = true;
        this.refetchConfig = () => {
            const { action, dynamicFieldValues } = this.state;
            const query = Object.assign({ action }, dynamicFieldValues);
            const endpoint = this.getEndPointString();
            this.api.request(endpoint, {
                method: 'GET',
                query,
                success: (data, _, resp) => {
                    this.handleRequestSuccess({ stateKey: 'integrationDetails', data, resp }, true);
                },
                error: error => {
                    this.handleError(error, ['integrationDetails', endpoint, null, null]);
                },
            });
        };
        this.getConfigName = () => {
            // Explicitly returning a non-interpolated string for clarity.
            const { action } = this.state;
            switch (action) {
                case 'create':
                    return 'createIssueConfig';
                case 'link':
                    return 'linkIssueConfig';
                default:
                    throw new Error('illegal action');
            }
        };
        /**
         * Convert IntegrationIssueConfig to an object that maps field names to the
         * values of fields where `updatesFrom` is true. This function prefers to read
         * configs from its parameters and otherwise falls back to reading from state.
         * @param integrationDetailsParam
         * @returns Object of field names to values.
         */
        this.getDynamicFields = (integrationDetailsParam) => {
            const { integrationDetails: integrationDetailsFromState } = this.state;
            const integrationDetails = integrationDetailsParam || integrationDetailsFromState;
            const config = (integrationDetails || {})[this.getConfigName()];
            return Object.fromEntries((config || [])
                .filter((field) => field.updatesForm)
                .map((field) => [field.name, field.default || null]));
        };
        this.onRequestSuccess = ({ stateKey, data }) => {
            if (stateKey === 'integrationDetails') {
                this.handleReceiveIntegrationDetails(data);
                this.setState({
                    dynamicFieldValues: this.getDynamicFields(data),
                });
            }
        };
        /**
         * If this field should updateFrom, updateForm. Otherwise, do nothing.
         */
        this.onFieldChange = (label, value) => {
            const { dynamicFieldValues } = this.state;
            const dynamicFields = this.getDynamicFields();
            if (dynamicFields.hasOwnProperty(label) && dynamicFieldValues) {
                dynamicFieldValues[label] = value;
                this.setState({
                    dynamicFieldValues,
                    reloading: true,
                    error: false,
                    remainingRequests: 1,
                }, this.refetchConfig);
            }
        };
        /**
         * For fields with dynamic fields, cache the fetched choices.
         */
        this.updateFetchedFieldOptionsCache = (field, result) => {
            const { fetchedFieldOptionsCache } = this.state;
            this.setState({
                fetchedFieldOptionsCache: Object.assign(Object.assign({}, fetchedFieldOptionsCache), { [field.name]: result.map(obj => [obj.value, obj.label]) }),
            });
        };
        /**
         * Get the list of options for a field via debounced API call. For example,
         * the list of users that match the input string. The Promise rejects if there
         * are any errors.
         */
        this.getOptions = (field, input) => new Promise((resolve, reject) => {
            if (!input) {
                return resolve(this.getDefaultOptions(field));
            }
            return this.debouncedOptionLoad(field, input, (err, result) => {
                if (err) {
                    reject(err);
                }
                else {
                    this.updateFetchedFieldOptionsCache(field, result);
                    resolve(result);
                }
            });
        });
        this.debouncedOptionLoad = (0, debounce_1.default)((field, input, cb) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { dynamicFieldValues } = this.state;
            const query = queryString.stringify(Object.assign(Object.assign({}, dynamicFieldValues), { field: field.name, query: input }));
            const url = field.url || '';
            const separator = url.includes('?') ? '&' : '?';
            // We can't use the API client here since the URL is not scoped under the
            // API endpoints (which the client prefixes)
            try {
                const response = yield fetch(url + separator + query);
                cb(null, response.ok ? yield response.json() : []);
            }
            catch (err) {
                cb(err);
            }
        }), DEBOUNCE_MS, { trailing: true });
        this.getDefaultOptions = (field) => {
            const choices = field.choices || [];
            return choices.map(([value, label]) => ({ value, label }));
        };
        /**
         * If this field is an async select (field.url is not null), add async props.
         */
        this.getFieldProps = (field) => field.url
            ? {
                async: true,
                autoload: true,
                cache: false,
                loadOptions: (input) => this.getOptions(field, input),
                defaultOptions: this.getDefaultOptions(field),
                onBlurResetsInput: false,
                onCloseResetsInput: false,
                onSelectResetsInput: false,
            }
            : {};
        // Abstract methods.
        this.handleReceiveIntegrationDetails = (_data) => {
            // Do nothing.
        };
        this.renderNavTabs = () => null;
        this.renderBodyText = () => null;
        this.getTitle = () => (0, locale_1.tct)('Issue Link Settings', {});
        this.getFormProps = () => {
            throw new Error("Method 'getFormProps()' must be implemented.");
        };
        this.getDefaultFormProps = () => {
            return {
                footerClass: 'modal-footer',
                onFieldChange: this.onFieldChange,
                submitDisabled: this.state.reloading,
                // Other form props implemented by child classes.
            };
        };
        this.getCleanedFields = () => {
            const { fetchedFieldOptionsCache, integrationDetails } = this.state;
            const configsFromAPI = (integrationDetails || {})[this.getConfigName()];
            return (configsFromAPI || []).map(field => {
                const fieldCopy = Object.assign({}, field);
                // Overwrite choices from cache.
                if (fetchedFieldOptionsCache === null || fetchedFieldOptionsCache === void 0 ? void 0 : fetchedFieldOptionsCache.hasOwnProperty(field.name)) {
                    fieldCopy.choices = fetchedFieldOptionsCache[field.name];
                }
                return fieldCopy;
            });
        };
        this.renderForm = (formFields) => {
            const initialData = (formFields || []).reduce((accumulator, field) => {
                accumulator[field.name] =
                    // Passing an empty array breaks MultiSelect.
                    field.multiple && field.default === [] ? '' : field.default;
                return accumulator;
            }, {});
            const { Header, Body } = this.props;
            return (<React.Fragment>
        <Header closeButton>{this.getTitle()}</Header>
        {this.renderNavTabs()}
        <Body>
          {this.shouldRenderLoading() ? (this.renderLoading()) : (<React.Fragment>
              {this.renderBodyText()}
              <form_1.default initialData={initialData} {...this.getFormProps()}>
                {(formFields || [])
                        .filter((field) => field.hasOwnProperty('name'))
                        .map(fields => (Object.assign(Object.assign({}, fields), { noOptionsMessage: () => 'No options. Type to search.' })))
                        .map(field => (<fieldFromConfig_1.default disabled={this.state.reloading} field={field} flexibleControlStateSize inline={false} key={`${field.name}-${field.default}-${field.required}`} stacked {...this.getFieldProps(field)}/>))}
              </form_1.default>
            </React.Fragment>)}
        </Body>
      </React.Fragment>);
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { action: 'create', dynamicFieldValues: null, fetchedFieldOptionsCache: {}, integrationDetails: null });
    }
    getEndPointString() {
        throw new Error("Method 'getEndPointString()' must be implemented.");
    }
    renderComponent() {
        return this.state.error
            ? this.renderError(new Error('Unable to load all required endpoints'))
            : this.renderBody();
    }
}
exports.default = AbstractExternalIssueForm;
//# sourceMappingURL=abstractExternalIssueForm.jsx.map