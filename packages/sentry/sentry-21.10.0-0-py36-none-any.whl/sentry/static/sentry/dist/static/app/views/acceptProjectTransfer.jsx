Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const narrowLayout_1 = (0, tslib_1.__importDefault)(require("app/components/narrowLayout"));
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
class AcceptProjectTransfer extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSubmit = formData => {
            this.api.request('/accept-transfer/', {
                method: 'POST',
                data: {
                    data: this.props.location.query.data,
                    organization: formData.organization,
                },
                success: () => {
                    const orgSlug = formData.organization;
                    this.props.router.push(`/${orgSlug}`);
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Project successfully transferred'));
                },
                error: error => {
                    const errorMsg = error && error.responseJSON && typeof error.responseJSON.detail === 'string'
                        ? error.responseJSON.detail
                        : '';
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to transfer project') + errorMsg ? `: ${errorMsg}` : '');
                },
            });
        };
    }
    getEndpoints() {
        const query = this.props.location.query;
        return [['transferDetails', '/accept-transfer/', { query }]];
    }
    getTitle() {
        return (0, locale_1.t)('Accept Project Transfer');
    }
    renderError(error) {
        let disableLog = false;
        // Check if there is an error message with `transferDetails` endpoint
        // If so, show as toast and ignore, otherwise log to sentry
        if (error && error.responseJSON && typeof error.responseJSON.detail === 'string') {
            (0, indicator_1.addErrorMessage)(error.responseJSON.detail);
            disableLog = true;
        }
        return super.renderError(error, disableLog);
    }
    renderBody() {
        var _a;
        const { transferDetails } = this.state;
        const options = transferDetails === null || transferDetails === void 0 ? void 0 : transferDetails.organizations.map(org => ({
            label: org.slug,
            value: org.slug,
        }));
        const organization = (_a = options === null || options === void 0 ? void 0 : options[0]) === null || _a === void 0 ? void 0 : _a.value;
        return (<narrowLayout_1.default>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Approve Transfer Project Request')}/>
        <p>
          {(0, locale_1.tct)('Projects must be transferred to a specific [organization]. ' +
                'You can grant specific teams access to the project later under the [projectSettings]. ' +
                '(Note that granting access to at least one team is necessary for the project to ' +
                'appear in all parts of the UI.)', {
                organization: <strong>{(0, locale_1.t)('Organization')}</strong>,
                projectSettings: <strong>{(0, locale_1.t)('Project Settings')}</strong>,
            })}
        </p>
        {transferDetails && (<p>
            {(0, locale_1.tct)('Please select which [organization] you want for the project [project].', {
                    organization: <strong>{(0, locale_1.t)('Organization')}</strong>,
                    project: transferDetails.project.slug,
                })}
          </p>)}
        <form_1.default onSubmit={this.handleSubmit} submitLabel={(0, locale_1.t)('Transfer Project')} submitPriority="danger" initialData={organization ? { organization } : undefined}>
          <selectField_1.default options={options} label={(0, locale_1.t)('Organization')} name="organization" style={{ borderBottom: 'none' }}/>
        </form_1.default>
      </narrowLayout_1.default>);
    }
}
exports.default = AcceptProjectTransfer;
//# sourceMappingURL=acceptProjectTransfer.jsx.map