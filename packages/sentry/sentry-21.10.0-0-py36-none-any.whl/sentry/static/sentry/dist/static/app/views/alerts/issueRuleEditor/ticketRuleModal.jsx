Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const abstractExternalIssueForm_1 = (0, tslib_1.__importDefault)(require("app/components/externalIssues/abstractExternalIssueForm"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class TicketRuleModal extends abstractExternalIssueForm_1.default {
    constructor() {
        super(...arguments);
        this.handleReceiveIntegrationDetails = (integrationDetails) => {
            this.setState({
                issueConfigFieldsCache: integrationDetails[this.getConfigName()],
            });
        };
        /**
         * Get a list of formFields names with valid config data.
         */
        this.getValidAndSavableFieldNames = () => {
            const { issueConfigFieldsCache } = this.state;
            return (issueConfigFieldsCache || [])
                .filter(field => field.hasOwnProperty('name'))
                .map(field => field.name);
        };
        /**
         * Clean up the form data before saving it to state.
         */
        this.cleanData = (data) => {
            const { instance } = this.props;
            const { issueConfigFieldsCache } = this.state;
            const names = this.getValidAndSavableFieldNames();
            const formData = {};
            if (instance === null || instance === void 0 ? void 0 : instance.hasOwnProperty('integration')) {
                formData.integration = instance.integration;
            }
            formData.dynamic_form_fields = issueConfigFieldsCache;
            for (const [key, value] of Object.entries(data)) {
                if (names.includes(key)) {
                    formData[key] = value;
                }
            }
            return formData;
        };
        this.onFormSubmit = (data, _success, _error, e, model) => {
            const { onSubmitAction, closeModal } = this.props;
            const { fetchedFieldOptionsCache } = this.state;
            // This is a "fake form", so don't actually POST to an endpoint.
            e.preventDefault();
            e.stopPropagation();
            if (model.validateForm()) {
                onSubmitAction(this.cleanData(data), fetchedFieldOptionsCache);
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Changes applied.'));
                closeModal();
            }
        };
        this.getFormProps = () => {
            const { closeModal } = this.props;
            return Object.assign(Object.assign({}, this.getDefaultFormProps()), { cancelLabel: (0, locale_1.t)('Close'), onCancel: closeModal, onSubmit: this.onFormSubmit, submitLabel: (0, locale_1.t)('Apply Changes') });
        };
        /**
         * Set the initial data from the Rule, replace `title` and `description` with
         * disabled inputs, and use the cached dynamic choices.
         */
        this.cleanFields = () => {
            const { instance } = this.props;
            const fields = [
                {
                    name: 'title',
                    label: 'Title',
                    type: 'string',
                    default: 'This will be the same as the Sentry Issue.',
                    disabled: true,
                },
                {
                    name: 'description',
                    label: 'Description',
                    type: 'string',
                    default: 'This will be generated from the Sentry Issue details.',
                    disabled: true,
                },
            ];
            return fields.concat(this.getCleanedFields()
                // Skip fields if they already exist.
                .filter(field => !fields.map(f => f.name).includes(field.name))
                .map(field => {
                // Overwrite defaults from cache.
                if (instance.hasOwnProperty(field.name)) {
                    field.default = instance[field.name] || field.default;
                }
                return field;
            }));
        };
        this.renderBodyText = () => {
            // `ticketType` already includes indefinite article.
            const { ticketType, link } = this.props;
            return (<BodyText>
        {(0, locale_1.tct)('When this alert is triggered [ticketType] will be ' +
                    'created with the following fields. It will also [linkToDocs] ' +
                    'with the new Sentry Issue.', {
                    linkToDocs: <externalLink_1.default href={link}>{(0, locale_1.t)('stay in sync')}</externalLink_1.default>,
                    ticketType,
                })}
      </BodyText>);
        };
    }
    getDefaultState() {
        const { instance } = this.props;
        const issueConfigFieldsCache = Object.values((instance === null || instance === void 0 ? void 0 : instance.dynamic_form_fields) || {});
        return Object.assign(Object.assign({}, super.getDefaultState()), { fetchedFieldOptionsCache: Object.fromEntries(issueConfigFieldsCache.map(field => [field.name, field.choices])), issueConfigFieldsCache });
    }
    getEndpoints() {
        const { instance } = this.props;
        const query = (instance.dynamic_form_fields || [])
            .filter(field => field.updatesForm)
            .filter(field => instance.hasOwnProperty(field.name))
            .reduce((accumulator, { name }) => {
            accumulator[name] = instance[name];
            return accumulator;
        }, { action: 'create' });
        return [['integrationDetails', this.getEndPointString(), { query }]];
    }
    getEndPointString() {
        const { instance, organization } = this.props;
        return `/organizations/${organization.slug}/integrations/${instance.integration}/`;
    }
    render() {
        return this.renderForm(this.cleanFields());
    }
}
const BodyText = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(3)};
`;
exports.default = TicketRuleModal;
//# sourceMappingURL=ticketRuleModal.jsx.map