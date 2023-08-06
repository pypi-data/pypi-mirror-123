Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const locale_1 = require("app/locale");
const forms_1 = require("app/views/settings/components/forms");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
class IntegrationExternalMappingForm extends react_1.Component {
    get initialData() {
        const { integration, mapping } = this.props;
        return Object.assign({ externalName: '', userId: '', teamId: '', sentryName: '', provider: integration.provider.key, integrationId: integration.id }, (0, pick_1.default)(mapping, ['externalName', 'userId', 'sentryName', 'teamId']));
    }
    get formFields() {
        const { type, sentryNamesMapper, url, mapping } = this.props;
        const optionMapper = sentryNames => sentryNames.map(({ name, id }) => ({ value: id, label: name }));
        const fields = [
            {
                name: 'externalName',
                type: 'string',
                required: true,
                label: (0, locale_1.tct)('External [type]', { type: (0, capitalize_1.default)(type) }),
                placeholder: (0, locale_1.t)(`${type === 'team' ? '@org/teamname' : '@username'}`),
            },
        ];
        if (type === 'user') {
            fields.push({
                name: 'userId',
                type: 'select_async',
                required: true,
                label: (0, locale_1.tct)('Sentry [type]', { type: (0, capitalize_1.default)(type) }),
                placeholder: (0, locale_1.t)(`Choose your Sentry User`),
                url,
                onResults: result => {
                    var _a, _b;
                    // For organizations with >100 users, we want to make sure their
                    // saved mapping gets populated in the results if it wouldn't have
                    // been in the initial 100 API results, which is why we add it here
                    if (mapping && !result.find(({ user }) => user.id === mapping.userId)) {
                        result = [{ id: mapping.userId, name: mapping.sentryName }, ...result];
                    }
                    (_b = (_a = this.props).onResults) === null || _b === void 0 ? void 0 : _b.call(_a, result);
                    return optionMapper(sentryNamesMapper(result));
                },
            });
        }
        if (type === 'team') {
            fields.push({
                name: 'teamId',
                type: 'select_async',
                required: true,
                label: (0, locale_1.tct)('Sentry [type]', { type: (0, capitalize_1.default)(type) }),
                placeholder: (0, locale_1.t)(`Choose your Sentry Team`),
                url,
                onResults: result => {
                    var _a, _b;
                    // For organizations with >100 teams, we want to make sure their
                    // saved mapping gets populated in the results if it wouldn't have
                    // been in the initial 100 API results, which is why we add it here
                    if (mapping && !result.find(({ id }) => id === mapping.teamId)) {
                        result = [{ id: mapping.teamId, name: mapping.sentryName }, ...result];
                    }
                    // The team needs `this.props.onResults` so that we have team slug
                    // when a user submits a team mapping, the endpoint needs the slug
                    // as a path param: /teams/${organization.slug}/${team.slug}/external-teams/
                    (_b = (_a = this.props).onResults) === null || _b === void 0 ? void 0 : _b.call(_a, result);
                    return optionMapper(sentryNamesMapper(result));
                },
            });
        }
        return fields;
    }
    render() {
        const { onSubmitSuccess, onCancel, mapping, baseEndpoint, onSubmit } = this.props;
        // endpoint changes if we are making a new row or updating an existing one
        const endpoint = !baseEndpoint
            ? undefined
            : mapping
                ? `${baseEndpoint}${mapping.id}/`
                : baseEndpoint;
        const apiMethod = !baseEndpoint ? undefined : mapping ? 'PUT' : 'POST';
        return (<FormWrapper>
        <form_1.default requireChanges onSubmitSuccess={onSubmitSuccess} initialData={this.initialData} apiEndpoint={endpoint} apiMethod={apiMethod} onCancel={onCancel} onSubmit={onSubmit}>
          {this.formFields.map(field => (<forms_1.FieldFromConfig key={field.name} field={field} inline={false} stacked flexibleControlStateSize/>))}
        </form_1.default>
      </FormWrapper>);
    }
}
exports.default = IntegrationExternalMappingForm;
// Prevents errors from appearing off the modal
const FormWrapper = (0, styled_1.default)('div') `
  position: relative;
`;
//# sourceMappingURL=integrationExternalMappingForm.jsx.map