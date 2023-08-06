Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const sentryAppInstallations_1 = require("app/actionCreators/sentryAppInstallations");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const organizationAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/organizationAvatar"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const sentryAppDetailsModal_1 = (0, tslib_1.__importDefault)(require("app/components/modals/sentryAppDetailsModal"));
const narrowLayout_1 = (0, tslib_1.__importDefault)(require("app/components/narrowLayout"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const integrationUtil_1 = require("app/utils/integrationUtil");
const queryString_1 = require("app/utils/queryString");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
class SentryAppExternalInstallation extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.hasAccess = (org) => org.access.includes('org:integrations');
        this.onClose = () => {
            // if we came from somewhere, go back there. Otherwise, back to the integrations page
            const { selectedOrgSlug } = this.state;
            const newUrl = document.referrer || `/settings/${selectedOrgSlug}/integrations/`;
            window.location.assign(newUrl);
        };
        this.onInstall = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, sentryApp } = this.state;
            if (!organization || !sentryApp) {
                return undefined;
            }
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.installation_start', {
                integration_type: 'sentry_app',
                integration: sentryApp.slug,
                view: 'external_install',
                integration_status: sentryApp.status,
                organization,
            });
            const install = yield (0, sentryAppInstallations_1.installSentryApp)(this.api, organization.slug, sentryApp);
            // installation is complete if the status is installed
            if (install.status === 'installed') {
                (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.installation_complete', {
                    integration_type: 'sentry_app',
                    integration: sentryApp.slug,
                    view: 'external_install',
                    integration_status: sentryApp.status,
                    organization,
                });
            }
            if (sentryApp.redirectUrl) {
                const queryParams = {
                    installationId: install.uuid,
                    code: install.code,
                    orgSlug: organization.slug,
                };
                const redirectUrl = (0, queryString_1.addQueryParamsToExistingUrl)(sentryApp.redirectUrl, queryParams);
                return window.location.assign(redirectUrl);
            }
            return this.onClose();
        });
        this.onSelectOrg = (orgSlug) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ selectedOrgSlug: orgSlug, reloading: true });
            try {
                const [organization, installations] = yield Promise.all([
                    this.api.requestPromise(`/organizations/${orgSlug}/`),
                    this.api.requestPromise(`/organizations/${orgSlug}/sentry-app-installations/`),
                ]);
                const isInstalled = installations
                    .map(install => install.app.slug)
                    .includes(this.sentryAppSlug);
                // all state fields should be set at the same time so analytics in SentryAppDetailsModal works properly
                this.setState({ organization, isInstalled, reloading: false });
            }
            catch (err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to retrieve organization or integration details'));
                this.setState({ reloading: false });
            }
        });
        this.onRequestSuccess = ({ stateKey, data }) => {
            // if only one org, we can immediately update our selected org
            if (stateKey === 'organizations' && data.length === 1) {
                this.onSelectOrg(data[0].slug);
            }
        };
    }
    getDefaultState() {
        const state = super.getDefaultState();
        return Object.assign(Object.assign({}, state), { selectedOrgSlug: null, organization: null, organizations: [], reloading: false });
    }
    getEndpoints() {
        return [
            ['organizations', '/organizations/'],
            ['sentryApp', `/sentry-apps/${this.sentryAppSlug}/`],
        ];
    }
    getTitle() {
        return (0, locale_1.t)('Choose Installation Organization');
    }
    get sentryAppSlug() {
        return this.props.params.sentryAppSlug;
    }
    get isSingleOrg() {
        return this.state.organizations.length === 1;
    }
    get isSentryAppInternal() {
        const { sentryApp } = this.state;
        return sentryApp && sentryApp.status === 'internal';
    }
    get isSentryAppUnavailableForOrg() {
        var _a;
        const { sentryApp, selectedOrgSlug } = this.state;
        // if the app is unpublished for a different org
        return (selectedOrgSlug &&
            ((_a = sentryApp === null || sentryApp === void 0 ? void 0 : sentryApp.owner) === null || _a === void 0 ? void 0 : _a.slug) !== selectedOrgSlug &&
            sentryApp.status === 'unpublished');
    }
    get disableInstall() {
        const { reloading, isInstalled } = this.state;
        return isInstalled || reloading || this.isSentryAppUnavailableForOrg;
    }
    getOptions() {
        return this.state.organizations.map(org => ({
            value: org.slug,
            label: (<div key={org.slug}>
          <organizationAvatar_1.default organization={org}/>
          <OrgNameHolder>{org.slug}</OrgNameHolder>
        </div>),
        }));
    }
    renderInternalAppError() {
        const { sentryApp } = this.state;
        return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
        {(0, locale_1.tct)('Integration [sentryAppName] is an internal integration. Internal integrations are automatically installed', {
                sentryAppName: <strong>{sentryApp.name}</strong>,
            })}
      </alert_1.default>);
    }
    checkAndRenderError() {
        var _a, _b;
        const { organization, selectedOrgSlug, isInstalled, sentryApp } = this.state;
        if (selectedOrgSlug && organization && !this.hasAccess(organization)) {
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          <p>
            {(0, locale_1.tct)(`You do not have permission to install integrations in
          [organization]. Ask an organization owner or manager to
          visit this page to finish installing this integration.`, { organization: <strong>{organization.slug}</strong> })}
          </p>
          <InstallLink>{window.location.href}</InstallLink>
        </alert_1.default>);
        }
        if (isInstalled && organization) {
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {(0, locale_1.tct)('Integration [sentryAppName] already installed for [organization]', {
                    organization: <strong>{organization.name}</strong>,
                    sentryAppName: <strong>{sentryApp.name}</strong>,
                })}
        </alert_1.default>);
        }
        if (this.isSentryAppUnavailableForOrg) {
            // use the slug of the owner if we have it, otherwise use 'another organization'
            const ownerSlug = (_b = (_a = sentryApp === null || sentryApp === void 0 ? void 0 : sentryApp.owner) === null || _a === void 0 ? void 0 : _a.slug) !== null && _b !== void 0 ? _b : 'another organization';
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {(0, locale_1.tct)('Integration [sentryAppName] is an unpublished integration for [otherOrg]. An unpublished integration can only be installed on the organization which created it.', {
                    sentryAppName: <strong>{sentryApp.name}</strong>,
                    otherOrg: <strong>{ownerSlug}</strong>,
                })}
        </alert_1.default>);
        }
        return null;
    }
    renderMultiOrgView() {
        const { selectedOrgSlug, sentryApp } = this.state;
        return (<div>
        <p>
          {(0, locale_1.tct)('Please pick a specific [organization:organization] to install [sentryAppName]', {
                organization: <strong />,
                sentryAppName: <strong>{sentryApp.name}</strong>,
            })}
        </p>
        <field_1.default label={(0, locale_1.t)('Organization')} inline={false} stacked required>
          {() => (<selectControl_1.default onChange={({ value }) => this.onSelectOrg(value)} value={selectedOrgSlug} placeholder={(0, locale_1.t)('Select an organization')} options={this.getOptions()}/>)}
        </field_1.default>
      </div>);
    }
    renderSingleOrgView() {
        const { organizations, sentryApp } = this.state;
        // pull the name out of organizations since state.organization won't be loaded initially
        const organizationName = organizations[0].name;
        return (<div>
        <p>
          {(0, locale_1.tct)('You are installing [sentryAppName] for organization [organization]', {
                organization: <strong>{organizationName}</strong>,
                sentryAppName: <strong>{sentryApp.name}</strong>,
            })}
        </p>
      </div>);
    }
    renderMainContent() {
        const { organization, sentryApp } = this.state;
        return (<div>
        <OrgViewHolder>
          {this.isSingleOrg ? this.renderSingleOrgView() : this.renderMultiOrgView()}
        </OrgViewHolder>
        {this.checkAndRenderError()}
        {organization && (<sentryAppDetailsModal_1.default sentryApp={sentryApp} organization={organization} onInstall={this.onInstall} closeModal={this.onClose} isInstalled={this.disableInstall}/>)}
      </div>);
    }
    renderBody() {
        return (<narrowLayout_1.default>
        <Content>
          <h3>{(0, locale_1.t)('Finish integration installation')}</h3>
          {this.isSentryAppInternal
                ? this.renderInternalAppError()
                : this.renderMainContent()}
        </Content>
      </narrowLayout_1.default>);
    }
}
exports.default = SentryAppExternalInstallation;
const InstallLink = (0, styled_1.default)('pre') `
  margin-bottom: 0;
  background: #fbe3e1;
`;
const OrgNameHolder = (0, styled_1.default)('span') `
  margin-left: 5px;
`;
const Content = (0, styled_1.default)('div') `
  margin-bottom: 40px;
`;
const OrgViewHolder = (0, styled_1.default)('div') `
  margin-bottom: 20px;
`;
//# sourceMappingURL=sentryAppExternalInstallation.jsx.map