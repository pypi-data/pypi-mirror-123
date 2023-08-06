Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_select_1 = require("react-select");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("@sentry/utils");
const indicator_1 = require("app/actionCreators/indicator");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const narrowLayout_1 = (0, tslib_1.__importDefault)(require("app/components/narrowLayout"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const integrationUtil_1 = require("app/utils/integrationUtil");
const marked_1 = require("app/utils/marked");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const addIntegration_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/addIntegration"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
class IntegrationOrganizationLink extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.trackIntegrationAnalytics = (eventName, startSession) => {
            const { organization, provider } = this.state;
            // should have these set but need to make TS happy
            if (!organization || !provider) {
                return;
            }
            (0, integrationUtil_1.trackIntegrationAnalytics)(eventName, {
                integration_type: 'first_party',
                integration: provider.key,
                // We actually don't know if it's installed but neither does the user in the view and multiple installs is possible
                already_installed: false,
                view: 'external_install',
                organization,
            }, { startSession: !!startSession });
        };
        this.getOrgBySlug = (orgSlug) => {
            return this.state.organizations.find((org) => org.slug === orgSlug);
        };
        this.onSelectOrg = ({ value: orgSlug }) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ selectedOrgSlug: orgSlug, reloading: true, organization: undefined });
            try {
                const [organization, { providers }] = yield Promise.all([
                    this.api.requestPromise(`/organizations/${orgSlug}/`),
                    this.api.requestPromise(`/organizations/${orgSlug}/config/integrations/?provider_key=${this.integrationSlug}`),
                ]);
                // should never happen with a valid provider
                if (providers.length === 0) {
                    throw new Error('Invalid provider');
                }
                this.setState({ organization, reloading: false, provider: providers[0] }, this.trackOpened);
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to retrieve organization or integration details'));
                this.setState({ reloading: false });
            }
        });
        this.hasAccess = () => {
            const { organization } = this.state;
            return organization === null || organization === void 0 ? void 0 : organization.access.includes('org:integrations');
        };
        // used with Github to redirect to the the integration detail
        this.onInstallWithInstallationId = (data) => {
            const { organization } = this.state;
            const orgId = organization && organization.slug;
            this.props.router.push(`/settings/${orgId}/integrations/${data.provider.key}/${data.id}/`);
        };
        // non-Github redirects to the extension view where the backend will finish the installation
        this.finishInstallation = () => {
            // add the selected org to the query parameters and then redirect back to configure
            const { selectedOrgSlug } = this.state;
            const query = Object.assign({ orgSlug: selectedOrgSlug }, this.queryParams);
            this.trackInstallationStart();
            window.location.assign(`/extensions/${this.integrationSlug}/configure/?${(0, utils_1.urlEncode)(query)}`);
        };
        this.customOption = orgProps => {
            const organization = this.getOrgBySlug(orgProps.value);
            if (!organization) {
                return null;
            }
            return (<react_select_1.components.Option {...orgProps}>
        <idBadge_1.default organization={organization} avatarSize={20} displayName={organization.name} avatarProps={{ consistentWidth: true }}/>
      </react_select_1.components.Option>);
        };
        this.customValueContainer = containerProps => {
            const valueList = containerProps.getValue();
            // if no value set, we want to return the default component that is rendered
            if (valueList.length === 0) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            const orgSlug = valueList[0].value;
            const organization = this.getOrgBySlug(orgSlug);
            if (!organization) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            return (<react_select_1.components.ValueContainer {...containerProps}>
        <idBadge_1.default organization={organization} avatarSize={20} displayName={organization.name} avatarProps={{ consistentWidth: true }}/>
      </react_select_1.components.ValueContainer>);
        };
    }
    getEndpoints() {
        return [['organizations', '/organizations/']];
    }
    getTitle() {
        return (0, locale_1.t)('Choose Installation Organization');
    }
    trackOpened() {
        this.trackIntegrationAnalytics('integrations.integration_viewed', true);
    }
    trackInstallationStart() {
        this.trackIntegrationAnalytics('integrations.installation_start');
    }
    get integrationSlug() {
        return this.props.params.integrationSlug;
    }
    get queryParams() {
        return this.props.location.query;
    }
    onLoadAllEndpointsSuccess() {
        // auto select the org if there is only one
        const { organizations } = this.state;
        if (organizations.length === 1) {
            this.onSelectOrg({ value: organizations[0].slug });
        }
    }
    renderAddButton() {
        const { installationId } = this.props.params;
        const { organization, provider } = this.state;
        // should never happen but we need this check for TS
        if (!provider || !organization) {
            return null;
        }
        const { features } = provider.metadata;
        // Prepare the features list
        const featuresComponents = features.map(f => ({
            featureGate: f.featureGate,
            description: (<FeatureListItem dangerouslySetInnerHTML={{ __html: (0, marked_1.singleLineRenderer)(f.description) }}/>),
        }));
        const { IntegrationDirectoryFeatures } = (0, integrationUtil_1.getIntegrationFeatureGate)();
        // Github uses a different installation flow with the installationId as a parameter
        // We have to wrap our installation button with AddIntegration so we can get the
        // addIntegrationWithInstallationId callback.
        // if we don't hve an installationId, we need to use the finishInstallation callback.
        return (<IntegrationDirectoryFeatures organization={organization} features={featuresComponents}>
        {({ disabled }) => (<addIntegration_1.default provider={provider} onInstall={this.onInstallWithInstallationId} organization={organization}>
            {addIntegrationWithInstallationId => (<ButtonWrapper>
                <button_1.default priority="primary" disabled={!this.hasAccess() || disabled} onClick={() => installationId
                        ? addIntegrationWithInstallationId({
                            installation_id: installationId,
                        })
                        : this.finishInstallation()}>
                  {(0, locale_1.t)('Install %s', provider.name)}
                </button_1.default>
              </ButtonWrapper>)}
          </addIntegration_1.default>)}
      </IntegrationDirectoryFeatures>);
    }
    renderBottom() {
        const { organization, selectedOrgSlug, provider, reloading } = this.state;
        const { FeatureList } = (0, integrationUtil_1.getIntegrationFeatureGate)();
        if (reloading) {
            return <loadingIndicator_1.default />;
        }
        return (<react_1.Fragment>
        {selectedOrgSlug && organization && !this.hasAccess() && (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
            <p>
              {(0, locale_1.tct)(`You do not have permission to install integrations in
                [organization]. Ask an organization owner or manager to
                visit this page to finish installing this integration.`, { organization: <strong>{organization.slug}</strong> })}
            </p>
            <InstallLink>{window.location.href}</InstallLink>
          </alert_1.default>)}

        {provider && organization && this.hasAccess() && FeatureList && (<react_1.Fragment>
            <p>
              {(0, locale_1.tct)('The following features will be available for [organization] when installed.', { organization: <strong>{organization.slug}</strong> })}
            </p>
            <FeatureList organization={organization} features={provider.metadata.features} provider={provider}/>
          </react_1.Fragment>)}

        <div className="form-actions">{this.renderAddButton()}</div>
      </react_1.Fragment>);
    }
    renderBody() {
        const { selectedOrgSlug } = this.state;
        const options = this.state.organizations.map((org) => ({
            value: org.slug,
            label: org.name,
        }));
        return (<narrowLayout_1.default>
        <h3>{(0, locale_1.t)('Finish integration installation')}</h3>
        <p>
          {(0, locale_1.tct)(`Please pick a specific [organization:organization] to link with
            your integration installation of [integation].`, {
                organization: <strong />,
                integation: <strong>{this.integrationSlug}</strong>,
            })}
        </p>

        <field_1.default label={(0, locale_1.t)('Organization')} inline={false} stacked required>
          <selectControl_1.default onChange={this.onSelectOrg} value={selectedOrgSlug} placeholder={(0, locale_1.t)('Select an organization')} options={options} components={{
                Option: this.customOption,
                ValueContainer: this.customValueContainer,
            }}/>
        </field_1.default>
        {this.renderBottom()}
      </narrowLayout_1.default>);
    }
}
exports.default = IntegrationOrganizationLink;
const InstallLink = (0, styled_1.default)('pre') `
  margin-bottom: 0;
  background: #fbe3e1;
`;
const FeatureListItem = (0, styled_1.default)('span') `
  line-height: 24px;
`;
const ButtonWrapper = (0, styled_1.default)('div') `
  margin-left: auto;
  align-self: center;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
//# sourceMappingURL=integrationOrganizationLink.jsx.map